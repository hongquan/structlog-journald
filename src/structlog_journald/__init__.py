from .detect import is_journald_connected
from .processors import JournaldProcessor


__version__ = '1.0.0'


__all__ = [
    'is_journald_connected',
    'JournaldProcessor',
    '__version__',
]
