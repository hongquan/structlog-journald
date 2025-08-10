import logging
import random

import structlog
from structlog.contextvars import bound_contextvars, clear_contextvars

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
        JournaldProcessor(extra_field_prefix='f_'),
        # This processor should be added for development environment only.
        structlog.dev.ConsoleRenderer(),
    ],
    # In this example, we want to print log entries of all levels
    wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
    context_class=dict,
    logger_factory=structlog.WriteLoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.stdlib.get_logger()

clear_contextvars()


def get_sensor_values() -> dict[str, int | float]:
    return {'temperature': random.randint(25, 30), 'humidity': random.randint(80, 99)}


def control_farm(farm_name: str) -> None:
    # To avoid repeatly passing `f_farm=farm_name` to each calls of info, debug,
    # we can just call bind() once.
    log = logger.bind(f_farm=farm_name)
    sensors = get_sensor_values()
    log.debug('Sensor values: %s', sensors)
    log.warning('Farm %s is too hot', farm_name)
    log.info('Turn pump on...')
    log.info('Turn pump off.')


def control_farm_ctxv(farm_name: str) -> None:
    # To avoid repeatly passing `f_farm=farm_name` to each calls of info, debug,
    # we can open a context.
    with bound_contextvars(f_farm=farm_name):
        sensors = get_sensor_values()
        logger.debug('Sensor values: %s', sensors)
        logger.warning('Farm %s is too hot', farm_name)
        logger.info('Turn pump on...')
        logger.info('Turn pump off.')


control_farm('tomato')
control_farm_ctxv('rose')
