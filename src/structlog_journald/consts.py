from journald_send import Priority


# Translate from structlog method names of log level to systemd journal priority.
# The available method names can be seen in https://github.com/hynek/structlog/blob/main/src/structlog/typing.py
LEVEL_TO_PRIORITY: dict[str, Priority] = {
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
