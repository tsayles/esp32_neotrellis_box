# Hardware Development Plan

> **Approach**: Agent-first, autonomous HIL development
> with SPICE simulation.
>
> **Parent requirements**:
> [PROJECT_SPEC.md](../PROJECT_SPEC.md) §2 (Hardware
> Requirements)
>
> **HIL reference**:
> [Autonomous Agent Operations](https://github.com/tsayles/homelab/blob/main/hil-agentic-development/docs/architecture/autonomous-agent-operations.md)

---

## 1. Architecture Overview

```
┌──────────────────────────────────────────┐
│        ESP32 NeoTrellis Box PCB          │
│                                          │
│  ┌──────────┐       ┌──────────────┐    │
│  │  ESP32   │◄─I2C─►│  NeoTrellis  │    │
│  │  Module  │       │  4x4 Keypad  │    │
│  └────┬─────┘       └──────────────┘    │
│       │                                  │
│  ┌────┴──────────────────────────────┐  │
│  │        Power Management           │  │
│  │  USB-C ─► TP4056 ─► 18650 Cell   │  │
│  │              │                     │  │
│  │         3.3 V LDO ─► ESP32 + NT  │  │
│  └───────────────────────────────────┘  │
│       │                                  │
│       ├─► WiFi Antenna (keep-out zone)   │
│       ├─► Battery voltage divider → ADC  │
│       └─► GPIO expansion header          │
└──────────────────────────────────────────┘
```

---

## 2. Agent-First Development Paradigm

### 2.1 How the Agent Drives Hardware Development

The autonomous agent owns every step that can be done in
software.  Human involvement is required only for
**physical actions** (soldering, measuring, flashing).

| Step | Owner | Notes |
|------|-------|-------|
| Schematic capture (KiCAD) | Agent | Generates netlist from requirements |
| SPICE simulation | Agent | Validates power circuits before layout |
| PCB layout & DRC | Agent | Iterates until DRC-clean |
| Gerber generation | Agent | Output to `hardware/gerbers/` |
| BOM generation | Agent | Output to `hardware/bom/` |
| Enclosure search | Agent | Scrapes Thingiverse, proposes candidates |
| **PCB ordering** | **Human** | Approves BOM + Gerbers, places order |
| **Assembly** | **Human** | Solders prototype |
| HIL bring-up tests | Agent + Human | Agent runs test firmware; human probes hardware |
| **Enclosure printing** | **Human** | Prints chosen STL |

### 2.2 Communication Protocol

- **Primary channel**: GitHub Pull Request on the
  `hardware/` feature branch.
- Agent posts structured status updates every 1–2 hours
  during autonomous operation.
- Escalation format per
  [HIL instructions](https://github.com/tsayles/homelab/blob/main/hil-agentic-development/instructions/autonomous-hil-development.instructions.md).

### 2.3 Session Lifecycle

```
Phase 1  ──►  Collaborative Setup & HW Verification
Phase 2  ──►  Human Disconnects — Agent Iterates
Phase 3  ──►  Bidirectional Communication via PR
Phase 4  ──►  Self-Management (Agent Autonomous)
Phase 5  ──►  Completion & Human Validation
```

---

## 3. Component Selection

### 3.1 Microcontroller

- **ESP32-WROOM-32** (or ESP32-DevKitC for prototyping).
- Dual-core 240 MHz, 520 KB SRAM, WiFi + BLE.
- REQ-HW-010.

### 3.2 Input Device

- **Adafruit NeoTrellis 4x4** (product #3954).
- 16 RGB keys, I2C seesaw protocol, default address
  `0x2E`.
- REQ-HW-020.

### 3.3 Battery & Power Management

- **18650 Li-ion cell** — 3 000–3 500 mAh, flat-top,
  unprotected (protection provided by PCB).
- **TP4056 charge controller** (or DW01A + FS8205A
  protection IC combo) — 1 A charge rate from USB 5 V.
- **3.3 V LDO** (e.g. AMS1117-3.3 or MCP1700-3302E)
  — powers ESP32 and NeoTrellis from battery or USB.
- **Power-path control** — P-channel MOSFET or
  load-sharing circuit for seamless USB / battery
  switchover.
- **Battery voltage sense** — resistor divider
  (100 kΩ / 100 kΩ) to ESP32 ADC pin for battery level
  monitoring (REQ-FW-080).
- REQ-HW-030, REQ-HW-031, REQ-HW-032.

### 3.4 Passive Components

| Component | Value | Purpose |
|-----------|-------|---------|
| R_I2C (×2) | 4.7 kΩ | I2C pull-ups |
| R_VBAT (×2) | 100 kΩ | Battery voltage divider |
| C_VCC | 100 µF + 100 nF | LDO input decoupling |
| C_3V3 | 10 µF + 100 nF | LDO output decoupling |

---

## 4. SPICE Simulation

SPICE simulation validates the power management
subsystem **before** committing to a PCB layout.  The
agent creates, runs, and iterates on simulations
autonomously.

### 4.1 Tool

- **ngspice** (open-source, CLI-driven — ideal for
  agent automation).
- Netlists stored in `hardware/spice/`.
- Simulation results (plots, logs) stored in
  `hardware/spice/results/`.

### 4.2 Simulations Required

| Simulation | Circuit | Key Measurements | Pass Criteria |
|------------|---------|------------------|---------------|
| SIM-01: LDO regulation | AMS1117-3.3 + load | Output voltage vs. load current (0–1 A) | 3.3 V ± 5 % across full load |
| SIM-02: TP4056 charge profile | TP4056 + 18650 model | Charge current vs. time, cell voltage ramp | CC @ 1 A → CV @ 4.2 V, terminates < 100 mA |
| SIM-03: Battery discharge | 18650 + LDO + ESP32 load | Runtime estimate, LDO dropout point | ≥ 3 h @ typical load (see REQ-HW-032) |
| SIM-04: USB–battery switchover | Power-path MOSFET circuit | Voltage glitch at switchover | Output glitch < 100 mV, < 10 ms |
| SIM-05: Battery voltage divider | Divider + ESP32 ADC model | ADC input voltage vs. cell voltage | Linear mapping 3.0–4.2 V → 1.5–2.1 V |
| SIM-06: I2C pull-up timing | 4.7 kΩ + bus capacitance | Rise / fall time at 400 kHz | Rise time < 300 ns for 50 pF bus |

### 4.3 Agent Workflow for SPICE

1. Agent creates ngspice netlist from component values.
2. Agent runs simulation:
   `ngspice -b -o results.log netlist.cir`
3. Agent parses output, compares against pass criteria.
4. On **pass** → commit netlist + results, proceed.
5. On **fail** → adjust component values, re-simulate,
   iterate until converged or escalate.
6. Simulation artifacts committed alongside schematic.

---

## 5. PCB Design

### 5.1 Tool & Files

- **KiCAD 7.0+**
- Project files: `hardware/kicad/`
- Custom symbols: `hardware/kicad/symbols/`
- Custom footprints: `hardware/kicad/footprints/`
- 3D models: `hardware/kicad/3dmodels/`

### 5.2 Design Rules

| Parameter | Value |
|-----------|-------|
| Layers | 2 |
| Min trace width | 0.25 mm (signal), 0.5 mm (power) |
| Min via diameter | 0.8 mm |
| Copper weight | 1 oz |
| Board outline | TBD — sized to enclosure |

### 5.3 Layout Considerations

- WiFi antenna keep-out zone (≥ 10 mm clearance).
- Decoupling caps adjacent to IC power pins.
- I2C traces routed together, length < 30 cm.
- Mounting holes matching NeoTrellis + enclosure.
- Separate high-current charge path from signal traces.

---

## 6. Pin Mapping

*Finalise during schematic capture.*

| ESP32 Pin | Function | Connection |
|-----------|----------|------------|
| GPIO21 | SDA | I2C Data (NeoTrellis) |
| GPIO22 | SCL | I2C Clock (NeoTrellis) |
| GPIO34 | ADC1_CH6 | Battery voltage sense |
| 3.3 V | Power | VCC rail |
| GND | Ground | GND rail |

---

## 7. Enclosure

### 7.1 Approach

Search [Thingiverse](https://www.thingiverse.com/) for
an existing NeoTrellis or 4×4 keypad enclosure and adapt
to fit this project's PCB and 18650 cell.

### 7.2 Agent Enclosure Search Workflow

1. Agent searches Thingiverse using keywords:
   `NeoTrellis`, `4x4 keypad enclosure`,
   `ESP32 button box`, `elastomer keypad case`.
2. Agent evaluates candidate dimensions against:
   - NeoTrellis 4×4 board (~56 × 56 mm).
   - Custom PCB (dimensions from KiCAD).
   - 18650 cell holder (~20 × 70 mm).
   - USB Type-C port access.
3. Agent posts top candidates on PR with links and
   dimensional analysis.
4. Human selects preferred design.
5. Agent downloads and adapts (FreeCAD / OpenSCAD).
6. Output: STL → `enclosure/3d-print/`,
   DXF → `enclosure/laser-cut/`.

---

## 8. Bill of Materials

*Generated from KiCAD during schematic capture.*

Preliminary BOM:

| Qty | Part | Description | Source |
|-----|------|-------------|--------|
| 1 | ESP32-WROOM-32 | Microcontroller module | Mouser / DigiKey |
| 1 | Adafruit 3954 | NeoTrellis 4x4 RGB Keypad | Adafruit |
| 1 | TP4056 module | Li-ion charge controller | Amazon / AliExpress |
| 1 | AMS1117-3.3 | 3.3 V LDO regulator | Mouser |
| 1 | 18650 cell | 3 000+ mAh Li-ion battery | Amazon |
| 1 | 18650 holder | PCB-mount or spring clip | Amazon |
| 1 | USB-C connector | 6-pin power-only | LCSC |
| 2 | 4.7 kΩ 0603 | I2C pull-up resistors | — |
| 2 | 100 kΩ 0603 | Battery voltage divider | — |
| — | Capacitors | See §3.4 | — |
| 1 | PCB | 2-layer, fabricated | JLCPCB / OSH Park |

---

## 9. Development Phases

### Phase 1 — Collaborative Setup (Human + Agent)

- [ ] Human and agent review requirements and agree on
      component selection.
- [ ] Agent verifies tool availability (KiCAD, ngspice,
      Python, `gh` CLI).
- [ ] Agent creates feature branch and opens **draft PR**.
- [ ] Define autonomous operation parameters:
  - Update cadence (every 2 hours).
  - Escalation thresholds.

### Phase 2 — Schematic Capture (Agent — Autonomous)

- [ ] Create KiCAD project and schematic
  - ESP32 module symbol and connections
  - NeoTrellis I2C interface
  - TP4056 charge circuit
  - 3.3 V LDO regulation
  - Battery voltage divider
  - USB Type-C power input
  - Power-path switchover MOSFET
- [ ] Run ERC (Electrical Rules Check) — iterate until
      zero errors.
- [ ] Post schematic review on PR, tag human.

### Phase 3 — SPICE Simulation (Agent — Autonomous)

- [ ] Create ngspice netlists for SIM-01 through SIM-06
      (see §4.2).
- [ ] Run each simulation; iterate on component values
      until all pass.
- [ ] Commit netlists + results to `hardware/spice/`.
- [ ] Post simulation summary on PR with pass/fail
      table.
- [ ] **Gate**: All simulations pass before proceeding to
      PCB layout.

### Phase 4 — PCB Layout (Agent — Autonomous)

- [ ] Assign footprints to all components.
- [ ] Define board outline (matched to enclosure
      candidate dimensions).
- [ ] Place components; route traces.
- [ ] Run DRC — iterate until zero errors.
- [ ] Generate Gerber files → `hardware/gerbers/`.
- [ ] Generate BOM → `hardware/bom/`.
- [ ] Post layout screenshots and DRC report on PR.

### Phase 5 — Enclosure Sourcing (Agent — Autonomous)

- [ ] Search Thingiverse for candidate enclosures.
- [ ] Evaluate dimensional fit (PCB + 18650 + NeoTrellis).
- [ ] Post top 3 candidates on PR with links and
      analysis.
- [ ] **Human selects** preferred enclosure design.
- [ ] Agent downloads and adapts design to final PCB
      dimensions.
- [ ] Export STL / DXF to `enclosure/`.

### Phase 6 — Prototype Fabrication (Human — Physical)

- [ ] Human reviews and approves Gerbers + BOM on PR.
- [ ] Order PCBs (JLCPCB or OSH Park).
- [ ] Order components per BOM.
- [ ] Solder and assemble prototype.
- [ ] Print enclosure.

### Phase 7 — HIL Bring-Up & Validation (Agent + Human)

This phase follows the HIL paradigm: agent runs
automated tests on the physical prototype connected to
the lab workstation (ESP32 via USB serial).

#### 7.1 Hardware Verification Checklist

Before autonomous testing begins:

- [ ] ESP32 board connected via USB and detected
      (`/dev/ttyUSB0` or `/dev/ttyACM0`).
- [ ] NeoTrellis I2C bus scan returns `0x2E`.
- [ ] Multimeter confirms 3.3 V rail within spec.
- [ ] Battery installed and charging indicator active.
- [ ] `gh` CLI authenticated; PR accessible.

#### 7.2 Autonomous HIL Test Execution

Agent runs the hardware test suite (§10) iteratively:

1. Flash test firmware to ESP32 via PlatformIO.
2. Execute each test over serial/MQTT.
3. Capture results; commit as test artifacts.
4. **Pass** → mark test complete, continue.
5. **Fail** → analyse, adjust firmware/configuration,
   re-test (up to 5 retries).
6. **Escalate** if hardware intervention needed (e.g.
   probe a voltage, press a button, reconnect a cable).

#### 7.3 Post-HIL Actions

- [ ] Agent posts full test report on PR.
- [ ] Agent documents errata and revision notes.
- [ ] If significant issues → revise schematic, re-run
      SPICE, produce Rev B.
- [ ] Human performs final physical validation.

---

## 10. Hardware Test Plan

*Maps to PROJECT_SPEC.md §7.1.*

| ID | Test | Method | Pass Criteria |
|----|------|--------|---------------|
| HW-T01 | Power rail voltages | Multimeter (human) + ADC (agent) | 3.3 V ± 5 % on LDO output |
| HW-T02 | USB charging | Multimeter + ammeter | TP4056 charges at ≤ 1 A; LED status correct |
| HW-T03 | Battery switchover | Disconnect USB during operation | Device continues seamlessly |
| HW-T04 | I2C bus scan | Agent runs scan firmware | NeoTrellis at 0x2E |
| HW-T05 | Button registration | Agent test firmware + human presses | All 16 buttons report events |
| HW-T06 | LED accuracy | Agent sets colours; human inspects | Correct colours per status table |
| HW-T07 | Battery ADC | Agent reads ADC; human reads multimeter | ± 50 mV accuracy |
| HW-T08 | Thermal | IR thermometer after 1 h (human) | No component > 60 °C |
| HW-T09 | 48 h soak | Agent monitors serial + MQTT | No crashes, no brownouts |

### Graceful Degradation

| Failure Scenario | Agent Response |
|------------------|----------------|
| ESP32 unresponsive | Re-flash firmware, power cycle, escalate |
| NeoTrellis not on bus | Check connections, escalate for re-seat |
| Battery not charging | Verify USB power, escalate for hardware check |
| Serial port lost | Attempt reconnect, escalate after 3 retries |
| Test fails 5× consecutive | Pause live tests, escalate, continue mock work |

---

## 11. References

- [TP4056 Datasheet (PDF)](https://dlnmh9ip6v2uc.cloudfront.net/datasheets/Prototyping/TP4056.pdf)
- [AMS1117-3.3 Datasheet](https://www.advanced-monolithic.com/pdf/ds1117.pdf)
- [KiCAD 7 Documentation](https://docs.kicad.org/)
- [ngspice Manual](https://ngspice.sourceforge.io/docs.html)
- [Adafruit NeoTrellis Learn Guide](https://learn.adafruit.com/adafruit-neotrellis)
- [ESP32-WROOM-32 Datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-wroom-32_datasheet_en.pdf)
- [Autonomous Agent Operations](https://github.com/tsayles/homelab/blob/main/hil-agentic-development/docs/architecture/autonomous-agent-operations.md)
