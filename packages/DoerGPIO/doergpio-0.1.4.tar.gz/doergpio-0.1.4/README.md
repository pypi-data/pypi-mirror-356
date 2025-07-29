# DoerGPIO

An Arduino-based GPIO interface for Python, providing a simple way to interact with GPIO pins through serial communication.

## Installation

```bash
pip install DoerGPIO
```

## Usage

```python
from DoerGPIO import GPIO

# Set up a pin
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.OUT)

# Control the pin
GPIO.output(18, GPIO.HIGH)
```

## Features

- Arduino-based GPIO control
- Simple and intuitive API
- Support for both input and output modes
- Pull-up/pull-down resistor configuration
- Compatible with Python 3.9+

## Requirements

- Python 3.9 or higher
- pyserial package
- Arduino board with compatible firmware

## License

[Add your license information here] 