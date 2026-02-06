# ESP32 NeoTrellis Box - Project Specification

## Document Information

- **Project Name**: ESP32 NeoTrellis Box
- **Version**: 1.0
- **Date**: February 2026
- **Status**: In Development

## 1. Project Overview

### 1.1 Purpose

The ESP32 NeoTrellis Box is a home automation human interface device (HID) designed to provide tactile control and visual feedback for smart home systems. It supersedes the original NeoTrellis keypad built on the Particle.io Electron platform, offering improved performance, reliability, and features through the ESP32 platform.

### 1.2 Scope

This project encompasses both hardware and software development:

- **Hardware**: Custom PCB design for integrating ESP32 and Adafruit NeoTrellis
- **Firmware**: ESP32 software for button handling, LED control, and home automation integration
- **Integration**: Communication protocols for home automation platforms

### 1.3 Goals

- Create a reliable, modular home automation controller
- Provide intuitive visual feedback through RGB LEDs
- Enable easy configuration and customization
- Support popular home automation protocols (MQTT, HTTP, etc.)
- Design manufacturable hardware suitable for DIY assembly

## 2. Hardware Specifications

### 2.1 Architecture Overview

```
┌─────────────────────────────────────┐
│     ESP32 NeoTrellis Box PCB        │
│                                     │
│  ┌──────────┐      ┌─────────────┐ │
│  │  ESP32   │◄────►│  NeoTrellis │ │
│  │  Module  │ I2C  │  4x4 Keypad │ │
│  └──────────┘      └─────────────┘ │
│       │                             │
│       ├─► Power Regulation          │
│       ├─► WiFi Antenna              │
│       └─► GPIO Expansion            │
└─────────────────────────────────────┘
```

### 2.2 Core Components

#### 2.2.1 Microcontroller

- **Part**: ESP32-WROOM-32 or compatible module
- **Specifications**:
  - Dual-core Xtensa LX6 @ 240 MHz
  - 520 KB SRAM
  - WiFi 802.11 b/g/n
  - Bluetooth 4.2 BR/EDR and BLE
  - Multiple I2C, SPI, UART interfaces

#### 2.2.2 Input Device

- **Part**: Adafruit NeoTrellis 4x4 Elastomer Keypad
- **Specifications**:
  - 16 RGB backlit buttons
  - I2C interface (seesaw protocol)
  - 3.3V or 5V operation
  - Individual button addressing
  - Elastomer button pad with RGB LED matrix

#### 2.2.3 Power Supply

- **Input**: 5V DC via USB Type-C or barrel jack
- **Regulation**: 3.3V LDO for ESP32 and NeoTrellis
- **Current Requirements**:
  - ESP32: ~500mA (peak during WiFi transmission)
  - NeoTrellis: ~200mA (all LEDs at full brightness)
  - Total budget: 1A recommended

### 2.3 PCB Design

#### 2.3.1 Design Tool

- **Software**: KiCAD 7.0 or later
- **Files Location**: `/hardware` directory

#### 2.3.2 PCB Specifications

- **Layers**: 2-layer PCB
- **Dimensions**: TBD (optimized for enclosure)
- **Mounting**: Standoff holes for ESP32 and NeoTrellis
- **Connectors**:
  - USB Type-C or Micro USB for power
  - I2C header for NeoTrellis
  - GPIO header for expansion (optional)

#### 2.3.3 Key Design Considerations

- Proper I2C pull-up resistors (4.7kΩ recommended)
- Decoupling capacitors for stable power delivery
- RF considerations for WiFi antenna placement
- ESD protection on exposed connectors
- Optional battery backup circuit

### 2.4 Enclosure

- Design to accommodate PCB and NeoTrellis
- Access for USB connector
- Ventilation for heat dissipation
- Mounting options (wall-mount, desktop stand)
- Suggested material: 3D printed plastic or laser-cut acrylic

## 3. Software Specifications

### 3.1 Development Environment

#### 3.1.1 Platform Options

- **Option 1**: Arduino IDE with ESP32 board support
- **Option 2**: PlatformIO (recommended for advanced features)
- **Option 3**: ESP-IDF native development

#### 3.1.2 Required Libraries

