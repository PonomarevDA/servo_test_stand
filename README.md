# servo test stand

based on pydronecan

## Hardware requirements

- SLCAN sniffer
- CAN-PWM nodef

## Software requirements

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