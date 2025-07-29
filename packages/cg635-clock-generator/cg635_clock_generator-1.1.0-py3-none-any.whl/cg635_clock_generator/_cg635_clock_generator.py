"""
Module for the control of the SRS CG635 clock generator.
"""

import logging
from functools import wraps
from time import sleep, time
from typing import Optional

import pyvisa
import pyvisa.constants

from cg635_clock_generator._constants import (
    CG635CMOSStandard,
    CG635Communication,
    CG635QStandard,
    CG635Timebase,
)
from cg635_clock_generator._exceptions import (
    CG635CommandError,
    CG635CommunicationError,
    CG635OperationTimeoutError,
)

__author__ = "Leandro Lanzieri"
__copyright__ = "Deutsches Elektronen-Synchrotron, DESY"
__license__ = "LGPL-3.0"

_LOGGER = logging.getLogger(__name__)


def _verify_operation(method):
    """
    A decorator to verify that an operation has completed successfully.
    It sets the event status register to generate a service request when the operation
    is completed, and waits for the request to be fired.
    """

    @wraps(method)
    def _verify_operation_complete(instance: "CG635ClockGenerator", *args, **kwargs):
        # clear the ESR, CESR, LCKR and INSR registers and LERR error buffer
        instance._resource.write("*CLS")

        # set a bit on the event register when any of the following occurs:
        # - the completion of an operation
        # - query error
        # - device error
        # - execution error
        # - command error
        instance._resource.write("*ESE 61")

        # generate a service request when any unmasked bit on the event register is set
        instance._resource.write("*SRE 32")

        # now execute the operation
        method(instance, *args, **kwargs)

        # wait for the operation to complete,.
        # this sets the OPC bit on the event register when the operation is completed.
        instance._resource.write("*OPC")

        start = time()
        while time() - start < instance._operation_complete_timeout:
            sleep(instance._operation_complete_polling_interval)
            serial_poll_status = int(instance._resource.query("*STB?"))
            if serial_poll_status & 1 << 5:
                # instrument requests service
                break
        else:
            raise CG635OperationTimeoutError("Operation did not complete in time")

        event_status = int(instance._resource.query("*ESR?"))
        if event_status > 1:
            raise CG635CommunicationError(
                f"Operation failed with status: {event_status}"
            )

        # clear the event registers
        instance._resource.write("*ESE 0")
        instance._resource.write("*SRE 0")

    return _verify_operation_complete


