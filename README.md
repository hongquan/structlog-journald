# structlog-journald

![made-in-vietnam](https://madewithlove.vercel.app/vn?heart=true&colorA=%23ffcd00&colorB=%23da251d)
[![structlog-journald](https://badge.fury.io/py/structlog-journald.svg)](https://pypi.org/project/structlog-journald/)
[![ReadTheDocs](https://readthedocs.org/projects/structlog-journald/badge/?version=latest)](https://structlog-journald.readthedocs.io?badge=latest)

Structlog processor to send logs to journald.

Documentation: [https://structlog-journald.readthedocs.io](https://structlog-journald.readthedocs.io)

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

To let the log has more useful information, you should also add these processors before `JournaldProcessor`:

- `CallsiteParameterAdder`
- `format_exc_info`

Example:

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
        structlog.processors.format_exc_info,
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

![Journalctl](https://raw.githubusercontent.com/hongquan/structlog-journald/refs/heads/main/misc/screenshot.png)
