# Changelog

## [0.5.0] - 2025-08-11

### Fixed
- Call cysystemd's journal.send correctly.

### Added
- Collect more fields to send to journald: MODULE, TID, LOGGER.
- Write documentation for how to attach extra info to journald log entry and filter by it.

## [0.4.0] - 2025-07-13

### Fixed
- Use fullpath for CODE_FILE.

### Changed
- Render extra items in event_dict.
- Show example in documentation.

## [0.3.0] - 2025-07-03

### Fixed
- Send correct CODE_FILE, CODE_LINE, CODE_FUNC info to journald.

### Changed
- Be more flexible when library user pass non-string to `message`.

## [0.2.0] - 2026-06-22

### Added
- Include traceback for log.exception.

## [0.1.0] - 2026-06-21

_Initial release._

[0.5.0]: https://github.com/hongquan/structlog-journald/releases/tag/v0.5.0
[0.4.0]: https://github.com/hongquan/structlog-journald/releases/tag/v0.4.0
[0.3.0]: https://github.com/hongquan/structlog-journald/releases/tag/v0.3.0
[0.2.0]: https://github.com/hongquan/structlog-journald/releases/tag/v0.2.0
[0.1.0]: https://github.com/hongquan/structlog-journald/releases/tag/v0.1.0
