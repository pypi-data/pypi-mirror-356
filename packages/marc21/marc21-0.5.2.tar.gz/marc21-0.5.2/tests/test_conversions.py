import pytest

from build.lib.marc21.lib import MarcSubfieldException
from marc21 import MarcDto, SubField, to_iso2709, from_iso2709, to_marcxml, from_marcxml, MarcInvalidTagException
from marc21.lib.marcException import MarcSubfieldException, MarcException

@pytest.fixture
def simple_dto():
    dto = MarcDto()
    dto.insert_field(dto.create_field(tag="001", data="ABC123"))
    dto.insert_field(dto.create_field(tag="100", indicators="1 ", subfields=[
        SubField(tag='a', value='Smith, John'),
        SubField(tag='d', value='1980-')
    ]))
    dto.insert_field(dto.create_field(tag="245", indicators="10", subfields=[
        SubField(tag='a', value='Example Book'),
        SubField(tag='c', value='John Smith')
    ]))
    return dto


def test_to_from_iso2709(simple_dto):
    binary = to_iso2709(simple_dto)
    parsed = from_iso2709(binary)
    assert parsed.to_string() == simple_dto.to_string()


def test_to_from_marcxml(simple_dto):
    xml = to_marcxml(simple_dto)
    parsed = from_marcxml(xml)
    assert parsed.to_string() == simple_dto.to_string()


def test_iso2709_to_marcxml_roundtrip(simple_dto):
    binary = to_iso2709(simple_dto)
    dto_from_binary = from_iso2709(binary)
    xml = to_marcxml(dto_from_binary)
    dto_from_marcxml = from_marcxml(xml)
    assert dto_from_marcxml.to_string() == simple_dto.to_string()


def test_marcxml_to_iso2709_roundtrip(simple_dto):
    xml = to_marcxml(simple_dto)
    dto_from_marcxml = from_marcxml(xml)
    binary = to_iso2709(dto_from_marcxml)
    dto_from_binary = from_iso2709(binary)
    assert dto_from_binary.to_string() == simple_dto.to_string()

def test_empty_dto_roundtrip():
    dto = MarcDto()
    binary = to_iso2709(dto)
    parsed = from_iso2709(binary)
    assert parsed.to_string() == dto.to_string()

    xml = to_marcxml(dto)
    parsed_xml = from_marcxml(xml)
    assert parsed_xml.to_string() == dto.to_string()


def test_missing_indicators():
    dto = MarcDto()
    dto.insert_field(dto.create_field(tag="245", indicators="  ", subfields=[
        SubField(tag='a', value='Title without indicators')
    ]))
    binary = to_iso2709(dto)
    parsed = from_iso2709(binary)
    assert parsed.to_string() == dto.to_string()


def test_invalid_subfield_tag():
    dto = MarcDto()
    with pytest.raises(MarcSubfieldException):
        dto.insert_field(dto.create_field(tag="100", indicators="1 ", subfields=[
            SubField(tag='', value='Missing code')
        ]))


def test_long_tags_and_values():
    long_tag = 'x' * 10
    long_value = 'y' * 1000
    dto = MarcDto()
    with pytest.raises(MarcException):
        dto.insert_field(dto.create_field(tag="999", indicators="  ", subfields=[
            SubField(tag=long_tag, value=long_value)
        ]))

    binary = to_iso2709(dto)
    parsed = from_iso2709(binary)
    assert parsed.to_string() == dto.to_string()


def test_unicode_characters():
    dto = MarcDto()
    dto.insert_field(dto.create_field(tag="100", indicators="1 ", subfields=[
        SubField(tag='a', value='Søren Kierkegård')
    ]))
    binary = to_iso2709(dto)
    parsed = from_iso2709(binary)
    assert parsed.to_string() == dto.to_string()

    xml = to_marcxml(dto)
    parsed_xml = from_marcxml(xml)
    assert parsed_xml.to_string() == dto.to_string()