# -*- coding: utf-8 -*-
import re
import typing

from arkindex.exceptions import SchemaError


class Document:
    def __init__(
        self,
        links: typing.Sequence["Link"],
        url: str = "",
    ):
        if not len(links):
            raise SchemaError(
                "An OpenAPI document must contain at least one valid operation."
            )

        links_by_name = {}

        # Ensure all names within a document are unique.
        for link in links:
            assert (
                link.name not in links_by_name
            ), f'Link "{link.name}" in Document must have a unique name.'
            links_by_name[link.name] = link

        self.links = links_by_name
        self.url = url


class Link:
    """
    Links represent the actions that a client may perform.
    """

    def __init__(
        self,
        url: str,
        method: str,
        handler: typing.Callable = None,
        name: str = "",
        encoding: str = "",
        fields: typing.Sequence["Field"] = None,
        deprecated: bool = False,
        paginated: typing.Optional[bool] = None,
    ):
        method = method.upper()
        fields = [] if (fields is None) else list(fields)

        url_path_names = set(
            [item.strip("{}").lstrip("+") for item in re.findall("{[^}]*}", url)]
        )
        path_fields = [field for field in fields if field.location == "path"]
        body_fields = [field for field in fields if field.location == "body"]

        assert method in (
            "GET",
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
            "OPTIONS",
            "HEAD",
            "TRACE",
        )
        assert len(body_fields) < 2
        if body_fields:
            assert encoding
        for field in path_fields:
            assert field.name in url_path_names

        # Add in path fields for any "{param}" items that don't already have
        # a corresponding path field.
        for path_name in url_path_names:
            if path_name not in [field.name for field in path_fields]:
                fields += [Field(name=path_name, location="path", required=True)]

        self.url = url
        self.method = method
        self.handler = handler
        self.name = name if name else handler.__name__
        self.encoding = encoding
        self.fields = fields
        self.deprecated = deprecated
        self.paginated = paginated

    def get_path_fields(self):
        return [field for field in self.fields if field.location == "path"]

    def get_query_fields(self):
        return [field for field in self.fields if field.location == "query"]

    def get_body_field(self):
        for field in self.fields:
            if field.location == "body":
                return field
        return None

    def get_expanded_body(self):
        field = self.get_body_field()
        if field is None or not hasattr(field.schema, "properties"):
            return None
        return field.schema.properties


class Field:
    def __init__(
        self,
        name: str,
        location: str,
        required: bool = None,
        schema: typing.Any = None,
        example: typing.Any = None,
        deprecated: bool = False,
    ):
        assert location in ("path", "query", "body", "cookie", "header", "formData")
        if required is None:
            required = True if location in ("path", "body") else False
        if location == "path":
            assert required, "May not set 'required=False' on path fields."

        self.name = name
        self.location = location
        self.required = required
        self.schema = schema
        self.example = example
        self.deprecated = deprecated
