#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import textwrap
import uuid
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
KICAD_DIR = ROOT / "hardware" / "kicad"
SYMBOL_DIR = KICAD_DIR / "symbols"
CUSTOM_LIB_PATH = SYMBOL_DIR / "Custom.kicad_sym"
PROJECT_PATH = KICAD_DIR / "esp32_neotrellis_box.kicad_pro"
SCHEMATIC_PATH = KICAD_DIR / "esp32_neotrellis_box.kicad_sch"
SYSTEM_SYMBOL_DIR = Path("/usr/share/kicad/symbols")
PROJECT_NAME = "esp32_neotrellis_box"

STANDARD_SYMBOLS = {
    "Connector": ["USB_C_Receptacle"],
    "Connector_Generic": ["Conn_01x02", "Conn_01x04"],
    "Device": ["Battery", "C", "L", "R"],
    "Diode": ["SS34"],
    "Regulator_Linear": ["AMS1117-3.3"],
    "Transistor_FET": ["AO3401A"],
    "power": ["+12V", "+3V3", "+5V", "GND", "PWR_FLAG"],
}

CUSTOM_SYMBOLS = {
    "ESP32-C3-Super-Mini": textwrap.dedent(
        """
        (symbol "ESP32-C3-Super-Mini" (pin_names (offset 1.016)) (in_bom yes) (on_board yes)
          (property "Reference" "U" (id 0) (at -12.7 24.13 0)
            (effects (font (size 1.27 1.27)))
          )
          (property "Value" "ESP32-C3-Super-Mini" (id 1) (at 0 -24.13 0)
            (effects (font (size 1.27 1.27)))
          )
          (property "Footprint" "" (id 2) (at 0 0 0)
            (effects (font (size 1.27 1.27)) hide)
          )
          (property "Datasheet" "" (id 3) (at 0 0 0)
            (effects (font (size 1.27 1.27)) hide)
          )
          (property "ki_keywords" "ESP32-C3 module WiFi BLE" (id 4) (at 0 0 0)
            (effects (font (size 1.27 1.27)) hide)
          )
          (property "ki_description" "ESP32-C3 Super Mini module, 16-pin development board" (id 5) (at 0 0 0)
            (effects (font (size 1.27 1.27)) hide)
          )
          (symbol "ESP32-C3-Super-Mini_0_1"
            (rectangle (start -12.7 20.32) (end 12.7 -20.32)
              (stroke (width 0.254) (type default))
              (fill (type background))
            )
            (text "ESP32-C3" (at 0 1.27 0)
              (effects (font (size 1.27 1.27)))
            )
            (text "Super Mini" (at 0 -1.27 0)
              (effects (font (size 1.016 1.016)))
            )
          )
          (symbol "ESP32-C3-Super-Mini_1_1"
            (pin bidirectional line (at -15.24 17.78 0) (length 2.54)
              (name "GPIO21/TX" (effects (font (size 1.016 1.016))))
              (number "1" (effects (font (size 1.016 1.016))))
            )
            (pin bidirectional line (at -15.24 12.7 0) (length 2.54)
              (name "GPIO20/RX" (effects (font (size 1.016 1.016))))
              (number "2" (effects (font (size 1.016 1.016))))
            )
            (pin bidirectional line (at -15.24 7.62 0) (length 2.54)
              (name "GPIO10" (effects (font (size 1.016 1.016))))
              (number "3" (effects (font (size 1.016 1.016))))
            )
            (pin bidirectional line (at -15.24 2.54 0) (length 2.54)
              (name "GPIO9/BOOT" (effects (font (size 1.016 1.016))))
              (number "4" (effects (font (size 1.016 1.016))))
            )
            (pin bidirectional line (at -15.24 -2.54 0) (length 2.54)
              (name "GPIO8/LED" (effects (font (size 1.016 1.016))))
              (number "5" (effects (font (size 1.016 1.016))))
            )
            (pin bidirectional line (at -15.24 -7.62 0) (length 2.54)
              (name "GPIO7" (effects (font (size 1.016 1.016))))
              (number "6" (effects (font (size 1.016 1.016))))
            )
            (pin bidirectional line (at -15.24 -12.7 0) (length 2.54)
              (name "GPIO6" (effects (font (size 1.016 1.016))))
              (number "7" (effects (font (size 1.016 1.016))))
            )
            (pin bidirectional line (at -15.24 -17.78 0) (length 2.54)
              (name "GPIO5" (effects (font (size 1.016 1.016))))
              (number "8" (effects (font (size 1.016 1.016))))
            )
            (pin power_in line (at 15.24 17.78 180) (length 2.54)
              (name "5V" (effects (font (size 1.016 1.016))))
              (number "9" (effects (font (size 1.016 1.016))))
            )
            (pin power_in line (at 15.24 12.7 180) (length 2.54)
              (name "GND" (effects (font (size 1.016 1.016))))
              (number "10" (effects (font (size 1.016 1.016))))
            )
            (pin power_in line (at 15.24 7.62 180) (length 2.54)
              (name "3V3" (effects (font (size 1.016 1.016))))
              (number "11" (effects (font (size 1.016 1.016))))
            )
            (pin bidirectional line (at 15.24 2.54 180) (length 2.54)
              (name "GPIO4" (effects (font (size 1.016 1.016))))
              (number "12" (effects (font (size 1.016 1.016))))
            )
            (pin input line (at 15.24 -2.54 180) (length 2.54)
              (name "GPIO3/ADC" (effects (font (size 1.016 1.016))))
              (number "13" (effects (font (size 1.016 1.016))))
            )
            (pin bidirectional line (at 15.24 -7.62 180) (length 2.54)
              (name "GPIO2" (effects (font (size 1.016 1.016))))
              (number "14" (effects (font (size 1.016 1.016))))
            )
            (pin bidirectional line (at 15.24 -12.7 180) (length 2.54)
              (name "GPIO1" (effects (font (size 1.016 1.016))))
              (number "15" (effects (font (size 1.016 1.016))))
            )
            (pin bidirectional line (at 15.24 -17.78 180) (length 2.54)
              (name "GPIO0/SDA" (effects (font (size 1.016 1.016))))
              (number "16" (effects (font (size 1.016 1.016))))
            )
          )
        )
        """
    ).strip(),
    "TP4056": textwrap.dedent(
        """
        (symbol "TP4056" (pin_names (offset 1.016)) (in_bom yes) (on_board yes)
          (property "Reference" "U" (id 0) (at -7.62 13.97 0)
            (effects (font (size 1.27 1.27)))
          )
          (property "Value" "TP4056" (id 1) (at 0 -13.97 0)
            (effects (font (size 1.27 1.27)))
          )
          (property "Footprint" "Package_SO:SOP-8_3.9x4.9mm_P1.27mm" (id 2) (at 0 0 0)
            (effects (font (size 1.27 1.27)) hide)
          )
          (property "Datasheet" "" (id 3) (at 0 0 0)
            (effects (font (size 1.27 1.27)) hide)
          )
          (property "ki_keywords" "lithium charger TP4056" (id 4) (at 0 0 0)
            (effects (font (size 1.27 1.27)) hide)
          )
          (property "ki_description" "Standalone linear Li-ion charger" (id 5) (at 0 0 0)
            (effects (font (size 1.27 1.27)) hide)
          )
          (symbol "TP4056_0_1"
            (rectangle (start -7.62 10.16) (end 7.62 -10.16)
              (stroke (width 0.254) (type default))
              (fill (type background))
            )
          )
          (symbol "TP4056_1_1"
            (pin input line (at -10.16 7.62 0) (length 2.54)
              (name "TEMP" (effects (font (size 1.016 1.016))))
              (number "1" (effects (font (size 1.016 1.016))))
            )
            (pin input line (at -10.16 2.54 0) (length 2.54)
              (name "PROG" (effects (font (size 1.016 1.016))))
              (number "2" (effects (font (size 1.016 1.016))))
            )
            (pin power_in line (at -10.16 -2.54 0) (length 2.54)
              (name "GND" (effects (font (size 1.016 1.016))))
              (number "3" (effects (font (size 1.016 1.016))))
            )
            (pin power_in line (at -10.16 -7.62 0) (length 2.54)
              (name "VCC" (effects (font (size 1.016 1.016))))
              (number "4" (effects (font (size 1.016 1.016))))
            )
            (pin passive line (at 10.16 -7.62 180) (length 2.54)
              (name "BAT" (effects (font (size 1.016 1.016))))
              (number "5" (effects (font (size 1.016 1.016))))
            )
            (pin output line (at 10.16 -2.54 180) (length 2.54)
              (name "CHRG" (effects (font (size 1.016 1.016))))
              (number "6" (effects (font (size 1.016 1.016))))
            )
            (pin output line (at 10.16 2.54 180) (length 2.54)
              (name "STDBY" (effects (font (size 1.016 1.016))))
              (number "7" (effects (font (size 1.016 1.016))))
            )
            (pin input line (at 10.16 7.62 180) (length 2.54)
              (name "CE" (effects (font (size 1.016 1.016))))
              (number "8" (effects (font (size 1.016 1.016))))
            )
          )
        )
        """
    ).strip(),
    "MP1584EN": textwrap.dedent(
        """
        (symbol "MP1584EN" (pin_names (offset 1.016)) (in_bom yes) (on_board yes)
          (property "Reference" "U" (id 0) (at -7.62 13.97 0)
            (effects (font (size 1.27 1.27)))
          )
          (property "Value" "MP1584EN" (id 1) (at 0 -13.97 0)
            (effects (font (size 1.27 1.27)))
          )
          (property "Footprint" "Package_SO:SOP-8_3.9x4.9mm_P1.27mm" (id 2) (at 0 0 0)
            (effects (font (size 1.27 1.27)) hide)
          )
          (property "Datasheet" "" (id 3) (at 0 0 0)
            (effects (font (size 1.27 1.27)) hide)
          )
          (property "ki_keywords" "buck regulator MP1584EN" (id 4) (at 0 0 0)
            (effects (font (size 1.27 1.27)) hide)
          )
          (property "ki_description" "Monolithic buck regulator controller symbol for prototype schematic" (id 5) (at 0 0 0)
            (effects (font (size 1.27 1.27)) hide)
          )
          (symbol "MP1584EN_0_1"
            (rectangle (start -7.62 10.16) (end 7.62 -10.16)
              (stroke (width 0.254) (type default))
              (fill (type background))
            )
          )
          (symbol "MP1584EN_1_1"
            (pin input line (at -10.16 7.62 0) (length 2.54)
              (name "EN" (effects (font (size 1.016 1.016))))
              (number "1" (effects (font (size 1.016 1.016))))
            )
            (pin power_in line (at -10.16 2.54 0) (length 2.54)
              (name "VIN" (effects (font (size 1.016 1.016))))
              (number "2" (effects (font (size 1.016 1.016))))
            )
            (pin output line (at -10.16 -2.54 0) (length 2.54)
              (name "SW" (effects (font (size 1.016 1.016))))
              (number "3" (effects (font (size 1.016 1.016))))
            )
            (pin power_in line (at -10.16 -7.62 0) (length 2.54)
              (name "VIN_EP" (effects (font (size 1.016 1.016))))
              (number "4" (effects (font (size 1.016 1.016))))
            )
            (pin power_in line (at 10.16 -7.62 180) (length 2.54)
              (name "GND" (effects (font (size 1.016 1.016))))
              (number "5" (effects (font (size 1.016 1.016))))
            )
            (pin power_in line (at 10.16 -2.54 180) (length 2.54)
              (name "GND" (effects (font (size 1.016 1.016))))
              (number "6" (effects (font (size 1.016 1.016))))
            )
            (pin input line (at 10.16 2.54 180) (length 2.54)
              (name "FB" (effects (font (size 1.016 1.016))))
              (number "7" (effects (font (size 1.016 1.016))))
            )
            (pin passive line (at 10.16 7.62 180) (length 2.54)
              (name "COMP" (effects (font (size 1.016 1.016))))
              (number "8" (effects (font (size 1.016 1.016))))
            )
          )
        )
        """
    ).strip(),
}