class CG635ClockGenerator:
    """
    Implements the control of the SRS CG635 clock generator.

    Args:
        communication_type (CG635Communication): The communication method to use.
        serial_device (Optional[str]): The serial device to use for communication, in
            case RS-232 or USB (via an adapter) is used. Cannot be used together with
            gpib_address nor resource_path. Default is None.
        gpib_address (Optional[int]): The GPIB address to use for communication, in case
            GPIB is used. Cannot be used together with serial_device nor resource_path.
            Default is None.
        gpib_card (Optional[int]): The number of the GPIB card to use for communication.
            Default is None.
        resource_path (Optional[str]): The resource path to use for communication.
            Cannot be used together with serial_device nor gpib_device. Default is None.
        resource_manager (pyvisa.Optional[ResourceManager]): The resource manager to use
            for communication. If None, a new resource manager will be created. Default
            is None.
        communication_timeout (int): The communication timeout in milliseconds. Default
            is 1000.
        operation_complete_timeout (int): Maximum time to wait for an operation to
            complete (in seconds). Default is 5.
        operation_complete_polling_interval (int): Interval between checks for operation
            completion (in seconds). Default is 0.1.
    """

    RS232_BAUDRATE = 9600
    """Baud rate for the RS232 communication."""

    RS323_BITS = 8
    """Number of bits for the RS232 communication."""

    RS232_STOP_BITS = pyvisa.constants.StopBits.one
    """Number of stop bits for the RS232 communication."""

    RS232_PARITY = pyvisa.constants.Parity.none
    """Parity for the RS232 communication."""

    RS232_FLOW_CONTROL = pyvisa.constants.VI_ASRL_FLOW_RTS_CTS
    """Flow control for the RS232 communication."""

    LINE_TERMINATION = "\n"
    """Line termination."""

    GPIB_DEFAULT_ADDRESS = 23
    """GPIB default address."""

    GPIP_DEFAULT_CARD = 0
    """GPIB default card."""

    def __init__(
        self,
        communication_type: CG635Communication,
        serial_device: Optional[str] = None,
        gpib_address: Optional[int] = None,
        gpib_card: Optional[int] = None,
        resource_path: Optional[str] = None,
        resource_manager: Optional[pyvisa.ResourceManager] = None,
        communication_timeout: int = 1000,
        operation_complete_timeout: int = 5,
        operation_complete_polling_interval: float = 0.1,
    ):
        self._communication_timeout = communication_timeout
        self._communication_type = communication_type
        self._operation_complete_timeout = operation_complete_timeout
        self._operation_complete_polling_interval = operation_complete_polling_interval
        self._resource_manager = resource_manager or pyvisa.ResourceManager("@py")

        self._serial_device: Optional[str] = None
        self._gpib_address: Optional[int] = None
        self._gpib_card: Optional[int] = None

        if self._communication_type == CG635Communication.RS232:
            assert serial_device is not None
            self._serial_device = serial_device
            self._resource_path = f"ASRL{serial_device}::INSTR"

        if self._communication_type == CG635Communication.GPIB:
            self._gpib_address = gpib_address or self.GPIB_DEFAULT_ADDRESS
            self._gpib_card = gpib_card or self.GPIP_DEFAULT_CARD
            self._resource_path = f"GPIB{self._gpib_card}::{self._gpib_address}::INSTR"

        if resource_path is not None:
            self._resource_path = resource_path

        self._resource: pyvisa.resources.MessageBasedResource = (
            self._resource_manager.open_resource(self._resource_path)
        )

        self._resource.timeout = self._communication_timeout
        self._resource.read_termination = self.LINE_TERMINATION
        self._resource.write_termination = self.LINE_TERMINATION

        if self._communication_type == CG635Communication.RS232:
            self._resource.baud_rate = self.RS232_BAUDRATE
            self._resource.data_bits = self.RS323_BITS
            self._resource.stop_bits = self.RS232_STOP_BITS
            self._resource.parity = self.RS232_PARITY
            self._resource.flow_control = self.RS232_FLOW_CONTROL

    def get_identification(self) -> str:
        """
        Gets the identification of the device.
        """
        return self._resource.query("*IDN?")

    def reset(self):
        """
        Resets the device to factory settings. This is equivalent to pressing the keys
        'SHIFT', 'INIT', 'Hz' on the front panel. The remote interface, GPIB address and
        the power-on status clear are not affected by this command.
        """
        self._resource.write("*RST")

    @_verify_operation
    def set_cmos_standard(self, standard: CG635CMOSStandard):
        """
        Sets the CMOS standard.

        Args:
            standard: The CMOS standard to set.
        """
        if not isinstance(standard, CG635CMOSStandard):
            _LOGGER.debug(f"The type of the parameter is {type(standard)}")
            raise CG635CommandError(f"Invalid CMOS standard: {standard}")

        self._resource.write(f"STDC {standard.value}")

    def get_cmos_standard(self) -> Optional[CG635CMOSStandard]:
        """
        Gets the CMOS standard. If the current CMOS levels are not standard, returns
        None.

        Raises:
            CG635CommunicationError: If the CMOS standard is invalid.
        """
        response: str = self._resource.query("STDC?").strip()
        if response == "-1":
            return None

        try:
            level = CG635CMOSStandard(int(response))
        except ValueError:
            raise CG635CommunicationError(f"Invalid CMOS standard: {response}")

        return level

    @_verify_operation
    def set_cmos_low_level(self, level: float):
        """
        Sets the low level of the CMOS output. To set to standard levels, use the
        set_cmos_standard method.

        Args:
            level: The low level of the CMOS output in volts. The range is -1.0 to
            1.0 V.

        Raises:
            CG635CommandError: If the level is invalid.
        """
        if not -1.0 <= level <= 1.0:
            raise CG635CommandError(f"Invalid CMOS low level: {level}")

        self._resource.write(f"CMOS 0,{level:.2f}")

    def get_cmos_low_level(self) -> float:
        """
        Gets the low level of the CMOS output in volts.
        """
        return float(self._resource.query("CMOS?0"))

    @_verify_operation
    def set_cmos_high_level(self, level: float):
        """
        Sets the high level of the CMOS output. To set to standard levels, use the
        set_cmos_standard method.

        Args:
            level: The high level of the CMOS output in volts. The range is -0.5 to
            6.0 V.

        Raises:
            CG635CommandError: If the level is invalid.
        """
        if not -0.5 <= level <= 6.0:
            raise CG635CommandError(f"Invalid CMOS high level: {level}")

        self._resource.write(f"CMOS 1,{level:.2f}")

    def get_cmos_high_level(self) -> float:
        """
        Gets the high level of the CMOS output in volts.
        """
        return float(self._resource.query("CMOS?1"))

    @_verify_operation
    def set_frequency(self, frequency: float):
        """
        Sets the frequency of the output signal.

        Args:
            frequency: The frequency of the output signal in Hz.
        """
        self._resource.write(f"FREQ {frequency}")

    def get_frequency(self) -> float:
        """
        Gets the frequency of the output signal in Hz.
        """
        return float(self._resource.query("FREQ?"))

    @_verify_operation
    def set_output(self, enabled: bool):
        """
        Enables or disables the output signal.

        Args:
            enabled: Whether to enable the output signals.
        """
        self._resource.write(f"RUNS {1 if enabled else 0}")

    def get_output(self) -> bool:
        """
        Gets whether the output signal is enabled.
        """
        return bool(int(self._resource.query("RUNS?")))

    @_verify_operation
    def set_phase(self, phase: float):
        """
        Sets the phase of the output signal.

        Args:
            phase: The phase of the output signal in degrees.

        Raises:
            CG635TimeoutError: If the operation does not complete in time.
        """
        self._resource.write(f"PHAS {phase}")

    def get_phase(self) -> float:
        """
        Gets the phase of the output signal in degrees.
        """
        return float(self._resource.query("PHAS?"))

    @_verify_operation
    def set_relative_phase(self):
        """
        Sets the current phase to be zero degrees. This doesn't change the phase of the
        output signal.
        """
        self._resource.write("RPHS")

    @_verify_operation
    def set_q_low_voltage(self, voltage: float):
        """
        Sets the low voltage of the Q output.

        Args:
            voltage: The low voltage of the Q output in volts. The range is -3.00 to
            4.80 V.
        """
        if not -3.00 <= voltage <= 4.80:
            raise CG635CommandError(f"Invalid Q low voltage: {voltage}")

        self._resource.write(f"QOUT 0,{voltage:.2f}")

    def get_q_low_voltage(self) -> float:
        """
        Gets the low voltage of the Q output in volts.
        """
        return float(self._resource.query("QOUT?0"))

    @_verify_operation
    def set_q_high_voltage(self, voltage: float):
        """
        Sets the high voltage of the Q output.

        Args:
            voltage: The high voltage of the Q output in volts. The range is -2.00 to
            5.00 V.
        """
        if not -2.00 <= voltage <= 5.00:
            raise CG635CommandError(f"Invalid Q high voltage: {voltage}")

        self._resource.write(f"QOUT 1,{voltage:.2f}")

    def get_q_high_voltage(self) -> float:
        """
        Gets the high voltage of the Q output in volts.
        """
        return float(self._resource.query("QOUT?1"))

    @_verify_operation
    def set_q_standard(self, standard: CG635QStandard):
        """
        Sets the Q standard.

        Args:
            standard: The Q standard to set.
        """
        if not isinstance(standard, CG635QStandard):
            raise CG635CommandError(f"Invalid Q standard: {standard}")

        self._resource.write(f"STDQ {standard.value}")

    def get_q_standard(self) -> Optional[CG635QStandard]:
        """
        Gets the Q standard. If the current Q levels are not standard, returns None.

        Raises:
            CG635CommunicationError: If the Q standard is invalid.
        """
        response = int(self._resource.query("STDQ?").strip())
        if response == -1:
            return None

        try:
            level = CG635QStandard(response)
        except ValueError:
            raise CG635CommunicationError(f"Invalid Q standard: {response}")

        return level

    def get_timebase(self) -> CG635Timebase:
        """
        Gets the timebase of the device.

        Raises:
            CG635CommunicationError: If the timebase is invalid.
        """
        response = int(self._resource.query("TIMB?").strip())

        try:
            timebase = CG635Timebase(response)
        except ValueError:
            raise CG635CommunicationError(f"Invalid timebase: {response}")

        return timebase

    def close(self):
        """
        Closes the connection to the device.
        """
        self._resource.close()

    def __del__(self):
        self.close()
