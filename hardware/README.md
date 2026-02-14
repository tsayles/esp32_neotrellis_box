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
- RF clearance for ESP32 WiFi antenna
- ESD protection on exposed connectors

## Pin Mapping

| ESP32 Pin | Function | NeoTrellis Connection |
|-----------|----------|----------------------|
| GPIO21    | SDA      | I2C Data             |
| GPIO22    | SCL      | I2C Clock            |
| 3.3V      | Power    | VCC                  |
| GND       | Ground   | GND                  |
