import pytest
import uuid
from datetime import datetime, timezone
from chunk_metadata_adapter.semantic_chunk import SemanticChunk, ChunkMetrics, FeedbackMetrics
from chunk_metadata_adapter.chunk_query import ChunkQuery
from chunk_metadata_adapter.data_types import ChunkType, LanguageEnum, ChunkRole, ChunkStatus, BlockType
import pydantic
import hashlib

def test_semanticchunk_factory_valid():
    data = dict(
        chunk_uuid=str(uuid.uuid4()),
        type=ChunkType.DOC_BLOCK.value,
        text="test",
        language=LanguageEnum.EN,
        sha256="a"*64,
        created_at="2024-01-01T00:00:00+00:00",
        body="b",
        summary="s"
    )
    chunk = SemanticChunk.from_dict_with_autofill_and_validation(data)
    assert chunk.text == "test"
    assert chunk.body == "b"
    assert chunk.summary == "s"
    assert chunk.language == LanguageEnum.EN


def test_semanticchunk_factory_missing_required():
    with pytest.raises(pydantic.ValidationError) as e:
        SemanticChunk.from_dict_with_autofill_and_validation({})
    assert "[type=missing" in str(e.value)

def valid_uuid():
    return str(uuid.uuid4())

def valid_sha256():
    return "a" * 64

def valid_created_at():
    return datetime.now(timezone.utc).isoformat()

def test_chunkquery_empty():
    # Пустой фильтр — все поля None
    q = ChunkQuery()
    for field in q.model_fields:
        assert getattr(q, field) is None

def test_chunkquery_equality_fields():
    # Проверка равенства для обычных полей (только нужные поля)
    q = ChunkQuery(type='DocBlock', language='en', uuid=valid_uuid())
    assert q.type == 'DocBlock'
    assert q.language == 'en'
    assert len(q.uuid) == 36

def test_chunkquery_comparison_fields_str():
    # Проверка полей с операторами сравнения (строка)
    q = ChunkQuery(start='>100', end='<200', quality_score='[0.7,1.0]', year='in:2022,2023')
    assert q.start == '>100'
    assert q.end == '<200'
    assert q.quality_score == '[0.7,1.0]'
    assert q.year == 'in:2022,2023'

def test_chunkquery_comparison_fields_native():
    # Проверка полей с исходным типом
    q = ChunkQuery(start=10, end=20, quality_score=0.95, year=2023)
    assert q.start == 10
    assert q.end == 20
    assert q.quality_score == 0.95
    assert q.year == 2023

def test_chunkquery_mixed_fields():
    # Комбинированные условия
    q = ChunkQuery(type='DocBlock', start='>=0', end=100, coverage='>0.5', status='verified')
    assert q.type == 'DocBlock'
    assert q.start == '>=0'
    assert q.end == 100
    assert q.coverage == '>0.5'
    assert q.status == 'verified'

def example_chunkquery_usage():
    """
    Пример: поиск всех чанков типа 'DocBlock' с quality_score > 0.8 и годом 2022 или 2023
    """
    q = ChunkQuery(type='DocBlock', quality_score='>0.8', year='in:2022,2023')
    assert q.type == 'DocBlock'
    assert q.quality_score == '>0.8'
    assert q.year == 'in:2022,2023'

