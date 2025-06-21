# Indicate if we can use cysystemd (CY == True) or systemd-python (CY == False).
# We prefer systemd-python to cysystemd, so we try to import systemd-python first.
CY = False
LEVEL_TO_PRIORITY: dict[str, int] = {}

try:
    from systemd import journal

    # Translate from structlog method names of log level to systemd journal priority.
    # The available method names can be seen in https://github.com/hynek/structlog/blob/main/src/structlog/typing.py
    LEVEL_TO_PRIORITY = {
        'debug': journal.LOG_DEBUG,
        'adebug': journal.LOG_DEBUG,
        'info': journal.LOG_INFO,
        'ainfo': journal.LOG_INFO,
        'warning': journal.LOG_WARNING,
        'awarning': journal.LOG_WARNING,
        'error': journal.LOG_ERR,
        'aerror': journal.LOG_ERR,
        'exception': journal.LOG_ERR,
        'aexception': journal.LOG_ERR,
        'fatal': journal.LOG_CRIT,
        'afatal': journal.LOG_CRIT,
        'critical': journal.LOG_CRIT,
        'acritical': journal.LOG_CRIT,
        # Other method names will be mapped to 'info' level.
    }
except ModuleNotFoundError:
    from cysystemd.journal import Priority

    CY = True
    LEVEL_TO_PRIORITY = {
        'debug': Priority.DEBUG,
        'adebug': Priority.DEBUG,
        'info': Priority.INFO,
        'ainfo': Priority.INFO,
        'warning': Priority.WARNING,
        'awarning': Priority.WARNING,
        'error': Priority.ERROR,
        'aerror': Priority.ERROR,
        'exception': Priority.ERROR,
        'aexception': Priority.ERROR,
        'fatal': Priority.CRITICAL,
        'afatal': Priority.CRITICAL,
        'critical': Priority.CRITICAL,
        'acritical': Priority.CRITICAL,
        # Other method names will be mapped to 'info' level.
    }
