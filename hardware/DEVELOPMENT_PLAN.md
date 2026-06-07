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
│  ┌──────────┐  JST-PH ┌──────────────┐ │
│  │  ESP32   │◄──I2C──►│  NeoTrellis  │ │
│  │  Module  │         │  4x4 Keypad  │ │
│  └────┬─────┘         └──────────────┘ │
│       │                                  │
│  ┌────┴──────────────────────────────┐  │
│  │        Power Management           │  │
│  │  USB-C ──┐                        │  │
│  │          ├─► TP4056 ─► 18650 Cell │  │
│  │  12 V ───┤      │                 │  │
│  │  Barrel  └► 5 V Step-Down         │  │
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

- **ESP32-C3 Super Mini**.
- Single-core RISC-V @ 160 MHz, 400 KB SRAM, 4 MB flash,
  WiFi 802.11 b/g/n, BLE 5.0, native USB-C.
- REQ-HW-010.

### 3.2 Input Device

- **Adafruit NeoTrellis 4x4** (product #3954).
- 16 RGB keys, I2C seesaw protocol, default address
  `0x2E`.
- Connected to PCB via 4 Pin JST-PH 2 mm cable
  ([Adafruit #3568](https://www.adafruit.com/product/3568)).
- REQ-HW-020.

### 3.3 Power Management

- **18650 Li-ion cell** — 3 000–3 500 mAh, flat-top,
  unprotected (protection provided by PCB).
- **TP4056 charge controller** (or DW01A + FS8205A
  protection IC combo) — 1 A charge rate from USB 5 V
  or regulated 5 V from 12 V input.
- **12 V → 5 V step-down regulator** (e.g. MP1584EN
  or LM2596) — accepts 12 V DC barrel jack input,
  feeds TP4056 and 5 V rail.
- **12 V barrel jack** — 5.5 × 2.1 mm DC barrel
  connector with Schottky diode reverse-polarity
  protection.
- **3.3 V LDO** (e.g. AMS1117-3.3 or MCP1700-3302E)
  — powers ESP32 and NeoTrellis from battery, USB,
  or 12 V input.
- **Power-path control** — P-channel MOSFET or
  load-sharing circuit for seamless switchover between
  USB, 12 V, and battery.
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
| C_12V | 100 µF + 100 nF | 12 V input decoupling |
| C_5V | 22 µF + 100 nF | Step-down output decoupling |
| D_RPP | SS34 Schottky | Reverse-polarity protection |

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
| SIM-03: Battery discharge | 18650 + LDO + ESP32 load | Runtime estimate, LDO dropout point | ≥ 3 months @ typical load with duty cycling (see REQ-HW-032) |
| SIM-04: USB–battery switchover | Power-path MOSFET circuit | Voltage glitch at switchover | Output glitch < 100 mV, < 10 ms |
| SIM-05: Battery voltage divider | Divider + ESP32 ADC model | ADC input voltage vs. cell voltage | Linear mapping 3.0–4.2 V → 1.5–2.1 V |
| SIM-06: I2C pull-up timing | 4.7 kΩ + bus capacitance | Rise / fall time at 400 kHz | Rise time < 300 ns for 50 pF bus |
| SIM-07: 12 V step-down | MP1584EN + load | Output voltage vs. load (0–1.5 A) | 5.0 V ± 3 % across full load, ripple < 50 mV |
| SIM-08: 12 V reverse-polarity | Schottky protection + load | Current flow under reversed input | Zero current to circuit; diode clamps voltage |

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

## 5. Enclosure ↔ PCB Co-Design

The enclosure and PCB are designed together in an
**iterative convergence loop**.  The enclosure is
selected first (Thingiverse search), then the PCB is
designed to fit inside it.  If the PCB cannot fit, the
enclosure choice is revisited, and the loop repeats.

### 5.1 Convergence Loop

```
  ┌───────────────────────────────────────────┐
  │  1. Search Thingiverse for enclosures     │
  │  2. Extract internal dimensions &         │
  │     mounting constraints                  │
  │  3. Define PCB board outline to fit       │
  └──────────────────┬────────────────────────┘
                     ▼
  ┌───────────────────────────────────────────┐
  │  4. Place components; route PCB           │
  │  5. Run DRC                               │
  └──────────────────┬────────────────────────┘
                     ▼
              ┌──────────────┐
              │  PCB fits    │──► YES ──► Done
              │  enclosure?  │
              └──────┬───────┘
                     │ NO
                     ▼
              ┌──────────────┐
              │ Can enclosure│──► YES ──► Adapt
              │ be adapted?  │           enclosure
              └──────┬───────┘           & retry
                     │ NO
                     ▼
              Select next enclosure
              candidate & retry
```

### 5.2 Enclosure-First Search (Agent — Autonomous)

1. Agent searches
   [Thingiverse](https://www.thingiverse.com/) using
   keywords: `NeoTrellis`, `4x4 keypad enclosure`,
   `ESP32 button box`, `elastomer keypad case`.
2. Agent evaluates candidates against:
   - NeoTrellis 4×4 board (~56 × 56 mm).
   - 18650 cell holder (~20 × 70 mm).
   - USB Type-C port access.
   - 12 V DC barrel jack access.
   - Wall-mount option (preferred).
3. Agent ranks top 3 candidates by fit, posts on PR
   with links, internal dimensions, and mounting
   analysis.
4. **Human selects** preferred enclosure (or agent
   proceeds with best-ranked if human defers).
5. Agent extracts:
   - Maximum PCB X × Y dimensions.
   - Board-edge keep-out zones.
   - Standoff / mounting hole positions.
   - Connector opening locations.

### 5.3 PCB Layout to Enclosure (Agent — Autonomous)

1. Agent sets KiCAD board outline from enclosure
   internal dimensions.
2. Agent places mounting holes to match enclosure
   standoffs.
3. Agent positions USB-C and 12 V barrel connectors
   aligned with enclosure openings.
4. Agent places components and routes traces within
   the constrained outline.
5. Agent runs DRC — iterates until zero errors.

### 5.4 Fit Verification

After each layout iteration the agent checks:

| Check | Method | Action on Fail |
|-------|--------|----------------|
| Board fits enclosure X × Y | Compare outline vs. enclosure dims | Re-place components or try next enclosure |
| Max component height | Check 3D model clearance | Swap to lower-profile part or adapt enclosure lid |
| Mounting holes align | Overlay PCB on enclosure model | Adjust board outline or hole positions |
| USB-C aligns with opening | Compare connector position | Shift board or modify enclosure cutout |
| 12 V barrel aligns with opening | Compare connector position | Shift board or modify enclosure cutout |
| 18650 holder clears PCB | Check 3D interference | Relocate holder or adapt enclosure depth |
| WiFi antenna not blocked | Verify keep-out in enclosure | Reposition ESP32 or adjust enclosure material/shape |

### 5.5 Enclosure Adaptation

If the selected enclosure requires modification:

- Agent downloads source files (SCAD / STEP / STL).
- Agent modifies in FreeCAD or OpenSCAD:
  - Adjust internal dimensions.
  - Add / move standoff bosses.
  - Modify connector cutouts.
  - Add 18650 compartment if missing.
- Agent exports modified STL → `enclosure/3d-print/`.
- Agent posts before/after dimensional comparison on PR.

### 5.6 Convergence Criteria

The loop exits when **all** of the following are true:

- [ ] PCB outline fits within enclosure internal dims
      with ≥ 0.5 mm clearance on all sides.
- [ ] All mounting holes align with enclosure standoffs.
- [ ] USB-C connector centred on enclosure opening.
- [ ] 12 V barrel jack centred on enclosure opening.
- [ ] 18650 cell holder fits without interference.
- [ ] WiFi antenna has clear path (no metal/dense
      plastic obstruction).
- [ ] DRC passes with zero errors.
- [ ] 3D model assembly shows no collisions.

---

## 6. PCB Design Details

### 6.1 Tool & Files

- **KiCAD 7.0+**
- Project files: `hardware/kicad/`
- Custom symbols: `hardware/kicad/symbols/`
- Custom footprints: `hardware/kicad/footprints/`
- 3D models: `hardware/kicad/3dmodels/`

### 6.2 Design Rules

| Parameter | Value |
|-----------|-------|
| Layers | 2 or 4 (per spec REQ-HW-040) |
| Min trace width | 0.25 mm (signal), 0.5 mm (power) |
| Min via diameter | 0.8 mm |
| Copper weight | 1 oz |
| Board outline | Derived from enclosure internal dims (§5) |

### 6.3 Layout Considerations

- WiFi antenna keep-out zone (≥ 10 mm clearance).
- Decoupling caps adjacent to IC power pins.
- I2C traces routed together, length < 30 cm.
- Mounting holes matching NeoTrellis + enclosure.
- Separate high-current charge path from signal traces.
- 12 V power traces: wide (≥ 1 mm) with dedicated
  ground return.
- Barrel jack and USB-C placed on same PCB edge where
  possible for enclosure cutout simplicity.

---

## 7. Pin Mapping

*Finalise during schematic capture.*

| ESP32-C3 Pin | Function | Connection |
|--------------|----------|------------|
| GPIO0  | SDA      | I2C Data (NeoTrellis) |
| GPIO10 | SCL      | I2C Clock (NeoTrellis) |
| GPIO3  | ADC1_CH3 | Battery voltage sense |
| 3.3 V  | Power    | VCC rail |
| GND    | Ground   | GND rail |

> GPIO8 and GPIO9 are strapping pins; use GPIO0 / GPIO10 for
> I2C to avoid boot-mode interference.

---

---

## 8. Bill of Materials

*Generated from KiCAD during schematic capture.*

Preliminary BOM:

| Qty | Part | Description | Source |
|-----|------|-------------|--------|
| 1 | ESP32-C3 Super Mini | Microcontroller module | AliExpress / Amazon |
| 1 | Adafruit 3954 | NeoTrellis 4x4 RGB Keypad | Adafruit |
| 1 | TP4056 module | Li-ion charge controller | Amazon / AliExpress |
| 1 | AMS1117-3.3 | 3.3 V LDO regulator | Mouser |
| 1 | 18650 cell | 3 000+ mAh Li-ion battery | Amazon |
| 1 | 18650 holder | PCB-mount or spring clip | Amazon |
| 1 | USB-C connector | 6-pin power-only | LCSC |
| 1 | DC barrel jack | 5.5 × 2.1 mm, PCB-mount | LCSC |
| 1 | MP1584EN module | 12 V → 5 V step-down regulator | Amazon / AliExpress |
| 1 | SS34 Schottky | Reverse-polarity protection | Mouser |
| 1 | JST-PH 4-pin header | NeoTrellis I2C cable connector | Adafruit / LCSC |
| 1 | JST-PH 4-pin cable | Female/female 150 mm | Adafruit #3568 |
| 2 | 4.7 kΩ 0603 | I2C pull-up resistors | — |
| 2 | 100 kΩ 0603 | Battery voltage divider | — |
| — | Capacitors | See §3.4 | — |
| 1 | PCB | 2 or 4-layer, fabricated | JLCPCB / OSH Park |

---

## 9. Development Phases

### Phase 1 — Collaborative Setup (Human + Agent)

- [x] Human and agent review requirements and agree on
      component selection (ESP32-C3 Super Mini confirmed,
      see PROJECT_SPEC.md §2.1 v2.2).
- [x] Agent verifies tool availability: KiCAD 7.0.11,
      ngspice 42, Python 3.12, gh 2.45 — all present.
- [x] Agent creates feature branch `dev/hardware-phase-1-2`
      and opens **draft PR**.
- [x] Autonomous operation parameters defined:
  - Update cadence: every ~2 hours via PR comments.
  - Escalation: on tool failure, ERC errors > 5 iter,
    or any step requiring physical action.

### Phase 2 — Schematic Capture (Agent — Autonomous)

- [x] Create KiCAD project and schematic
  - ESP32-C3 Super Mini symbol and connections
  - NeoTrellis I2C interface (JST-PH header)
  - TP4056 charge circuit
  - 12 V DC barrel jack input
  - 12 V → 5 V step-down regulator (MP1584EN)
  - Reverse-polarity protection (SS34 Schottky)
  - 3.3 V LDO regulation (AMS1117-3.3)
  - Battery voltage divider (ADC on GPIO3)
  - USB Type-C power input
  - Power-path switchover MOSFET (AO3401A)
- [x] Schematic validated by `kicad-cli sch export netlist`.
      All 7 key nets verified correct (+3V3, +5V, GND,
      VBATT, SDA, SCL, BATT_ADC). 13 expected unconnected
      pins (unused GPIOs, TP4056 LED pins) correct.
- [x] Post schematic review on PR, @-tag human for review.

> **Schematic files**: `hardware/kicad/`
> **Generator script**: `hardware/kicad/scripts/generate_schematic.py`
> **Note**: KiCAD 7 CLI has no `sch erc` command; netlist
> export used for structural validation.

### Phase 3 — SPICE Simulation (Agent — Autonomous)

- [ ] Create ngspice netlists for SIM-01 through SIM-08
      (see §4.2).
- [ ] Run each simulation; iterate on component values
      until all pass.
- [ ] Commit netlists + results to `hardware/spice/`.
- [ ] Post simulation summary on PR with pass/fail
      table.
- [ ] **Gate**: All simulations pass before proceeding to
      PCB layout.

### Phase 4 — Enclosure ↔ PCB Co-Design (Agent — Autonomous)

This phase implements the convergence loop described in
§5.  Enclosure selection drives the PCB board outline;
the two iterate until both fit.

- [ ] **4a — Enclosure search**: Search Thingiverse for
      candidate enclosures (see §5.2).
- [ ] **4b — Rank & propose**: Post top 3 candidates on
      PR with internal dimensions and fitment analysis.
- [ ] **4c — Human selects** preferred enclosure (or
      agent proceeds with best-ranked).
- [ ] **4d — Extract constraints**: Board outline,
      mounting holes, connector openings from enclosure.
- [ ] **4e — PCB layout**: Set board outline in KiCAD;
      place components; route traces (see §6).
- [ ] **4f — DRC**: Run Design Rules Check — iterate
      until zero errors.
- [ ] **4g — Fit check**: Verify PCB fits enclosure per
      §5.4 checks.
- [ ] **4h — Iterate**: If fit check fails:
  - Attempt enclosure adaptation (§5.5), **or**
  - Select next enclosure candidate and repeat from 4d.
- [ ] **4i — Convergence**: All §5.6 criteria met.
- [ ] **4j — Generate outputs**:
  - Gerber files → `hardware/gerbers/`.
  - BOM → `hardware/bom/`.
  - Adapted enclosure STL → `enclosure/3d-print/`.
- [ ] Post final layout + enclosure report on PR.

### Phase 5 — Prototype Fabrication (Human — Physical)

- [ ] Human reviews and approves Gerbers + BOM on PR.
- [ ] Order PCBs (JLCPCB or OSH Park).
- [ ] Order components per BOM.
- [ ] Solder and assemble prototype.
- [ ] Print enclosure.

### Phase 6 — HIL Bring-Up & Validation (Agent + Human)

This phase follows the HIL paradigm: agent runs
automated tests on the physical prototype connected to
the lab workstation (ESP32 via USB serial).

#### 6.1 Hardware Verification Checklist

Before autonomous testing begins:

- [ ] ESP32 board connected via USB and detected
      (`/dev/ttyUSB0` or `/dev/ttyACM0`).
- [ ] NeoTrellis I2C bus scan returns `0x2E`.
- [ ] Multimeter confirms 3.3 V rail within spec.
- [ ] Battery installed and charging indicator active.
- [ ] `gh` CLI authenticated; PR accessible.

#### 6.2 Autonomous HIL Test Execution

Agent runs the hardware test suite (§10) iteratively:

1. Flash test firmware to ESP32 via PlatformIO.
2. Execute each test over serial/MQTT.
3. Capture results; commit as test artifacts.
4. **Pass** → mark test complete, continue.
5. **Fail** → analyse, adjust firmware/configuration,
   re-test (up to 5 retries).
6. **Escalate** if hardware intervention needed (e.g.
   probe a voltage, press a button, reconnect a cable).

#### 6.3 Post-HIL Actions

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
| HW-T01 | Power rail voltages | Multimeter (human) + ADC (agent) | 3.3 V ± 5 % on LDO; 5 V ± 3 % from step-down |
| HW-T02 | USB charging | Multimeter + ammeter | TP4056 charges at ≤ 1 A; LED status correct |
| HW-T03 | 12 V charging | Multimeter + ammeter | Step-down outputs 5 V; TP4056 charges from 12 V input |
| HW-T04 | 12 V reverse-polarity | Apply reversed 12 V; check current | Zero current to circuit; no component damage |
| HW-T05 | Power-path switchover | Disconnect/reconnect USB, 12 V, battery during operation | Device continues seamlessly across all transitions |
| HW-T06 | I2C bus scan | Agent runs scan firmware | NeoTrellis at 0x2E |
| HW-T07 | Button registration | Agent test firmware + human presses | All 16 buttons report events |
| HW-T08 | LED accuracy | Agent sets colours; human inspects | Correct colours per status table |
| HW-T09 | Battery ADC | Agent reads ADC; human reads multimeter | ± 50 mV accuracy |
| HW-T10 | Thermal | IR thermometer after 1 h (human) | No component > 60 °C (incl. 12 V regulator) |
| HW-T11 | 48 h soak | Agent monitors serial + MQTT | No crashes, no brownouts |

### Graceful Degradation

| Failure Scenario | Agent Response |
|------------------|----------------|
| ESP32 unresponsive | Re-flash firmware, power cycle, escalate |
| NeoTrellis not on bus | Check connections, escalate for re-seat |
| Battery not charging | Verify USB and 12 V power, escalate for hardware check |
| Serial port lost | Attempt reconnect, escalate after 3 retries |
| Test fails 5× consecutive | Pause live tests, escalate, continue mock work |

---

## 11. References

- [TP4056 Datasheet (PDF)](https://dlnmh9ip6v2uc.cloudfront.net/datasheets/Prototyping/TP4056.pdf)
- [AMS1117-3.3 Datasheet](https://www.advanced-monolithic.com/pdf/ds1117.pdf)
- [KiCAD 7 Documentation](https://docs.kicad.org/)
- [ngspice Manual](https://ngspice.sourceforge.io/docs.html)
- [Adafruit NeoTrellis Learn Guide](https://learn.adafruit.com/adafruit-neotrellis)
- [ESP32-C3 Datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf)
- [STEMMA Cable - JST-PH 4-pin](https://www.adafruit.com/product/3568)
- [Autonomous Agent Operations](https://github.com/tsayles/homelab/blob/main/hil-agentic-development/docs/architecture/autonomous-agent-operations.md)