- **Adafruit_NeoTrellis**: Button and LED control
- **WiFi**: Network connectivity
- **PubSubClient**: MQTT communication
- **ArduinoJson**: Configuration and message parsing
- **AsyncWebServer**: Web interface (optional)
- **ArduinoOTA**: Over-the-air updates

### 3.2 Firmware Architecture

#### 3.2.1 Core Modules

```
┌─────────────────────────────────────┐
│         Main Application            │
├─────────────────────────────────────┤
│  Button Handler  │  LED Controller  │
├──────────────────┼──────────────────┤
│    Configuration Manager            │
├─────────────────────────────────────┤
│  WiFi Manager    │  MQTT Client     │
├──────────────────┼──────────────────┤
│  Web Server      │  OTA Updater     │
└─────────────────────────────────────┘
```

#### 3.2.2 Button Handler

- **Functionality**:
  - Poll NeoTrellis for button events
  - Debounce button presses
  - Support press, hold, and release actions
  - Map buttons to automation commands

- **Configuration**:
  - JSON-based button mapping
  - Per-button action definitions
  - Support for multiple action types

#### 3.2.3 LED Controller

- **Functionality**:
  - Set individual LED colors
  - Support color animations
  - Indicate device status through color/pattern
  - Brightness control

- **Status Indicators**:
  - Off: Device inactive
  - Dim color: Device reachable but off
  - Bright color: Device active
  - Blinking: Transitioning state
  - White: System status

### 3.3 Home Automation Integration

#### 3.3.1 Communication Protocols

**MQTT (Primary)**
- Connect to MQTT broker
- Subscribe to device state topics
- Publish button press commands
- Support for Home Assistant autodiscovery

**HTTP/REST API (Secondary)**
- Direct HTTP requests to smart home devices
- RESTful API integration
- Webhook support

#### 3.3.2 Supported Platforms

- Home Assistant (via MQTT)
- OpenHAB
- Node-RED
- Custom MQTT-based systems

### 3.4 Configuration

#### 3.4.1 WiFi Setup

- **Captive Portal**: Initial setup mode for WiFi credentials
- **Fallback**: Revert to AP mode if connection fails
- **Storage**: Persistent storage in ESP32 NVS

#### 3.4.2 Button Configuration

Format example (JSON):
```json
{
  "buttons": [
    {
      "id": 0,
      "label": "Bedroom Light",
      "action": {
        "type": "mqtt",
        "topic": "home/bedroom/light/set",
        "payload": "toggle"
      },
      "status": {
        "topic": "home/bedroom/light/state",
        "on_color": [255, 200, 100],
        "off_color": [50, 40, 20]
      }
    }
  ]
}
```

#### 3.4.3 Web Interface

- Configuration page served by ESP32
- Real-time button status display
- MQTT broker settings
- Button mapping editor
- Firmware update interface

### 3.5 Security

- **WiFi**: WPA2/WPA3 encryption
- **MQTT**: TLS encryption support (optional)
- **Authentication**: Username/password for MQTT
- **OTA**: Secured firmware updates
- **Web Interface**: Basic authentication

## 4. Functional Requirements

### 4.1 User Stories

1. **As a user**, I want to press a button to turn on my bedroom light
2. **As a user**, I want the button LED to show the current light status
3. **As a user**, I want to configure button actions through a web interface
4. **As a user**, I want to update firmware without disassembling the device
5. **As a user**, I want the device to reconnect automatically after network outages

### 4.2 System Requirements

#### 4.2.1 Performance

- Button press response time: < 100ms
- LED update latency: < 500ms
- WiFi reconnection time: < 10 seconds
- MQTT reconnection: Automatic with exponential backoff

#### 4.2.2 Reliability

- 24/7 operation capability
- Automatic recovery from network failures
- Watchdog timer for crash recovery
- Persistent configuration storage

#### 4.2.3 Usability

- Clear LED status indicators
- Simple web-based configuration
- Responsive button feedback
- Minimal setup requirements

## 5. Development Roadmap

### Phase 1: Hardware Design (Weeks 1-4)

- [ ] Create schematic in KiCAD
- [ ] Design PCB layout
- [ ] Generate BOM (Bill of Materials)
- [ ] Order prototype PCBs
- [ ] Assemble and test prototype

### Phase 2: Core Firmware (Weeks 3-6)