@dataclass
class Pin:
    number: str
    name: str
    x: float
    y: float
    angle: int


@dataclass
class Component:
    ref: str
    lib_id: str
    symbol_key: tuple[str, str]
    x: float
    y: float
    rotation: int = 0
    value: str | None = None
    footprint: str | None = None
    datasheet: str | None = None
    in_bom: str = "yes"
    on_board: str = "yes"
    dnp: str = "no"


class SymbolRepository:
    def __init__(self, library: str, path: Path) -> None:
        self.library = library
        self.path = path
        self.text = path.read_text(encoding="utf-8")
        self.raw_blocks = self._extract_top_level_symbols()
        self.exprs = {name: parse_sexpr(block) for name, block in self.raw_blocks.items()}
        self._pins_cache: dict[str, list[Pin]] = {}
        self._prop_cache: dict[str, dict[str, str]] = {}

    def _extract_top_level_symbols(self) -> dict[str, str]:
        result: dict[str, str] = {}
        depth = 0
        i = 0
        while i < len(self.text):
            ch = self.text[i]
            if ch == '"':
                i = skip_string(self.text, i)
                continue
            if ch == '(':
                if depth == 1 and self.text.startswith('(symbol "', i):
                    block = extract_balanced(self.text, i)
                    match = re.match(r'\(symbol\s+"([^"]+)"', block)
                    if not match:
                        raise ValueError(f"Could not parse symbol name in {self.path}")
                    result[match.group(1)] = block
                    i += len(block)
                    continue
                depth += 1
            elif ch == ')':
                depth -= 1
            i += 1
        return result

    def ensure_symbols(self, names: list[str]) -> list[str]:
        ordered: list[str] = []
        seen: set[str] = set()

        def add(name: str) -> None:
            if name in seen:
                return
            expr = self.exprs[name]
            parent = symbol_extends(expr)
            if parent:
                add(parent)
            seen.add(name)
            ordered.append(name)

        for name in names:
            add(name)
        return ordered

    def properties(self, name: str) -> dict[str, str]:
        if name in self._prop_cache:
            return self._prop_cache[name]
        expr = self.exprs[name]
        merged: dict[str, str] = {}
        parent = symbol_extends(expr)
        if parent:
            merged.update(self.properties(parent))
        for item in expr[2:]:
            if isinstance(item, list) and item and item[0] == "property":
                merged[str(item[1])] = str(item[2])
        self._prop_cache[name] = merged
        return merged

    def pins(self, name: str) -> list[Pin]:
        if name in self._pins_cache:
            return self._pins_cache[name]
        expr = self.exprs[name]
        pins: list[Pin] = []
        parent = symbol_extends(expr)
        if parent:
            pins.extend(self.pins(parent))
        pins.extend(collect_pins(expr))
        self._pins_cache[name] = pins
        return pins


