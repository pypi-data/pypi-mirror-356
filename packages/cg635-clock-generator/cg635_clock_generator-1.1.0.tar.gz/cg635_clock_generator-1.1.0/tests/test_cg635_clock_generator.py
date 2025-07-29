import pytest
from cg635_clock_generator_mocker import CG635ClockGeneratorMocker

from cg635_clock_generator import (
    CG635ClockGenerator,
    CG635CMOSStandard,
    CG635CommandError,
    CG635OperationTimeoutError,
    CG635QStandard,
    CG635Timebase,
)

CMOS_NON_STD_HIGH_LEVEL = 1.6
CMOS_NON_STD_LOW_LEVEL = 0.4


def test_identification(cg635_clock_generator: CG635ClockGenerator):
    assert (
        "Stanford Research Systems,CG635" in cg635_clock_generator.get_identification()
    )


def test_set_cmos_levels(cg635_clock_generator: CG635ClockGenerator):

    cg635_clock_generator.set_cmos_high_level(CMOS_NON_STD_HIGH_LEVEL)
    assert cg635_clock_generator.get_cmos_high_level() == CMOS_NON_STD_HIGH_LEVEL

    cg635_clock_generator.set_cmos_low_level(CMOS_NON_STD_LOW_LEVEL)
    assert cg635_clock_generator.get_cmos_low_level() == CMOS_NON_STD_LOW_LEVEL

    with pytest.raises(CG635CommandError):
        cg635_clock_generator.set_cmos_high_level(-1.0)

    with pytest.raises(CG635CommandError):
        cg635_clock_generator.set_cmos_low_level(2.0)


def test_cmos_standards(cg635_clock_generator: CG635ClockGenerator):
    assert cg635_clock_generator.get_cmos_standard() is None

    cg635_clock_generator.set_cmos_standard(CG635CMOSStandard.V1_2)
    assert cg635_clock_generator.get_cmos_standard() == CG635CMOSStandard.V1_2
    assert cg635_clock_generator.get_cmos_high_level() == 1.2
    assert cg635_clock_generator.get_cmos_low_level() == 0.0

    cg635_clock_generator.set_cmos_standard(CG635CMOSStandard.V1_8)
    assert cg635_clock_generator.get_cmos_standard() == CG635CMOSStandard.V1_8
    assert cg635_clock_generator.get_cmos_high_level() == 1.8
    assert cg635_clock_generator.get_cmos_low_level() == 0.0

    cg635_clock_generator.set_cmos_standard(CG635CMOSStandard.V2_5)
    assert cg635_clock_generator.get_cmos_standard() == CG635CMOSStandard.V2_5
    assert cg635_clock_generator.get_cmos_high_level() == 2.5
    assert cg635_clock_generator.get_cmos_low_level() == 0.0

    cg635_clock_generator.set_cmos_standard(CG635CMOSStandard.V3_3)
    assert cg635_clock_generator.get_cmos_standard() == CG635CMOSStandard.V3_3
    assert cg635_clock_generator.get_cmos_high_level() == 3.3
    assert cg635_clock_generator.get_cmos_low_level() == 0.0

    cg635_clock_generator.set_cmos_standard(CG635CMOSStandard.V5_0)
    assert cg635_clock_generator.get_cmos_standard() == CG635CMOSStandard.V5_0
    assert cg635_clock_generator.get_cmos_high_level() == 5.0
    assert cg635_clock_generator.get_cmos_low_level() == 0.0

    with pytest.raises(CG635CommandError):
        cg635_clock_generator.set_cmos_standard(5)


def test_q_voltages(cg635_clock_generator: CG635ClockGenerator):
    cg635_clock_generator.set_q_high_voltage(5.00)

    cg635_clock_generator.set_q_high_voltage(1.53)
    assert cg635_clock_generator.get_q_high_voltage() == 1.53

    cg635_clock_generator.set_q_high_voltage(-2.00)
    assert cg635_clock_generator.get_q_high_voltage() == -2.00

    cg635_clock_generator.set_q_low_voltage(-3.0)
    assert cg635_clock_generator.get_q_low_voltage() == -3.0

    cg635_clock_generator.set_q_low_voltage(4.47)
    assert cg635_clock_generator.get_q_low_voltage() == 4.47

    cg635_clock_generator.set_q_low_voltage(4.80)
    assert cg635_clock_generator.get_q_low_voltage() == 4.80

    with pytest.raises(CG635CommandError):
        cg635_clock_generator.set_q_high_voltage(-2.01)

    with pytest.raises(CG635CommandError):
        cg635_clock_generator.set_q_low_voltage(5.02)


