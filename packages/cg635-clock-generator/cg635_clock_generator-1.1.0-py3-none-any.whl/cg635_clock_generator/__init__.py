import sys

from ._cg635_clock_generator import CG635ClockGenerator
from ._constants import (
    CG635CMOSStandard,
    CG635Communication,
    CG635QStandard,
    CG635Timebase,
)
from ._exceptions import (
    CG635CommandError,
    CG635CommunicationError,
    CG635OperationTimeoutError,
)

__all__ = [
    "CG635ClockGenerator",
    "CG635Communication",
    "CG635CMOSStandard",
    "CG635QStandard",
    "CG635Timebase",
    "CG635CommunicationError",
    "CG635OperationTimeoutError",
    "CG635CommandError",
]

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "cg635-clock-generator"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError
