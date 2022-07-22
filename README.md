# servo test stand

## Purpose

This software allows to perform some tests to verify that the hardware and software corresponds to the expected quality. It should:

1. Send setpoint ([RawCommand](https://dronecan.github.io/Specification/7._List_of_standard_data_types/#rawcommand) message) with values from 0 to 1.0 in a given period of time (let's say 1 second) within given amount of time (let's say 1 day).

2. Subscribe on following data types:
- [CircuitStatus](https://dronecan.github.io/Specification/7._List_of_standard_data_types/#circuitstatus)
- [NodeStatus](https://dronecan.github.io/Specification/7._List_of_standard_data_types/#nodestatus)
- [LogMessage](https://dronecan.github.io/Specification/7._List_of_standard_data_types/#logmessage)

3. Store few things in a file:
- all received LogMessage,
- timestamps of events when CircuitStatus or NodeStatus is not appear,
- timestamps of events when CircuitStatus has out of bound voltage,
- timestamps of events when NodeStatus has ERROR health,
- CircuitStatus and NodeStatus once per hour.

4. Allows to test simultaniously several devices (let's say 4 can-pwm nodes).

## Hardware requirements

- SLCAN sniffer
- few CAN-PWM nodes

## Software dependencies

- ubuntu at least 18:04
- python3
- pydronecan library
- can-utils

## Installation

```bash
./scripts/install.sh
```

## Usage

```bash
./scripts/create_slcan_from_serial.sh
python3 main.py
```
