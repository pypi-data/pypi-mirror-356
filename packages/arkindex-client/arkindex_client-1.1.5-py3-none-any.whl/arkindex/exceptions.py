# -*- coding: utf-8 -*-
from collections import namedtuple

Position = namedtuple("Position", ["line_no", "column_no", "index"])


class ErrorMessage:
    def __init__(self, text, code, index=None, position=None):
        self.text = text
        self.code = code
        self.index = index
        self.position = position

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.code == other.code
            and self.index == other.index
            and self.position == other.position
        )

    def __repr__(self):
        return "%s(%s, code=%s, index=%s, position=%s)" % (
            self.__class__.__name__,
            repr(self.text),
            repr(self.code),
            repr(self.index),
            repr(self.position),
        )


class ErrorResponse(Exception):
    """
    Raised when a client request results in an error response being returned.
    """

    def __init__(self, title, status_code, content):
        self.title = title
        self.status_code = status_code
        self.content = content

    def __repr__(self):
        return "%s(%s, status_code=%s, content=%s)" % (
            self.__class__.__name__,
            repr(self.title),
            repr(self.status_code),
            repr(self.content),
        )

    def __str__(self):
        return repr(self.content)


class ClientError(Exception):
    """
    Raised when a client is unable to fulfil an API request.
    """

    def __init__(self, messages):
        self.messages = messages
        super().__init__(messages)

    def __repr__(self):
        return "%s(messages=%s)" % (
            self.__class__.__name__,
            repr(self.messages),
        )

    def __str__(self):
        if len(self.messages) == 1 and not self.messages[0].index:
            return self.messages[0].text
        return str(self.messages)


class SchemaError(Exception):
    """
    Any error occurring during the acquisition and processing of the OpenAPI schema.
    """
