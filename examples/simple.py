import getpass
import logging
import platform

import structlog

from structlog_journald import JournaldProcessor


structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.CallsiteParameterAdder(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt='%Y-%m-%d %H:%M:%S', utc=False),
        structlog.processors.EventRenamer('message'),
        JournaldProcessor(),
        # This processor should be added for development environment only.
        structlog.dev.ConsoleRenderer(),
    ],
    # In this example, we want to print log entries of all levels
    wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
    context_class=dict,
    logger_factory=structlog.WriteLoggerFactory(),
    cache_logger_on_first_use=True,
)

log = structlog.stdlib.get_logger()


user = getpass.getuser()


log.info('Current Linux user: %s', user, linux=platform.freedesktop_os_release())
log.warning('This is a warning.', platform=platform.platform())
try:
    int('abc')
except ValueError:
    log.exception('Failed to convert string to integer.')