- [ ] Set up development environment
- [ ] Implement NeoTrellis driver integration
- [ ] Develop button handler
- [ ] Implement LED controller
- [ ] Test basic functionality

### Phase 3: Network Integration (Weeks 5-8)

- [ ] WiFi manager implementation
- [ ] MQTT client integration
- [ ] Configuration storage
- [ ] Network reliability testing

### Phase 4: Home Automation Integration (Weeks 7-10)

- [ ] Home Assistant MQTT discovery
- [ ] Button-to-action mapping
- [ ] Status feedback implementation
- [ ] Integration testing

### Phase 5: Web Interface (Weeks 9-12)

- [ ] Basic web server
- [ ] Configuration interface
- [ ] Real-time status display
- [ ] OTA update mechanism

### Phase 6: Testing & Documentation (Weeks 11-14)

- [ ] Comprehensive testing
- [ ] User documentation
- [ ] Installation guide
- [ ] Example configurations
- [ ] Final hardware revision

## 6. Technical Constraints

### 6.1 Hardware Limitations

- I2C bus speed limitations (max 400 kHz)
- ESP32 power consumption considerations
- PCB size constraints for enclosure
- Heat dissipation requirements

### 6.2 Software Limitations

- ESP32 memory constraints
- WiFi range limitations
- MQTT broker availability dependency
- NeoTrellis library compatibility

## 7. Testing Strategy

### 7.1 Hardware Testing

- Continuity and power supply verification
- I2C communication validation
- Button press detection
- LED brightness and color accuracy
- Long-term reliability testing

### 7.2 Software Testing

- Unit tests for core modules
- Integration tests for MQTT communication
- Network failure recovery testing
- Load testing (rapid button presses)
- Power cycle recovery testing

### 7.3 Integration Testing

- End-to-end home automation scenarios
- Multi-device status monitoring
- Configuration persistence
- OTA update validation

## 8. Documentation Deliverables

- [ ] Hardware schematic (PDF)
- [ ] PCB layout and Gerber files
- [ ] Bill of Materials (BOM)
- [ ] Assembly instructions
- [ ] Firmware installation guide
- [ ] Configuration guide
- [ ] API documentation
- [ ] Troubleshooting guide
- [ ] Example configurations

## 9. Future Enhancements

### Potential Features

- **Battery Backup**: Operate during power outages
- **Display Integration**: Add small OLED for status messages
- **Sensors**: Temperature, humidity, or motion sensors
- **Audio Feedback**: Piezo buzzer for button confirmations
- **Multi-Panel Support**: Chain multiple NeoTrellis units
- **Scenes**: Complex multi-device actions
- **Scheduling**: Time-based automation triggers
- **Voice Control**: Integration with voice assistants

## 10. References

### Hardware

- [Adafruit NeoTrellis Documentation](https://learn.adafruit.com/adafruit-neotrellis)
- [ESP32 Technical Reference](https://www.espressif.com/en/support/documents/technical-documents)
- [KiCAD Documentation](https://docs.kicad.org/)

### Software

- [Arduino-ESP32 Documentation](https://docs.espressif.com/projects/arduino-esp32/)
- [MQTT Protocol Specification](https://mqtt.org/)
- [Home Assistant MQTT Discovery](https://www.home-assistant.io/docs/mqtt/discovery/)

### Related Projects

- Original Particle.io Electron NeoTrellis keypad (predecessor)
- [Adafruit NeoTrellis M4](https://www.adafruit.com/product/4020)

## Appendix A: Pin Mapping

*To be completed during hardware design phase*

| ESP32 Pin | Function | NeoTrellis Connection |
|-----------|----------|----------------------|
| GPIO21    | SDA      | I2C Data             |
| GPIO22    | SCL      | I2C Clock            |
| 3.3V      | Power    | VCC                  |
| GND       | Ground   | GND                  |

## Appendix B: Color Codes

Suggested LED color scheme for device status:

| Device State | RGB Color      | Hex Code |
|-------------|---------------|----------|
| Off         | Dim White     | #0A0A0A  |
| On          | Warm White    | #FFC864  |
| Unavailable | Red           | #FF0000  |
| Loading     | Blue (pulse)  | #0000FF  |
| Error       | Red (blink)   | #FF0000  |

## Appendix C: Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0     | Feb 2026 | Initial | Initial project specification |
