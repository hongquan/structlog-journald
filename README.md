# structlog-journald

![made-in-vietnam](https://madewithlove.vercel.app/vn?heart=true&colorA=%23ffcd00&colorB=%23da251d)

Structlog processor to send logs to journald.

Installation
------------

To install `structlog-journald`, run:

```sh
pip install structlog-journald
```

You also need to install one of the journald binding implementations:

- CPython-based [`systemd-python`](https://pypi.org/project/systemd-python/).
- Cython-based [`cysystemd`](https://pypi.org/project/cysystemd/).

Usage
-----

Add the `structlog_journald.JournaldProcessor` to your list of structlog processors.

Before it, you should add the `CallsiteParameterAdder`.

```py
import logging

import structlog
from structlog_journald import JournaldProcessor


structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.CallsiteParameterAdder(),
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt='%Y-%m-%d %H:%M:%S', utc=False),
        structlog.processors.EventRenamer('message'),
        JournaldProcessor(),
        structlog.dev.ConsoleRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=False,
)

log = structlog.stdlib.get_logger()

log.info('Hello, world!')
```
