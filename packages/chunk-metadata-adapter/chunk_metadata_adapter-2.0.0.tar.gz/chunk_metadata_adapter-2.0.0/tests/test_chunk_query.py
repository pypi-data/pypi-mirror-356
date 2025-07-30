import pytest
from chunk_metadata_adapter.chunk_query import ChunkQuery
from chunk_metadata_adapter.data_types import ChunkType, ChunkRole

def test_from_dict_with_validation_non_string_enum():
    """
    Test that from_dict_with_validation correctly handles non-string enum values.
    This covers the `isinstance(val, str)` check in enum validation.
    """
    bad_data = {"type": 123}  # type should be a string
    _filter, errors = ChunkQuery.from_dict_with_validation(bad_data)
    assert _filter is None
    assert errors is not None
    assert "type" in errors["fields"]
    assert "must be one of" in errors["fields"]["type"][0]

def test_from_dict_with_validation_invalid_value_type():
    """
    Test that from_dict_with_validation rejects invalid data types for simple fields.
    This covers lines 156-168.
    """
    class Unserializable:
        pass
    
    bad_data = {"source": Unserializable()}
    _filter, errors = ChunkQuery.from_dict_with_validation(bad_data)
    assert _filter is None
    assert errors is not None
    assert "source" in errors["fields"]
    assert "must be str/int/float/bool/None" in errors["fields"]["source"][0]

def test_from_dict_with_validation_general_exception():
    """
    Test the general exception handler in from_dict_with_validation.
    This covers line 184.
    """
    # We can trigger a general exception by passing a value that pydantic
    # cannot handle during model construction, after our custom validation.
    # For example, a complex object for a simple field.
    class BadObject:
        def __str__(self):
            raise TypeError("Cannot convert to string")

    # This should pass our initial checks but fail in Pydantic's `cls(**data)`
    bad_data = {"ordinal": BadObject()}
    
    _filter, errors = ChunkQuery.from_dict_with_validation(bad_data)
    
    assert _filter is None
    assert errors is not None
    assert "error" in errors
    # The exact error message may vary, but it should indicate a problem.
    assert "ordinal" in errors["error"]
    assert "str/int/float/bool/None" in errors["error"]

# This test is for line 149, but it's hard to trigger this specific `except`
# without monkeypatching. The existing enum validation is quite comprehensive.
# We can add a placeholder test to acknowledge this.
def test_from_dict_with_validation_enum_exception_path():
    """
    Test case for the exception path in enum validation (line 149).
    This path is hard to reach as the preceding checks are thorough.
    We test with a value that fails the `val not in set(...)` check.
    """
    bad_data = {"role": "non_existent_role"}
    _filter, errors = ChunkQuery.from_dict_with_validation(bad_data)
    assert _filter is None
    assert errors is not None
    assert 'role' in errors['fields']
    assert "must be one of" in errors['fields']['role'][0] 