def skip_string(text: str, start: int) -> int:
    i = start + 1
    while i < len(text):
        if text[i] == '\\':
            i += 2
            continue
        if text[i] == '"':
            return i + 1
        i += 1
    raise ValueError("Unterminated string")


def extract_balanced(text: str, start: int) -> str:
    depth = 0
    i = start
    while i < len(text):
        ch = text[i]
        if ch == '"':
            i = skip_string(text, i)
            continue
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
            if depth == 0:
                return text[start : i + 1]
        i += 1
    raise ValueError("Unbalanced expression")


def tokenize(text: str) -> list[str]:
    tokens: list[str] = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch.isspace():
            i += 1
            continue
        if ch in "()":
            tokens.append(ch)
            i += 1
            continue
        if ch == '"':
            j = i + 1
            chars: list[str] = []
            while j < len(text):
                if text[j] == '\\':
                    if j + 1 < len(text):
                        chars.append(text[j + 1])
                        j += 2
                        continue
                if text[j] == '"':
                    break
                chars.append(text[j])
                j += 1
            tokens.append("".join(chars))
            i = j + 1
            continue
        j = i
        while j < len(text) and not text[j].isspace() and text[j] not in "()":
            j += 1
        tokens.append(text[i:j])
        i = j
    return tokens


