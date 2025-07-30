# -*- coding: utf-8 -*-
import logging
import math
import random
import time
from collections.abc import Iterator, Sized
from enum import Enum
from urllib.parse import parse_qs, urlsplit

import requests

from arkindex.exceptions import ErrorResponse

logger = logging.getLogger(__name__)


class PaginationMode(Enum):
    """Pagination modes with their different indexes"""

    PageNumber = "page"
    Cursor = "cursor"


class ResponsePaginator(Sized, Iterator):
    """
    A lazy generator to handle paginated Arkindex API endpoints.
    Does not perform any requests to the API until it is required.
    """

    def __init__(self, client, operation_id, *request_args, **request_kwargs):
        r"""
        :param client arkindex.ArkindexClient: An API client to use to perform requests for each page.
        :param \*request_args: Arguments to send to :meth:`arkindex.ArkindexClient.request`.
        :param \**request_kwargs: Keyword arguments to send to :meth:`arkindex.ArkindexClient.request`.
        """
        self.client = client
        """The API client used to perform requests on each page."""

        self.data = {}
        """Stored data from the last performed request."""

        self.results = []
        """Stored results from the last performed request."""

        self.operation_id = operation_id
        """Client operation"""

        self.request_args = request_args
        """Arguments to send to :meth:`arkindex.ArkindexClient.request` with each request."""

        self.request_kwargs = request_kwargs
        """Keyword arguments to send to :meth:`arkindex.ArkindexClient.request` with each request."""

        self.count = None
        """Total results count."""

        self.pages_count = None
        """Total pages count."""

        self.pages_loaded = 0
        """Number of pages already loaded."""

        self.retries = request_kwargs.pop("retries", 5)
        assert (
            isinstance(self.retries, int) and self.retries > 0
        ), "retries must be a positive integer"
        """Max number of retries per API request"""

        # Detect and store the pagination mode
        self.mode = None
        if any(
            field.name == "cursor"
            for field in self.client.lookup_operation(self.operation_id).fields
        ):
            self.mode = PaginationMode.Cursor
        elif any(
            field.name == "page"
            for field in self.client.lookup_operation(self.operation_id).fields
        ):
            self.mode = PaginationMode.PageNumber
        if not self.mode:
            raise NotImplementedError(
                "Pagination only implements page and cursor modes."
            )

        # First page key is an empty string by default (to stay coherent with page or cursor modes)
        self.initial_page = request_kwargs.get(self.mode.value, "")

        # Store retrieved pages remaining retries
        self.pages = {self.initial_page: self.retries}

        # Store missing page indexes
        self.missing = set()
        self.allow_missing_data = request_kwargs.pop("allow_missing_data", False)
        assert isinstance(
            self.allow_missing_data, bool
        ), "allow_missing_data must be a boolean"

    def _fetch_page(self):
        """
        Retrieve the next page and store its results

        Returns None in case of a failure
        Returns True in case the page returned results
        Returns False in case the page returned an empty result
        Raises a StopIteration in case there are no pages left to iterate on
        """
        # Transform as a list of tuples for simpler output
        remaining = [(m, v) for m, v in self.pages.items()]

        # No remaining pages, end of iteration
        if not remaining:
            raise StopIteration

        # Get next page to load
        index, retry = remaining[0]

        if index:
            self.request_kwargs[self.mode.value] = index

        try:
            extra_kwargs = {}
            if not self.pages_loaded:
                if (
                    self.mode == PaginationMode.PageNumber
                    and self.initial_page
                    and int(self.initial_page) > 1
                ) or (self.mode == PaginationMode.Cursor and self.initial_page):
                    logger.info(
                        f"Loading page {self.initial_page} on try {self.retries - retry + 1}/{self.retries}"
                    )
                else:
                    logger.info(
                        f"Loading first page on try {self.retries - retry + 1}/{self.retries}"
                    )
                operation_fields = [
                    f.name
                    for f in self.client.lookup_operation(self.operation_id).fields
                ]
                # Ask to count results if the operation handle it (this is usually the case with cursors)
                if "with_count" in operation_fields:
                    extra_kwargs = {
                        "with_count": "true",
                        **extra_kwargs,
                    }
            else:
                message = f"Loading {self.mode.value} {index} on try {self.retries - retry + 1}/{self.retries}"
                if self.pages_count is not None:
                    if self.mode is PaginationMode.Cursor and self.initial_page:
                        # The number of remaining pages is unknown when an initial cursor is set
                        max_pages = self.pages_count - self.pages_loaded
                        message = message + (
                            f" - remains a maximum of {max_pages} page{'s' if max_pages > 1 else ''} to load."
                        )
                    else:
                        initial = int(self.initial_page) if self.initial_page else 1
                        remaining_count = (
                            self.pages_count - self.pages_loaded - (initial - 1)
                        )
                        message = message + (
                            f" - remains {remaining_count} page{'s' if remaining_count > 1 else ''} to load."
                        )

                logger.info(message)

            # Fetch the next page
            self.data = self.client.single_request(
                self.operation_id,
                *self.request_args,
                **self.request_kwargs,
                **extra_kwargs,
            )
            self.results = self.data.get("results", [])

            # Retrieve information on the first page with results count
            if self.count is None and "count" in self.data:
                self.count = self.data["count"]
                if self.count == 0:
                    # Pagination has retrieved 0 results
                    self.pages = {}
                    return False
                self.pages_count = math.ceil(self.count / len(self.results))
                if self.mode == PaginationMode.Cursor:
                    logger.info(
                        f"Pagination will load a {'maximum' if self.initial_page else 'total'} "
                        f"of {self.pages_count} page{'s' if self.pages_count > 1 else ''}"
                    )
                elif self.mode == PaginationMode.PageNumber:
                    initial = int(self.initial_page) if self.initial_page else 1
                    total = self.pages_count - initial + 1
                    logger.info(
                        f"Pagination will load a total of {total} page{'s' if total > 1 else ''}."
                    )
                    # Initialize all pages once
                    self.pages.update(
                        {
                            i: self.retries
                            for i in range(initial + 1, self.pages_count + 1)
                        }
                    )
            if self.mode == PaginationMode.Cursor:
                # Parse next URL to retrieve the cursor of the next page
                query = urlsplit(self.data["next"]).query
                cursor_query = parse_qs(query).get("cursor")
                if not cursor_query:
                    self.pages = {}
                else:
                    self.pages = {cursor_query[0]: self.retries}
            elif self.mode == PaginationMode.PageNumber:
                # Mark the current page as loaded
                del self.pages[index]

            # Stop happy path here, we don't need to process errors
            self.pages_loaded += 1
            return True

        except ErrorResponse as e:
            logger.warning(f"API Error {e.status_code} on pagination: {e.content}")

            # Decrement pages counter
            self.pages[index] -= 1

            # Sleep a bit (less than a second)
            time.sleep(random.random())

        except requests.exceptions.ConnectionError as e:
            logger.error(f"Server connection error, will retry in a few seconds: {e}")

            # Decrement pages counter
            self.pages[index] -= 1

            # Sleep a few seconds
            time.sleep(random.randint(1, 10))

        # Detect and store references to missing pages
        # when a page has no retries left
        if self.pages[index] <= 0:
            error_text = "No more retries left"
            if self.mode:
                error_text += f" for {self.mode.value} {index}"

            logger.warning(error_text)
            if self.allow_missing_data:
                self.missing.add(index)
                del self.pages[index]
            else:
                raise Exception("Stopping pagination as data will be incomplete")

        # No data could be fetch, return None
        return None

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.results) < 1:
            if self.data and self.data.get("next") is None:
                raise StopIteration

            # Continuously try to fetch a page until there are some retries left
            # This will still yield as soon as some data is fetched
            while self._fetch_page() is None:
                pass

        # Even after fetching a new page, if the new page is empty, just fail
        if len(self.results) < 1:
            raise StopIteration

        return self.results.pop(0)

    def __len__(self):
        # Handle calls to len when no requests have been made yet
        if not self.pages_loaded and self.count is None:
            # Continuously try to fetch a page until there are no retries left
            while self._fetch_page() is None:
                pass
        # Count may be null in case of a StopIteration
        if self.count is None:
            raise Exception("An error occurred fetching items total count")
        return self.count

    def __repr__(self):
        return "<{} via {!r}: {!r} {!r}>".format(
            self.__class__.__name__,
            self.client,
            (self.operation_id, self.request_args),
            self.request_kwargs,
        )
