import pytest
import json
import uuid
from datetime import datetime, timezone
from chunk_metadata_adapter.semantic_chunk import SemanticChunk, ChunkMetrics, FeedbackMetrics, _autofill_min_length_str_fields
from chunk_metadata_adapter.data_types import ChunkType, ChunkRole, ChunkStatus, LanguageEnum, BlockType
from chunk_metadata_adapter.utils import ChunkId
from pydantic import ValidationError


def test_get_default_prop_val_invalid_property():
    """Test get_default_prop_val with invalid property name - lines 154-158"""
    with pytest.raises(ValueError, match="No such property: invalid_field"):
        SemanticChunk.get_default_prop_val("invalid_field")


def test_from_flat_dict_malformed_json_tags():
    """Test from_flat_dict with malformed JSON for tags field - lines 213-219"""
    data = {
        "body": "test",
        "type": ChunkType.DOC_BLOCK.value,
        "tags": 'not,valid,json'  # Comma-separated fallback should work
    }
    chunk = SemanticChunk.from_flat_dict(data)
    # Should fallback to comma-separated parsing for tags
    assert chunk.tags == ["not", "valid", "json"]


def test_from_flat_dict_malformed_json_links():
    """Test from_flat_dict with malformed JSON for links field - lines 213-219"""
    # Links do NOT get comma-separated fallback parsing, unlike tags
    data = {
        "body": "test",
        "type": ChunkType.DOC_BLOCK.value,
        "links": 'invalid,json,for,links'  # Should raise error
    }
    with pytest.raises(ValueError, match="Field 'links' must be a list"):
        SemanticChunk.from_flat_dict(data)


def test_from_flat_dict_malformed_json_embedding():
    """Test from_flat_dict with malformed JSON for embedding field - lines 213-219"""
    data = {
        "body": "test", 
        "type": ChunkType.DOC_BLOCK.value,
        "embedding": '[0.1, 0.2, invalid]'  # Malformed JSON for embedding
    }
    # This should raise ValueError during JSON parsing
    with pytest.raises(ValueError, match="Field 'embedding' must be a list"):
        SemanticChunk.from_flat_dict(data)


def test_from_flat_dict_year_zero_in_data():
    """Test from_flat_dict with year=0 in original data - lines 218-221"""
    data = {
        "body": "test",
        "type": ChunkType.DOC_BLOCK.value,
        "year": 0  # Zero in original data
    }
    chunk = SemanticChunk.from_flat_dict(data)
    assert chunk.year is None


def test_from_flat_dict_embedding_from_metrics():
    """Test that embedding is preserved when provided directly - lines 262-263"""
    # Test case 1: embedding provided directly in data
    data_with_embedding = {
        "body": "test",
        "type": ChunkType.DOC_BLOCK.value,
        "embedding": [0.1, 0.2, 0.3],  # Direct embedding
        "metrics": json.dumps({"quality_score": 0.9})
    }
    chunk = SemanticChunk.from_flat_dict(data_with_embedding)
    # Embedding should be preserved when provided directly
    assert chunk.embedding == [0.1, 0.2, 0.3]
    
    # Test case 2: no embedding provided - should default to empty list
    data_without_embedding = {
        "body": "test",
        "type": ChunkType.DOC_BLOCK.value,
        "metrics": json.dumps({"quality_score": 0.9})
    }
    chunk2 = SemanticChunk.from_flat_dict(data_without_embedding)
    # Should default to empty list when no embedding
    assert chunk2.embedding == []


def test_validate_metadata_non_list_tags():
    """Test validate_metadata with non-list tags - lines 274-275"""
    # Create chunk first, then modify tags to bypass validation
    chunk = SemanticChunk(body="test", type=ChunkType.DOC_BLOCK, tags=["valid"])
    # Directly modify the __dict__ to bypass pydantic validation
    chunk.__dict__['tags'] = "not_a_list"  # Force invalid state
    with pytest.raises(ValueError, match="tags must be a list for structured metadata"):
        chunk.validate_metadata()


def test_validate_metadata_non_list_links():
    """Test validate_metadata with non-list links - lines 276-277"""
    # Create chunk first, then modify links to bypass validation
    chunk = SemanticChunk(body="test", type=ChunkType.DOC_BLOCK, links=["valid"])
    # Directly modify the __dict__ to bypass pydantic validation for tags first
    chunk.__dict__['tags'] = ["valid"]  # Keep tags valid
    chunk.__dict__['links'] = "not_a_list"  # Force invalid state for links
    with pytest.raises(ValueError, match="links must be a list for structured metadata"):
        chunk.validate_metadata()


def test_validate_and_fill_tokens_with_metrics_dict():
    """Test validate_and_fill with tokens and metrics as dict - lines 310, 314-317"""
    data = {
        "body": "test",
        "type": ChunkType.DOC_BLOCK.value,
        "tokens": 100,
        "metrics": {"quality_score": 0.5}
    }
    chunk, error = SemanticChunk.validate_and_fill(data)
    assert error is None
    assert chunk.metrics.tokens == 100