def parse_tokens(tokens: list[str], index: int = 0):
    if tokens[index] != '(':
        return tokens[index], index + 1
    result: list = []
    index += 1
    while tokens[index] != ')':
        if tokens[index] == '(':
            item, index = parse_tokens(tokens, index)
        else:
            item = tokens[index]
            index += 1
        result.append(item)
    return result, index + 1


def parse_sexpr(text: str):
    expr, _ = parse_tokens(tokenize(text))
    return expr


def symbol_extends(expr) -> str | None:
    for item in expr[2:]:
        if isinstance(item, list) and item and item[0] == "extends":
            return str(item[1])
    return None


def collect_pins(expr) -> list[Pin]:
    pins: list[Pin] = []

    def walk(node) -> None:
        if not isinstance(node, list) or not node:
            return
        if node[0] == "pin":
            at = next(item for item in node if isinstance(item, list) and item and item[0] == "at")
            name = next(item for item in node if isinstance(item, list) and item and item[0] == "name")
            number = next(item for item in node if isinstance(item, list) and item and item[0] == "number")
            pins.append(
                Pin(
                    number=str(number[1]),
                    name=str(name[1]),
                    x=float(at[1]),
                    y=float(at[2]),
                    angle=int(float(at[3])),
                )
            )
        for child in node:
            walk(child)

    walk(expr)
    return pins


def fmt(value: float) -> str:
    if abs(value - round(value)) < 1e-6:
        return str(int(round(value)))
    return f"{value:.3f}".rstrip("0").rstrip(".")


def uuid_str() -> str:
    return str(uuid.uuid4())


def indent_block(block: str, prefix: str = "  ") -> str:
    return "\n".join(prefix + line if line else line for line in block.splitlines())


def top_level_blocks(block: str, head: str) -> list[str]:
    results: list[str] = []
    start = block.find('(')
    depth = 0
    i = start
    while i < len(block):
        ch = block[i]
        if ch == '"':
            i = skip_string(block, i)
            continue
        if ch == '(':
            depth += 1
            if depth == 2 and block.startswith(f'({head} ', i):
                child = extract_balanced(block, i)
                results.append(child)
                i += len(child)
                depth -= 1
                continue
        elif ch == ')':
            depth -= 1
        i += 1
    return results