def test_chunkquery_factory_valid():
    # Корректный фильтр с равенством
    data = {"type": "DocBlock", "language": "en"}
    f, err = ChunkQuery.from_dict_with_validation(data)
    assert err is None
    assert f.type == "DocBlock"
    assert f.language == "en"

    # Корректный фильтр с диапазоном и in
    data2 = {"start": ">=10", "end": "<100", "year": "in:2022,2023"}
    f2, err2 = ChunkQuery.from_dict_with_validation(data2)
    assert err2 is None
    assert f2.start == ">=10"
    assert f2.end == "<100"
    assert f2.year == "in:2022,2023"

    # Сериализация и восстановление
    flat = f2.to_flat_dict()
    f2_restored = ChunkQuery.from_flat_dict(flat)
    assert f2_restored.start == f2.start
    assert f2_restored.end == f2.end
    assert f2_restored.year == f2.year

    # Пустой фильтр
    f3, err3 = ChunkQuery.from_dict_with_validation({})
    assert err3 is None
    for field in f3.__class__.model_fields:
        assert getattr(f3, field) is None

    # Ошибка: неверный тип
    bad = {"start": [1,2,3]}
    f4, err4 = ChunkQuery.from_dict_with_validation(bad)
    # Теперь возвращается объект с ошибочным значением, а не None
    assert err4 is not None
    assert "start" in err4["fields"]
    assert "must be str, int, float, bool or dict" in err4["fields"]["start"][0]

    # --- Негативные сценарии: несуществующее поле ---
    bad2 = {"not_a_field": 123}
    f5, err5 = ChunkQuery.from_dict_with_validation(bad2)
    # Pydantic игнорирует неизвестные поля, ошибки не будет
    assert f5 is not None
    assert err5 is None

    # None как значение
    f6, err6 = ChunkQuery.from_dict_with_validation({"type": None})
    assert err6 is None
    assert f6.type is None

    # Проверка фильтрации списка (минимальная логика)
    chunks = [
        {"type": "DocBlock", "start": 15, "year": 2022},
        {"type": "CodeBlock", "start": 5, "year": 2023},
        {"type": "DocBlock", "start": 50, "year": 2023},
    ]
    filter_data = {"type": "DocBlock", "start": ">=10"}
    f, _ = ChunkQuery.from_dict_with_validation(filter_data)
    def match(chunk, f):
        if f.type and chunk["type"] != f.type:
            return False
        if f.start and isinstance(f.start, str) and f.start.startswith(">="):
            try:
                val = int(f.start[2:])
                if chunk["start"] < val:
                    return False
            except Exception:
                return False
        return True
    filtered = [c for c in chunks if match(c, f)]
    assert len(filtered) == 2
    assert filtered[0]["start"] == 15
    assert filtered[1]["start"] == 50

def test_chunkquery_factory_positive_negative_cases():
    # --- Позитивные сценарии ---
    import uuid
    from chunk_metadata_adapter.data_types import ChunkType, ChunkRole, ChunkStatus, BlockType, LanguageEnum
    valid_uuid = str(uuid.uuid4())
    # Валидные UUID и enum
    data = {
        "uuid": valid_uuid,
        "source_id": valid_uuid,
        "task_id": valid_uuid,
        "subtask_id": valid_uuid,
        "unit_id": valid_uuid,
        "block_id": valid_uuid,
        "link_parent": valid_uuid,
        "link_related": valid_uuid,
        "type": ChunkType.DOC_BLOCK.value,
        "role": ChunkRole.DEVELOPER.value,
        "status": ChunkStatus.RAW.value,
        "block_type": BlockType.PARAGRAPH.value,
        "language": LanguageEnum.EN.value,
        "start": 10,
        "end": "<100",
        "year": "in:2022,2023",
        "quality_score": 0.9,
        "coverage": ">0.5",
        "cohesion": None,
        "boundary_prev": None,
        "boundary_next": None,
    }
    f, err = ChunkQuery.from_dict_with_validation(data)
    assert err is None, f"Unexpected error: {err}"
    assert f.type == ChunkType.DOC_BLOCK.value
    assert f.language == LanguageEnum.EN.value
    assert f.uuid == valid_uuid
    assert f.status == ChunkStatus.RAW.value
    assert f.start == 10
    assert f.end == "<100"
    assert f.year == "in:2022,2023"
    # --- Негативные сценарии: невалидные UUID ---
    bad_uuid = "not-a-uuid"
    data_bad_uuid = data.copy()
    data_bad_uuid["uuid"] = bad_uuid
    f2, err2 = ChunkQuery.from_dict_with_validation(data_bad_uuid)
    assert f2 is None
    assert err2 is not None
    assert "uuid" in err2["fields"]
    assert "UUIDv4" in err2["fields"]["uuid"][0]
    # --- Негативные сценарии: невалидный enum ---
    data_bad_enum = data.copy()
    data_bad_enum["type"] = "NotAChunkType"
    f3, err3 = ChunkQuery.from_dict_with_validation(data_bad_enum)
    assert f3 is None
    assert err3 is not None
    assert "type" in err3["fields"]
    assert "one of" in err3["fields"]["type"][0]
    # --- Негативные сценарии: невалидный тип для поля, где допускается только str/int/float/bool ---
    data_bad_type = data.copy()
    data_bad_type["start"] = [1,2,3]  # список не допускается
    f4, err4 = ChunkQuery.from_dict_with_validation(data_bad_type)
    # Теперь возвращается объект с ошибочным значением, а не None
    assert err4 is not None
    assert "start" in err4["fields"]
    assert "must be str, int, float, bool or dict" in err4["fields"]["start"][0]
    # --- Позитив: допускается str для start/end/year ---
    data_str = data.copy()
    data_str["start"] = ">=10"
    data_str["end"] = "<100"
    data_str["year"] = "in:2022,2023"
    f5, err5 = ChunkQuery.from_dict_with_validation(data_str)
    assert err5 is None
    assert f5.start == ">=10"
    assert f5.end == "<100"
    assert f5.year == "in:2022,2023"

