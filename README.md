# ESP32 NeoTrellis Box

A home automation control interface based on the ESP32 microcontroller and Adafruit NeoTrellis 4x4 RGB keypad.

![Project Status](https://img.shields.io/badge/status-in%20development-yellow)
![License](https://img.shields.io/badge/license-GPL%20v3-blue)

## Overview

The ESP32 NeoTrellis Box is a customizable home automation human interface device (HID) that provides 16 programmable backlit buttons for controlling smart home devices and displaying their status. This project supersedes the original NeoTrellis keypad built on the Particle.io Electron platform.

### Key Features

- **16 Programmable Buttons**: Each button can be configured to trigger home automation actions (e.g., turn on lights, control scenes, toggle devices)
- **RGB LED Feedback**: Individual RGB LEDs under each button display real-time device status
- **ESP32-Based**: Leverages the powerful ESP32 microcontroller with built-in WiFi/Bluetooth
- **Modular Hardware**: Custom PCB design for easy assembly and integration
- **Home Automation Integration**: Designed to work with popular home automation platforms

## Repository Structure

```
esp32_neotrellis_box/
├── hardware/           KiCAD PCB design, BOM, gerbers
├── firmware/           PlatformIO / ESP32 firmware
├── enclosure/          3D-print and laser-cut enclosure
├── docs/               Assembly, configuration, API docs
├── examples/           Sample button-config JSON files
├── PROJECT_SPEC.md     Full technical specification
└── LICENSE
```

## Hardware

Hardware design files live in [`hardware/`](hardware/)
and are developed with **KiCAD 7.0+**.

### Core Components

- ESP32-C3 Super Mini
- Adafruit NeoTrellis 4x4 RGB Keypad
- Custom 2-layer PCB
- USB Type-C / barrel-jack power input

See [`hardware/README.md`](hardware/README.md) for
design details and pin mapping.

## Firmware

The PlatformIO project lives in [`firmware/`](firmware/).

Key capabilities:

- **Button Handler** — NeoTrellis polling, debounce,
  action mapping
- **LED Controller** — per-button RGB status feedback
- **WiFi Manager** — captive portal, auto-reconnect
- **MQTT Client** — Home Assistant discovery, pub/sub
- **Web Server** — configuration and status UI
- **OTA Updater** — over-the-air firmware updates

See [`firmware/README.md`](firmware/README.md) for build
and upload instructions.

## Enclosure

3D-printable and laser-cut enclosure designs live in
[`enclosure/`](enclosure/).

## Getting Started

### Prerequisites

- **KiCAD 7.0+** — hardware schematic and PCB layout
- **PlatformIO** — firmware build and upload
- ESP32 board support package (installed by PlatformIO)

### Quick Start

```bash
# Clone
git clone https://github.com/tsayles/esp32_neotrellis_box.git
cd esp32_neotrellis_box

# Build firmware
cd firmware
pio run

# Flash to ESP32
pio run -t upload
```

## Project Status

🚧 **Currently in Development** 🚧

This project is in active development. Hardware design and firmware are being developed concurrently.

### Roadmap

- [ ] Complete hardware PCB design in KiCAD
- [ ] Prototype PCB fabrication and testing
- [ ] Core firmware development
- [ ] Home automation integration
- [ ] Web interface development
- [ ] Documentation and examples

## Documentation

- [Project Specification](PROJECT_SPEC.md) — Detailed technical specifications and requirements
- [Assembly Guide](docs/assembly-guide.md) — Hardware assembly
- [Configuration Guide](docs/configuration-guide.md) — WiFi, MQTT, button setup
- [API Reference](docs/api-reference.md) — MQTT topics, HTTP endpoints
- [Troubleshooting](docs/troubleshooting.md) — Common issues

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Adafruit Industries for the NeoTrellis hardware
- ESP32 community for extensive documentation and libraries
- Original Particle.io Electron-based NeoTrellis keypad project

## Contact

For questions or suggestions, please open an issue on GitHub.
