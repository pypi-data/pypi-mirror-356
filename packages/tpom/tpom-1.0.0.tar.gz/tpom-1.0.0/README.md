# 🍅 tpom - Pomodoro Timer CLI

A simple and elegant Pomodoro timer for the command line, built with Python.

## Features

- ⏰ Clean countdown display
- 🔔 Gentle alarm sound notification
- 🚫 Easy cancellation with Ctrl+C
- 🎵 Custom sound file support
- 📦 Easy installation via pip
- 🔇 Silent operation if sound unavailable (no grating fallbacks)

## Installation

### From PyPI (when published)
```bash
pip install tpom
```

### From source
```bash
git clone https://github.com/yourusername/tpom.git
cd tpom
pip install -e .
```

## Usage

### Basic usage
```bash
tpom
# You'll be prompted to enter the duration in minutes
```

### Specify duration directly
```bash
tpom --minutes 25
```

### Use custom sound file
```bash
tpom --minutes 25 --sound-file /path/to/your/sound.mp3
```

### Get help
```bash
tpom --help
```

## Development

### Setup development environment
```bash
git clone https://github.com/yourusername/tpom.git
cd tpom
pip install -e ".[dev]"
```

### Run tests
```bash
pytest
```

### Format code
```bash
black src/
```

### Lint code
```bash
flake8 src/
mypy src/
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.