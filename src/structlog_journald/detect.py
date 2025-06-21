import os


def is_journald_connected() -> bool:
    """Test if current process is connected with journald."""
    # In desktop (development): JOURNAL_STREAM and TERM are set. We want to log to console.
    # In service: JOURNAL_STREAM is set. TERM is set if stderr is connected to tty instead of journald.
    journal_stream = os.getenv('JOURNAL_STREAM')
    if not journal_stream:
        return False
    return not os.getenv('TERM')