def top_level_properties(block: str) -> dict[str, str]:
    props: dict[str, str] = {}
    for child in top_level_blocks(block, 'property'):
        match = re.match(r'\(property\s+"([^"]+)"', child)
        if match:
            props[match.group(1)] = child
    return props


def rename_symbol_family(block: str, old: str, new: str) -> str:
    block = re.sub(r'\(symbol\s+"[^"]+"', f'(symbol "{new}"', block, count=1)
    return block.replace(f'"{old}_', f'"{new}_')


def flatten_source_block(repo: SymbolRepository, name: str) -> str:
    raw = repo.raw_blocks[name]
    parent = symbol_extends(repo.exprs[name])
    if not parent:
        return raw
    base = rename_symbol_family(flatten_source_block(repo, parent), parent, name)
    base_props = top_level_properties(base)
    child_props = top_level_properties(raw)
    for prop_name, child_block in child_props.items():
        if prop_name in base_props:
            base = base.replace(base_props[prop_name], child_block, 1)
        else:
            insert_at = base.rfind(')')
            base = base[:insert_at] + '\n  ' + child_block + base[insert_at:]
    return base


def prefix_symbol_block(block: str, library: str) -> str:
    block = re.sub(r'\(symbol\s+"([^"]+)"', fr'(symbol "{library}:\1"', block, count=1)
    return re.sub(r'\(extends\s+"([^"]+)"\)', fr'(extends "{library}:\1")', block)


def embedded_symbol_block(repo: SymbolRepository, name: str, library: str) -> str:
    return prefix_symbol_block(flatten_source_block(repo, name), library)


def rotate(x: float, y: float, angle: int) -> tuple[float, float]:
    angle %= 360
    if angle == 0:
        return x, y
    if angle == 90:
        return -y, x
    if angle == 180:
        return -x, -y
    if angle == 270:
        return y, -x
    raise ValueError(f"Unsupported rotation: {angle}")


def point_for(component: Component, pin: Pin) -> tuple[float, float]:
    rx, ry = rotate(pin.x, pin.y, component.rotation)
    return component.x + rx, component.y + ry


def pin_angle(component: Component, pin: Pin) -> int:
    return (pin.angle + component.rotation) % 360


def effects(size: float = 1.27, hide: bool = False, justify: str | None = None) -> str:
    parts = [f"(font (size {fmt(size)} {fmt(size)}))"]
    if justify:
        parts.append(f"(justify {justify})")
    text = f"(effects {' '.join(parts)})"
    if hide:
        text = text[:-1] + " hide)"
    return text


def instance_properties(component: Component, props: dict[str, str]) -> list[str]:
    ref_hide = component.ref.startswith("#")
    value_hide = False
    ref_y = component.y + 6.35
    value_y = component.y - 6.35
    footprint = component.footprint if component.footprint is not None else props.get("Footprint", "")
    datasheet = component.datasheet if component.datasheet is not None else props.get("Datasheet", "")
    value = component.value if component.value is not None else props.get("Value", component.symbol_key[1])
    return [
        property_block("Reference", component.ref, component.x, ref_y, 0, hide=ref_hide),
        property_block("Value", value, component.x, value_y, 0, hide=value_hide),
        property_block("Footprint", footprint, component.x, component.y, 0, hide=True),
        property_block("Datasheet", datasheet, component.x, component.y, 0, hide=True),
    ]


def property_block(name: str, value: str, x: float, y: float, rotation: int, hide: bool = False) -> str:
    hide_suffix = " hide" if hide else ""
    return textwrap.dedent(
        f"""
        (property "{name}" "{value}" (at {fmt(x)} {fmt(y)} {rotation})
          {effects(hide=hide)}
        )
        """
    ).strip()


def instantiate_component(component: Component, repo_map: dict[tuple[str, str], SymbolRepository], root_uuid: str) -> str:
    repo = repo_map[component.symbol_key]
    props = repo.properties(component.symbol_key[1])
    pins = repo.pins(component.symbol_key[1])
    body: list[str] = [
        f'(symbol (lib_id "{component.lib_id}") (at {fmt(component.x)} {fmt(component.y)} {component.rotation}) (unit 1)',
        f'  (in_bom {component.in_bom}) (on_board {component.on_board}) (dnp {component.dnp})',
        f'  (uuid {uuid_str()})',
    ]
    for prop in instance_properties(component, props):
        body.append(indent_block(prop, "  "))
    for pin in pins:
        body.append(f'  (pin "{pin.number}" (uuid {uuid_str()}))')
    body.extend(
        [
            '  (instances',
            f'    (project "{PROJECT_NAME}"',
            f'      (path "/{root_uuid}"',
            f'        (reference "{component.ref}") (unit 1)',
            '      )',
            '    )',
            '  )',
            ')',
        ]
    )
    return "\n".join(body)


