# -*- coding: utf-8 -*-
import typing

import typesystem

from arkindex.schema.openapi import OPEN_API, OpenAPI


def validate(schema: typing.Union[dict, str, bytes]):
    if not isinstance(schema, (dict, str, bytes)):
        raise ValueError("schema must be either str, bytes, or dict.")

    if isinstance(schema, bytes):
        schema = schema.decode("utf8", "ignore")

    if isinstance(schema, str):
        token = typesystem.tokenize_json(schema)
        value = typesystem.validate_with_positions(token=token, validator=OpenAPI)
    else:
        value = OPEN_API.validate(schema)

    return OpenAPI().load(value)
