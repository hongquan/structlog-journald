from .detect import is_journald_connected
from .processors import JournaldProcessor


__version__ = '0.6.0'


__all__ = [
    'is_journald_connected',
    'JournaldProcessor',
    '__version__',
]
