
# Loggy

Loggy is a simple and colorful logging utility for console and file logging in Python.

## Features

- Colored console output for different log levels
- Optional file logging with customizable filename
- Supports common log levels: info, success, error, warning, debug, critical, exception
- Easy to use and integrate into your projects

## Installation

```bash
pip install logita
```

Then include Logita in your project.

## Usage

```python
from Logita import Logita

logger = Loggy(log_to_file=True, log_filename="app.log")
logger.info("This is an info message")
logger.success("This is a success message")
logger.error("This is an error message")
```

## License

This project is licensed under the MIT License.
