#!/usr/bin/env python3
"""
ESP32 NeoTrellis Box — KiCAD 7 schematic generator (v3).

Strategy: Label-only connectivity.
Every pin endpoint gets exactly one of:
  - power symbol  (for +5V, +3V3, GND, +12V, VBATT nets)
  - net label     (for signal nets)
  - no_connect    (for intentionally unconnected pins)
No wires are placed. Coordinates are explicitly pre-computed.
"""
import json, re, uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
KICAD_DIR   = ROOT / "hardware" / "kicad"
SYM_DIR     = KICAD_DIR / "symbols"
SYS_SYM_DIR = Path("/usr/share/kicad/symbols")
PROJ        = "esp32_neotrellis_box"
SCH_UUID    = "4d8712f5-64b3-4f62-aa5c-d4181edabe64"

def uid(): return str(uuid.uuid4())

# Pin numbers for each component type (lib_id → list of pin numbers as strings)
PIN_NUMBERS = {
    "Custom:ESP32-C3-Super-Mini": [str(i) for i in range(1, 17)],
    "Custom:TP4056":              [str(i) for i in range(1, 9)],
    "Custom:MP1584EN":            [str(i) for i in range(1, 9)],
    "Connector_Generic:Conn_01x02": ["1", "2"],
    "Connector_Generic:Conn_01x04": ["1", "2", "3", "4"],
    "Device:Battery":             ["1", "2"],
    "Device:C":                   ["1", "2"],
    "Device:L":                   ["1", "2"],
    "Device:R":                   ["1", "2"],
    "Diode:SS34":                 ["A1", "A2"],
    "Regulator_Linear:AMS1117-3.3": ["1", "2", "3"],
    "Transistor_FET:AO3401A":     ["1", "2", "3"],
}

# ── Symbol extraction ─────────────────────────────────────────────────────────
def extract_sym(lib_path: Path, sym_name: str) -> str:
    """Return the raw (symbol "sym_name" ...) block from a .kicad_sym file."""
    text = lib_path.read_text()
    pat = f'(symbol "{sym_name}"'
    idx = text.find(pat)
    if idx < 0:
        raise ValueError(f"{sym_name} not found in {lib_path}")
    depth, i = 0, idx
    while i < len(text):
        if text[i] == '(':  depth += 1
        elif text[i] == ')':
            depth -= 1
            if depth == 0:
                return text[idx:i+1]
        i += 1
    raise ValueError(f"Unbalanced parens for {sym_name}")

def lib_sym(lib_name: str, sym_name: str, _seen=None) -> str:
    """Extract symbol from system lib for embedding in lib_symbols.

    For 'extends' symbols: inline parent geometry, rename to child name,
    override Value property. Sub-symbols keep base name (no lib: prefix).
    """
    if _seen is None:
        _seen = set()
    if sym_name in _seen:
        return ""
    _seen.add(sym_name)

    lib_path = SYS_SYM_DIR / f"{lib_name}.kicad_sym"
    text = lib_path.read_text()
    extends_m = re.search(
        r'\(symbol "' + re.escape(sym_name) + r'" \(extends "([^"]+)"', text)

    if extends_m:
        parent = extends_m.group(1)
        parent_block = extract_sym(lib_path, parent)
        child_block  = extract_sym(lib_path, sym_name)

        # Build resolved block from parent geometry, renaming to child
        resolved = parent_block
        # Rename parent sub-symbols (e.g. SB120_0_1 → SS34_0_1)
        resolved = re.sub(
            r'\(symbol "' + re.escape(parent) + r'(_\d+_\d+)"',
            f'(symbol "{sym_name}\\1"',
            resolved)
        # Rename top-level
        resolved = resolved.replace(
            f'(symbol "{parent}"', f'(symbol "{lib_name}:{sym_name}"', 1)
        # Override Value property with child's value (simple string replace)
        child_val = re.search(r'\(property "Value" "([^"]+)"', child_block)
        parent_val = re.search(r'\(property "Value" "([^"]+)"', resolved)
        if child_val and parent_val and child_val.group(1) != parent_val.group(1):
            resolved = resolved.replace(
                f'(property "Value" "{parent_val.group(1)}"',
                f'(property "Value" "{child_val.group(1)}"',
                1)
        return "\n" + resolved
    else:
        block = extract_sym(lib_path, sym_name)
        # Rename top-level only; sub-symbols keep their bare names (no lib: prefix)
        block = block.replace(f'(symbol "{sym_name}"', f'(symbol "{lib_name}:{sym_name}"', 1)
        return "\n" + block

