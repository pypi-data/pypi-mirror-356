"""
Mocker for the control of the SRS CG635 clock generator.
"""

import logging
from typing import Tuple

from pyvisa_mock.base.base_mocker import BaseMocker, scpi

from cg635_clock_generator import CG635CMOSStandard, CG635QStandard

__author__ = "Leandro Lanzieri"
__copyright__ = "Deutsches Elektronen-Synchrotron, DESY"
__license__ = "LGPL-3.0"

_LOGGER = logging.getLogger(__name__)


class CG635ClockGeneratorMocker(BaseMocker):
    """
    A mocker for a SRS CG635 clock generator.
    """

    LINE_TERMINATION = "\r\n"
    """The line termination character for the mocker."""

    def __init__(
        self,
        call_delay: float = 0.0,
    ):
        super().__init__(call_delay=call_delay)

        self._go_to_factory_settings()

        self.timeout_next_operation = False
        """Flag to simulate a timeout in the next operation."""

        self._esr = 0

    def _go_to_factory_settings(self) -> None:
        """
        Reset the mocker to factory settings. Taken from the user manual.
        """
        self._frequency = 10e6
        self._phase = 0.0
        self._q_high_level = 1.43
        self._q_low_level = 1.07
        self._cmos_high_level = 3.3
        self._cmos_low_level = 0.0
        self._running = True

    def _get_cmos_standard_levels(
        self, standard: CG635CMOSStandard
    ) -> Tuple[float, float]:
        """
        Get the CMOS standard levels for the given standard. The levels are returned as
        a tuple of high and low levels.

        Args:
            standard: The CMOS standard.
        """
        if standard == CG635CMOSStandard.V1_2:
            return 1.2, 0.0
        elif standard == CG635CMOSStandard.V1_8:
            return 1.8, 0.0
        elif standard == CG635CMOSStandard.V2_5:
            return 2.5, 0.0
        elif standard == CG635CMOSStandard.V3_3:
            return 3.3, 0.0
        elif standard == CG635CMOSStandard.V5_0:
            return 5.0, 0.0

    def _get_q_standard_levels(self, standard: CG635QStandard) -> Tuple[float, float]:
        """
        Get the Q/Q standard levels for the given standard. The levels are returned as a
        tuple of high and low levels.

        Args:
            standard: The Q/Q standard.
        """
        if standard == CG635QStandard.LVDS:
            return 1.43, 1.07
        elif standard == CG635QStandard.PLUS_DBM7:
            return 0.5, -0.5
        elif standard == CG635QStandard.PECL_V3_3:
            return 2.3, 1.5
        elif standard == CG635QStandard.PECL_V5_0:
            return 4.0, 3.2
        elif standard == CG635QStandard.ECL:
            return -1.0, -1.8

    @scpi("*CLS")
    def _clear_stb(self) -> None:
        self.stb = 0

    @scpi("*ESE <value>")
    def _set_event_status_enable(self, value: str) -> None:
        pass

    @scpi("*ESR?")
    def _get_event_status_register(self) -> str:
        return f"{self._esr}"

    @scpi("*SRE <value>")
    def _set_service_request_enable(self, value: str) -> None:
        pass

    @scpi("*OPC")
    def _operation_complete(self) -> None:
        if self.timeout_next_operation:
            # simulate an error
            self._esr = 1 << 3  # device dependent error
            self.stb = 0
            self.timeout_next_operation = False
        else:
            # simulate the operation complete bit
            self._esr = 0x01
            self.stb |= 1 << 5
            self.set_service_request_event()

    @scpi("*STB?")
    def _get_status_byte(self) -> str:
        return f"{self.stb}"

    @scpi("*RST")
    def _reset(self) -> None:
        self._go_to_factory_settings()

    @scpi("*IDN?")
    def _get_identification(self) -> str:
        return "Stanford Research Systems,CG635,s/n004025,ver0.01"

    @scpi("STDC <standard>")
    def _set_cmos_standard(self, standard: str) -> None:
        _standard = CG635CMOSStandard(int(standard))
        high, low = self._get_cmos_standard_levels(_standard)
        self._cmos_high_level = high
        self._cmos_low_level = low

    @scpi("STDC?")
    def _get_cmos_standard(self) -> str:
        if self._cmos_low_level != 0.0:
            response = "-1"
        elif self._cmos_high_level == 1.2:
            response = CG635CMOSStandard.V1_2.value
        elif self._cmos_high_level == 1.8:
            response = CG635CMOSStandard.V1_8.value
        elif self._cmos_high_level == 2.5:
            response = CG635CMOSStandard.V2_5.value
        elif self._cmos_high_level == 3.3:
            response = CG635CMOSStandard.V3_3.value
        elif self._cmos_high_level == 5.0:
            response = CG635CMOSStandard.V5_0.value
        else:
            response = "-1"

        return response

    @scpi("CMOS 0,<voltage>")
    def _set_cmos_low_level(self, voltage: str) -> None:
        _voltage = float(voltage)
        self._cmos_low_level = _voltage

    @scpi("CMOS?0")
    def _get_cmos_low_level(self) -> str:
        return f"{self._cmos_low_level}"

    @scpi("CMOS 1,<voltage>")
    def _set_cmos_high_level(self, voltage: str) -> None:
        _voltage = float(voltage)
        self._cmos_high_level = _voltage

    @scpi("CMOS?1")
    def _get_cmos_high_level(self) -> str:
        return f"{self._cmos_high_level}"

    @scpi("STDQ <standard>")
    def _set_q_standard(self, standard: str) -> None:
        _standard = CG635QStandard(int(standard))
        high, low = self._get_q_standard_levels(_standard)
        self._q_high_level = high
        self._q_low_level = low

    @scpi("STDQ?")
    def _get_q_standard(self) -> str:
        if self._q_low_level == -1.8 and self._q_high_level == -1.0:
            response = CG635QStandard.ECL.value
        elif self._q_low_level == -0.5 and self._q_high_level == 0.5:
            response = CG635QStandard.PLUS_DBM7.value
        elif self._q_low_level == 1.07 and self._q_high_level == 1.43:
            response = CG635QStandard.LVDS.value
        elif self._q_low_level == 1.5 and self._q_high_level == 2.3:
            response = CG635QStandard.PECL_V3_3.value
        elif self._q_low_level == 3.2 and self._q_high_level == 4.0:
            response = CG635QStandard.PECL_V5_0.value
        else:
            response = -1

        return f"{response}"

    @scpi("QOUT 0,<voltage>")
    def _set_q_low_voltage(self, voltage: str) -> None:
        _voltage = float(voltage)
        self._q_low_level = _voltage

    @scpi("QOUT?0")
    def _get_q_low_voltage(self) -> str:
        return f"{self._q_low_level}"

    @scpi("QOUT 1,<voltage>")
    def _set_q_high_voltage(self, voltage: str) -> None:
        _voltage = float(voltage)
        self._q_high_level = _voltage

    @scpi("QOUT?1")
    def _get_q_high_voltage(self) -> str:
        return f"{self._q_high_level}"

    @scpi("FREQ <frequency>")
    def _set_frequency(self, frequency: str) -> None:
        _frequency = float(frequency)
        self._frequency = _frequency

    @scpi("FREQ?")
    def _get_frequency(self) -> str:
        return f"{self._frequency}"

    @scpi("PHAS <phase>")
    def _set_phase(self, phase: str) -> None:
        _phase = float(phase)
        self._phase = _phase

    @scpi("PHAS?")
    def _get_phase(self) -> str:
        return f"{self._phase}"

    @scpi("RUNS <state>")
    def _set_output(self, state: str) -> None:
        _state = int(state)
        assert _state in [0, 1], f"Invalid state: {_state}"
        self._running = _state == 1

    @scpi("RUNS?")
    def _get_output(self) -> str:
        return f"{1 if self._running else 0}"

    @scpi("TIMB?")
    def _get_timebase(self) -> str:
        return "0"
