# Hardware Design

This directory contains all hardware design files for the
ESP32 NeoTrellis Box.

## Directory Structure

```
hardware/
├── kicad/              KiCAD project files
│   ├── symbols/        Custom schematic symbols
│   ├── footprints/     Custom PCB footprints
│   └── 3dmodels/       3D component models
├── bom/                Bill of Materials
├── gerbers/            Manufacturing output files
└── datasheets/         Component datasheets and links
```

## Tools Required

- **KiCAD 7.0+** — schematic capture and PCB layout
- See [PROJECT_SPEC.md](../PROJECT_SPEC.md) §2.3 for PCB
  design specifications.

## Key Design Considerations

- 2-layer PCB
- I2C pull-up resistors (4.7 kΩ)
- Decoupling capacitors for stable power delivery
- RF clearance for ESP32-C3 Super Mini WiFi antenna
- ESD protection on exposed connectors

## Pin Mapping

| ESP32-C3 Pin | Function       | NeoTrellis Connection |
|--------------|----------------|-----------------------|
| GPIO8        | SDA            | I2C Data              |
| GPIO9        | SCL            | I2C Clock             |
| GPIO3        | ADC1_CH3       | Battery voltage sense |
| 3.3 V        | Power          | VCC                   |
| GND          | Ground         | GND                   |

## ESP32-C3 Super Mini — Breadboard Pinout

Pin positions with USB-C connector at the top.  The module
bridges the centre gap of a standard 830-point breadboard,
leaving **one column free on each side** for jumper wires.

```
              ┌─────[USB-C]─────┐
              │  ESP32-C3       │
              │   Super Mini    │
       3V3  ──┤ L1           R1 ├──  GND
        EN  ──┤ L2           R2 ├──  GPIO10
     GPIO4  ──┤ L3           R3 ├──  GPIO3   (ADC — battery sense)
     GPIO5  ──┤ L4           R4 ├──  GPIO2   (ADC)
     GPIO6  ──┤ L5           R5 ├──  GPIO1   (UART TX)
     GPIO7  ──┤ L6           R6 ├──  GPIO0   (UART RX)
  GPIO8/SDA ──┤ L7           R7 ├──  GPIO9/SCL
       GND  ──┤ L8           R8 ├──  5V
              └─────────────────┘
```

### Breadboard Layout (top view)

```
  col:  a   b   c   d   e ║ f   g   h   i   j
        ·   ·   ·   ·   · ║ ·   ·   ·   ·   ·   ← free rows (above module)
        ·  ┌─────────────────────────────┐  ·
3V3     ·  │L1        USB-C         R1  │  ·   GND
EN      ·  │L2                      R2  │  ·   GPIO10
GPIO4   ·  │L3                      R3  │  ·   GPIO3
GPIO5   ·  │L4                      R4  │  ·   GPIO2
GPIO6   ·  │L5                      R5  │  ·   GPIO1/TX
GPIO7   ·  │L6                      R6  │  ·   GPIO0/RX
SDA/8   ·  │L7                      R7  │  ·   GPIO9/SCL
GND     ·  │L8                      R8  │  ·   5V
        ·  └─────────────────────────────┘  ·
        ·   ·   ·   ·   · ║ ·   ·   ·   ·   ·   ← free rows (below module)
```

- Left-side pins land in **column b**; right-side pins in **column i**.
- Columns **a** and **j** remain free for jumper wires.

### NeoTrellis I2C Wiring (Breadboard Prototype)

| NeoTrellis Pin | Colour | ESP32-C3 Pin           |
|----------------|--------|------------------------|
| SDA            | Blue   | GPIO8 — L7, column b   |
| SCL            | Yellow | GPIO9 — R7, column i   |
| VCC            | Red    | 3V3  — L1, column b    |
| GND            | Black  | GND  — R1, column i    |