# ── Schematic element builders ────────────────────────────────────────────────
_pwr_n = 0
def power(net: str, x: float, y: float) -> str:
    global _pwr_n
    _pwr_n += 1
    ref = f"#PWR{_pwr_n:03d}"
    # GND points down so value label goes below (higher y); others go above (lower y)
    vy = y + 3.81 if net == "GND" else y - 3.81
    return (
        f'  (symbol (lib_id "power:{net}") (at {x:.3f} {y:.3f} 0) (unit 1)\n'
        f'    (in_bom no) (on_board no) (dnp no)\n'
        f'    (uuid "{uid()}")\n'
        f'    (property "Reference" "{ref}" (at {x:.3f} {y+6.35:.3f} 0)\n'
        f'      (effects (font (size 1.27 1.27)) hide)\n    )\n'
        f'    (property "Value" "{net}" (at {x:.3f} {vy:.3f} 0)\n'
        f'      (effects (font (size 1.27 1.27)))\n    )\n'
        f'    (property "Footprint" "" (at {x:.3f} {y:.3f} 0)\n'
        f'      (effects (font (size 1.27 1.27)) hide)\n    )\n'
        f'    (property "Datasheet" "" (at {x:.3f} {y:.3f} 0)\n'
        f'      (effects (font (size 1.27 1.27)) hide)\n    )\n'
        f'    (pin "1" (uuid "{uid()}"))\n'
        f'    (instances\n      (project "{PROJ}"\n'
        f'        (path "/{SCH_UUID}"\n'
        f'          (reference "{ref}") (unit 1)\n'
        f'        )\n      )\n    )\n  )\n'
    )

def label(name: str, x: float, y: float, justify: str = "left") -> str:
    return (
        f'  (label "{name}" (at {x:.3f} {y:.3f} 0) (fields_autoplaced)\n'
        f'    (effects (font (size 1.27 1.27)) (justify {justify}))\n'
        f'    (uuid "{uid()}")\n  )\n'
    )

def nc(x: float, y: float) -> str:
    return f'  (no_connect (at {x:.3f} {y:.3f}) (uuid "{uid()}"))\n'

_comp_n = 0
def component(lib_id: str, ref: str, value: str,
              cx: float, cy: float, rotation: int = 0,
              footprint: str = "") -> str:
    global _comp_n
    _comp_n += 1
    pins = PIN_NUMBERS.get(lib_id, [])
    pin_lines = "".join(f'    (pin "{p}" (uuid "{uid()}"))\n' for p in pins)
    return (
        f'  (symbol (lib_id "{lib_id}") (at {cx:.3f} {cy:.3f} {rotation}) (unit 1)\n'
        f'    (in_bom yes) (on_board yes) (dnp no)\n'
        f'    (uuid "{uid()}")\n'
        f'    (property "Reference" "{ref}" (at {cx:.3f} {cy+6.35:.3f} 0)\n'
        f'      (effects (font (size 1.27 1.27)))\n    )\n'
        f'    (property "Value" "{value}" (at {cx:.3f} {cy-6.35:.3f} 0)\n'
        f'      (effects (font (size 1.27 1.27)))\n    )\n'
        f'    (property "Footprint" "{footprint}" (at {cx:.3f} {cy:.3f} 0)\n'
        f'      (effects (font (size 1.27 1.27)) hide)\n    )\n'
        f'    (property "Datasheet" "~" (at {cx:.3f} {cy:.3f} 0)\n'
        f'      (effects (font (size 1.27 1.27)) hide)\n    )\n'
        + pin_lines
        + f'    (instances\n      (project "{PROJ}"\n'
        f'        (path "/{SCH_UUID}"\n'
        f'          (reference "{ref}") (unit 1)\n'
        f'        )\n      )\n    )\n  )\n'
    )

