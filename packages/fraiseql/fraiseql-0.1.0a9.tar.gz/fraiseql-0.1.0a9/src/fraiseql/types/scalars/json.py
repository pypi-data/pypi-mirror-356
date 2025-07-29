"""Custom JSON scalar type for FraiseQL."""

import json
from typing import Any

from graphql import GraphQLError, GraphQLScalarType
from graphql.language import (
    BooleanValueNode,
    FloatValueNode,
    IntValueNode,
    ListValueNode,
    NullValueNode,
    ObjectValueNode,
    StringValueNode,
    ValueNode,
)

from fraiseql.types.definitions import ScalarMarker

# Python-side recursive JSON type
JSONData = str | int | float | bool | None | dict[str, "JSONData"] | list["JSONData"]


def serialize_json(
    value: Any,
) -> str | dict[str, Any] | list[Any] | int | float | bool | None:
    """Serialize JSON-compatible data."""
    return value


def parse_json_value(
    value: Any,
) -> str | dict[str, Any] | list[Any] | int | float | bool | None:
    """Parse value that must conform to JSON structure."""
    # If value is one of the expected types, return it
    if isinstance(value, dict | list | str | int | float | bool | type(None)):
        return value  # type: ignore[return-value]

    # If it's an unsupported type, raise an error
    msg = f"JSON cannot represent value: {value!r}"
    raise GraphQLError(msg)


def parse_json_literal(
    ast: ValueNode,
    variables: dict[str, Any] | None = None,
) -> str | dict[str, Any] | list[Any] | int | float | bool | None:
    """Parse JSON from a GraphQL literal.

    Accepts:
    - String literals containing JSON
    - Numeric literals (int/float)
    - Boolean literals
    - Null literals
    - Object literals (GraphQL object notation)
    - List literals (GraphQL list notation)

    Args:
        ast: The GraphQL AST node to parse
        variables: Optional variables dict (not used for JSON parsing)

    Returns:
        The parsed JSON value as a Python object

    Raises:
        GraphQLError: If the literal cannot be parsed as JSON
    """
    _ = variables  # Not used here

    if isinstance(ast, StringValueNode):
        # If it's a string, try to parse it as JSON
        # If it fails, return it as a plain string
        try:
            return json.loads(ast.value)
        except json.JSONDecodeError:
            return ast.value

    if isinstance(ast, IntValueNode):
        # IntValueNode stores the value as a string, convert to int
        return int(ast.value)

    if isinstance(ast, FloatValueNode):
        # FloatValueNode stores the value as a string, convert to float
        return float(ast.value)

    if isinstance(ast, BooleanValueNode):
        # BooleanValueNode already has a boolean value
        return ast.value

    if isinstance(ast, NullValueNode):
        # NullValueNode represents JSON null
        return None

    if isinstance(ast, ObjectValueNode):
        # Parse GraphQL object literal to Python dict
        result = {}
        for field in ast.fields:
            field_name = field.name.value
            field_value = parse_json_literal(field.value, variables)
            result[field_name] = field_value
        return result

    if isinstance(ast, ListValueNode):
        # Parse GraphQL list literal to Python list
        return [parse_json_literal(value, variables) for value in ast.values]

    msg = f"JSON cannot represent literal of type {type(ast).__name__}"
    raise GraphQLError(msg)


# GraphQL scalar definition
JSONScalar = GraphQLScalarType(
    name="JSON",
    description="The `JSON` scalar type represents JSON values as specified by ECMA-404.",
    serialize=serialize_json,
    parse_value=parse_json_value,
    parse_literal=parse_json_literal,
)


# Python marker for use in dataclasses
class JSONField(dict[str, Any], ScalarMarker):
    """Python marker for the GraphQL JSON scalar."""

    __slots__ = ()

    def __repr__(self) -> str:
        """String representation used in type annotations and debug output."""
        return "JSON"
