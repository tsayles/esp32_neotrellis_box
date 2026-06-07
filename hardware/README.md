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

| ESP32-C3 Pin | Function       | Connection            | Notes                        |
|--------------|----------------|-----------------------|------------------------------|
| GPIO0        | SDA            | I2C Data (NeoTrellis) | ADC1_CH0; safe GPIO          |
| GPIO10       | SCL            | I2C Clock (NeoTrellis)| Safe GPIO                    |
| GPIO3        | ADC1_CH3       | Battery voltage sense | ADC1 only — works with WiFi  |
| 3V3          | Power          | NeoTrellis VCC        |                              |
| GND          | Ground         | NeoTrellis GND        |                              |

> **Note — I2C pins:** GPIO8 and GPIO9 are strapping pins on the
> ESP32-C3.  Attaching I2C pull-ups there can disturb the boot mode.
> GPIO0 and GPIO10 are the recommended safe alternatives.

> **Note — ADC2:** GPIO5 belongs to ADC2, which is unavailable
> when Wi-Fi is active.  Always use ADC1 pins (GPIO0–4) for
> analog measurements in this project.

## ESP32-C3 Super Mini — Breadboard Pinout

Pin positions with USB-C connector at the top.  The module
bridges the centre gap of a standard 830-point breadboard,
leaving **one column free on each side** for jumper wires.

```
              ┌─────[USB-C]─────┐
              │  ESP32-C3       │
              │   Super Mini    │
  GPIO21/TX ──┤ L1           R1 ├──  5V
  GPIO20/RX ──┤ L2           R2 ├──  GND
     GPIO10 ──┤ L3           R3 ├──  3V3
    GPIO9 ★ ──┤ L4           R4 ├──  GPIO4  (ADC1_CH4, RTC)
    GPIO8 ★ ──┤ L5           R5 ├──  GPIO3  (ADC1_CH3, RTC)  ← battery ADC
      GPIO7 ──┤ L6           R6 ├──  GPIO2  (ADC1_CH2, RTC, ★)
      GPIO6 ──┤ L7           R7 ├──  GPIO1  (ADC1_CH1, RTC)
      GPIO5 ──┤ L8           R8 ├──  GPIO0  (ADC1_CH0, RTC)  ← I2C SDA
              └─────────────────┘
  L3 GPIO10 ──────────────────────────────────────────────── I2C SCL

  ★  strapping pin — use with caution (affects boot mode)
```

### Breadboard Layout (top view)

Left-side pins occupy **column b**; right-side pins occupy **column i**.
Columns **a** and **j** remain free for jumper wires.

```
  col:  a   b   c   d   e ║ f   g   h   i   j
        ·   ·   ·   ·   · ║ ·   ·   ·   ·   ·   ← free rows (above)
        ·  ┌───────────────────────────────┐  ·
TX/21   ·  │L1        USB-C           R1  │  ·   5V
RX/20   ·  │L2                        R2  │  ·   GND
GPIO10  ·  │L3                        R3  │  ·   3V3
GPIO9 ★ ·  │L4                        R4  │  ·   GPIO4
GPIO8 ★ ·  │L5                        R5  │  ·   GPIO3 ← bat. ADC
GPIO7   ·  │L6                        R6  │  ·   GPIO2
GPIO6   ·  │L7                        R7  │  ·   GPIO1
GPIO5   ·  │L8                        R8  │  ·   GPIO0 ← SDA
        ·  └───────────────────────────────┘  ·
        ·   ·   ·   ·   · ║ ·   ·   ·   ·   ·   ← free rows (below)
```

### NeoTrellis I2C Wiring (Breadboard Prototype)

| NeoTrellis Pin | Colour | ESP32-C3 Pin                  |
|----------------|--------|-------------------------------|
| SDA            | Blue   | GPIO0 — R8, column i (bottom) |
| SCL            | Yellow | GPIO10 — L3, column b         |
| VCC            | Red    | 3V3  — R3, column i           |
| GND            | Black  | GND  — R2, column i           |