# ── Custom symbols ────────────────────────────────────────────────────────────
CUSTOM_ESP32 = '''\
  (symbol "Custom:ESP32-C3-Super-Mini" (pin_names (offset 1.016)) (in_bom yes) (on_board yes)
    (property "Reference" "U" (id 0) (at 0 22.86 0) (effects (font (size 1.27 1.27))))
    (property "Value" "ESP32-C3-Super-Mini" (id 1) (at 0 -22.86 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "" (id 2) (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (id 3) (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
    (symbol "ESP32-C3-Super-Mini_0_1"
      (rectangle (start -12.7 20.32) (end 12.7 -20.32)
        (stroke (width 0.254) (type default)) (fill (type background)))
      (text "ESP32-C3" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
      (text "Super Mini" (at 0 0 0) (effects (font (size 1.016 1.016))))
    )
    (symbol "ESP32-C3-Super-Mini_1_1"
      (pin bidirectional line (at -15.24 17.78 0) (length 2.54)
        (name "GPIO21/TX" (effects (font (size 1.016 1.016)))) (number "1" (effects (font (size 1.016 1.016)))))
      (pin bidirectional line (at -15.24 12.70 0) (length 2.54)
        (name "GPIO20/RX" (effects (font (size 1.016 1.016)))) (number "2" (effects (font (size 1.016 1.016)))))
      (pin bidirectional line (at -15.24 7.62 0) (length 2.54)
        (name "GPIO10" (effects (font (size 1.016 1.016)))) (number "3" (effects (font (size 1.016 1.016)))))
      (pin bidirectional line (at -15.24 2.54 0) (length 2.54)
        (name "GPIO9/BOOT" (effects (font (size 1.016 1.016)))) (number "4" (effects (font (size 1.016 1.016)))))
      (pin bidirectional line (at -15.24 -2.54 0) (length 2.54)
        (name "GPIO8/LED" (effects (font (size 1.016 1.016)))) (number "5" (effects (font (size 1.016 1.016)))))
      (pin bidirectional line (at -15.24 -7.62 0) (length 2.54)
        (name "GPIO7" (effects (font (size 1.016 1.016)))) (number "6" (effects (font (size 1.016 1.016)))))
      (pin bidirectional line (at -15.24 -12.70 0) (length 2.54)
        (name "GPIO6" (effects (font (size 1.016 1.016)))) (number "7" (effects (font (size 1.016 1.016)))))
      (pin bidirectional line (at -15.24 -17.78 0) (length 2.54)
        (name "GPIO5" (effects (font (size 1.016 1.016)))) (number "8" (effects (font (size 1.016 1.016)))))
      (pin power_in line (at 15.24 17.78 180) (length 2.54)
        (name "5V" (effects (font (size 1.016 1.016)))) (number "9" (effects (font (size 1.016 1.016)))))
      (pin power_in line (at 15.24 12.70 180) (length 2.54)
        (name "GND" (effects (font (size 1.016 1.016)))) (number "10" (effects (font (size 1.016 1.016)))))
      (pin power_in line (at 15.24 7.62 180) (length 2.54)
        (name "3V3" (effects (font (size 1.016 1.016)))) (number "11" (effects (font (size 1.016 1.016)))))
      (pin bidirectional line (at 15.24 2.54 180) (length 2.54)
        (name "GPIO4" (effects (font (size 1.016 1.016)))) (number "12" (effects (font (size 1.016 1.016)))))
      (pin input line (at 15.24 -2.54 180) (length 2.54)
        (name "GPIO3/ADC" (effects (font (size 1.016 1.016)))) (number "13" (effects (font (size 1.016 1.016)))))
      (pin bidirectional line (at 15.24 -7.62 180) (length 2.54)
        (name "GPIO2" (effects (font (size 1.016 1.016)))) (number "14" (effects (font (size 1.016 1.016)))))
      (pin bidirectional line (at 15.24 -12.70 180) (length 2.54)
        (name "GPIO1" (effects (font (size 1.016 1.016)))) (number "15" (effects (font (size 1.016 1.016)))))
      (pin bidirectional line (at 15.24 -17.78 180) (length 2.54)
        (name "GPIO0/SDA" (effects (font (size 1.016 1.016)))) (number "16" (effects (font (size 1.016 1.016)))))
    )
  )
'''

