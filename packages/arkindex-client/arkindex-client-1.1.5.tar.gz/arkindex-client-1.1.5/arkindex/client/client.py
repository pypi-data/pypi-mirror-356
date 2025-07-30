# -*- coding: utf-8 -*-
"""
Arkindex API Client
"""
import json
import logging
import os
import warnings
from importlib.metadata import version
from time import sleep
from urllib.parse import quote, urljoin, urlparse, urlsplit

import requests
import typesystem
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from arkindex.auth import TokenSessionAuthentication
from arkindex.client import decoders
from arkindex.exceptions import ClientError, ErrorMessage, ErrorResponse, SchemaError
from arkindex.pagination import ResponsePaginator
from arkindex.schema.validator import validate

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = (30, 60)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_BASE_URL = "https://arkindex.teklia.com/"

# Endpoint accessed by the client on instantiation to retrieve the OpenAPI schema
SCHEMA_ENDPOINT = "/api/v1/openapi/?format=json"


def _is_500_error(exc: Exception) -> bool:
    """
    Check if an Arkindex API error is a 50x
    This is used to retry most API calls implemented here
    """
    if not isinstance(exc, ErrorResponse):
        return False

    return 500 <= exc.status_code < 600


def options_from_env():
    """
    Get API client keyword arguments from environment variables.
    """
    options = {}
    # ARKINDEX_TASK_TOKEN takes priority over ARKINDEX_API_TOKEN
    if "ARKINDEX_TASK_TOKEN" in os.environ:
        options["auth_scheme"] = "Ponos"
        options["token"] = os.environ.get("ARKINDEX_TASK_TOKEN")
    elif "ARKINDEX_API_TOKEN" in os.environ:
        options["auth_scheme"] = "Token"
        options["token"] = os.environ.get("ARKINDEX_API_TOKEN")

    # Allow overriding the default auth schemes
    if "ARKINDEX_API_AUTH_SCHEME" in os.environ:
        options["auth_scheme"] = os.environ.get("ARKINDEX_API_AUTH_SCHEME")

    if "ARKINDEX_API_URL" in os.environ:
        options["base_url"] = os.environ.get("ARKINDEX_API_URL")

    if "ARKINDEX_API_SCHEMA_URL" in os.environ:
        options["schema_url"] = os.environ.get("ARKINDEX_API_SCHEMA_URL")

    if "ARKINDEX_API_CSRF_COOKIE" in os.environ:
        options["csrf_cookie"] = os.environ.get("ARKINDEX_API_CSRF_COOKIE")

    return options


