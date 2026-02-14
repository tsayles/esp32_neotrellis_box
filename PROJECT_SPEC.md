# ESP32 NeoTrellis Box — Requirements Specification

## Document Information

- **Project Name**: ESP32 NeoTrellis Box
- **Version**: 2.0
- **Date**: February 2026
- **Status**: In Development

## 1. Project Overview

### 1.1 Purpose

The ESP32 NeoTrellis Box is a home automation human
interface device (HID) that provides tactile control and
visual feedback for smart home systems.  It supersedes the
original NeoTrellis keypad built on the Particle.io
Electron platform, offering improved performance,
reliability, and features through the ESP32 platform.

### 1.2 Scope

This project encompasses hardware, firmware, and
integration work:

- **Hardware** — Custom PCB integrating ESP32, Adafruit
  NeoTrellis, and 18650 Li-ion battery management.
- **Firmware** — ESP32 software for button handling, LED
  control, and home automation integration.
- **Enclosure** — Sourced or adapted 3D-printable
  enclosure design.
- **Integration** — Communication protocols for home
  automation platforms (MQTT, HTTP).

### 1.3 Goals

1. Create a reliable, modular home automation controller.
2. Provide intuitive visual feedback through RGB LEDs.
3. Enable easy configuration and customisation.
4. Support popular home automation protocols.
5. Support wireless (battery) and wired (USB) operation.
6. Design manufacturable hardware suitable for DIY
   assembly.

---

## 2. Hardware Requirements

### 2.1 Microcontroller — REQ-HW-010

| Attribute | Requirement |
|-----------|-------------|
| Part | ESP32-WROOM-32 or compatible |
| CPU | Dual-core Xtensa LX6 @ 240 MHz |
| RAM | ≥ 520 KB SRAM |
| WiFi | 802.11 b/g/n |
| Bluetooth | 4.2 BR/EDR + BLE |
| Interfaces | I2C, SPI, UART, ADC |

### 2.2 Input Device — REQ-HW-020

| Attribute | Requirement |
|-----------|-------------|
| Part | Adafruit NeoTrellis 4x4 Keypad |
| Buttons | 16 RGB-backlit elastomer keys |
| Interface | I2C (seesaw protocol) |
| Voltage | 3.3 V or 5 V |
| Addressing | Individual button addressing |

### 2.3 Power Supply — REQ-HW-030

The device shall support **two operating modes**:

1. **Wired** — 5 V DC via USB Type-C.
2. **Wireless / Backup** — Rechargeable 18650 Li-ion cell.

| Attribute | Requirement |
|-----------|-------------|
| USB input | 5 V via USB Type-C connector |
| Battery | Single 18650 Li-ion cell (3.7 V nominal) |
| Charging | Integrated Li-ion charge controller (e.g. TP4056) charging from USB |
| Protection | Over-charge, over-discharge, and short-circuit protection |
| Regulation | 3.3 V LDO for ESP32 and NeoTrellis |
| Power path | Seamless switchover between USB and battery |

#### 2.3.1 Current Budget — REQ-HW-031

| Subsystem | Peak Current |
|-----------|-------------|
| ESP32 (WiFi TX) | ~500 mA |
| NeoTrellis (all LEDs max) | ~200 mA |
| Charge controller quiescent | ~2 mA |
| **Total budget** | **1 A recommended** |

#### 2.3.2 Battery Life — REQ-HW-032

- A 3 000 mAh 18650 cell shall provide ≥ 3 hours of
  continuous wireless operation at typical LED brightness.
- The firmware shall expose battery voltage via ADC for
  low-battery indication on the keypad LEDs.

### 2.4 PCB — REQ-HW-040

| Attribute | Requirement |
|-----------|-------------|
| Layers | 2-layer PCB |
| Design tool | KiCAD 7.0+ |
| Connectors | USB Type-C, I2C header, 18650 holder or JST connector |
| Mounting | Standoff holes for ESP32 and NeoTrellis |
| ESD | Protection on exposed connectors |
| RF | WiFi antenna clearance zone |
| Pull-ups | 4.7 kΩ I2C pull-up resistors |
| Decoupling | Capacitors on all power rails |