CUSTOM_TP4056 = '''\
  (symbol "Custom:TP4056" (pin_names (offset 1.016)) (in_bom yes) (on_board yes)
    (property "Reference" "U" (id 0) (at 0 11.43 0) (effects (font (size 1.27 1.27))))
    (property "Value" "TP4056" (id 1) (at 0 -11.43 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Package_SO:SOP-8_3.9x4.9mm_P1.27mm" (id 2) (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "https://dlnmh9ip6v2uc.cloudfront.net/datasheets/Prototyping/TP4056.pdf" (id 3) (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
    (symbol "TP4056_0_1"
      (rectangle (start -7.62 8.89) (end 7.62 -8.89)
        (stroke (width 0.254) (type default)) (fill (type background)))
      (text "TP4056" (at 0 0 0) (effects (font (size 1.27 1.27))))
    )
    (symbol "TP4056_1_1"
      (pin input line (at -10.16 6.35 0) (length 2.54)
        (name "TEMP" (effects (font (size 1.016 1.016)))) (number "1" (effects (font (size 1.016 1.016)))))
      (pin input line (at -10.16 1.27 0) (length 2.54)
        (name "PROG" (effects (font (size 1.016 1.016)))) (number "2" (effects (font (size 1.016 1.016)))))
      (pin power_in line (at -10.16 -3.81 0) (length 2.54)
        (name "GND" (effects (font (size 1.016 1.016)))) (number "3" (effects (font (size 1.016 1.016)))))
      (pin power_in line (at -10.16 -8.89 0) (length 2.54)
        (name "VCC" (effects (font (size 1.016 1.016)))) (number "4" (effects (font (size 1.016 1.016)))))
      (pin output line (at 10.16 6.35 180) (length 2.54)
        (name "BAT" (effects (font (size 1.016 1.016)))) (number "5" (effects (font (size 1.016 1.016)))))
      (pin output line (at 10.16 1.27 180) (length 2.54)
        (name "CHRG" (effects (font (size 1.016 1.016)))) (number "6" (effects (font (size 1.016 1.016)))))
      (pin output line (at 10.16 -3.81 180) (length 2.54)
        (name "STDBY" (effects (font (size 1.016 1.016)))) (number "7" (effects (font (size 1.016 1.016)))))
      (pin input line (at 10.16 -8.89 180) (length 2.54)
        (name "CE" (effects (font (size 1.016 1.016)))) (number "8" (effects (font (size 1.016 1.016)))))
    )
  )
'''

CUSTOM_MP1584 = '''\
  (symbol "Custom:MP1584EN" (pin_names (offset 1.016)) (in_bom yes) (on_board yes)
    (property "Reference" "U" (id 0) (at 0 11.43 0) (effects (font (size 1.27 1.27))))
    (property "Value" "MP1584EN" (id 1) (at 0 -11.43 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Package_SO:SOP-8_3.9x4.9mm_P1.27mm" (id 2) (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "" (id 3) (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
    (symbol "MP1584EN_0_1"
      (rectangle (start -7.62 8.89) (end 7.62 -8.89)
        (stroke (width 0.254) (type default)) (fill (type background)))
      (text "MP1584EN" (at 0 0 0) (effects (font (size 1.27 1.27))))
    )
    (symbol "MP1584EN_1_1"
      (pin input line (at -10.16 6.35 0) (length 2.54)
        (name "EN" (effects (font (size 1.016 1.016)))) (number "1" (effects (font (size 1.016 1.016)))))
      (pin power_in line (at -10.16 1.27 0) (length 2.54)
        (name "VIN" (effects (font (size 1.016 1.016)))) (number "2" (effects (font (size 1.016 1.016)))))
      (pin output line (at -10.16 -3.81 0) (length 2.54)
        (name "SW" (effects (font (size 1.016 1.016)))) (number "3" (effects (font (size 1.016 1.016)))))
      (pin power_in line (at -10.16 -8.89 0) (length 2.54)
        (name "VIN_EP" (effects (font (size 1.016 1.016)))) (number "4" (effects (font (size 1.016 1.016)))))
      (pin power_in line (at 10.16 6.35 180) (length 2.54)
        (name "GND" (effects (font (size 1.016 1.016)))) (number "5" (effects (font (size 1.016 1.016)))))
      (pin power_in line (at 10.16 1.27 180) (length 2.54)
        (name "GND2" (effects (font (size 1.016 1.016)))) (number "6" (effects (font (size 1.016 1.016)))))
      (pin input line (at 10.16 -3.81 180) (length 2.54)
        (name "FB" (effects (font (size 1.016 1.016)))) (number "7" (effects (font (size 1.016 1.016)))))
      (pin passive line (at 10.16 -8.89 180) (length 2.54)
        (name "COMP" (effects (font (size 1.016 1.016)))) (number "8" (effects (font (size 1.016 1.016)))))
    )
  )
'''

# ── Build lib_symbols section ─────────────────────────────────────────────────
def build_lib_symbols() -> str:
    parts = [CUSTOM_ESP32, CUSTOM_TP4056, CUSTOM_MP1584]
    for lib, syms in [
        ("Connector_Generic", ["Conn_01x02", "Conn_01x04"]),
        ("Device",            ["Battery", "C", "L", "R"]),
        ("Diode",             ["SS34"]),
        ("Regulator_Linear",  ["AMS1117-3.3"]),
        ("Transistor_FET",    ["AO3401A"]),
        ("power",             ["+3V3", "+5V", "+12V", "GND", "PWR_FLAG", "VBATT"]),
    ]:
        for s in syms:
            try:
                parts.append(lib_sym(lib, s))
            except Exception as e:
                print(f"  WARNING: {lib}:{s} → {e}")
    return "  (lib_symbols\n" + "\n".join(parts) + "\n  )\n"

