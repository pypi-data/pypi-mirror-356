# volt-logger

**volt-logger** is a lightweight, file-capable logging utility for Python CLI tools and small applications.  
It offers basic log levels, optional timestamping, and file logging without the complexity of the standard `logging` module.

## Features

- Print logs to console and/or file
- Supports basic log levels: `info`, `warn`, `error`, `debug`, `progress`, etc.
- Toggle file logging with `.set_log_file()`
- Timestamp support
- Built-in `Logger` instance for quick use

## Install

```bash
pip install git+https://github.com/stuarttempleton/volt-logger.git
````

## Usage

```python
from voltlogger import Logger

Logger.log("This is an info message.")
Logger.warn("Watch out!")
Logger.set_log_file("run.log")
Logger.report("This will log to file, if a log file is specified.")
```

## License

[MIT](LICENSE)
