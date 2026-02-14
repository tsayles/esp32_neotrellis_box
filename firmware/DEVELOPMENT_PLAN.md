# Firmware Development Plan

> **Approach**: Agent-first, autonomous HIL development
> with bottom-up mock/live driver parity.
>
> **Parent requirements**:
> [PROJECT_SPEC.md](../PROJECT_SPEC.md) §3 (Firmware
> Requirements)
>
> **HIL reference**:
> [Autonomous Agent Operations](https://github.com/tsayles/homelab/blob/main/hil-agentic-development/docs/architecture/autonomous-agent-operations.md)

---

## 1. Firmware Architecture

```
┌─────────────────────────────────────────┐
│           Main Application              │
├─────────────────────────────────────────┤
│  Button Handler    │  LED Controller    │
├────────────────────┼────────────────────┤
│  Battery Monitor   │  Config Manager    │
├─────────────────────────────────────────┤
│  WiFi Manager      │  MQTT Client       │
├────────────────────┼────────────────────┤
│  Web Server        │  OTA Updater       │
├─────────────────────────────────────────┤
│         Hardware Abstraction Layer       │
│  ┌──────────┐  ┌──────────┐  ┌───────┐ │
│  │NeoTrellis│  │  WiFi    │  │  ADC  │ │
│  │ Driver   │  │  Driver  │  │Driver │ │
│  └──────────┘  └──────────┘  └───────┘ │
│        ▲               ▲          ▲     │
│   Mock / Live     Mock / Live  Mock/Live│
└─────────────────────────────────────────┘
```

---

## 2. Agent-First Development Paradigm

### 2.1 Bottom-Up, Layer-by-Layer

The agent develops firmware **from the hardware up**,
verifying each layer before building the next:

```
Layer 1 ─► Hardware Drivers (NeoTrellis, ADC, WiFi)
Layer 2 ─► Core Modules (Button Handler, LED, Battery)
Layer 3 ─► Network Services (WiFi Mgr, MQTT, Web)
Layer 4 ─► Application Logic (Config, Scenes, OTA)
Layer 5 ─► Integration (End-to-End, System Tests)
```

Each layer is committed and verified (mock + live)
before the next layer begins.

### 2.2 Mock / Live Driver Parity

Every hardware driver has **two implementations**:

| Driver | Live (hardware) | Mock (testing) |
|--------|-----------------|----------------|
| NeoTrellis | I2C via seesaw lib | Simulated key events + LED state |
| WiFi | ESP32 WiFi stack | Loopback / stub |
| ADC (battery) | ESP32 ADC peripheral | Configurable voltage model |
| MQTT | PubSubClient | In-process broker stub |

**Parity rule**: Mock and live drivers implement the
same abstract interface.  All tests must pass against
**both** drivers.  Any behavioural mismatch is a bug in
the mock and must be resolved before proceeding.

### 2.3 Communication Protocol

- **Primary channel**: GitHub Pull Request on the
  firmware feature branch.
- Agent posts structured status updates every 1–2 hours.
- Escalation when:
  - ESP32 unresponsive after reset attempts.
  - Serial port lost and not recoverable.
  - Test failures exceed threshold (5 consecutive).
  - Requirements ambiguity blocks progress.

### 2.4 Session Lifecycle

```
Phase 1  ──►  Collaborative Setup & HW Verification
               (ESP32 on USB, NeoTrellis on I2C)
Phase 2  ──►  Human Disconnects — Agent Iterates
               (bottom-up driver → application)
Phase 3  ──►  Bidirectional Communication via PR
Phase 4  ──►  Self-Management (Agent Autonomous)
Phase 5  ──►  Completion & Human Validation
```

---

## 3. Development Environment

### 3.1 Toolchain

- **PlatformIO** (CLI) — build, upload, test, monitor.
- `platformio.ini` in `firmware/`.
- Framework: Arduino (ESP32 board support).

### 3.2 Required Libraries

| Library | Purpose | PlatformIO lib_deps |
|---------|---------|---------------------|
| Adafruit seesaw | NeoTrellis I2C driver | `adafruit/Adafruit seesaw Library` |
| PubSubClient | MQTT client | `knolleary/PubSubClient` |
| ArduinoJson | JSON config parsing | `bblanchon/ArduinoJson` |
| ESPAsyncWebServer | Web UI | `me-no-dev/ESPAsyncWebServer` |
| ArduinoOTA | Over-the-air updates | (built-in) |
| LittleFS | File-system for config/web assets | (built-in) |

### 3.3 HIL Lab Setup

```
┌──────────┐  USB/Serial  ┌──────────────┐
│   Lab    │◄────────────►│  ESP32 Dev   │
│Workstation│              │   Board      │
│ (agent)  │              │  + NeoTrellis│
└──────────┘              │  + 18650     │
                          └──────────────┘
```

Agent connects to ESP32 via serial port for:
- Flashing firmware (`pio run -t upload`).
- Serial monitor for logs and test output.
- PlatformIO test runner for on-device tests.

---

## 4. Development Phases

### Phase 1 — Collaborative Setup (Human + Agent)

- [ ] Human connects ESP32 + NeoTrellis to lab
      workstation via USB.
- [ ] Agent verifies hardware connectivity:
  - ESP32 serial port detected.
  - PlatformIO can build and upload a blink sketch.
  - I2C scan detects NeoTrellis at `0x2E`.
- [ ] Agent creates feature branch
      (`dev/firmware-core`) and opens **draft PR**.
- [ ] Define autonomous operation parameters.
- [ ] Human disconnects — agent begins autonomous work.

### Phase 2 — Hardware Abstraction Layer (Agent — Autonomous)

**Layer 1: Drivers — closest to hardware.**

#### 2a. NeoTrellis Driver

- [ ] Define abstract `ITrellis` interface
      (`firmware/include/itrellis.h`):
  - `begin()`, `readButtons()`, `setPixelColor()`,
    `show()`, `setBrightness()`.
- [ ] Implement **live driver** (`TrellisLive`) wrapping
      Adafruit seesaw library.
- [ ] Implement **mock driver** (`TrellisMock`) with
      simulated button events and LED state tracking.
- [ ] Write unit tests for both drivers:
  - Button event generation.
  - LED colour setting and readback.
  - Error injection (I2C timeout, bus error).
- [ ] Run tests on device (live) and host (mock).
- [ ] **Parity check**: mock and live produce identical
      results for identical inputs.
- [ ] Commit passing layer; post status on PR.

#### 2b. ADC / Battery Driver

- [ ] Define abstract `IBattery` interface:
  - `readVoltage()`, `getPercentage()`,
    `isLowBattery()`.
- [ ] Implement live driver (ESP32 ADC + divider).
- [ ] Implement mock driver (configurable voltage model).
- [ ] Unit tests + parity check.
- [ ] Commit; post status.

#### 2c. WiFi Driver

- [ ] Define abstract `IWiFi` interface:
  - `connect()`, `disconnect()`, `isConnected()`,
    `getIP()`, `startAP()`.
- [ ] Implement live driver (ESP32 WiFi).
- [ ] Implement mock driver (always-connected stub or
      configurable failure injection).
- [ ] Unit tests + parity check.
- [ ] Commit; post status.

### Phase 3 — Core Modules (Agent — Autonomous)

**Layer 2: Built on verified drivers.**

#### 3a. Button Handler

- [ ] Implement button handler using `ITrellis`:
  - Polling loop with configurable interval.
  - Software debounce.
  - Press, long-press, release events.
  - Button-to-action mapping from JSON config.
- [ ] Unit tests against mock driver.
- [ ] HIL tests against live driver (agent triggers
      events; human may assist with physical presses
      initially, then agent uses test jig or serial
      commands).
- [ ] Parity check; commit.

#### 3b. LED Controller

- [ ] Implement LED controller using `ITrellis`:
  - Set colour per button.
  - Animations (pulse, blink, fade).
  - Status-based colour mapping.
  - Global brightness control.
- [ ] Unit tests (mock: verify state; live: visual).
- [ ] Parity check; commit.

#### 3c. Battery Monitor

- [ ] Implement battery monitor using `IBattery`:
  - Periodic voltage sampling.
  - Percentage estimation (voltage curve lookup).
  - Low-battery LED warning trigger.
- [ ] Unit tests + parity check; commit.

### Phase 4 — Network Services (Agent — Autonomous)

**Layer 3: Built on verified core modules.**

#### 4a. WiFi Manager

- [ ] Implement WiFi manager using `IWiFi`:
  - Captive portal for first-time setup.
  - Credential storage in NVS.
  - Auto-reconnect with exponential backoff.
  - Fallback to AP mode.
- [ ] Tests: mock (connection state machine),
      live (actual WiFi connect).
- [ ] Parity check; commit.

#### 4b. MQTT Client

- [ ] Implement MQTT client:
  - Configurable broker, port, credentials.
  - Publish button events.
  - Subscribe to device state topics.
  - Home Assistant auto-discovery.
  - Reconnection with backoff.
- [ ] Tests: mock (in-process broker stub),
      live (connect to real broker on LAN).
- [ ] Parity check; commit.

#### 4c. Web Server

- [ ] Implement async web server:
  - Serve configuration UI from LittleFS.
  - REST endpoints: `/api/status`, `/api/config`.
  - Basic authentication.
- [ ] Tests: mock (HTTP request/response validation),
      live (browser + curl).
- [ ] Commit.

### Phase 5 — Application Logic (Agent — Autonomous)

**Layer 4: Top-level features.**

- [ ] Configuration manager:
  - Load/save JSON config from LittleFS.
  - Button mapping, MQTT settings, WiFi credentials.
  - Web UI import/export.
- [ ] OTA updater:
  - ArduinoOTA + web upload.
  - Password protection.
- [ ] Battery reporting via MQTT:
  - Publish `neotrellis/<id>/battery` topic.
- [ ] Tests for each module; commit.

### Phase 6 — Integration Testing (Agent — Autonomous)

**Layer 5: Full-stack validation.**

- [ ] End-to-end test: button press → MQTT publish →
      Home Assistant receives event.
- [ ] End-to-end test: HA state change → MQTT → LED
      update on keypad.
- [ ] OTA update → verify config persistence.
- [ ] Battery switchover during active MQTT session.
- [ ] 24-hour soak test (agent monitors serial + MQTT
      for crashes or brownouts).
- [ ] Full mock suite: all tests pass without hardware.
- [ ] Full live suite: all tests pass on hardware.
- [ ] **Parity report**: mock vs. live comparison across
      all layers.
- [ ] Post final test report on PR.

### Phase 7 — Completion & Human Validation

- [ ] Agent marks PR as **ready for review**.
- [ ] Agent posts completion summary:
  - Total commits, test counts, parity status.
  - Coverage report.
  - Known issues / errata.
- [ ] Human performs final validation:
  - Physical button presses → correct actions.
  - LED colours match spec.
  - Web UI functional.
  - OTA update works.
- [ ] Human approves or requests further iteration.

---

## 5. Test Strategy

### 5.1 Test Hierarchy

| Level | Scope | Runner | Driver |
|-------|-------|--------|--------|
| Unit | Single function / class | PlatformIO native | Mock |
| Integration | Module interactions | PlatformIO native | Mock |
| HIL | On-device behaviour | PlatformIO device | Live |
| Parity | Mock vs. live comparison | Both | Both |
| System | End-to-end scenarios | Agent orchestrated | Live |

### 5.2 Test Naming Convention

```
test/<layer>/<module>/test_<behaviour>.cpp
```

Example:
```
test/drivers/neotrellis/test_button_events.cpp
test/drivers/neotrellis/test_led_control.cpp
test/core/button_handler/test_debounce.cpp
test/network/mqtt/test_reconnect.cpp
test/integration/test_button_to_mqtt.cpp
```

### 5.3 Parity Test Framework

For each driver interface, a parity test:

1. Instantiate mock driver.
2. Instantiate live driver.
3. Execute identical operation sequence on both.
4. Compare outputs (return values, state, timing
   tolerances).
5. Report any differences as failures.

### 5.4 Autonomous Test Execution

Agent runs tests in a loop:

```
┌──► Build firmware (pio run)
│    ├─ Fail → fix, retry
│    └─ Pass ▼
│    Run mock tests (pio test -e native)
│    ├─ Fail → fix, retry
│    └─ Pass ▼
│    Flash to ESP32 (pio run -t upload)
│    ├─ Fail → reconnect serial, retry, escalate
│    └─ Pass ▼
│    Run live tests (pio test -e esp32dev)
│    ├─ Fail → analyse, fix, retry (max 5)
│    └─ Pass ▼
│    Run parity comparison
│    ├─ Mismatch → update mock, re-test
│    └─ Match ▼
│    Commit + push + post status on PR
└────── Next task
```

---

## 6. Graceful Degradation

| Failure Scenario | Agent Response |
|------------------|----------------|
| ESP32 unresponsive | Re-flash, power cycle, escalate |
| Serial port lost | Reconnect (3 retries), escalate |
| WiFi unavailable | Continue mock tests, skip live network tests |
| MQTT broker down | Continue mock tests, skip live MQTT tests |
| Build failure | Analyse error, fix, retry |
| Test fails 5× consecutive | Pause, escalate, continue other work |
| NeoTrellis not on I2C bus | Skip live trellis tests, escalate |
| Disk space low | Clean build artifacts, escalate if < 5 % |

---

## 7. Directory Layout

```
firmware/
├── platformio.ini
├── src/
│   ├── main.cpp
│   ├── drivers/
│   │   ├── itrellis.h          Interface
│   │   ├── trellis_live.cpp    Live driver
│   │   ├── trellis_mock.cpp    Mock driver
│   │   ├── ibattery.h          Interface
│   │   ├── battery_live.cpp
│   │   ├── battery_mock.cpp
│   │   ├── iwifi.h             Interface
│   │   ├── wifi_live.cpp
│   │   └── wifi_mock.cpp
│   ├── core/
│   │   ├── button_handler.cpp
│   │   ├── led_controller.cpp
│   │   └── battery_monitor.cpp
│   ├── network/
│   │   ├── wifi_manager.cpp
│   │   ├── mqtt_client.cpp
│   │   └── web_server.cpp
│   └── app/
│       ├── config_manager.cpp
│       └── ota_updater.cpp
├── include/
│   └── (header files)
├── lib/
│   └── (project-specific libs)
├── test/
│   ├── drivers/
│   ├── core/
│   ├── network/
│   ├── integration/
│   └── parity/
├── data/
│   └── (LittleFS web UI assets)
└── DEVELOPMENT_PLAN.md    ← this file
```

---

## 8. References

- [PlatformIO ESP32 Docs](https://docs.platformio.org/en/latest/platforms/espressif32.html)
- [PlatformIO Unit Testing](https://docs.platformio.org/en/latest/advanced/testing/index.html)
- [Adafruit seesaw Library](https://github.com/adafruit/Adafruit_Seesaw)
- [PubSubClient](https://github.com/knolleary/pubsubclient)
- [ArduinoJson](https://arduinojson.org/)
- [Autonomous Agent Operations](https://github.com/tsayles/homelab/blob/main/hil-agentic-development/docs/architecture/autonomous-agent-operations.md)
- [Mock Driver Development Guide](https://github.com/tsayles/homelab/blob/main/hil-agentic-development/docs/guides/mock-driver-development.md)
- [HIL Development Instructions](https://github.com/tsayles/homelab/blob/main/hil-agentic-development/instructions/autonomous-hil-development.instructions.md)
