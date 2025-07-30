# -*- coding: utf-8 -*-
import re
from urllib.parse import urljoin

import typesystem
from typesystem.json_schema import JSONSchema

from arkindex.document import Document, Field, Link

SCHEMA_REF = typesystem.Object(
    properties={"$ref": typesystem.String(pattern="^#/components/schemas/")}
)
REQUESTBODY_REF = typesystem.Object(
    properties={"$ref": typesystem.String(pattern="^#/components/requestBodies/")}
)

definitions = typesystem.Definitions()

OPEN_API = typesystem.Schema(
    fields={
        "openapi": typesystem.String(),
        "servers": typesystem.Array(
            items=typesystem.Reference("Server", definitions=definitions),
            default=[],
        ),
        "paths": typesystem.Reference("Paths", definitions=definitions),
        "components": typesystem.Reference(
            "Components", default=None, definitions=definitions
        ),
    },
)

definitions["Server"] = typesystem.Schema(
    fields={
        "url": typesystem.String(),
    },
)

definitions["Paths"] = typesystem.Object(
    pattern_properties={
        "^/": typesystem.Reference("Path", definitions=definitions),
        "^x-": typesystem.Any(),
    },
    additional_properties=False,
)

definitions["Path"] = typesystem.Object(
    properties={
        "summary": typesystem.String(allow_blank=True),
        "get": typesystem.Reference("Operation", definitions=definitions),
        "put": typesystem.Reference("Operation", definitions=definitions),
        "post": typesystem.Reference("Operation", definitions=definitions),
        "delete": typesystem.Reference("Operation", definitions=definitions),
        "options": typesystem.Reference("Operation", definitions=definitions),
        "head": typesystem.Reference("Operation", definitions=definitions),
        "patch": typesystem.Reference("Operation", definitions=definitions),
        "trace": typesystem.Reference("Operation", definitions=definitions),
        "servers": typesystem.Array(
            items=typesystem.Reference("Server", definitions=definitions)
        ),
        "parameters": typesystem.Array(
            items=typesystem.Reference("Parameter", definitions=definitions)
        ),
        # TODO: | ReferenceObject
    },
    additional_properties=True,
)

definitions["Operation"] = typesystem.Object(
    properties={
        "operationId": typesystem.String(),
        "parameters": typesystem.Array(
            items=typesystem.Reference("Parameter", definitions=definitions)
        ),  # TODO: | ReferenceObject
        "requestBody": REQUESTBODY_REF
        | typesystem.Reference(
            "RequestBody", definitions=definitions
        ),  # TODO: RequestBody | ReferenceObject
        "deprecated": typesystem.Boolean(),
        "servers": typesystem.Array(
            items=typesystem.Reference("Server", definitions=definitions)
        ),
        # A custom property added by Arkindex to provide a hint to the API client
        # that this endpoint is paginated, which changes the behavior of ArkindexClient.paginate.
        "x-paginated": typesystem.Boolean(default=None),
    },
    additional_properties=True,
)

definitions["Parameter"] = typesystem.Schema(
    fields={
        "name": typesystem.String(),
        "in": typesystem.Choice(choices=["query", "header", "path", "cookie"]),
        "required": typesystem.Boolean(default=False),
        "deprecated": typesystem.Boolean(default=False),
        "schema": JSONSchema | SCHEMA_REF,
    },
)

definitions["RequestBody"] = typesystem.Object(
    properties={
        "content": typesystem.Object(
            additional_properties=typesystem.Reference(
                "MediaType", definitions=definitions
            )
        ),
        "required": typesystem.Boolean(),
    },
    additional_properties=True,
)

definitions["MediaType"] = typesystem.Object(
    properties={
        "schema": JSONSchema | SCHEMA_REF,
    },
    additional_properties=True,
)