def label_justify(angle: int) -> str:
    if angle == 0:
        return "right"
    return "left"


def make_label(name: str, x: float, y: float, angle: int = 0) -> str:
    return textwrap.dedent(
        f"""
        (label "{name}" (at {fmt(x)} {fmt(y)} {angle}) (fields_autoplaced)
          {effects(justify=label_justify(angle))}
          (uuid {uuid_str()})
        )
        """
    ).strip()


def make_global_label(name: str, x: float, y: float, shape: str = "input", angle: int = 0) -> str:
    return textwrap.dedent(
        f"""
        (global_label "{name}" (shape {shape}) (at {fmt(x)} {fmt(y)} {angle})
          {effects(justify=label_justify(angle))}
          (uuid {uuid_str()})
          (property "Intersheetrefs" "${{INTERSHEET_REFS}}" (at 0 0 0)
            {effects(hide=True)}
          )
        )
        """
    ).strip()


def make_no_connect(x: float, y: float) -> str:
    return f'(no_connect (at {fmt(x)} {fmt(y)}) (uuid {uuid_str()}))'


def make_text(value: str, x: float, y: float) -> str:
    return textwrap.dedent(
        f"""
        (text "{value}" (at {fmt(x)} {fmt(y)} 0)
          {effects(justify="left bottom")}
          (uuid {uuid_str()})
        )
        """
    ).strip()


def write_custom_library() -> None:
    SYMBOL_DIR.mkdir(parents=True, exist_ok=True)
    body = [
        '(kicad_symbol_lib (version 20220914) (generator generate_schematic)',
    ]
    for block in CUSTOM_SYMBOLS.values():
        body.append(indent_block(block, "  "))
    body.append(')')
    CUSTOM_LIB_PATH.write_text("\n".join(body) + "\n", encoding="utf-8")


def write_project_file() -> None:
    data = {
        "board": {},
        "cvpcb": {},
        "erc": {},
        "libraries": {
            "pinned_footprint_libs": [],
            "pinned_symbol_libs": [],
        },
        "meta": {
            "filename": PROJECT_PATH.name,
            "version": 1,
        },
        "net_settings": {},
        "pcbnew": {},
        "schematic": {
            "legacy_lib_dir": "",
            "legacy_lib_list": [],
        },
        "sheets": [],
        "text_variables": {},
    }
    PROJECT_PATH.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def build_repositories() -> tuple[dict[str, SymbolRepository], dict[tuple[str, str], SymbolRepository], list[str]]:
    repos: dict[str, SymbolRepository] = {}
    repo_map: dict[tuple[str, str], SymbolRepository] = {}
    embedded_blocks: list[str] = []

    for library, names in STANDARD_SYMBOLS.items():
        repo = SymbolRepository(library, SYSTEM_SYMBOL_DIR / f"{library}.kicad_sym")
        repos[library] = repo
        for name in names:
            repo_map[(library, name)] = repo
            embedded_blocks.append(embedded_symbol_block(repo, name, library))

    custom_repo = SymbolRepository("Custom", CUSTOM_LIB_PATH)
    repos["Custom"] = custom_repo
    for name in CUSTOM_SYMBOLS:
        repo_map[("Custom", name)] = custom_repo
        embedded_blocks.append(prefix_symbol_block(custom_repo.raw_blocks[name], "Custom"))

    return repos, repo_map, embedded_blocks


def component_by_ref(components: list[Component]) -> dict[str, Component]:
    return {component.ref: component for component in components}


def find_pin(repo_map: dict[tuple[str, str], SymbolRepository], component: Component, pin_id: str) -> Pin:
    repo = repo_map[component.symbol_key]
    for pin in repo.pins(component.symbol_key[1]):
        if pin.number == pin_id or pin.name == pin_id:
            return pin
    raise KeyError(f"Pin {pin_id} not found on {component.ref}")


