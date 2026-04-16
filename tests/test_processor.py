from __future__ import annotations

import pytest
from structlog.processors import CallsiteParameter

from structlog_journald.processors import JournaldProcessor


def test_extra_field_prefix_cannot_start_with_underscore() -> None:
    with pytest.raises(ValueError, match="extra_field_prefix cannot start with '_'"):
        JournaldProcessor(extra_field_prefix='_invalid')


def test_extract_common_fields_returns_logger_field() -> None:
    processor = JournaldProcessor()
    event_dict = {'logger': 'my_logger', 'event': 'test'}
    result = processor._extract_common_fields(event_dict)
    assert result == {'LOGGER': 'my_logger'}


def test_extract_common_fields_returns_empty_dict_without_logger() -> None:
    processor = JournaldProcessor()
    event_dict = {'event': 'test'}
    result = processor._extract_common_fields(event_dict)
    assert result == {}


def test_extract_extra_fields_extracts_prefixed_fields() -> None:
    processor = JournaldProcessor()
    event_dict = {'f_user': 'alice', 'f_role': 'admin', 'other': 'value'}
    result = processor._extract_extra_fields(event_dict)
    assert result == {'F_USER': 'alice', 'F_ROLE': 'admin'}


def test_extract_extra_fields_empty_prefix_returns_empty() -> None:
    processor = JournaldProcessor(extra_field_prefix='')
    event_dict = {'f_user': 'alice'}
    result = processor._extract_extra_fields(event_dict)
    assert result == {}


def test_extract_extra_fields_no_matching_prefix() -> None:
    processor = JournaldProcessor()
    event_dict = {'user': 'alice', 'role': 'admin'}
    result = processor._extract_extra_fields(event_dict)
    assert result == {}


def test_extract_callsite_info_extracts_all_fields() -> None:
    processor = JournaldProcessor()
    event_dict = {
        CallsiteParameter.MODULE.value: 'my_module',
        CallsiteParameter.FUNC_NAME.value: 'my_function',
        CallsiteParameter.PATHNAME.value: '/path/to/file.py',
        CallsiteParameter.LINENO.value: 42,
        CallsiteParameter.THREAD.value: 1234,
    }
    result = processor._extract_callsite_info(event_dict)
    assert result == {
        'MODULE': 'my_module',
        'CODE_FUNC': 'my_function',
        'CODE_FILE': '/path/to/file.py',
        'CODE_LINE': 42,
        'TID': 1234,
    }


def test_extract_callsite_info_partial_info() -> None:
    processor = JournaldProcessor()
    event_dict = {
        CallsiteParameter.FUNC_NAME.value: 'my_function',
        CallsiteParameter.PATHNAME.value: '/path/to/file.py',
    }
    result = processor._extract_callsite_info(event_dict)
    assert result == {
        'CODE_FUNC': 'my_function',
        'CODE_FILE': '/path/to/file.py',
    }


def test_extract_callsite_info_empty_dict_without_info() -> None:
    processor = JournaldProcessor()
    event_dict: dict = {}
    result = processor._extract_callsite_info(event_dict)
    assert result == {}


def test_format_extra_items_formats_items() -> None:
    processor = JournaldProcessor()
    event_dict = {
        'event': 'test',
        'user': 'alice',
        'count': 42,
    }
    result = processor._format_extra_items(event_dict)
    assert 'user=' in result
    assert "'alice'" in result
    assert 'count=42' in result


def test_format_extra_items_ignores_other_processor_keys() -> None:
    processor = JournaldProcessor()
    event_dict = {
        'event': 'test',
        'message': 'msg',
        'level': 'info',
        'user': 'alice',
    }
    result = processor._format_extra_items(event_dict)
    assert 'user=' in result
    assert 'event=' not in result
    assert 'message=' not in result
    assert 'level=' not in result


def test_format_extra_items_ignores_extra_field_prefix_keys() -> None:
    processor = JournaldProcessor(extra_field_prefix='f_')
    event_dict = {
        'event': 'test',
        'f_user': 'alice',
        'user': 'bob',
    }
    result = processor._format_extra_items(event_dict)
    assert 'user=' in result
    assert 'f_user=' not in result


def test_format_extra_items_ignores_underscore_keys() -> None:
    processor = JournaldProcessor()
    event_dict = {
        'event': 'test',
        '_internal': 'secret',
        'user': 'alice',
    }
    result = processor._format_extra_items(event_dict)
    assert 'user=' in result
    assert '_internal=' not in result
