from pydantic import (
    BeforeValidator,
    PlainSerializer,
    WithJsonSchema,
)
from typing_extensions import Annotated

HexBinary = Annotated[
    bytes,
    BeforeValidator(lambda x: bytes.fromhex(x)),
    PlainSerializer(lambda x: bytes.hex(x), return_type=str),
    WithJsonSchema({"type": "string"}, mode="serialization"),
]


def hex_dec_value_before_validator(value: str) -> int:
    if value.startswith("#x"):
        return int("0" + value[1:], base=16)  # int("0x12345")
    return int(value)


def hex_dec_value_serializer(value: int) -> str:
    return str(value)


HexDecValue = Annotated[
    int,
    BeforeValidator(hex_dec_value_before_validator),
    PlainSerializer(hex_dec_value_serializer, return_type=str),
    WithJsonSchema({"type": "string"}, mode="serialization"),
]
