# structlog-journald

![made-in-vietnam](https://madewithlove.vercel.app/vn?heart=true&colorA=%23ffcd00&colorB=%23da251d)
[![structlog-journald](https://badge.fury.io/py/structlog-journald.svg)](https://pypi.org/project/structlog-journald/)
[![ReadTheDocs](https://readthedocs.org/projects/structlog-journald/badge/?version=latest)](https://structlog-journald.readthedocs.io?badge=latest)
[![Common Changelog](https://common-changelog.org/badge.svg)](https://common-changelog.org)

[Structlog] processor to send logs to [journald].

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

Add the `structlog_journald.JournaldProcessor` to your list of `structlog` processors.
It will do nothing if the journald socket is not available,
in other words, the app was not started by systemd.

To let the log have more useful information, you should also add these processors before `JournaldProcessor`:

- `CallsiteParameterAdder`
- `format_exc_info`

Example:

```py
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
```

![Journalctl](https://raw.githubusercontent.com/hongquan/structlog-journald/refs/heads/main/misc/screenshot.png)

[structlog]: https://www.structlog.org
[journald]: https://www.freedesktop.org/software/systemd/man/latest/journalctl.html
