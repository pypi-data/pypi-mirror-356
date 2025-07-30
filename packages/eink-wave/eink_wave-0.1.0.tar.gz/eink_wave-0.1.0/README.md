# E-Paper Display Library

A modernized version of the [Waveshare e-Paper library](https://github.com/waveshareteam/e-Paper.git) that uses `python-periphery` for hardware interface and `uv` for package management.

## What's Different

- Uses `python-periphery` instead of direct GPIO/SPI access
- Uses `uv` for fast Python package management
- Updated to modern Python practices
- Better error handling and logging
- Simplified project structure
- Lazy imports to avoid GPIO initialization on development machines

## Quick Start

1. Install dependencies:
```bash
uv sync
```

2. Run the simple demo:
```bash
python start.py
```

## Project Structure

```
waveshare_epaper/
├── src/waveshare_epd/     # E-paper display modules
├── start.py               # Demo script
├── pyproject.toml         # Project configuration
├── README.md              # This file
```

## Usage

Import specific display modules as needed:

```python
from waveshare_epd.epd4in2_V2 import EPD

# Initialize display
epd = EPD()
epd.init()
epd.Clear()

# Create and display image
from PIL import Image, ImageDraw
image = Image.new('1', (epd.width, epd.height), 255)
draw = ImageDraw.Draw(image)
draw.text((10, 10), 'Hello World!', fill=0)
epd.display(epd.getbuffer(image))
```

## Supported Displays

Works with various e-paper displays: 1.54", 2.13", 2.7", 2.9", 4.2", 5.83", and 7.5" models.

## Demo Features

The demo script showcases:
- Text and graphics rendering
- 4-gray mode display
- Partial update animations
- System information display

## Requirements

- Python 3.8+
- uv package manager
- python-periphery
- PIL (Pillow)
- Raspberry Pi or Jetson Nano (for hardware)

## License

Based on the original Waveshare e-Paper library. See the [original repository](https://github.com/waveshareteam/e-Paper.git) for licensing details.