def test_chunkquery_only_source_id():
    # Передаём только source_id
    from chunk_metadata_adapter.chunk_query import ChunkQuery
    import uuid
    sid = str(uuid.uuid4())
    data = {"source_id": sid}
    obj, err = ChunkQuery.from_dict_with_validation(data)
    assert err is None
    assert obj.source_id == sid
    flat_dict = obj.to_flat_dict()
    # Все остальные поля должны быть None
    for field in obj.model_fields:
        if field != "source_id":
            assert getattr(obj, field) is None, f"Field {field} is not None: {getattr(obj, field)}" 
    for field in flat_dict:
        if field != "source_id":
            assert flat_dict[field] is None, f"Field {field} is not None: {flat_dict[field]}"

def test_json_and_dict_serialization():
    """
    Test to_dict, to_json, from_dict, and from_json methods.
    """
    chunk = SemanticChunk(
        uuid=valid_uuid(),
        source_id=valid_uuid(),
        body="Test for serialization",
        text="Test for serialization",
        type=ChunkType.COMMENT
    )
    
    # to_dict and from_dict
    chunk_dict = chunk.model_dump()
    assert isinstance(chunk_dict, dict)
    assert chunk_dict['text'] == "Test for serialization"
    
    recreated_from_dict = SemanticChunk.model_validate(chunk_dict)
    assert recreated_from_dict.uuid == chunk.uuid
    assert recreated_from_dict.text == chunk.text

    # to_json and from_json
    chunk_json = chunk.model_dump_json()
    assert isinstance(chunk_json, str)
    
    recreated_from_json = SemanticChunk.model_validate_json(chunk_json)
    assert recreated_from_json.uuid == chunk.uuid
    assert recreated_from_json.text == chunk.text

def test_validate_and_fill_tags_links_processing():
    """
    Test the specific processing of tags and links in validate_and_fill.
    """
    data = {
        "uuid": valid_uuid(),
        "source_id": valid_uuid(),
        "body": "testing tags and links",
        "text": "testing tags and links",
        "type": "Comment",
        "tags": ["tag1", "tag2", "tag3"],
        "links": ["parent:d1b3e4f5-a1b2-4c3d-8e9f-a0b1c2d3e4f5"]
    }
    chunk, err = SemanticChunk.validate_and_fill(data)
    assert err is None
    assert chunk is not None
    assert chunk.tags == ["tag1", "tag2", "tag3"]
    assert chunk.links == ["parent:d1b3e4f5-a1b2-4c3d-8e9f-a0b1c2d3e4f5"]

    # Test with lists
    data_list = {
        "uuid": valid_uuid(),
        "source_id": valid_uuid(),
        "body": "testing tags and links with lists",
        "text": "testing tags and links with lists",
        "type": "Comment",
        "tags": ["tag1", "tag2"],
        "links": ["related:d1b3e4f5-a1b2-4c3d-8e9f-a0b1c2d3e4f5"]
    }
    chunk_list, err_list = SemanticChunk.validate_and_fill(data_list)
    assert err_list is None
    assert chunk_list is not None
    assert chunk_list.tags == ["tag1", "tag2"]
    assert chunk_list.links == ["related:d1b3e4f5-a1b2-4c3d-8e9f-a0b1c2d3e4f5"]

def test_validate_and_fill_created_at_processing():
    """
    Test the specific processing of created_at in validate_and_fill.
    """
    # 1. Test autofill
    data_no_date = {
        "uuid": valid_uuid(), "source_id": valid_uuid(), "text": "t", "body": "b", "type": "Log"
    }
    chunk_no_date, err_no_date = SemanticChunk.validate_and_fill(data_no_date)
    assert err_no_date is None
    assert chunk_no_date is not None
    assert chunk_no_date.created_at is not None

    # 2. Test parsing from timestamp
    import time
    ts = int(time.time())
    date_from_ts = datetime.fromtimestamp(ts, tz=timezone.utc)
    date_str_from_ts = date_from_ts.isoformat()
    data_ts = {
        "uuid": valid_uuid(), "source_id": valid_uuid(), "text": "t", "body": "b", "type": "Log", "created_at": date_str_from_ts
    }
    chunk_ts, err_ts = SemanticChunk.validate_and_fill(data_ts)
    assert err_ts is None
    assert chunk_ts is not None
    assert str(date_from_ts.year) in chunk_ts.created_at

    # 3. Test parsing from string
    date_str = "2023-01-01T12:00:00Z"
    data_str = {
        "uuid": valid_uuid(), "source_id": valid_uuid(), "text": "t", "body": "b", "type": "Log", "created_at": date_str
    }
    chunk_str, err_str = SemanticChunk.validate_and_fill(data_str)
    assert err_str is None
    assert chunk_str is not None
    assert "2023" in chunk_str.created_at