# ── Main schematic body ───────────────────────────────────────────────────────
def build_body() -> str:
    b = []

    # ── U1: ESP32-C3 Super Mini at (200, 170) ──────────────────────────────
    # CORRECT formula for pin → schematic coords:
    #   sch_x = cx + sym_x
    #   sch_y = cy - sym_y  (KiCAD symbol editor uses Y-up; schematic uses Y-down)

    # ── U1: ESP32-C3 Super Mini at (200, 170) ──────────────────────────────
    U1x, U1y = 200.0, 170.0
    Lx = U1x - 15.24   # 184.76
    Rx = U1x + 15.24   # 215.24
    b.append(component("Custom:ESP32-C3-Super-Mini", "U1", "ESP32-C3-Super-Mini", U1x, U1y))
    # Left pins: sym_y = 17.78,12.70,7.62,2.54,-2.54,-7.62,-12.70,-17.78
    # sch_y = U1y - sym_y = 152.22,157.30,162.38,167.46,172.54,177.62,182.70,187.78
    b.append(nc(Lx, U1y - 17.78))                          # pin1  GPIO21/TX  → 152.22
    b.append(nc(Lx, U1y - 12.70))                          # pin2  GPIO20/RX  → 157.30
    b.append(label("SCL",   Lx, U1y - 7.62,  "right"))     # pin3  GPIO10     → 162.38
    b.append(nc(Lx, U1y -  2.54))                          # pin4  GPIO9/BOOT → 167.46
    b.append(nc(Lx, U1y +  2.54))                          # pin5  GPIO8/LED  → 172.54
    b.append(nc(Lx, U1y +  7.62))                          # pin6  GPIO7      → 177.62
    b.append(nc(Lx, U1y + 12.70))                          # pin7  GPIO6      → 182.70
    b.append(nc(Lx, U1y + 17.78))                          # pin8  GPIO5      → 187.78
    # Right pins
    b.append(nc(Rx, U1y - 17.78))                          # pin9  5V         → 152.22
    b.append(power("GND",    Rx, U1y - 12.70))             # pin10 GND        → 157.30
    b.append(power("+3V3",   Rx, U1y -  7.62))             # pin11 3V3        → 162.38
    b.append(nc(Rx, U1y -  2.54))                          # pin12 GPIO4      → 167.46
    b.append(label("BATT_ADC", Rx, U1y + 2.54, "left"))    # pin13 GPIO3/ADC  → 172.54
    b.append(nc(Rx, U1y +  7.62))                          # pin14 GPIO2      → 177.62
    b.append(nc(Rx, U1y + 12.70))                          # pin15 GPIO1      → 182.70
    b.append(label("SDA",    Rx, U1y + 17.78, "left"))     # pin16 GPIO0/SDA  → 187.78

    # ── J3: NeoTrellis JST-PH Conn_01x04 at (280, 170) ────────────────────
    # sym: pin1(-5.08,+2.54) pin2(-5.08,0) pin3(-5.08,-2.54) pin4(-5.08,-5.08)
    # sch: pin1(274.92,167.46) pin2(274.92,170) pin3(274.92,172.54) pin4(274.92,175.08)
    J3x, J3y = 280.0, 170.0
    J3px = J3x - 5.08   # 274.92
    b.append(component("Connector_Generic:Conn_01x04", "J3", "NeoTrellis_I2C", J3x, J3y))
    b.append(power("+3V3", J3px, J3y - 2.54))   # pin1 VCC  → (274.92, 167.46)
    b.append(power("GND",  J3px, J3y))           # pin2 GND  → (274.92, 170.00)
    b.append(label("SDA",  J3px, J3y + 2.54, "right"))  # pin3 SDA → (274.92, 172.54)
    b.append(label("SCL",  J3px, J3y + 5.08, "right"))  # pin4 SCL → (274.92, 175.08)

    # ── R3, R4: I2C pull-ups ───────────────────────────────────────────────
    # Device:R: pin1 at sch(cx, cy-3.81), pin2 at sch(cx, cy+3.81)
    b.append(component("Device:R", "R3", "4.7k", 255.0, 155.0))
    b.append(power("+3V3", 255.0, 155.0 - 3.81))             # pin1 → +3V3
    b.append(label("SDA",  255.0, 155.0 + 3.81, "right"))    # pin2 → SDA

    b.append(component("Device:R", "R4", "4.7k", 255.0, 175.0))
    b.append(power("+3V3", 255.0, 175.0 - 3.81))             # pin1 → +3V3
    b.append(label("SCL",  255.0, 175.0 + 3.81, "right"))    # pin2 → SCL

    # ── R1, R2: Battery voltage divider ───────────────────────────────────
    b.append(component("Device:R", "R1", "100k", 175.0, 155.0))
    b.append(label("VBATT",    175.0, 155.0 - 3.81, "right"))   # pin1 (upper)
    b.append(label("BATT_ADC", 175.0, 155.0 + 3.81, "left"))    # pin2 (lower)

    b.append(component("Device:R", "R2", "100k", 175.0, 175.0))
    b.append(label("BATT_ADC", 175.0, 175.0 - 3.81, "right"))   # pin1 (upper)
    b.append(power("GND",      175.0, 175.0 + 3.81))             # pin2 (lower)

    # ── C3: ESP32 3V3 decoupling at (230, 170) ────────────────────────────
    b.append(component("Device:C", "C3", "100nF", 230.0, 170.0))
    b.append(power("+3V3", 230.0, 170.0 - 3.81))   # pin1 (upper)
    b.append(power("GND",  230.0, 170.0 + 3.81))   # pin2 (lower)

    # ── U3: AMS1117-3.3 at (220, 100) ─────────────────────────────────────
    # sym: pin1 GND(0,-7.62), pin2 VO(+7.62,0), pin3 VI(-7.62,0)
    # sch: pin1(220,107.62), pin2(227.62,100), pin3(212.38,100)
    b.append(component("Regulator_Linear:AMS1117-3.3", "U3", "AMS1117-3.3", 220.0, 100.0))
    b.append(power("GND",  220.0,        100.0 + 7.62))   # pin1 GND  → (220, 107.62)
    b.append(power("+3V3", 220.0 + 7.62, 100.0))           # pin2 VO   → (227.62, 100)
    b.append(power("+5V",  220.0 - 7.62, 100.0))           # pin3 VI   → (212.38, 100)

    # ── C1: AMS1117 input bypass at (210, 113) ────────────────────────────
    b.append(component("Device:C", "C1", "10uF", 210.0, 113.0))
    b.append(power("+5V", 210.0, 113.0 - 3.81))   # pin1 (upper)
    b.append(power("GND", 210.0, 113.0 + 3.81))   # pin2 (lower)

    # ── C2: AMS1117 output bypass at (230, 113) ───────────────────────────
    b.append(component("Device:C", "C2", "10uF", 230.0, 113.0))
    b.append(power("+3V3", 230.0, 113.0 - 3.81))   # pin1 (upper)
    b.append(power("GND",  230.0, 113.0 + 3.81))   # pin2 (lower)

    # ── J1: USB-C power (Conn_01x02) at (40, 50) ──────────────────────────
    # sym: pin1(-5.08,0)→sch(34.92,50), pin2(-5.08,-2.54)→sch(34.92,52.54)
    b.append(component("Connector_Generic:Conn_01x02", "J1", "USB-C_5V_In", 40.0, 50.0))
    b.append(power("+5V", 34.92, 50.0))     # pin1 VBUS
    b.append(power("GND", 34.92, 52.54))    # pin2 GND

    # ── J2: 12V barrel jack (Conn_01x02) at (40, 100) ─────────────────────
    b.append(component("Connector_Generic:Conn_01x02", "J2", "12V_Barrel_In", 40.0, 100.0))
    b.append(label("12V_IN", 34.92, 100.0,  "right"))  # pin1
    b.append(power("GND",    34.92, 102.54))             # pin2

    # ── D1: SS34 reverse polarity at (75, 100) ────────────────────────────
    # Inherits SB120 geometry: A1(anode) sym(-3.81,0)→sch(71.19,100), A2(cathode) sym(+3.81,0)→sch(78.81,100)
    b.append(component("Diode:SS34", "D1", "SS34", 75.0, 100.0))
    b.append(label("12V_IN",   71.19, 100.0, "right"))  # pin A1 anode
    b.append(label("12V_PROT", 78.81, 100.0, "left"))   # pin A2 cathode

    # ── U4: MP1584EN step-down at (115, 85) ───────────────────────────────
    # Custom sym pins: left at sx=-10.16, right at sx=+10.16
    # sym_y: 6.35,1.27,-3.81,-8.89 → sch_y: 85-6.35=78.65, 83.73, 88.81, 93.89
    U4x, U4y = 115.0, 85.0
    U4Lx = U4x - 10.16  # 104.84
    U4Rx = U4x + 10.16  # 125.16
    b.append(component("Custom:MP1584EN", "U4", "MP1584EN", U4x, U4y))
    b.append(label("12V_PROT", U4Lx, U4y - 6.35, "right"))   # pin1 EN  → 78.65
    b.append(label("12V_PROT", U4Lx, U4y - 1.27, "right"))   # pin2 VIN → 83.73
    b.append(label("SW_NODE",  U4Lx, U4y + 3.81, "right"))   # pin3 SW  → 88.81
    b.append(label("12V_PROT", U4Lx, U4y + 8.89, "right"))   # pin4 VIN_EP → 93.89
    b.append(power("GND",  U4Rx, U4y - 6.35))                # pin5 GND → 78.65
    b.append(power("GND",  U4Rx, U4y - 1.27))                # pin6 GND2 → 83.73
    b.append(label("FB_5V",    U4Rx, U4y + 3.81, "left"))    # pin7 FB  → 88.81
    b.append(label("COMP_5V",  U4Rx, U4y + 8.89, "left"))    # pin8 COMP → 93.89

    # ── L1: 10uH inductor at (140, 72) (vertical) ─────────────────────────
    # Device:L: pin1 sym_y=+3.81 → sch_y=cy-3.81, pin2 sym_y=-3.81 → sch_y=cy+3.81
    b.append(component("Device:L", "L1", "10uH", 140.0, 72.0))
    b.append(label("SW_NODE", 140.0, 72.0 - 3.81, "right"))  # pin1 (upper) → SW
    b.append(power("+5V",     140.0, 72.0 + 3.81))           # pin2 (lower) → +5V

    # ── R7: 100k FB divider high at (152, 82) ─────────────────────────────
    b.append(component("Device:R", "R7", "100k", 152.0, 82.0))
    b.append(power("+5V",    152.0, 82.0 - 3.81))            # pin1 (upper) → +5V
    b.append(label("FB_5V",  152.0, 82.0 + 3.81, "left"))    # pin2 (lower) → FB

    # ── R8: 39k FB divider low at (152, 95) ───────────────────────────────
    b.append(component("Device:R", "R8", "39k", 152.0, 95.0))
    b.append(label("FB_5V", 152.0, 95.0 - 3.81, "right"))    # pin1 (upper) → FB
    b.append(power("GND",   152.0, 95.0 + 3.81))              # pin2 (lower) → GND

    # ── C4: 22uF MP1584EN output bypass at (162, 72) ─────────────────────
    b.append(component("Device:C", "C4", "22uF", 162.0, 72.0))
    b.append(power("+5V", 162.0, 72.0 - 3.81))   # pin1 (upper)
    b.append(power("GND", 162.0, 72.0 + 3.81))   # pin2 (lower)

    # ── C6: 10uF MP1584EN input bypass at (104, 92) ───────────────────────
    b.append(component("Device:C", "C6", "10uF", 104.0, 92.0))
    b.append(label("12V_PROT", 104.0, 92.0 - 3.81, "right"))   # pin1 (upper)
    b.append(power("GND",      104.0, 92.0 + 3.81))             # pin2 (lower)

    # ── U2: TP4056 Li-ion charger at (115, 130) ───────────────────────────
    # Custom sym pins: sym_y 6.35,1.27,-3.81,-8.89 → sch_y: 123.65,128.73,133.81,138.89
    U2x, U2y = 115.0, 130.0
    U2Lx = U2x - 10.16  # 104.84
    U2Rx = U2x + 10.16  # 125.16
    b.append(component("Custom:TP4056", "U2", "TP4056", U2x, U2y))
    b.append(power("GND",     U2Lx, U2y - 6.35))               # pin1 TEMP  → 123.65
    b.append(label("PROG_1A", U2Lx, U2y - 1.27, "right"))      # pin2 PROG  → 128.73
    b.append(power("GND",     U2Lx, U2y + 3.81))               # pin3 GND   → 133.81
    b.append(power("+5V",     U2Lx, U2y + 8.89))               # pin4 VCC   → 138.89
    b.append(label("VBATT",   U2Rx, U2y - 6.35, "left"))       # pin5 BAT   → 123.65
    b.append(nc(U2Rx, U2y - 1.27))                             # pin6 CHRG  → 128.73
    b.append(nc(U2Rx, U2y + 3.81))                             # pin7 STDBY → 133.81
    b.append(power("+5V",     U2Rx, U2y + 8.89))               # pin8 CE    → 138.89

    # ── R5: 1.2k PROG resistor at (95, 128) ──────────────────────────────
    b.append(component("Device:R", "R5", "1.2k", 95.0, 128.0))
    b.append(label("PROG_1A", 95.0, 128.0 - 3.81, "right"))    # pin1 (upper)
    b.append(power("GND",     95.0, 128.0 + 3.81))              # pin2 (lower)

    # ── BT1: 18650 battery at (155, 130) ──────────────────────────────────
    # Device:Battery: pin+(1) sym_y=+5.08→sch_y=cy-5.08, pin-(2) sym_y=-5.08→sch_y=cy+5.08
    b.append(component("Device:Battery", "BT1", "18650_Li-ion", 155.0, 130.0))
    b.append(label("VBATT", 155.0, 130.0 - 5.08, "right"))   # pin+ (1) → 124.92
    b.append(power("GND",   155.0, 130.0 + 5.08))             # pin- (2) → 135.08

    # ── Q1: AO3401A P-ch MOSFET power path at (180, 100) ─────────────────
    # sym: G(1)(-5.08,0), S(2)(+2.54,-5.08), D(3)(+2.54,+5.08)
    # sch: G(174.92,100), S(182.54,105.08), D(182.54,94.92)
    b.append(component("Transistor_FET:AO3401A", "Q1", "AO3401A", 180.0, 100.0))
    b.append(label("Q1_GATE", 174.92, 100.0,   "right"))   # pin G(1)
    b.append(power("+5V",     182.54, 105.08))              # pin S(2) source
    b.append(label("VBATT",   182.54, 94.92,  "left"))      # pin D(3) drain

    # ── R6: 100k gate pull-up at (165, 100) ───────────────────────────────
    b.append(component("Device:R", "R6", "100k", 165.0, 100.0))
    b.append(power("+5V",     165.0, 100.0 - 3.81))             # pin1 (upper) → +5V
    b.append(label("Q1_GATE", 165.0, 100.0 + 3.81, "left"))     # pin2 (lower) → gate

    return "".join(b)