definitions["Components"] = typesystem.Object(
    properties={
        "schemas": typesystem.Object(additional_properties=JSONSchema),
        "parameters": typesystem.Object(
            additional_properties=typesystem.Reference(
                "Parameter", definitions=definitions
            )
        ),
        "requestBodies": typesystem.Object(
            additional_properties=typesystem.Reference(
                "RequestBody", definitions=definitions
            )
        ),
    },
    additional_properties=True,
)

METHODS = ["get", "put", "post", "delete", "options", "head", "patch", "trace"]


def lookup(value, keys, default=None):
    for key in keys:
        try:
            value = value[key]
        except (KeyError, IndexError, TypeError):
            return default
    return value


def _simple_slugify(text):
    if text is None:
        return None
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"[_]+", "_", text)
    return text.strip("_")


class OpenAPI:
    def load(self, data):
        schema_definitions = self.get_schema_definitions(data)
        links = self.get_links(data, schema_definitions)

        return Document(links=links)

    def get_schema_definitions(self, data):
        definitions = typesystem.Definitions()
        schemas = lookup(data, ["components", "schemas"], {})
        for key, value in schemas.items():
            ref = f"#/components/schemas/{key}"
            definitions[ref] = typesystem.from_json_schema(
                value, definitions=definitions
            )
        return definitions

    def get_links(self, data, schema_definitions):
        """
        Return all the links in the document, laid out by operationId.
        """
        links = []

        for path, path_info in data.get("paths", {}).items():
            operations = {key: path_info[key] for key in path_info if key in METHODS}
            for operation, operation_info in operations.items():
                link = self.get_link(
                    path,
                    path_info,
                    operation,
                    operation_info,
                    schema_definitions,
                )
                if link is None:
                    continue

                links.append(link)

        return links

    def get_link(self, path, path_info, operation, operation_info, schema_definitions):
        """
        Return a single link in the document.
        """
        name = operation_info["operationId"]
        deprecated = operation_info.get("deprecated", False)
        paginated = operation_info.get("x-paginated")

        # Allow path info and operation info to override the base URL, which is normally managed by the ArkindexClient.
        base_url = lookup(path_info, ["servers", 0, "url"], default=None)
        base_url = lookup(operation_info, ["servers", 0, "url"], default=base_url)

        # Parameters are taken both from the path info, and from the operation.
        parameters = path_info.get("parameters", [])
        parameters += operation_info.get("parameters", [])

        fields = [
            self.get_field(parameter, schema_definitions) for parameter in parameters
        ]

        # TODO: Handle media type generically here...
        body_schema = lookup(
            operation_info, ["requestBody", "content", "application/json", "schema"]
        )

        encoding = None
        if body_schema:
            encoding = "application/json"
            if "$ref" in body_schema:
                ref = body_schema["$ref"]
                schema = schema_definitions.get(ref)
                prefix_length = len("#/components/schemas/")
                field_name = ref[prefix_length:].lower()
            else:
                schema = typesystem.from_json_schema(
                    body_schema, definitions=schema_definitions
                )
                field_name = "body"
            field_name = lookup(
                operation_info, ["requestBody", "x-name"], default=field_name
            )
            fields += [Field(name=field_name, location="body", schema=schema)]

        return Link(
            name=name,
            url=urljoin(base_url, path),
            method=operation,
            fields=fields,
            encoding=encoding,
            deprecated=deprecated,
            paginated=paginated,
        )

    def get_field(self, parameter, schema_definitions):
        """
        Return a single field in a link.
        """
        name = parameter.get("name")
        location = parameter.get("in")
        required = parameter.get("required", False)
        schema = parameter.get("schema")
        deprecated = parameter.get("deprecated", False)

        if schema is not None:
            if "$ref" in schema:
                ref = schema["$ref"]
                schema = schema_definitions.get(ref)
            else:
                schema = typesystem.from_json_schema(
                    schema, definitions=schema_definitions
                )

        return Field(
            name=name,
            location=location,
            required=required,
            schema=schema,
            deprecated=deprecated,
        )