def test_flat_dict_conversion_roundtrip():
    """
    Test the roundtrip conversion: semantic -> flat -> semantic
    """
    original_chunk = SemanticChunk(
        uuid=valid_uuid(),
        source_id=valid_uuid(),
        body="testing flat dict roundtrip",
        text="testing flat dict roundtrip",
        type=ChunkType.TASK,
        tags=["a", "b"],
        links=["parent:d1b3e4f5-a1b2-4c3d-8e9f-a0b1c2d3e4f5"],
        block_meta={"author": "tester"},
        quality_score=0.88
    )
    
    flat_dict = original_chunk.to_flat_dict(for_redis=False)
    assert isinstance(flat_dict, dict)
    assert flat_dict['tags'] == ["a", "b"]
    assert flat_dict['links'] == ["parent:d1b3e4f5-a1b2-4c3d-8e9f-a0b1c2d3e4f5"]
    assert flat_dict['block_meta.author'] == 'tester'
    assert flat_dict['quality_score'] == 0.88

    restored_chunk = SemanticChunk.from_flat_dict(flat_dict)
    assert restored_chunk.uuid == original_chunk.uuid
    assert restored_chunk.text == original_chunk.text
    assert restored_chunk.tags == original_chunk.tags
    assert restored_chunk.links == original_chunk.links
    assert restored_chunk.block_meta == original_chunk.block_meta
    assert restored_chunk.quality_score == original_chunk.quality_score

def test_from_flat_dict_with_unknown_fields():
    """
    Test that from_flat_dict correctly handles unknown fields.
    """
    flat_data = {
        "uuid": valid_uuid(),
        "source_id": valid_uuid(),
        "text": "test unknown",
        "type": "Log",
        "body": "b",
        "unknown_field": "some_value",
        "nested.unknown": "another_value"
    }
    chunk = SemanticChunk.from_flat_dict(flat_data)
    assert chunk is not None
    assert chunk.text == "test unknown"
    # Pydantic model should ignore unknown fields
    assert not hasattr(chunk, 'unknown_field')

def test_to_redis_dict_conversion():
    """
    Test the to_redis_dict method and its specific conversions.
    """
    chunk = SemanticChunk(
        uuid=valid_uuid(),
        source_id=valid_uuid(),
        body="testing redis dict",
        text="testing redis dict",
        type=ChunkType.METRIC,
        is_public=True,
        tags=['redis', 'test', '123'], # Now all are strings
        block_meta={'version': 1.0}
    )

    redis_dict = chunk.to_flat_dict(for_redis=True)
    assert redis_dict['is_public'] == 'true'
    assert redis_dict['block_meta.version'] == '1.0'
    assert 'embedding' not in redis_dict
    
    # Check that 'tags' is a list of strings
    assert 'tags' in redis_dict
    assert isinstance(redis_dict['tags'], list)
    assert redis_dict['tags'] == ['redis', 'test', '123']

def test_from_flat_dict_type_restoration():
    """
    Test that from_flat_dict correctly restores types from strings where possible.
    """
    flat = {
        'uuid': valid_uuid(),
        'source_id': valid_uuid(),
        'body': 'body',
        'type': 'Task',
        'is_public': 'true',
        'quality_score': '0.8',
        'ordinal': '50',
        'tags': '["a", "b", "1"]' # JSON string list
    }

    chunk = SemanticChunk.from_flat_dict(flat)
    assert chunk.is_public is True
    assert chunk.quality_score == 0.8
    assert chunk.ordinal == 50
    assert chunk.tags == ["a", "b", "1"]

def test_validate_and_fill_invalid_enum():
    """
    Test validate_and_fill with an invalid enum value that has a default.
    """
    data = {
        "uuid": valid_uuid(),
        "source_id": valid_uuid(),
        "body": "Test invalid enum",
        "type": "InvalidTypeValue"
    }
    chunk, err = SemanticChunk.validate_and_fill(data)
    assert err is None
    assert chunk is not None
    assert chunk.type == ChunkType.default_value()

