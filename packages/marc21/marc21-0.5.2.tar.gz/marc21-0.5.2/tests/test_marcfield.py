import pytest
from marc21 import MarcField, SubField, MarcDictionary, MarcException


class TestMarcField:

    #  Create a new MarcField object with valid parameters.
    def test_create_new_marcfield_with_valid_parameters(self):
        # Given
        tag = '245'
        field_type = 'd'
        repeatable = True
        description = 'Title Statement'
    
        # When
        field = MarcField(tag=tag, fieldtype=field_type, repeatable=repeatable, description=description)

        # Then
        assert field.tag == tag
        assert field.type == field_type
        assert field.repeatable == repeatable
        assert field.description == description
        assert field.has_indicators is True
        assert field.indicators == '  '
        assert field.subfields == []

    #  Add a new subfield to a MarcField object with valid parameters.
    def test_add_new_subfield_with_valid_parameters(self):
        # Given
        tag = '245'
        field_type = 'd'
        repeatable = True
        description = 'Title Statement'
        field = MarcField(tag=tag, fieldtype=field_type, repeatable=repeatable, description=description)
    
        subfield_tag = 'a'
        subfield_repeatable = False
        subfield_description = 'Title'
    
        # When
        field.add_SubField(tag=subfield_tag, repeatable=subfield_repeatable, description=subfield_description)
    
        # Then
        assert len(field.subfields) == 1
        assert field.subfields[0].tag == subfield_tag
        assert field.subfields[0].repeatable == subfield_repeatable
        assert field.subfields[0].description == subfield_description

        del field

    #  Set the value of the indicators attribute in a MarcField object.
    def test_set_indicators_attribute(self):
        # Given
        tag = '245'
        field_type = 'd'
        repeatable = True
        description = 'Title Statement'
        field = MarcField(tag=tag, fieldtype=field_type, repeatable=repeatable, description=description)
    
        indicators = '10'
    
        # When
        field.set_indicators(indicators=indicators)
    
        # Then
        assert field.indicators == indicators

        del field

    #  Check if a subfield with a given tag is present in a MarcField object.
    def test_check_if_subfield_present(self):
        # Given
        tag = '245'
        field_type = 'd'
        repeatable = True
        description = 'Title Statement'
        field = MarcField(tag=tag, fieldtype=field_type, repeatable=repeatable, description=description)
    
        subfield_tag = 'a'
        subfield_repeatable = False
        subfield_description = 'Title'
    
        field.add_SubField(tag=subfield_tag, repeatable=subfield_repeatable, description=subfield_description)
    
        # When
        is_present = field.is_subfield_present(tag=subfield_tag)
    
        # Then
        assert is_present is True

        del field

    #  Create a new MarcField object with repeatable set to True.
    def test_create_new_marcfield_with_repeatable_true(self):
        # Given
        tag = '245'
        field_type = 'd'
        repeatable = True
        description = 'Title Statement'
    
        # When
        field = MarcField(tag=tag, fieldtype=field_type, repeatable=repeatable, description=description)
    
        # Then
        assert field.repeatable is True

        del field

    #  Initializes a new instance of MarcField with mandatory parameters tag and type, and optional parameters
    #  repeatable, description, has_indicators, indicators, data, and subfields.
    def test_init_with_mandatory_and_optional_parameters(self):
        # Given
        tag = '001'
        field_type = 'c'
        repeatable = False
        description = 'Unique identifier'
        has_indicators = False
        indicators = ''
        data = '12345'
        subfields = []

        # When
        marc_field = MarcField(tag, field_type, repeatable, description, has_indicators, indicators, data, subfields)

        # Then
        assert marc_field.tag == tag
        assert marc_field.type == field_type
        assert marc_field.repeatable == repeatable
        assert marc_field.description == description
        assert marc_field.has_indicators == has_indicators
        assert marc_field.data == data

        del marc_field

    #  Initializes the tag, field_type, repeatable, description, has_indicators, indicators, data, and subfields attributes with the values passed as parameters.
    def test_init_with_parameters_values(self):
        # Given
        tag = '001'
        field_type = 'c'
        repeatable = True
        description = 'Description'
        has_indicators = False
        indicators = '12'
        data = 'Data'
        subfields = [SubField('a', True, 'Subfield A'), SubField('b', False, 'Subfield B')]

        # When
        marc_field = MarcField(tag, field_type, repeatable, description, has_indicators, indicators, data, subfields)

        # Then
        assert marc_field.tag == tag
        assert marc_field.type == field_type
        assert marc_field.repeatable == repeatable
        assert marc_field.description == description
        assert marc_field.has_indicators == has_indicators
        assert marc_field.data == data

        del marc_field


    #  Initializes the subfields attribute with an empty list if no subfields are passed as parameters.
    def test_init_with_no_subfields(self):
        # Given
        tag = '100'
        field_type = 'd'

        # When
        marc_field = MarcField(tag, field_type)

        # Then
        assert marc_field.subfields == []

        del marc_field

    #  Initializes the has_indicators attribute to True if the type is 'c' or 'd'.
    def test_init_has_indicators_true(self):
        # Given
        tag = '101'
        field_type = 'd'

        # When
        marc_field = MarcField(tag, field_type)

        # Then
        assert marc_field.has_indicators is True

        del marc_field

    #  Initializes the has_indicators attribute to True if the type is 'c' or 'd'.
    def test_init_has_indicators_false(self):
        # Given
        tag = '001'
        field_type = 'c'

        # When
        marc_field = MarcField(tag, field_type)

        # Then
        assert marc_field.has_indicators is False

        del marc_field

    #  Initializes the indicators attribute to '  ' if the type is 'c' or 'd'.
    def test_init_indicators(self):
        # Given
        tag = '101'
        field_type = 'd'

        # When
        marc_field = MarcField(tag, field_type)

        # Then
        assert marc_field.indicators == '  '

        del marc_field


    def test_set_indicators(self):
        # Given
        tag = '101'
        field_type = 'd'
        indicators = '12'

        # When
        marc_field = MarcField(tag, field_type)
        marc_field.indicators = indicators

        # Then
        assert marc_field.indicators == indicators

        del marc_field

    #  Initializes the data attribute to '  ' if the type is 'c' or 'd'.
    def test_init_data(self):
        # Given
        tag = '001'
        field_type = 'c'

        # When
        marc_field = MarcField(tag, field_type)

        # Then
        assert marc_field.data == '  '

        del marc_field

    #  Should return a new instance of MarcField with the same values as the original instance
    def test_return_new_instance_with_same_values(self):
        # Given
        field1 = MarcField('001', 'c', description='Control Number', data='12345')

        # When
        field2 = field1.__copy__()

        # Then
        assert isinstance(field2, MarcField)
        assert field2.tag == field1.tag
        assert field2.type == field1.type
        assert field2.repeatable == field1.repeatable
        assert field2.description == field1.description
        assert field2.has_indicators == field1.has_indicators
        if field2.type == 'c':
            assert field2.data == field1.data
        else:
            assert field2.subfields == field1.subfields

        del field1
        del field2


    #  Should return a new instance of MarcField with a different memory address than the original instance
    def test_return_new_instance_with_different_memory_address(self):
        # Given
        field1 = MarcField('001', 'c', description='Control Number', data='12345')

        # When
        field2 = field1.__copy__()

        # Then
        assert id(field2) != id(field1)

        del field1
        del field2


    #  Should return a new instance of MarcField with subfields that are also new instances with different memory addresses than the original subfields
    def test_return_new_instance_with_new_subfields(self):
        # Given
        subfield1 = SubField('a', repeatable=True, description='Subfield A', value='Value A')
        subfield2 = SubField('b', repeatable=False, description='Subfield B', value='Value B')
        field1 = MarcField('100', 'd', description='Control Number', data='12345', subfields=[subfield1, subfield2])

        # When
        field2 = field1.__copy__()

        # Then
        assert id(field2.subfields[0]) != id(field1.subfields[0])
        assert id(field2.subfields[1]) != id(field1.subfields[1])

        del field1
        del field2
        del subfield1
        del subfield2

    #  add a new subfield with valid parameters and repeatable=True
    def test_add_new_subfield_with_valid_parameters_and_repeatable_true(self):
        # Given
        tag = '245'
        field_type = 'd'
        repeatable = True
        description = 'Title Statement'
        field = MarcField(tag=tag, fieldtype=field_type, repeatable=repeatable, description=description)

        # When
        subfield_tag = 'a'
        subfield_repeatable = True
        subfield_description = 'Title'
        field.add_SubField(tag=subfield_tag, repeatable=subfield_repeatable, description=subfield_description)

        # Then
        assert len(field.subfields) == 1
        assert field.subfields[0].tag == subfield_tag
        assert field.subfields[0].repeatable == subfield_repeatable
        assert field.subfields[0].description == subfield_description

        del field

    #  add multiple subfields with different tags
    def test_add_multiple_subfields_with_different_tags(self):
        # Given
        tag = '245'
        field_type = 'd'
        repeatable = True
        description = 'Title Statement'
        field = MarcField(tag=tag, fieldtype=field_type, repeatable=repeatable, description=description)

        # When
        subfield1_tag = 'a'
        subfield1_repeatable = False
        subfield1_description = 'Title'
        field.add_SubField(tag=subfield1_tag, repeatable=subfield1_repeatable, description=subfield1_description)

        subfield2_tag = 'b'
        subfield2_repeatable = False
        subfield2_description = 'Subtitle'
        field.add_SubField(tag=subfield2_tag, repeatable=subfield2_repeatable, description=subfield2_description)

        # Then
        assert len(field.subfields) == 2
        assert field.subfields[0].tag == subfield1_tag
        assert field.subfields[0].repeatable == subfield1_repeatable
        assert field.subfields[0].description == subfield1_description
        assert field.subfields[1].tag == subfield2_tag
        assert field.subfields[1].repeatable == subfield2_repeatable
        assert field.subfields[1].description == subfield2_description

        del field


    #  add multiple subfields with the same tag and repeatable=True
    def test_add_multiple_subfields_with_same_tag_and_repeatable_true(self):
        # Given
        tag = '245'
        field_type = 'd'
        repeatable = True
        description = 'Title Statement'
        field = MarcField(tag=tag, fieldtype=field_type, repeatable=repeatable, description=description)

        # When
        subfield1_tag = 'a'
        subfield1_repeatable = True
        subfield1_description = 'Title'
        field.add_SubField(tag=subfield1_tag, repeatable=subfield1_repeatable, description=subfield1_description)

        subfield2_tag = 'a'
        subfield2_repeatable = True
        subfield2_description = 'Subtitle'
        field.add_SubField(tag=subfield2_tag, repeatable=subfield2_repeatable, description=subfield2_description)

        # Then
        assert len(field.subfields) == 2
        assert field.subfields[0].tag == subfield1_tag
        assert field.subfields[0].repeatable == subfield1_repeatable
        assert field.subfields[0].description == subfield1_description
        assert field.subfields[1].tag == subfield2_tag
        assert field.subfields[1].repeatable == subfield2_repeatable
        assert field.subfields[1].description == subfield2_description

        del field

    def test_testing_for_present_subfield(self):
        md = MarcDictionary()

        field = md.get_field_by_tag(tag='245', copy=True)

        assert field is not None

        result = field.is_subfield_present(tag='a')

        assert result == True


    def test_testing_for_not_present_subfield(self):
        md = MarcDictionary()

        field = md.get_field_by_tag(tag='245', copy=True)

        assert field is not None

        result = field.is_subfield_present(tag='d')

        assert result == False


    def test_testing_for_subfield_in_empty_list_of_subfields(self):
        field = MarcField(tag='999', fieldtype='d', repeatable=True, description='Test')

        assert field is not None

        result = field.is_subfield_present(tag='a')

        assert result == False


    def test_testing_for_subfield_with_empty_tag(self):
        field = MarcField(tag='999', fieldtype='d', repeatable=True, description='Test')

        assert field is not None

        result = field.is_subfield_present(tag='')

        assert result == False

    def test_add_duplicate_non_repeatable_subfield(self):
        md = MarcDictionary()

        field = md.get_field_by_tag(tag='245', copy=True)

        assert field is not None

        with pytest.raises(MarcException):
            field.add_SubField(tag='a', repeatable=False, description='Test')


    def test_add_invalid_subfield(self):
        md = MarcDictionary()

        field = md.get_field_by_tag(tag='245', copy=True)

        assert field is not None

        with pytest.raises(MarcException):
            field.add_SubField(tag='', repeatable=True, description='Test')

    def test_convert_control_field_to_json(self):
        tag = '003'
        md = MarcDictionary()

        field = md.get_field_by_tag(tag=tag, copy=True)

        assert field is not None

        json = field.__json__()

        assert len(json) > 0
        assert json['tag'] == tag

    def test_convert_data_field_to_json(self):
        tag = '245'
        md = MarcDictionary()

        field = md.get_field_by_tag(tag=tag, copy=True)

        assert field is not None

        json = field.__json__()

        assert len(json) > 0
        assert json['tag'] == tag

    def test_create_MarcField_with_invalid_type(self):
        with pytest.raises(MarcException):
            MarcField(tag='999', fieldtype='z', repeatable=True, description='Test')