def test_q_standards(cg635_clock_generator: CG635ClockGenerator):
    assert cg635_clock_generator.get_q_standard() is None

    cg635_clock_generator.set_q_standard(CG635QStandard.ECL)
    assert cg635_clock_generator.get_q_standard() == CG635QStandard.ECL
    assert cg635_clock_generator.get_q_high_voltage() == -1.0
    assert cg635_clock_generator.get_q_low_voltage() == -1.8

    cg635_clock_generator.set_q_standard(CG635QStandard.PLUS_DBM7)
    assert cg635_clock_generator.get_q_standard() == CG635QStandard.PLUS_DBM7
    assert cg635_clock_generator.get_q_high_voltage() == 0.5
    assert cg635_clock_generator.get_q_low_voltage() == -0.5

    cg635_clock_generator.set_q_standard(CG635QStandard.LVDS)
    assert cg635_clock_generator.get_q_standard() == CG635QStandard.LVDS
    assert cg635_clock_generator.get_q_high_voltage() == 1.43
    assert cg635_clock_generator.get_q_low_voltage() == 1.07

    cg635_clock_generator.set_q_standard(CG635QStandard.PECL_V3_3)
    assert cg635_clock_generator.get_q_standard() == CG635QStandard.PECL_V3_3
    assert cg635_clock_generator.get_q_high_voltage() == 2.3
    assert cg635_clock_generator.get_q_low_voltage() == 1.5

    cg635_clock_generator.set_q_standard(CG635QStandard.PECL_V5_0)
    assert cg635_clock_generator.get_q_standard() == CG635QStandard.PECL_V5_0
    assert cg635_clock_generator.get_q_high_voltage() == 4.0
    assert cg635_clock_generator.get_q_low_voltage() == 3.2

    with pytest.raises(CG635CommandError):
        cg635_clock_generator.set_q_standard(5)


def test_phase(cg635_clock_generator: CG635ClockGenerator):
    cg635_clock_generator.set_phase(0.0)
    assert cg635_clock_generator.get_phase() == 0.0

    cg635_clock_generator.set_phase(180.0)
    assert cg635_clock_generator.get_phase() == 180.0

    cg635_clock_generator.set_phase(-180.0)
    assert cg635_clock_generator.get_phase() == -180.0


def test_frequency(cg635_clock_generator: CG635ClockGenerator):
    cg635_clock_generator.set_frequency(10e6)
    assert cg635_clock_generator.get_frequency() == 10e6

    cg635_clock_generator.set_frequency(1e9)
    assert cg635_clock_generator.get_frequency() == 1e9

    cg635_clock_generator.set_frequency(1e-3)
    assert cg635_clock_generator.get_frequency() == 1e-3


@pytest.mark.skipif(
    "config.getvalue('hil')", reason="Not valid for hardware-in-the-loop"
)
def test_operation_timeout(
    cg635_clock_generator: CG635ClockGenerator,
    mock_cg635_clock_generator: CG635ClockGeneratorMocker,
):
    mock_cg635_clock_generator.timeout_next_operation = True
    cg635_clock_generator._operation_complete_timeout = 0.1

    with pytest.raises(CG635OperationTimeoutError):
        cg635_clock_generator.set_frequency(10e6)


def test_output(cg635_clock_generator: CG635ClockGenerator):
    cg635_clock_generator.set_output(False)
    assert cg635_clock_generator.get_output() is False

    cg635_clock_generator.set_output(True)
    assert cg635_clock_generator.get_output() is True


def test_timebase(cg635_clock_generator: CG635ClockGenerator):
    assert cg635_clock_generator.get_timebase() == CG635Timebase.INTERNAL


def test_reset(cg635_clock_generator: CG635ClockGenerator):
    cg635_clock_generator.reset()
    assert cg635_clock_generator.get_cmos_standard() is CG635CMOSStandard.V3_3
    assert cg635_clock_generator.get_cmos_high_level() == 3.3
    assert cg635_clock_generator.get_cmos_low_level() == 0.0

    assert cg635_clock_generator.get_frequency() == 10e6
    assert cg635_clock_generator.get_phase() == 0.0

    assert cg635_clock_generator.get_q_standard() is CG635QStandard.LVDS
    assert cg635_clock_generator.get_q_high_voltage() == 1.43
    assert cg635_clock_generator.get_q_low_voltage() == 1.07

    assert cg635_clock_generator.get_output() is True
