# -*- coding: utf-8 -*-
import collections
import logging

from arkindex.exceptions import ErrorResponse

logger = logging.getLogger(__name__)

MockRequest = collections.namedtuple("MockRequest", "operation, body, args, kwargs")


class MockApiClient(object):
    """A mockup of the Arkindex API Client to build unit tests"""

    def __init__(self):
        self.history = []
        self.responses = []

    def add_response(
        self, operation_id: str, response: dict, body=None, *args, **kwargs
    ):
        """Store a new mock response for a request on an endpoint"""
        request = MockRequest(operation_id, body, args, kwargs)
        self.responses.append((request, response))
        return (request, response)

    def add_error_response(
        self,
        operation_id: str,
        status_code: int,
        title="Mock error response",
        content="Mock error response",
        body=None,
        *args,
        **kwargs,
    ):
        """Store a new mock error response for a request on an endpoint"""
        request = MockRequest(operation_id, body, args, kwargs)
        error = ErrorResponse(
            title=title,
            status_code=status_code,
            content=content,
        )
        self.responses.append((request, error))
        return (request, error)

    def next_response(self, request: MockRequest):
        """Find the next available response for a request, and remove it from the stack"""
        for request_cmp, response in self.responses:
            if request_cmp == request:
                self.responses.remove((request_cmp, response))
                yield response

    def paginate(self, operation_id: str, body=None, *args, **kwargs):
        """Simply send back the next matching response"""
        return self.request(operation_id, body, *args, **kwargs)

    def request(self, operation_id: str, body=None, *args, **kwargs):
        """Send back a mocked response, or an exception"""

        # Save request in history
        request = MockRequest(operation_id, body, args, kwargs)
        self.history.append(request)

        # Find the next valid response
        response = next(self.next_response(request), None)
        if response is not None:
            logger.info(f"Sending mock response for {operation_id}")
            if isinstance(response, Exception):
                raise response
            return response

        # Throw exception when no response is found
        logger.error(
            f"No mock response found for {operation_id} with body={body} args={args} kwargs={kwargs}"
        )
        raise ErrorResponse(
            title="No mock response found",
            status_code=400,
            content="No mock response found",
        )