# ── Assemble schematic ────────────────────────────────────────────────────────
def build_schematic() -> str:
    return (
        f'(kicad_sch (version 20230121) (generator eeschema)\n'
        f'  (uuid "{SCH_UUID}")\n'
        f'  (paper "A3")\n'
        f'  (title_block\n'
        f'    (title "ESP32 NeoTrellis Box")\n'
        f'    (company "tsayles")\n'
        f'    (rev "2.2")\n'
        f'  )\n'
        + build_lib_symbols()
        + build_body()
        + f'  (sheet_instances\n    (path "/" (page "1"))\n  )\n)\n'
    )

# ── Write files ───────────────────────────────────────────────────────────────
def write_custom_lib():
    content = (
        '(kicad_symbol_lib (version 20220914) (generator kicad_symbol_editor)\n'
        + CUSTOM_ESP32 + CUSTOM_TP4056 + CUSTOM_MP1584
        + ')\n'
    )
    SYM_DIR.mkdir(parents=True, exist_ok=True)
    (SYM_DIR / "Custom.kicad_sym").write_text(content)
    print("  Wrote Custom.kicad_sym")

def write_project():
    proj = {
        "board": {}, "cvpcb": {}, "erc": {},
        "libraries": {"pinned_footprint_libs": [], "pinned_symbol_libs": []},
        "meta": {"filename": f"{PROJ}.kicad_pro", "version": 1},
        "net_settings": {}, "pcbnew": {},
        "schematic": {"legacy_lib_dir": "", "legacy_lib_list": []},
        "sheets": [], "text_variables": {}
    }
    (KICAD_DIR / f"{PROJ}.kicad_pro").write_text(json.dumps(proj, indent=2))
    print("  Wrote .kicad_pro")

def main():
    print("Generating KiCAD files...")
    write_custom_lib()
    write_project()
    sch = build_schematic()
    (KICAD_DIR / f"{PROJ}.kicad_sch").write_text(sch)
    print(f"  Wrote .kicad_sch ({len(sch.splitlines())} lines)")
    print("Done.")

if __name__ == "__main__":
    main()