def main() -> None:
    write_custom_library()
    write_project_file()
    _, repo_map, embedded_blocks = build_repositories()

    components = [
        Component("J1", "Connector:USB_C_Receptacle", ("Connector", "USB_C_Receptacle"), 50, 50, value="USB_C_Receptacle"),
        Component("J2", "Connector_Generic:Conn_01x02", ("Connector_Generic", "Conn_01x02"), 50, 100, value="12V_IN"),
        Component("D1", "Diode:SS34", ("Diode", "SS34"), 80, 100, value="SS34"),
        Component("U4", "Custom:MP1584EN", ("Custom", "MP1584EN"), 120, 85, value="MP1584EN"),
        Component("U2", "Custom:TP4056", ("Custom", "TP4056"), 120, 130, value="TP4056"),
        Component("BT1", "Device:Battery", ("Device", "Battery"), 160, 130, value="18650"),
        Component("Q1", "Transistor_FET:AO3401A", ("Transistor_FET", "AO3401A"), 180, 100, value="AO3401A"),
        Component("U3", "Regulator_Linear:AMS1117-3.3", ("Regulator_Linear", "AMS1117-3.3"), 220, 100, value="AMS1117-3.3"),
        Component("U1", "Custom:ESP32-C3-Super-Mini", ("Custom", "ESP32-C3-Super-Mini"), 200, 170, value="ESP32-C3-Super-Mini"),
        Component("J3", "Connector_Generic:Conn_01x04", ("Connector_Generic", "Conn_01x04"), 280, 170, value="NeoTrellis_JST_PH"),
        Component("R1", "Device:R", ("Device", "R"), 175, 155, value="100k"),
        Component("R2", "Device:R", ("Device", "R"), 175, 180, value="100k"),
        Component("R3", "Device:R", ("Device", "R"), 245, 160, value="4.7k"),
        Component("R4", "Device:R", ("Device", "R"), 245, 180, value="4.7k"),
        Component("R5", "Device:R", ("Device", "R"), 95, 140, value="1.2k"),
        Component("R6", "Device:R", ("Device", "R"), 165, 112, value="100k"),
        Component("R7", "Device:R", ("Device", "R"), 150, 70, value="47k"),
        Component("R8", "Device:R", ("Device", "R"), 150, 95, value="10k"),
        Component("C1", "Device:C", ("Device", "C"), 210, 80, value="10uF"),
        Component("C2", "Device:C", ("Device", "C"), 230, 80, value="10uF"),
        Component("C3", "Device:C", ("Device", "C"), 225, 150, value="100nF"),
        Component("C4", "Device:C", ("Device", "C"), 160, 60, value="22uF"),
        Component("C5", "Device:C", ("Device", "C"), 175, 60, value="22uF"),
        Component("C6", "Device:C", ("Device", "C"), 100, 60, value="10uF"),
        Component("L1", "Device:L", ("Device", "L"), 145, 50, value="10uH"),
    ]
    by_ref = component_by_ref(components)

    power_components: list[Component] = []
    labels: list[str] = []
    global_labels: list[str] = []
    no_connects: list[str] = []
    texts = [
        make_text("+5V rail is simplified: USB VBUS and MP1584 output are tied together for prototype review.", 95, 28),
        make_text("Q1 power-path MOSFET is shown in simplified form; review battery switchover intent in KiCad GUI.", 150, 118),
    ]

    pwr_counts = {"#PWR": 1, "#FLG": 1}

    def add_power(net: str, component_ref: str, pin_id: str) -> None:
        component = by_ref[component_ref]
        pin = find_pin(repo_map, component, pin_id)
        x, y = point_for(component, pin)
        ref = f"#PWR{pwr_counts['#PWR']:02d}"
        pwr_counts['#PWR'] += 1
        power_components.append(
            Component(ref, f"power:{net}", ("power", net), x, y, value=net, in_bom="no", on_board="no")
        )

    def add_flag(component_ref: str, pin_id: str) -> None:
        component = by_ref[component_ref]
        pin = find_pin(repo_map, component, pin_id)
        x, y = point_for(component, pin)
        ref = f"#FLG{pwr_counts['#FLG']:02d}"
        pwr_counts['#FLG'] += 1
        power_components.append(
            Component(ref, "power:PWR_FLAG", ("power", "PWR_FLAG"), x, y, value="PWR_FLAG", in_bom="no", on_board="no")
        )

    def add_label(name: str, component_ref: str, pin_id: str) -> None:
        component = by_ref[component_ref]
        pin = find_pin(repo_map, component, pin_id)
        x, y = point_for(component, pin)
        labels.append(make_label(name, x, y, 0))

    def add_global(name: str, component_ref: str, pin_id: str) -> None:
        component = by_ref[component_ref]
        pin = find_pin(repo_map, component, pin_id)
        x, y = point_for(component, pin)
        global_labels.append(make_global_label(name, x, y, shape="input", angle=0))

    def add_nc(component_ref: str, pin_id: str) -> None:
        component = by_ref[component_ref]
        pin = find_pin(repo_map, component, pin_id)
        x, y = point_for(component, pin)
        no_connects.append(make_no_connect(x, y))

    for pin_id in ["1", "2", "3", "4", "5"]:
        pass

    add_label("12V_RAW", "J2", "1")
    add_power("GND", "J2", "2")
    add_label("12V_RAW", "D1", "1")
    add_power("+12V", "D1", "2")
    add_flag("D1", "2")

    add_power("+12V", "U4", "1")
    add_power("+12V", "U4", "2")
    add_label("SW", "U4", "3")
    add_power("+12V", "U4", "4")
    add_power("GND", "U4", "5")
    add_power("GND", "U4", "6")
    add_label("FB", "U4", "7")
    add_nc("U4", "8")

    add_power("+12V", "C6", "1")
    add_power("GND", "C6", "2")
    add_label("SW", "L1", "1")
    add_power("+5V", "L1", "2")
    add_power("+5V", "C4", "1")
    add_power("GND", "C4", "2")
    add_power("+5V", "C5", "1")
    add_power("GND", "C5", "2")
    add_power("+5V", "R7", "1")
    add_label("FB", "R7", "2")
    add_label("FB", "R8", "1")
    add_power("GND", "R8", "2")

    for pin_id in ["A1", "A12", "B1", "B12", "S1"]:
        add_power("GND", "J1", pin_id)
    for pin_id in ["A4", "A9", "B4", "B9"]:
        add_power("+5V", "J1", pin_id)
    for pin_id in ["A10", "A11", "A2", "A3", "A5", "A6", "A7", "A8", "B10", "B11", "B2", "B3", "B5", "B6", "B7", "B8"]:
        add_nc("J1", pin_id)
    add_flag("J1", "A4")

    add_power("GND", "U2", "1")
    add_label("PROG", "U2", "2")
    add_power("GND", "U2", "3")
    add_power("+5V", "U2", "4")
    add_global("VBATT", "U2", "5")
    add_nc("U2", "6")
    add_nc("U2", "7")
    add_power("+5V", "U2", "8")
    add_label("PROG", "R5", "1")
    add_power("GND", "R5", "2")

    add_global("VBATT", "BT1", "1")
    add_power("GND", "BT1", "2")
    add_flag("BT1", "1")

    add_label("Q1_GATE", "Q1", "1")
    add_power("+5V", "Q1", "2")
    add_global("VBATT", "Q1", "3")
    add_label("Q1_GATE", "R6", "1")
    add_power("GND", "R6", "2")

    add_power("+5V", "U3", "3")
    add_power("GND", "U3", "1")
    add_power("+3V3", "U3", "2")
    add_power("+5V", "C1", "1")
    add_power("GND", "C1", "2")
    add_power("+3V3", "C2", "1")
    add_power("GND", "C2", "2")

    add_global("VBATT", "R1", "1")
    add_label("BATT_ADC", "R1", "2")
    add_label("BATT_ADC", "R2", "1")
    add_power("GND", "R2", "2")
    add_power("+3V3", "R3", "1")
    add_label("SDA", "R3", "2")
    add_power("+3V3", "R4", "1")
    add_label("SCL", "R4", "2")
    add_power("+3V3", "C3", "1")
    add_power("GND", "C3", "2")

    add_power("+5V", "U1", "9")
    add_power("GND", "U1", "10")
    add_power("+3V3", "U1", "11")
    add_label("BATT_ADC", "U1", "13")
    add_label("SCL", "U1", "3")
    add_label("SDA", "U1", "16")
    for pin_id in ["1", "2", "4", "5", "6", "7", "8", "12", "14", "15"]:
        add_nc("U1", pin_id)

    add_power("+3V3", "J3", "1")
    add_power("GND", "J3", "2")
    add_label("SDA", "J3", "3")
    add_label("SCL", "J3", "4")

    root_uuid = uuid_str()
    lines = [
        '(kicad_sch (version 20230121) (generator generate_schematic)',
        '',
        f'  (uuid {root_uuid})',
        '',
        '  (paper "A3" portrait)',
        '',
        '  (title_block',
        '    (title "ESP32 NeoTrellis Box")',
        '    (company "tsayles")',
        '  )',
        '',
        '  (lib_symbols',
    ]
    for block in embedded_blocks:
        lines.append(indent_block(block, '    '))
    lines.extend(['  )', ''])

    for item in texts + global_labels + labels + no_connects:
        lines.append(indent_block(item, '  '))
        lines.append('')

    for component in components + power_components:
        lines.append(indent_block(instantiate_component(component, repo_map, root_uuid), '  '))
        lines.append('')

    lines.extend(
        [
            '  (sheet_instances',
            '    (path "/" (page "1"))',
            '  )',
            ')',
            '',
        ]
    )
    SCHEMATIC_PATH.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