class ArkindexClient:
    """
    An Arkindex API client.
    """

    def __init__(
        self,
        token=None,
        auth_scheme="Token",
        base_url=DEFAULT_BASE_URL,
        schema_url=None,
        csrf_cookie=None,
        sleep=0,
        verify=True,
    ):
        r"""
        :param token: An API token to use. If omitted, access is restricted to public endpoints.
        :type token: str or None
        :param str base_url: A custom base URL for the client. If omitted, defaults to the Arkindex main server.
        :param schema_url: URL or local path to an OpenAPI schema to use instead of the Arkindex instance's own schema.
        :type schema_url: str or None
        :param csrf_cookie: Use a custom CSRF cookie name. By default, the client will try to use any cookie
           defined in ``x-csrf-cookie`` on the Server Object of the OpenAPI specification, and fall back to
           ``arkindex.csrf``.
        :type csrf_cookie: str or None
        :param float sleep: Number of seconds to wait before sending each API request,
           as a simple means of throttling.
        :param bool verify: Whether to verify the SSL certificate on each request. Enabled by default.
        """
        self.decoders = [
            decoders.JSONDecoder(),
            decoders.TextDecoder(),
            decoders.DownloadDecoder(),
        ]

        self.session = requests.Session()
        self.session.verify = verify
        client_version = version("arkindex-client")
        self.session.headers.update(
            {
                "accept": ", ".join([decoder.media_type for decoder in self.decoders]),
                "user-agent": f"arkindex-client/{client_version}",
            }
        )

        if not schema_url:
            schema_url = urljoin(base_url, SCHEMA_ENDPOINT)

        try:
            split = urlsplit(schema_url)
            if split.scheme == "file" or not (split.scheme or split.netloc):
                # This is a local path
                with open(schema_url) as f:
                    schema = json.load(f)
            else:
                resp = self.session.get(
                    schema_url,
                    headers={
                        # Explicitly request an OpenAPI schema in JSON and not YAML
                        "Accept": "application/vnd.oai.openapi+json, application/json",
                    },
                )
                resp.raise_for_status()
                schema = resp.json()
        except Exception as e:
            raise SchemaError(
                f"Could not retrieve a proper OpenAPI schema from {schema_url}"
            ) from e

        self.document = validate(schema)

        # Try to autodetect the CSRF cookie:
        # - Try to find a matching server for this base URL and look for the x-csrf-cookie extension
        # - Fallback to arkindex.csrf
        if not csrf_cookie:
            split_base_url = urlsplit(base_url or self.document.url)
            csrf_cookies = {
                urlsplit(server.get("url", "")).netloc: server.get("x-csrf-cookie")
                for server in schema.get("servers", [])
            }
            csrf_cookie = csrf_cookies.get(split_base_url.netloc) or "arkindex.csrf"

        self.configure(
            token=token,
            auth_scheme=auth_scheme,
            base_url=base_url,
            csrf_cookie=csrf_cookie,
            sleep=sleep,
        )

    def __repr__(self):
        return "<{} on {!r}>".format(
            self.__class__.__name__,
            self.document.url if hasattr(self, "document") else "",
        )

    def configure(
        self,
        token=None,
        auth_scheme="Token",
        base_url=None,
        csrf_cookie=None,
        sleep=None,
    ):
        """
        Reconfigure the API client.

        :param token: An API token to use. If omitted, access is restricted to public endpoints.
        :type token: str or None
        :param auth_scheme:
           An authentication scheme to use. This is added in the HTTP header before the token:
           ``Authorization: [scheme] [token]``.
           This should use ``Token`` to authenticate as a regular user and ``Ponos`` to authenticate as a Ponos task.
           If omitted, this defaults to ``Token``.
        :type auth_scheme: str or None
        :param base_url: A custom base URL for the client. If omitted, defaults to the Arkindex main server.
        :type base_url: str or None
        :param csrf_cookie: Use a custom CSRF cookie name. Falls back to ``arkindex.csrf``.
        :type csrf_cookie: str or None
        :param float sleep: Number of seconds to wait before sending each API request,
           as a simple means of throttling.
        """
        if not csrf_cookie:
            csrf_cookie = "arkindex.csrf"
        self.session.auth = TokenSessionAuthentication(
            token,
            csrf_cookie_name=csrf_cookie,
            scheme=auth_scheme,
        )

        if not sleep or not isinstance(sleep, float) or sleep < 0:
            self.sleep_duration = 0
        self.sleep_duration = sleep

        if base_url:
            self.document.url = base_url

        # Add the Referer header to allow Django CSRF to function
        self.session.headers.setdefault("Referer", self.document.url)

    def lookup_operation(self, operation_id: str):
        if operation_id in self.document.links:
            return self.document.links[operation_id]

        text = 'Operation ID "%s" not found in schema.' % operation_id
        message = ErrorMessage(text=text, code="invalid-operation")
        raise ClientError(messages=[message])

    def paginate(self, operation_id, *args, **kwargs):
        """
        Perform a usual API request, but handle paginated endpoints.

        :return: An iterator for a paginated endpoint.
        :rtype: Union[arkindex.pagination.ResponsePaginator, dict, list]
        """

        link = self.lookup_operation(operation_id)
        # If there was no x-paginated, trust the caller and assume the endpoint is paginated
        if link.paginated is not False:
            return ResponsePaginator(self, operation_id, *args, **kwargs)
        return self.request(operation_id, *args, **kwargs)

    def login(self, email, password):
        """
        Login to Arkindex using an email/password combination.
        This helper method automatically sets the client's authentication settings with the token.
        """
        resp = self.request("Login", body={"email": email, "password": password})
        if "auth_token" in resp:
            self.session.auth.scheme = "Token"
            self.session.auth.token = resp["auth_token"]
        return resp

    def get_query_params(self, link, params):
        return {
            field.name: params[field.name]
            for field in link.get_query_fields()
            if field.name in params
        }

    def get_url(self, link, params):
        url = urljoin(self.document.url, link.url)

        scheme = urlparse(url).scheme.lower()

        if not scheme:
            text = "URL missing scheme '%s'." % url
            message = ErrorMessage(text=text, code="invalid-url")
            raise ClientError(messages=[message])

        if scheme not in ("http", "https"):
            text = "Unsupported URL scheme '%s'." % scheme
            message = ErrorMessage(text=text, code="invalid-url")
            raise ClientError(messages=[message])

        for field in link.get_path_fields():
            value = str(params[field.name])
            if "{%s}" % field.name in url:
                url = url.replace("{%s}" % field.name, quote(value, safe=""))
            elif "{+%s}" % field.name in url:
                url = url.replace("{+%s}" % field.name, quote(value, safe="/"))

        return url

    def get_content(self, link, params):
        body_field = link.get_body_field()
        if body_field and body_field.name in params:
            assert (
                link.encoding == "application/json"
            ), "Only JSON request bodies are supported"
            return params[body_field.name]

    def get_decoder(self, content_type=None):
        """
        Given the value of a 'Content-Type' header, return the appropriate
        decoder for handling the response content.
        """
        if content_type is None:
            return self.decoders[0]

        content_type = content_type.split(";")[0].strip().lower()
        main_type = content_type.split("/")[0] + "/*"
        wildcard_type = "*/*"

        for codec in self.decoders:
            if codec.media_type in (content_type, main_type, wildcard_type):
                return codec

        text = (
            "Unsupported encoding '%s' in response Content-Type header." % content_type
        )
        message = ErrorMessage(text=text, code="cannot-decode-response")
        raise ClientError(messages=[message])

    def single_request(self, operation_id, **parameters):
        """
        Perform an API request.

        :param str operation_id: Name of the API endpoint.
        :param path_parameters: Path parameters for this endpoint.
        """
        link = self.lookup_operation(operation_id)
        if link.deprecated:
            warnings.warn(
                "Endpoint '{}' is deprecated.".format(operation_id),
                DeprecationWarning,
                stacklevel=2,
            )

        validator = typesystem.Object(
            properties={field.name: typesystem.Any() for field in link.fields},
            required=[field.name for field in link.fields if field.required],
            additional_properties=False,
        )
        try:
            validator.validate(parameters)
        except typesystem.ValidationError as exc:
            raise ClientError(messages=exc.messages()) from None

        method = link.method
        url = self.get_url(link, parameters)

        content = self.get_content(link, parameters)
        query_params = self.get_query_params(link, parameters)
        fields = link.get_query_fields()

        for field in fields:
            if field.deprecated and field.name in query_params:
                warnings.warn(
                    "Parameter '{}' is deprecated.".format(field.name),
                    DeprecationWarning,
                    stacklevel=2,
                )

        if self.sleep_duration:
            logger.debug(
                "Delaying request by {:f} seconds...".format(self.sleep_duration)
            )
            sleep(self.sleep_duration)

        return self._send_request(
            method, url, query_params=query_params, content=content
        )

    def _send_request(self, method, url, query_params=None, content=None):
        options = {
            "params": query_params,
            "timeout": REQUEST_TIMEOUT,
        }
        if content is not None:
            options["json"] = content

        response = self.session.request(method, url, **options)

        # Given an HTTP response, return the decoded data.
        result = None
        if response.content:
            content_type = response.headers.get("content-type")
            decoder = self.get_decoder(content_type)
            result = decoder.decode(response)

        if 400 <= response.status_code <= 599:
            title = "%d %s" % (response.status_code, response.reason)
            raise ErrorResponse(
                title=title, status_code=response.status_code, content=result
            )

        return result

    @retry(
        retry=retry_if_exception(_is_500_error),
        wait=wait_exponential(multiplier=2, min=3),
        reraise=True,
        stop=stop_after_attempt(5),
        before_sleep=before_sleep_log(logger, logging.INFO),
    )
    def request(self, operation_id, **parameters):
        """
        Perform an API request with an automatic retry mechanism in case of 50X errors.
        A failing API call will be retried 5 times, with an exponential sleep time going
        through 3, 4, 8 and 16 seconds of wait between call.
        If the 5th call still gives a 50x, the exception is re-raised and the caller should catch it.
        Log messages are displayed before sleeping (when at least one exception occurred).

        :param str operation_id: Name of the API endpoint.
        :param parameters: Body, Path or Query parameters passed as kwargs.
            Body parameters must be passed using the `body` keyword argument, others can be set directly.

        Example usage for POST and unpaginated GET requests:

        >>> request(
        ...     "CreateMetaDataBulk",
        ...     id="8f8f196f-49bc-444e-9cfe-c705c3cd01ae",
        ...     body={
        ...         "worker_run_id": "50e1f2d4-2087-41ed-a862-d17576bae480",
        ...         "metadata_list": [
        ...             …
        ...         ],
        ...     },
        ... )
        >>> request(
        ...     "ListElements",
        ...     corpus="7358ab03-cc36-4160-86ce-98f70e993a0f",
        ...     top_level=True,
        ... )
        """
        return self.single_request(operation_id, **parameters)