def test_validate_and_fill_tokens_with_metrics_object():
    """Test validate_and_fill with tokens and metrics as ChunkMetrics - lines 310, 314-317"""
    data = {
        "body": "test",
        "type": ChunkType.DOC_BLOCK.value,
        "tokens": 200,
        "metrics": ChunkMetrics(quality_score=0.7)
    }
    chunk, error = SemanticChunk.validate_and_fill(data)
    assert error is None
    assert chunk.metrics.tokens == 200


def test_validate_and_fill_tokens_no_metrics():
    """Test validate_and_fill with tokens but no metrics - lines 310, 314-317"""
    data = {
        "body": "test",
        "type": ChunkType.DOC_BLOCK.value,
        "tokens": 300
    }
    chunk, error = SemanticChunk.validate_and_fill(data)
    assert error is None
    assert chunk.metrics.tokens == 300


def test_validate_and_fill_malformed_tags():
    """Test validate_and_fill with malformed tags - lines 333, 337-340"""
    data = {
        "body": "test",
        "type": ChunkType.DOC_BLOCK.value,
        "tags": '{"invalid": "json"}'
    }
    chunk, error = SemanticChunk.validate_and_fill(data)
    assert chunk is None
    assert "must be a list" in error["error"]


def test_validate_and_fill_malformed_block_meta():
    """Test validate_and_fill with malformed block_meta - lines 276-278"""
    data = {
        "body": "test",
        "type": ChunkType.DOC_BLOCK.value,
        "block_meta": '{"invalid": json}'  # Malformed JSON
    }
    chunk, error = SemanticChunk.validate_and_fill(data)
    assert chunk is None
    assert "must be a dict" in error["error"]


def test_validate_and_fill_enum_handling():
    """Test enum handling in validate_and_fill - lines 384-389"""
    data = {
        "body": "test",
        "type": "invalid_type",  # Will be auto-filled
        "role": "invalid_role",  # Will be auto-filled  
        "status": "invalid_status",  # Will be auto-filled
        "block_type": "invalid_block_type",  # Will be auto-filled
        "language": "invalid_language"  # Will be auto-filled
    }
    chunk, error = SemanticChunk.validate_and_fill(data)
    # Should succeed due to auto-filling
    assert error is None
    assert chunk is not None


def test_validate_and_fill_str_min_length_chunking_version():
    """Test that chunking_version remains empty when None - user choice, not auto-filled"""
    data = {
        "body": "test",
        "type": ChunkType.DOC_BLOCK.value,
        "chunking_version": None  # None should become "" - left to user choice
    }
    chunk, error = SemanticChunk.validate_and_fill(data)
    assert error is None
    # chunking_version should NOT be auto-filled - left to user choice
    assert chunk.chunking_version == ""  # Empty string, not forced "1.0"


def test_validate_and_fill_general_exception():
    """Test general exception handling in validate_and_fill - lines 436, 438, 440"""
    data = {
        "body": "test",
        "type": ChunkType.DOC_BLOCK.value
    }
    
    # Mock to cause a general exception
    original_init = SemanticChunk.__init__
    def mock_init(self, **kwargs):
        raise RuntimeError("Test exception")
    
    SemanticChunk.__init__ = mock_init
    try:
        chunk, error = SemanticChunk.validate_and_fill(data)
        assert chunk is None
        assert error["error"] == "Test exception"
        assert error["fields"] == {}
    finally:
        SemanticChunk.__init__ = original_init


def test_model_post_init_metrics_dict():
    """Test model_post_init with metrics as dict - lines 462-463"""
    data = {
        "body": "test",
        "type": ChunkType.DOC_BLOCK,
        "metrics": {"quality_score": 0.8}  # Dict instead of ChunkMetrics
    }
    chunk = SemanticChunk(**data)
    assert isinstance(chunk.metrics, ChunkMetrics)
    assert chunk.metrics.quality_score == 0.8


def test_model_post_init_year_zero():
    """Test model_post_init with year=0 - lines 468"""
    chunk = SemanticChunk(body="test", type=ChunkType.DOC_BLOCK, year=0)
    assert chunk.year is None


def test_field_validator_chunkid_exception():
    """Test ChunkId field validator exception handling - lines 494"""
    # This will test the exception path in validate_chunkid_fields
    with pytest.raises(ValidationError):
        SemanticChunk(body="test", type=ChunkType.DOC_BLOCK, uuid="not_a_valid_uuid")


def test_chunk_metrics_properties():
    """Test ChunkMetrics properties - lines 65, 69, 73"""
    metrics = ChunkMetrics(feedback=FeedbackMetrics(accepted=5, rejected=2, modifications=1))
    assert metrics.feedback_accepted == 5
    assert metrics.feedback_rejected == 2
    assert metrics.feedback_modifications == 1
    
    # Test with default feedback (should be FeedbackMetrics with default values)
    metrics_none = ChunkMetrics()
    assert metrics_none.feedback_accepted == 0  # Default value from FeedbackMetrics
    assert metrics_none.feedback_rejected == 0   # Default value from FeedbackMetrics
    assert metrics_none.feedback_modifications == 0  # Default value from FeedbackMetrics


