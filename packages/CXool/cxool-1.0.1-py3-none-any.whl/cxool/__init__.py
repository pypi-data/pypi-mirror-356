try:
    from ._version import __version__
except ImportError:
    __version__ = "unknown"

try:
    from ._version import __commit__
except ImportError:
    __commit__ = "unknown"
