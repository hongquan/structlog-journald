from __future__ import annotations

import json
import subprocess
import time
from typing import Any

import structlog
from structlog.processors import CallsiteParameterAdder

from structlog_journald import JournaldProcessor


def query_journal(identifier: str, since: float, code_func: str | None = None) -> list[dict[str, Any]]:
    result = subprocess.run(
        [
            'journalctl',
            '--user',
            '-t',
            identifier,
            '--since=@' + str(int(since)),
            '-p',
            'debug',
            '--no-pager',
            '-o',
            'json',
        ],
        capture_output=True,
    )
    entries = [json.loads(ln) for ln in result.stdout.decode().splitlines() if ln.strip()]
    if code_func:
        entries = [e for e in entries if e.get('CODE_FUNC') == code_func]
    return entries


def test_integration_sends_message_to_journald() -> None:
    since = time.time()
    processor = JournaldProcessor(syslog_identifier='structlog-journald-test')

    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            CallsiteParameterAdder(),
            processor,
        ],
        logger_factory=structlog.PrintLoggerFactory(),
    )
    log = structlog.get_logger()

    log.info('Test message')

    entries = query_journal('structlog-journald-test', since, 'test_integration_sends_message_to_journald')
    assert len(entries) == 1
    assert entries[0]['MESSAGE'] == 'Test message'


def test_integration_sends_exception_to_journald() -> None:
    since = time.time()
    processor = JournaldProcessor(syslog_identifier='structlog-journald-test')

    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            CallsiteParameterAdder(),
            structlog.processors.format_exc_info,
            processor,
        ],
        logger_factory=structlog.PrintLoggerFactory(),
    )
    log = structlog.get_logger()

    try:
        raise ValueError('Test exception')
    except ValueError:
        log.exception('An error occurred')

    entries = query_journal('structlog-journald-test', since, 'test_integration_sends_exception_to_journald')
    assert len(entries) == 1
    assert 'An error occurred' in entries[0]['MESSAGE']
    assert 'ValueError: Test exception' in entries[0]['MESSAGE']


def test_integration_sends_extra_fields_to_journald() -> None:
    since = time.time()
    processor = JournaldProcessor(
        syslog_identifier='structlog-journald-test',
        extra_field_prefix='f_',
    )

    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            CallsiteParameterAdder(),
            processor,
        ],
        logger_factory=structlog.PrintLoggerFactory(),
    )
    log = structlog.get_logger()

    log.info('Message with extra', f_user='alice', f_role='admin')

    entries = query_journal('structlog-journald-test', since, 'test_integration_sends_extra_fields_to_journald')
    assert len(entries) == 1
    assert entries[0]['F_USER'] == 'alice'
    assert entries[0]['F_ROLE'] == 'admin'


def test_integration_sends_callsite_info_to_journald() -> None:
    since = time.time()
    processor = JournaldProcessor(syslog_identifier='structlog-journald-test')

    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            CallsiteParameterAdder(),
            processor,
        ],
        logger_factory=structlog.PrintLoggerFactory(),
    )
    log = structlog.get_logger()

    log.info('Message with callsite')

    entries = query_journal('structlog-journald-test', since, 'test_integration_sends_callsite_info_to_journald')
    assert len(entries) == 1
    assert 'CODE_FUNC' in entries[0]
    assert entries[0]['CODE_FUNC'] == 'test_integration_sends_callsite_info_to_journald'
    assert 'CODE_FILE' in entries[0]


def test_integration_maps_priority_by_level() -> None:
    since = time.time()
    processor = JournaldProcessor(syslog_identifier='structlog-journald-test')

    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            CallsiteParameterAdder(),
            processor,
        ],
        logger_factory=structlog.PrintLoggerFactory(),
    )
    log = structlog.get_logger()

    log.warning('Warning message')

    entries = query_journal('structlog-journald-test', since, 'test_integration_maps_priority_by_level')
    assert len(entries) == 1
    assert entries[0]['PRIORITY'] == '4'  # WARNING