def test_chunk_metrics_feedback_properties():
    """Test feedback properties in ChunkMetrics."""
    # Test with specific values
    metrics_with_feedback = ChunkMetrics(feedback=FeedbackMetrics(accepted=1, rejected=2, modifications=3))
    assert metrics_with_feedback.feedback_accepted == 1
    assert metrics_with_feedback.feedback_rejected == 2
    assert metrics_with_feedback.feedback_modifications == 3

    # Test case for when default_factory is used
    metrics_with_default_feedback = ChunkMetrics()
    assert metrics_with_default_feedback.feedback_accepted == 0
    assert metrics_with_default_feedback.feedback_rejected == 0
    assert metrics_with_default_feedback.feedback_modifications == 0

    # Test case for when feedback is None, which is allowed by Optional[]
    metrics_with_none_feedback = ChunkMetrics(feedback=None)
    assert metrics_with_none_feedback.feedback_accepted is None
    assert metrics_with_none_feedback.feedback_rejected is None
    assert metrics_with_none_feedback.feedback_modifications is None

def test_semantic_chunk_init_with_source_lines():
    """Test SemanticChunk initialization with source_lines."""
    chunk = SemanticChunk(
        uuid=valid_uuid(),
        source_id=valid_uuid(),
        body="body",
        type=ChunkType.DOC_BLOCK,
        source_lines=[10, 20]
    )
    assert chunk.source_lines_start == 10
    assert chunk.source_lines_end == 20
    assert chunk.source_lines == [10, 20]

def test_get_default_prop_val():
    """Test get_default_prop_val method."""
    assert SemanticChunk.get_default_prop_val("tags") == []
    assert SemanticChunk.get_default_prop_val("links") == []
    with pytest.raises(ValueError):
        SemanticChunk.get_default_prop_val("non_existent_prop")

def test_source_lines_setter():
    """Test the source_lines setter."""
    chunk = SemanticChunk(uuid=valid_uuid(), source_id=valid_uuid(), body="body", type=ChunkType.DOC_BLOCK)
    chunk.source_lines = [5, 15]
    assert chunk.source_lines_start == 5
    assert chunk.source_lines_end == 15

    chunk.source_lines = None
    assert chunk.source_lines_start is None
    assert chunk.source_lines_end is None

def test_from_flat_dict_edge_cases():
    """Test from_flat_dict with edge cases for lists and year."""
    # Test empty string and "null" for tags/links
    flat_empty = {
        'uuid': valid_uuid(), 'source_id': valid_uuid(), 'body': 'b', 'type': 'DocBlock',
        'tags': ' ', 'links': 'null'
    }
    chunk_empty = SemanticChunk.from_flat_dict(flat_empty)
    assert chunk_empty.tags == []
    assert chunk_empty.links == []

    # Test year=0 becomes None
    flat_year_zero = {
        'uuid': valid_uuid(), 'source_id': valid_uuid(), 'body': 'b', 'type': 'DocBlock', 'year': 0
    }
    chunk_year_zero = SemanticChunk.from_flat_dict(flat_year_zero)
    assert chunk_year_zero.year is None

    # Test bad list format raises error
    flat_bad_links = {
        'uuid': valid_uuid(), 'source_id': valid_uuid(), 'body': 'b', 'type': 'DocBlock',
        'links': 'not_a_json_list'
    }
    with pytest.raises(ValueError):
        SemanticChunk.from_flat_dict(flat_bad_links)

def test_sha256_validation():
    """Test sha256 validator."""
    with pytest.raises(pydantic.ValidationError):
        SemanticChunk(
            uuid=valid_uuid(), source_id=valid_uuid(), body="body", type=ChunkType.DOC_BLOCK,
            sha256="invalid_hash"
        )
    # Valid hash should pass
    valid_sha = hashlib.sha256(b"text").hexdigest()
    chunk = SemanticChunk(
        uuid=valid_uuid(), source_id=valid_uuid(), body="body", type=ChunkType.DOC_BLOCK,
        sha256=valid_sha
    )
    assert chunk.sha256 == valid_sha

def test_created_at_validation():
    """Test created_at validator."""
    with pytest.raises(pydantic.ValidationError):
        SemanticChunk(
            uuid=valid_uuid(), source_id=valid_uuid(), body="body", type=ChunkType.DOC_BLOCK,
            created_at="not-a-date"
        )
    
    valid_date = datetime.now(timezone.utc).isoformat()
    chunk = SemanticChunk(
        uuid=valid_uuid(), source_id=valid_uuid(), body="body", type=ChunkType.DOC_BLOCK,
        created_at=valid_date
    )
    assert chunk.created_at == valid_date

def test_uuid_validation():
    """Test uuid/chunkid field validators."""
    with pytest.raises(pydantic.ValidationError):
        SemanticChunk(
            uuid="not-a-uuid", source_id=valid_uuid(), body="body", type=ChunkType.DOC_BLOCK
        )

    
    