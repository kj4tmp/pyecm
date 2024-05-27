import pytest
from pydantic import ValidationError
from pydantic_xml import BaseXmlModel, element

from pyecm.eni_types import HexBinary, HexDecValue


def test_hex_binary_valid():
    xml_str = "<MyXml><my_tag>AABBCCDDeeFF001122</my_tag></MyXml>"

    class MyXml(BaseXmlModel):
        my_tag: HexBinary = element()

    my_xml = MyXml.from_xml(xml_str)

    assert my_xml.my_tag == bytes.fromhex("AABBCCDDeeFF001122")

    assert my_xml.to_xml() == b"<MyXml><my_tag>aabbccddeeff001122</my_tag></MyXml>"


def test_hex_binary_invalid_char():
    xml_str = "<MyXml><my_tag>ZAABBCCDDeeFF001122</my_tag></MyXml>"

    class MyXml(BaseXmlModel):
        my_tag: HexBinary = element()

    with pytest.raises(ValidationError, match="non-hexadecimal number found"):
        MyXml.from_xml(xml_str)


@pytest.mark.parametrize(("input_str", "expected_int"), [("#x123A", 4666), ("4666", 4666)])
def test_hex_dec_value_valid(input_str: str, expected_int: int):
    xml_str = f"<MyXml><my_tag>{input_str}</my_tag></MyXml>"

    class MyXml(BaseXmlModel):
        my_tag: HexDecValue = element()

    my_xml = MyXml.from_xml(xml_str)

    assert my_xml.my_tag == expected_int

    assert my_xml.to_xml() == f"<MyXml><my_tag>{str(expected_int)}</my_tag></MyXml>".encode()
