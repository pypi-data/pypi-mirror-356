import pytest
from marc21 import MarcDto, to_iso2709, from_iso2709, to_marcxml, from_marcxml, SubField


@pytest.fixture
def dto_with_extra_space():
    dto = MarcDto(extra_space=True)
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

def test_to_from_iso2709_with_extra_space(dto_with_extra_space):
    binary = to_iso2709(dto_with_extra_space)
    parsed = from_iso2709(binary, extra_space=True)
    assert parsed.to_string(show_description=False) == dto_with_extra_space.to_string(show_description=False)

def test_to_from_marcxml_with_extra_space(dto_with_extra_space):
    xml = to_marcxml(dto_with_extra_space)
    parsed = from_marcxml(xml, extra_space=True)
    assert parsed.to_string(show_description=False) == dto_with_extra_space.to_string(show_description=False)

def test_iso2709_to_marcxml_roundtrip_with_extra_space(dto_with_extra_space):
    binary = to_iso2709(dto_with_extra_space)
    dto_from_binary = from_iso2709(binary, extra_space=True)
    xml = to_marcxml(dto_from_binary)
    dto_from_marcxml = from_marcxml(xml, extra_space=True)
    assert dto_from_marcxml.to_string(show_description=False) == dto_with_extra_space.to_string(show_description=False)

def test_marcxml_to_iso2709_roundtrip_with_extra_space(dto_with_extra_space):
    xml = to_marcxml(dto_with_extra_space)
    dto_from_marcxml = from_marcxml(xml, extra_space=True)
    binary = to_iso2709(dto_from_marcxml)
    dto_from_binary = from_iso2709(binary, extra_space=True)
    assert dto_from_binary.to_string(show_description=False) == dto_with_extra_space.to_string(show_description=False)