### 2.5 Enclosure — REQ-HW-050

| Attribute | Requirement |
|-----------|-------------|
| Source | Search [Thingiverse](https://www.thingiverse.com/) for suitable existing designs; adapt as needed |
| Material | 3D-printed PLA or PETG |
| Fit | Accommodate PCB, NeoTrellis keypad, and 18650 cell |
| Access | USB Type-C port accessible for charging |
| Ventilation | Adequate heat dissipation |
| Mounting | Wall-mount and/or desktop stand option |

---

## 3. Firmware Requirements

### 3.1 Button Handling — REQ-FW-010

- Poll NeoTrellis for button events via I2C.
- Debounce presses in software.
- Support press, long-press, and release actions.
- Map each button to a configurable automation command.
- JSON-based per-button action definitions.

### 3.2 LED Control — REQ-FW-020

- Set individual LED colours (RGB, 8-bit per channel).
- Support colour animations and transitions.
- Indicate device status through colour and pattern:

| State | Indicator |
|-------|-----------|
| Off / inactive | Dim white (#0A0A0A) |
| On / active | Warm white (#FFC864) |
| Unavailable | Red (#FF0000) |
| Loading | Blue pulse (#0000FF) |
| Error | Red blink (#FF0000) |
| Low battery | Orange pulse (#FF8000) |

- Adjustable global brightness.

### 3.3 Network Connectivity — REQ-FW-030

- WiFi STA mode with WPA2/WPA3 encryption.
- Captive-portal AP mode for initial WiFi setup.
- Automatic reconnection with exponential backoff.
- Fallback to AP mode after repeated failures.
- Persistent credential storage in ESP32 NVS.

### 3.4 MQTT Integration — REQ-FW-040

- Connect to a configurable MQTT broker.
- Subscribe to device-state topics.
- Publish button-press command topics.
- Support Home Assistant MQTT auto-discovery.
- Optional TLS encryption.
- Username / password authentication.

### 3.5 HTTP / REST API — REQ-FW-050

- Direct HTTP requests to smart-home devices.
- RESTful status and configuration endpoints.
- Webhook support.

### 3.6 Web Interface — REQ-FW-060

- Served from ESP32 LittleFS partition.
- Configuration page (WiFi, MQTT, button mapping).
- Real-time button-status display.
- Firmware update upload page.
- Protected by basic authentication.

### 3.7 OTA Updates — REQ-FW-070

- Over-the-air firmware update via ArduinoOTA and/or
  web upload.
- Secured with password.

### 3.8 Battery Monitoring — REQ-FW-080

- Read battery voltage via ESP32 ADC.
- Report battery level to home automation platform
  (MQTT topic).
- Display low-battery warning on keypad LEDs when
  voltage drops below threshold.

### 3.9 Configuration Storage — REQ-FW-090

- All user configuration stored in LittleFS or NVS.
- Survive power cycles and OTA updates.
- Export / import configuration via web UI.

---

## 4. Functional Requirements

### 4.1 User Stories

1. **As a user**, I want to press a button to toggle my
   bedroom light.
2. **As a user**, I want the button LED to show the
   current light status.
3. **As a user**, I want to configure button actions
   through a web interface.
4. **As a user**, I want to update firmware without
   disassembling the device.
5. **As a user**, I want the device to reconnect
   automatically after network outages.
6. **As a user**, I want the device to operate on battery
   power when unplugged.
7. **As a user**, I want to see a low-battery warning on
   the keypad.

### 4.2 Performance — REQ-SYS-010

| Metric | Target |
|--------|--------|
| Button response time | < 100 ms |
| LED update latency | < 500 ms |
| WiFi reconnection | < 10 s |
| MQTT reconnection | Automatic, exponential backoff |

### 4.3 Reliability — REQ-SYS-020

- 24/7 continuous operation capability.
- Automatic recovery from network failures.
- Hardware watchdog timer for crash recovery.
- Persistent configuration across power cycles.

### 4.4 Usability — REQ-SYS-030

- Clear, intuitive LED status indicators.
- Simple web-based configuration.
- Responsive tactile button feedback.
- Minimal first-time setup steps.

---

## 5. Supported Platforms

| Platform | Protocol |
|----------|----------|
| Home Assistant | MQTT (auto-discovery) |
| OpenHAB | MQTT |
| Node-RED | MQTT |
| Custom systems | MQTT / HTTP |

---

## 6. Technical Constraints

### 6.1 Hardware

- I2C bus speed: max 400 kHz.
- ESP32 peak current during WiFi TX: ~500 mA.
- PCB dimensions constrained by enclosure.
- 18650 cell adds ~18.5 × 65 mm to enclosure volume.
- Heat dissipation from charge controller and LDO.

### 6.2 Firmware

- ESP32 SRAM: 520 KB (shared with WiFi stack).
- LittleFS partition size limits web UI assets.
- WiFi range limited by on-module antenna.
- Dependent on external MQTT broker availability.
- NeoTrellis seesaw library compatibility.

---

## 7. Testing & Acceptance Criteria

### 7.1 Hardware Tests

- Power supply continuity and voltage regulation.
- I2C communication with NeoTrellis (bus scan).
- All 16 buttons register presses correctly.
- LED colour and brightness accuracy.
- Battery charging and protection circuit validation.
- Long-term reliability (48-hour soak test).

### 7.2 Firmware Tests

- Unit tests for each core module.
- MQTT publish / subscribe integration tests.
- Network failure and recovery tests.
- Rapid button-press load test.
- Power-cycle configuration persistence test.
- Battery voltage ADC accuracy test.

### 7.3 System Integration Tests

- End-to-end Home Assistant toggle scenario.
- Multi-device status monitoring.
- OTA update followed by configuration persistence
  check.
- Battery-to-USB switchover during operation.

---

## 8. Documentation Deliverables

- [ ] Hardware schematic (PDF export)
- [ ] PCB layout and Gerber files
- [ ] Bill of Materials (BOM)
- [ ] Assembly instructions
- [ ] Firmware installation guide
- [ ] Configuration guide
- [ ] API documentation (MQTT topics, HTTP endpoints)
- [ ] Troubleshooting guide
- [ ] Example button configurations

---

## 9. Future Enhancements

- **Display Integration** — small OLED for status
  messages.
- **Sensors** — temperature, humidity, or motion.
- **Audio Feedback** — piezo buzzer for button
  confirmations.
- **Multi-Panel Support** — chain multiple NeoTrellis
  units.
- **Scenes** — complex multi-device actions.
- **Scheduling** — time-based automation triggers.
- **Voice Control** — integration with voice assistants.

---

## 10. References

### Hardware

- [Adafruit NeoTrellis](https://learn.adafruit.com/adafruit-neotrellis)
- [ESP32 Technical Reference](https://www.espressif.com/en/support/documents/technical-documents)
- [KiCAD Documentation](https://docs.kicad.org/)
- [TP4056 Li-Ion Charger](https://dlnmh9ip6v2uc.cloudfront.net/datasheets/Prototyping/TP4056.pdf)

### Software

- [Arduino-ESP32](https://docs.espressif.com/projects/arduino-esp32/)
- [MQTT Protocol](https://mqtt.org/)
- [Home Assistant MQTT Discovery](https://www.home-assistant.io/docs/mqtt/discovery/)

### Related Projects

- Original Particle.io Electron NeoTrellis keypad
  (predecessor).
- [Adafruit NeoTrellis M4](https://www.adafruit.com/product/4020)

---

## Appendix A: Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Feb 2026 | Initial project specification |
| 2.0 | Feb 2026 | Split into requirements document; added 18650 battery requirements; added battery monitoring firmware requirements |
