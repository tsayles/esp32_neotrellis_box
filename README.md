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

## Hardware

The hardware consists of a custom PCB that provides:

- **ESP32 Module Mounting**: Socket or pads for ESP32 development board
- **NeoTrellis Interface**: I2C connection for Adafruit NeoTrellis 4x4 keypad
- **Power Management**: Regulated power supply for stable operation
- **Expansion Options**: Additional GPIO breakouts for future enhancements

### Components

- ESP32 Development Board (e.g., ESP32-DevKitC, ESP32-WROOM-32)
- Adafruit NeoTrellis 4x4 RGB Keypad
- Custom PCB (designed in KiCAD)
- Power supply (USB or wall adapter)

### Hardware Design

Hardware design files are located in the `/hardware` directory and are developed using KiCAD.

## Software

The firmware enables:

- **Button Programming**: Configure each button to trigger specific home automation actions
- **Status Display**: LED colors indicate device states (on/off, brightness levels, etc.)
- **Network Connectivity**: WiFi connection for communication with home automation systems
- **MQTT Support**: Integration with MQTT-based automation platforms
- **Web Interface**: Configuration and monitoring through a web UI
- **OTA Updates**: Over-the-air firmware updates for easy maintenance

### Software Architecture

- **Platform**: Arduino/ESP-IDF
- **Communication**: WiFi, MQTT, HTTP/HTTPS
- **Libraries**: Adafruit_NeoTrellis, WiFi, PubSubClient, etc.

## Getting Started

### Prerequisites

- KiCAD (for hardware design)
- Arduino IDE or PlatformIO (for firmware development)
- ESP32 board support package
- Adafruit NeoTrellis library

### Installation

*Detailed installation instructions will be added as the project develops.*

1. Clone this repository
2. Install required libraries
3. Configure WiFi and MQTT settings
4. Upload firmware to ESP32
5. Assemble hardware components

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

- [Project Specification](PROJECT_SPEC.md) - Detailed technical specifications and requirements

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
