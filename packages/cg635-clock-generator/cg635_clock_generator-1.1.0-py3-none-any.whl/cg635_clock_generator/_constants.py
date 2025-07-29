"""
Constants for the SRS CG635 clock generator.
"""

from enum import Enum, IntEnum

__author__ = "Leandro Lanzieri"
__copyright__ = "Deutsches Elektronen-Synchrotron, DESY"
__license__ = "LGPL-3.0"


class CG635Communication(Enum):
    """
    Enum for the communication buses of the SRS CG635 clock generator.
    """

    RS232 = "RS232"
    """RS-232 communication."""

    GPIB = "GPIB"
    """GPIB communication."""

    OTHER = "OTHER"
    """Other communication bus."""


class CG635CMOSStandard(IntEnum):
    """
    Enum for the CMOS levels of the SRS CG635 clock generator.
    """

    V1_2 = 0
    """1.2V CMOS level."""

    V1_8 = 1
    """1.8V CMOS level."""

    V2_5 = 2
    """2.5V CMOS level."""

    V3_3 = 3
    """3.3V CMOS level."""

    V5_0 = 4
    """5V CMOS level."""


class CG635QStandard(Enum):
    """
    Enum for the Q/Q# standards of the SRS CG635 clock generator.
    """

    ECL = 0
    """ECL levels (-1.00/-1.80 V)."""

    PLUS_DBM7 = 1
    """+7dBm (+0.50/-0.50 V)."""

    LVDS = 2
    """LVDS levels (1.43/1.07 V)."""

    PECL_V3_3 = 3
    """PECL 3.3V levels (2.30/1.50 V)."""

    PECL_V5_0 = 4
    """PECL 5.0V levels (4.00/3.20 V)."""


class CG635Timebase(Enum):
    """
    Enum for the timebases of the SRS CG635 clock generator.
    """

    INTERNAL = 0
    """Internal timebase."""

    OCXO = 1
    """OCXO timebase."""

    RUBIDIUM = 2
    """Rubidium timebase."""

    EXTERNAL = 3
    """External timebase."""
