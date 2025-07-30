# -*- coding: utf-8 -*-
from requests.auth import AuthBase


class TokenSessionAuthentication(AuthBase):

    safe_methods = ("GET", "HEAD", "OPTIONS", "TRACE")

    def __init__(
        self,
        token,
        scheme="Token",
        csrf_cookie_name="arkindex.csrf",
        csrf_header_name="X-CSRFToken",
    ):
        """
        :param str token: The API token to use.
        :param str scheme: The HTTP authentication scheme to use for token authentication.
        :param str csrf_cookie_name: Name of the CSRF token cookie.
        :param str csrf_header_name: Name of the CSRF request header.
        """
        self.token = token
        self.scheme = scheme
        self.csrf_cookie_name = csrf_cookie_name
        self.csrf_header_name = csrf_header_name
        self.csrf_token = None

    def store_csrf_token(self, response, **kwargs):
        if self.csrf_cookie_name in response.cookies:
            self.csrf_token = response.cookies[self.csrf_cookie_name]

    def __call__(self, request):
        # Add CSRF token
        if (
            self.csrf_token
            and self.csrf_header_name is not None
            and (request.method not in self.safe_methods)
        ):
            request.headers[self.csrf_header_name] = self.csrf_token

        if self.csrf_cookie_name is not None:
            request.register_hook("response", self.store_csrf_token)

        # Add API token
        if self.token is not None:
            request.headers["Authorization"] = f"{self.scheme} {self.token}"

        return request