def test_source_lines_property_setter():
    """Test source_lines property setter - lines 167-172"""
    chunk = SemanticChunk(body="test", type=ChunkType.DOC_BLOCK)
    
    # Valid case
    chunk.source_lines = [10, 20]
    assert chunk.source_lines_start == 10
    assert chunk.source_lines_end == 20


def test_autofill_min_length_str_fields_function():
    """Test _autofill_min_length_str_fields function - lines 517-518, 522-534"""
    data = {
        "body": "test",
        "type": ChunkType.DOC_BLOCK.value,
        "chunking_version": ""  # Empty string - should stay empty (user choice)
    }
    
    model_fields = SemanticChunk.model_fields
    result = _autofill_min_length_str_fields(data, model_fields)
    
    # chunking_version has min_length=0, so empty string stays empty
    assert result['chunking_version'] == ""  # Respects user choice, not forced to "1.0"


def test_validate_and_fill_int_float_handling():
    """Test int/float handling in validate_and_fill - lines 417-421"""
    data = {
        "body": "test",
        "type": ChunkType.DOC_BLOCK.value,
        "ordinal": None,  # Should be filled with 0
        "quality_score": ""  # Empty string should be handled
    }
    chunk, error = SemanticChunk.validate_and_fill(data)
    assert error is None
    assert chunk.ordinal == 0  # Default for int with ge=0
    assert chunk.quality_score == 0.0  # Default for float


def test_validate_and_fill_bool_handling():
    """Test bool handling in validate_and_fill - lines 417-421"""
    data = {
        "body": "test",
        "type": ChunkType.DOC_BLOCK.value,
        "is_public": None  # Should be filled with False
    }
    chunk, error = SemanticChunk.validate_and_fill(data)
    assert error is None
    assert chunk.is_public is False


def test_validate_and_fill_pydantic_basemodel():
    """Test BaseModel handling in validate_and_fill - lines 384-389"""
    data = {
        "body": "test",
        "type": ChunkType.DOC_BLOCK.value,
        "metrics": None  # Should be filled with empty ChunkMetrics
    }
    chunk, error = SemanticChunk.validate_and_fill(data)
    assert error is None
    assert chunk.metrics is not None


def test_validate_and_fill_list_handling():
    """Test list handling in validate_and_fill - lines 384-389"""
    data = {
        "body": "test",
        "type": ChunkType.DOC_BLOCK.value,
        "tags": None  # Should be filled with empty list
    }
    chunk, error = SemanticChunk.validate_and_fill(data)
    assert error is None
    assert chunk.tags == []


def test_validate_and_fill_dict_handling():
    """Test dict handling in validate_and_fill - lines 384-389"""
    data = {
        "body": "test",
        "type": ChunkType.DOC_BLOCK.value,
        "block_meta": None  # Should be filled with empty dict
    }
    chunk, error = SemanticChunk.validate_and_fill(data)
    assert error is None
    assert chunk.block_meta == {}


def test_from_flat_dict_year_not_in_data():
    """Test from_flat_dict when year not in original data - lines 218-221"""
    data = {
        "body": "test",
        "type": ChunkType.DOC_BLOCK.value
        # No year field at all
    }
    chunk = SemanticChunk.from_flat_dict(data)
    assert chunk.year is None


def test_model_post_init_block_meta_created_at():
    """Test model_post_init removes created_at from block_meta - lines ??? """
    data = {
        "body": "test",
        "type": ChunkType.DOC_BLOCK,
        "block_meta": {"created_at": "2023-01-01", "other": "value"}
    }
    chunk = SemanticChunk(**data)
    # created_at should be removed from block_meta
    assert "created_at" not in chunk.block_meta
    assert chunk.block_meta["other"] == "value"


def test_model_post_init_source_lines_sync():
    """Test model_post_init source_lines synchronization"""
    # This is tricky to test as source_lines isn't a real field
    chunk = SemanticChunk(body="test", type=ChunkType.DOC_BLOCK)
    chunk.source_lines_start = 10
    chunk.source_lines_end = 20
    # Manually call post_init
    chunk.model_post_init(None)
    # Should maintain the values
    assert chunk.source_lines_start == 10
    assert chunk.source_lines_end == 20


def test_from_flat_dict_empty_tags_null():
    """Test from_flat_dict with empty/null tags"""
    data = {
        "body": "test",
        "type": ChunkType.DOC_BLOCK.value,
        "tags": "null"  # Null string
    }
    chunk = SemanticChunk.from_flat_dict(data)
    assert chunk.tags == []


def test_from_flat_dict_empty_links_null():
    """Test from_flat_dict with empty/null links"""
    data = {
        "body": "test",
        "type": ChunkType.DOC_BLOCK.value,
        "links": ""  # Empty string
    }
    chunk = SemanticChunk.from_flat_dict(data)
    assert chunk.links == []


def test_from_flat_dict_empty_embedding_null():
    """Test from_flat_dict with empty/null embedding"""
    data = {
        "body": "test",
        "type": ChunkType.DOC_BLOCK.value,
        "embedding": "null"  # Null string
    }
    chunk = SemanticChunk.from_flat_dict(data)
    assert chunk.embedding == [] 