import concurrent.futures
import logging
import random
import time
from concurrent.futures import ThreadPoolExecutor
from itertools import cycle

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


def pretend_to_compute_for_decision() -> None:
    time.sleep(random.randint(2, 8) / 10)


def pretend_to_run_pump() -> None:
    time.sleep(random.randint(5, 20) / 10)


def control_farm(farm_name: str) -> None:
    # To avoid repeatly passing `f_farm=farm_name` to each calls of info, debug,
    # we can just call bind() once.
    log = logger.bind(f_farm=farm_name)
    sensors = get_sensor_values()
    log.debug('Sensor values: %s', sensors)
    pretend_to_compute_for_decision()
    log.warning('Farm %s is too hot', farm_name)
    log.info('Turn pump on...')
    pretend_to_run_pump()
    log.info('Turn pump off.')


def control_farm_ctxv(farm_name: str) -> None:
    # To avoid repeatly passing `f_farm=farm_name` to each calls of info, debug,
    # we can open a context.
    with bound_contextvars(f_farm=farm_name):
        sensors = get_sensor_values()
        logger.debug('Sensor values: %s', sensors)
        pretend_to_compute_for_decision()
        logger.warning('Farm %s is too hot', farm_name)
        logger.info('Turn pump on...')
        pretend_to_run_pump()
        logger.info('Turn pump off.')


farms = ('tomato', 'rose', 'mushroom')
jobs = []
# Control farms in parallel to let logs mixed.
with ThreadPoolExecutor(max_workers=2) as executor:
    # The `flag` is simply for choosing one of the two control_xxx functions above.
    for flag, farm in zip(cycle((False, True)), farms):
        ft = executor.submit(control_farm_ctxv if flag else control_farm, farm)
        jobs.append(ft)

concurrent.futures.wait(jobs)
