import pytest
from chunk_metadata_adapter.data_types import ChunkType, ChunkRole, ChunkStatus, BlockType, LanguageEnum, ComparableEnum

# Test data for all enums
ENUM_TEST_CASES = [
    (ChunkType, "DocBlock", "docblock", "InvalidType"),
    (ChunkRole, "system", "SYSTEM", "InvalidRole"),
    (ChunkStatus, "new", "NEW", "InvalidStatus"),
    (BlockType, "paragraph", "PARAGRAPH", "InvalidBlockType"),
    (LanguageEnum, "en", "EN", "InvalidLang"),
]

@pytest.mark.parametrize("enum_class, valid_str, valid_str_case, invalid_str", ENUM_TEST_CASES)
def test_enum_from_string(enum_class: ComparableEnum, valid_str: str, valid_str_case: str, invalid_str: str):
    """Test the from_string class method for all ComparableEnum subclasses."""
    # Test with a valid string
    result = enum_class.from_string(valid_str)
    assert result is not None
    assert result.value == valid_str or result.value.lower() == valid_str.lower()

    # Test with a case-insensitive valid string
    result_case = enum_class.from_string(valid_str_case)
    assert result_case is not None
    assert result_case == result  # Should be the same enum member

    # Test with an invalid string
    assert enum_class.from_string(invalid_str) is None

    # Test with None
    assert enum_class.from_string(None) is None

    # Test with an empty string
    assert enum_class.from_string("") is None

@pytest.mark.parametrize("enum_class, valid_str, valid_str_case, invalid_str", ENUM_TEST_CASES)
def test_enum_eqstr(enum_class: ComparableEnum, valid_str: str, valid_str_case: str, invalid_str: str):
    """Test the eqstr method for all ComparableEnum subclasses."""
    # Get the enum member using from_string
    enum_member = enum_class.from_string(valid_str)
    assert enum_member is not None

    # Test with a matching string
    assert enum_member.eqstr(valid_str) is True

    # Test with a case-insensitive matching string
    assert enum_member.eqstr(valid_str_case) is True

    # Test with a non-matching string
    assert enum_member.eqstr(invalid_str) is False

    # Test with None
    assert enum_member.eqstr(None) is False

    # Test with an empty string
    assert enum_member.eqstr("") is False

def test_language_enum_edge_cases():
    """Test edge cases for LanguageEnum."""
    # Check "uk" which was added recently
    assert LanguageEnum.from_string("uk") == LanguageEnum.UK
    assert LanguageEnum.from_string("UA") is None # Should be 'uk'
    assert LanguageEnum.UK.eqstr("uk") is True
    assert LanguageEnum.UK.eqstr("UK") is True

    # Check UNKNOWN
    assert LanguageEnum.from_string("UNKNOWN") == LanguageEnum.UNKNOWN
    assert LanguageEnum.UNKNOWN.eqstr("unknown") is True 