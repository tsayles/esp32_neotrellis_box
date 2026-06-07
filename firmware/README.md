# Firmware

ESP32 firmware for the NeoTrellis Box, built with
[PlatformIO](https://platformio.org/).

## Directory Structure

```
firmware/
├── platformio.ini      PlatformIO project configuration
├── src/                Application source files
│   └── main.cpp        Entry point
├── include/            Project header files
├── lib/                Project-specific libraries
├── test/               Unit tests
└── data/               SPIFFS/LittleFS web UI assets
```

## Getting Started

### Prerequisites

- [PlatformIO Core](https://docs.platformio.org/en/latest/core/installation.html)
  or PlatformIO IDE extension for VS Code.

### Build & Upload

```bash
cd firmware
pio run              # Build
pio run -t upload    # Flash to ESP32
pio run -t monitor   # Serial monitor
```

### Running Tests

```bash
cd firmware
pio test
```

## Architecture

See [PROJECT_SPEC.md](../PROJECT_SPEC.md) §3.2 for the
firmware module architecture:

- **Button Handler** — NeoTrellis polling, debounce,
  action mapping
- **LED Controller** — per-button RGB, animations,
  status indication
- **WiFi Manager** — connection, captive portal,
  auto-reconnect
- **MQTT Client** — broker connection, pub/sub,
  Home Assistant discovery
- **Web Server** — configuration UI, status display
- **OTA Updater** — over-the-air firmware updates
