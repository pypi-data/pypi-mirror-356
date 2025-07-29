# SRS-CG635 Synthesized Clock Generator Interface

Interface with a Stanford Research Systems CG635 Synthesized Clock Generator.

## Installation

```bash
$ pip install cg635-clock-generator
```

## Supported Features

- Frequency control
- Phase control
- CMOS output levels and standards control
- Q/*Q outputs levels and standards control
- R232 communication

## Usage

```python
from cg635_clock_generator import CG635ClockGenerator, CG635Communication

clock_generator = CG635ClockGenerator(
        communication_type=CG635Communication.RS232,
        serial_device='/dev/ttyUSB0',
)

print(clock_generator.get_identification())

FREQ = 10e6
PHASE = 90.0

clock_generator.set_frequency(FREQ)

frequency = clock_generator.get_frequency()
print(f"Frequency is {frequency} Hz")

clock_generator.set_phase(PHASE)

phase = clock_generator.get_phase()
print(f"Phase is {phase} degrees")

```

## Running tests on hardware

During normal development and for the CI the unit test suite is executed on a mock
device using pyvisa-mock. It is also possible to run tests on real hardware connected
to your system. Just call:

```bash
$ uv run poe test_hil
```

By default it will try to connect to `/dev/ttyUSB0`, but you can specify a different
device using the `--hil_serial_device` option:

```bash
$ uv run poe test_hil --hil_serial_device /dev/ttyUSB1
```

## Status

Currently only the RS232 communication has been tested on the device.

## Documentation

For more details of the module API, check the
[online documentation](http://cg635-clock-generator-leandro-lanzieri-c9d5fa14e6af42e02aa27f45.pages.desy.de/).

## Feeling like contributing?

Great! Check the [Contributing Guide](CONTRIBUTING.md) to get started.
