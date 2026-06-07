#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import textwrap
import uuid
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
KICAD_DIR = ROOT / "hardware" / "kicad"
SYMBOL_DIR = KICAD_DIR / "symbols"
CUSTOM_LIB_PATH = SYMBOL_DIR / "Custom.kicad_sym"
PROJECT_PATH = KICAD_DIR / "esp32_neotrellis_box.kicad_pro"
SCHEMATIC_PATH = KICAD_DIR / "esp32_neotrellis_box.kicad_sch"
PROJECT_NAME = "esp32_neotrellis_box"
SYSTEM_SYMBOL_DIR = Path("/usr/share/kicad/symbols")

PROJECT_UUID = gen_sheet_uuid = None
SHEET_UUID = None
POWER_COUNTER = 0
FLAG_COUNTER = 0

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
            (pin bidirectional line (at -15.24 -17.78 0) (length 2.54)
              (name "GPIO21/TX" (effects (font (size 1.016 1.016))))
              (number "1" (effects (font (size 1.016 1.016))))
            )
            (pin bidirectional line (at -15.24 -12.7 0) (length 2.54)
              (name "GPIO20/RX" (effects (font (size 1.016 1.016))))
              (number "2" (effects (font (size 1.016 1.016))))
            )
            (pin bidirectional line (at -15.24 -7.62 0) (length 2.54)
              (name "GPIO10" (effects (font (size 1.016 1.016))))
              (number "3" (effects (font (size 1.016 1.016))))
            )
            (pin bidirectional line (at -15.24 -2.54 0) (length 2.54)
              (name "GPIO9/BOOT" (effects (font (size 1.016 1.016))))
              (number "4" (effects (font (size 1.016 1.016))))
            )
            (pin bidirectional line (at -15.24 2.54 0) (length 2.54)
              (name "GPIO8/LED" (effects (font (size 1.016 1.016))))
              (number "5" (effects (font (size 1.016 1.016))))
            )
            (pin bidirectional line (at -15.24 7.62 0) (length 2.54)
              (name "GPIO7" (effects (font (size 1.016 1.016))))
              (number "6" (effects (font (size 1.016 1.016))))
            )
            (pin bidirectional line (at -15.24 12.7 0) (length 2.54)
              (name "GPIO6" (effects (font (size 1.016 1.016))))
              (number "7" (effects (font (size 1.016 1.016))))
            )
            (pin bidirectional line (at -15.24 17.78 0) (length 2.54)
              (name "GPIO5" (effects (font (size 1.016 1.016))))
              (number "8" (effects (font (size 1.016 1.016))))
            )
            (pin power_in line (at 15.24 -17.78 180) (length 2.54)
              (name "5V" (effects (font (size 1.016 1.016))))
              (number "9" (effects (font (size 1.016 1.016))))
            )
            (pin power_in line (at 15.24 -12.7 180) (length 2.54)
              (name "GND" (effects (font (size 1.016 1.016))))
              (number "10" (effects (font (size 1.016 1.016))))
            )
            (pin power_in line (at 15.24 -7.62 180) (length 2.54)
              (name "3V3" (effects (font (size 1.016 1.016))))
              (number "11" (effects (font (size 1.016 1.016))))
            )
            (pin bidirectional line (at 15.24 -2.54 180) (length 2.54)
              (name "GPIO4" (effects (font (size 1.016 1.016))))
              (number "12" (effects (font (size 1.016 1.016))))
            )
            (pin input line (at 15.24 2.54 180) (length 2.54)
              (name "GPIO3/ADC" (effects (font (size 1.016 1.016))))
              (number "13" (effects (font (size 1.016 1.016))))
            )
            (pin bidirectional line (at 15.24 7.62 180) (length 2.54)
              (name "GPIO2" (effects (font (size 1.016 1.016))))
              (number "14" (effects (font (size 1.016 1.016))))
            )
            (pin bidirectional line (at 15.24 12.7 180) (length 2.54)
              (name "GPIO1" (effects (font (size 1.016 1.016))))
              (number "15" (effects (font (size 1.016 1.016))))
            )
            (pin bidirectional line (at 15.24 17.78 180) (length 2.54)
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
            (rectangle (start -5.08 10.16) (end 5.08 -10.16)
              (stroke (width 0.254) (type default))
              (fill (type background))
            )
          )
          (symbol "TP4056_1_1"
            (pin input line (at -7.62 -8.89 0) (length 2.54)
              (name "TEMP" (effects (font (size 1.016 1.016))))
              (number "1" (effects (font (size 1.016 1.016))))
            )
            (pin input line (at -7.62 -2.54 0) (length 2.54)
              (name "PROG" (effects (font (size 1.016 1.016))))
              (number "2" (effects (font (size 1.016 1.016))))
            )
            (pin power_in line (at -7.62 2.54 0) (length 2.54)
              (name "GND" (effects (font (size 1.016 1.016))))
              (number "3" (effects (font (size 1.016 1.016))))
            )
            (pin power_in line (at -7.62 8.89 0) (length 2.54)
              (name "VCC" (effects (font (size 1.016 1.016))))
              (number "4" (effects (font (size 1.016 1.016))))
            )
            (pin passive line (at 7.62 -8.89 180) (length 2.54)
              (name "BAT" (effects (font (size 1.016 1.016))))
              (number "5" (effects (font (size 1.016 1.016))))
            )
            (pin output line (at 7.62 -2.54 180) (length 2.54)
              (name "CHRG" (effects (font (size 1.016 1.016))))
              (number "6" (effects (font (size 1.016 1.016))))
            )
            (pin output line (at 7.62 2.54 180) (length 2.54)
              (name "STDBY" (effects (font (size 1.016 1.016))))
              (number "7" (effects (font (size 1.016 1.016))))
            )
            (pin input line (at 7.62 8.89 180) (length 2.54)
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
            (rectangle (start -5.08 10.16) (end 5.08 -10.16)
              (stroke (width 0.254) (type default))
              (fill (type background))
            )
          )
          (symbol "MP1584EN_1_1"
            (pin input line (at -7.62 -8.89 0) (length 2.54)
              (name "EN" (effects (font (size 1.016 1.016))))
              (number "1" (effects (font (size 1.016 1.016))))
            )
            (pin power_in line (at -7.62 -2.54 0) (length 2.54)
              (name "VIN" (effects (font (size 1.016 1.016))))
              (number "2" (effects (font (size 1.016 1.016))))
            )
            (pin output line (at -7.62 2.54 0) (length 2.54)
              (name "SW" (effects (font (size 1.016 1.016))))
              (number "3" (effects (font (size 1.016 1.016))))
            )
            (pin power_in line (at -7.62 8.89 0) (length 2.54)
              (name "VIN_EP" (effects (font (size 1.016 1.016))))
              (number "4" (effects (font (size 1.016 1.016))))
            )
            (pin power_in line (at 7.62 -8.89 180) (length 2.54)
              (name "GND" (effects (font (size 1.016 1.016))))
              (number "5" (effects (font (size 1.016 1.016))))
            )
            (pin power_in line (at 7.62 -2.54 180) (length 2.54)
              (name "GND2" (effects (font (size 1.016 1.016))))
              (number "6" (effects (font (size 1.016 1.016))))
            )
            (pin input line (at 7.62 2.54 180) (length 2.54)
              (name "FB" (effects (font (size 1.016 1.016))))
              (number "7" (effects (font (size 1.016 1.016))))
            )
            (pin passive line (at 7.62 8.89 180) (length 2.54)
              (name "COMP" (effects (font (size 1.016 1.016))))
              (number "8" (effects (font (size 1.016 1.016))))
            )
          )
        )
        """
    ).strip(),
}

SYSTEM_SYMBOLS = [
    ("Connector_Generic", "Conn_01x02"),
    ("Connector_Generic", "Conn_01x04"),
    ("Device", "Battery"),
    ("Device", "C"),
    ("Device", "L"),
    ("Device", "R"),
    ("Diode", "SS34"),
    ("Regulator_Linear", "AMS1117-3.3"),
    ("Transistor_FET", "AO3401A"),
    ("power", "+3V3"),
    ("power", "+5V"),
    ("power", "GND"),
    ("power", "PWR_FLAG"),
]

PIN_ENDPOINTS = {
    ("Device:R", 0): {"1": (0.0, 3.81), "2": (0.0, -3.81)},
    ("Device:R", 90): {"1": (-3.81, 0.0), "2": (3.81, 0.0)},
    ("Device:C", 0): {"1": (0.0, 3.81), "2": (0.0, -3.81)},
    ("Device:L", 0): {"1": (0.0, 3.81), "2": (0.0, -3.81)},
    ("Device:Battery", 0): {"1": (0.0, 5.08), "2": (0.0, -5.08)},
    ("Connector_Generic:Conn_01x02", 0): {"1": (-5.08, 0.0), "2": (-5.08, -2.54)},
    ("Connector_Generic:Conn_01x04", 0): {
        "1": (-5.08, 2.54),
        "2": (-5.08, 0.0),
        "3": (-5.08, -2.54),
        "4": (-5.08, -5.08),
    },
    ("Diode:SS34", 0): {"1": (-3.81, 0.0), "2": (3.81, 0.0)},
    ("Regulator_Linear:AMS1117-3.3", 0): {
        "1": (0.0, -7.62),
        "2": (7.62, 0.0),
        "3": (-7.62, 0.0),
    },
    ("Transistor_FET:AO3401A", 0): {
        "1": (-5.08, 0.0),
        "2": (2.54, -5.08),
        "3": (2.54, 5.08),
    },
    ("Custom:ESP32-C3-Super-Mini", 0): {
        "1": (-15.24, -17.78),
        "2": (-15.24, -12.70),
        "3": (-15.24, -7.62),
        "4": (-15.24, -2.54),
        "5": (-15.24, 2.54),
        "6": (-15.24, 7.62),
        "7": (-15.24, 12.70),
        "8": (-15.24, 17.78),
        "9": (15.24, -17.78),
        "10": (15.24, -12.70),
        "11": (15.24, -7.62),
        "12": (15.24, -2.54),
        "13": (15.24, 2.54),
        "14": (15.24, 7.62),
        "15": (15.24, 12.70),
        "16": (15.24, 17.78),
    },
    ("Custom:TP4056", 0): {
        "1": (-7.62, -8.89),
        "2": (-7.62, -2.54),
        "3": (-7.62, 2.54),
        "4": (-7.62, 8.89),
        "5": (7.62, -8.89),
        "6": (7.62, -2.54),
        "7": (7.62, 2.54),
        "8": (7.62, 8.89),
    },
    ("Custom:MP1584EN", 0): {
        "1": (-7.62, -8.89),
        "2": (-7.62, -2.54),
        "3": (-7.62, 2.54),
        "4": (-7.62, 8.89),
        "5": (7.62, -8.89),
        "6": (7.62, -2.54),
        "7": (7.62, 2.54),
        "8": (7.62, 8.89),
    },
}

COMPONENTS = [
    {
        "lib_id": "Connector_Generic:Conn_01x02",
        "ref": "J2",
        "value": "12V Barrel",
        "cx": 40.0,
        "cy": 100.0,
        "rotation": 0,
        "footprint": "",
        "pin_nets": [("1", "label", "12V_IN"), ("2", "power", "GND")],
    },
    {
        "lib_id": "Connector_Generic:Conn_01x02",
        "ref": "J1",
        "value": "USB-C Power",
        "cx": 40.0,
        "cy": 50.0,
        "rotation": 0,
        "footprint": "",
        "pin_nets": [("1", "power", "+5V"), ("2", "power", "GND")],
    },
    {
        "lib_id": "Diode:SS34",
        "ref": "D1",
        "value": "SS34",
        "cx": 75.0,
        "cy": 100.0,
        "rotation": 0,
        "footprint": "Diode_SMD:D_SMA",
        "pin_nets": [("1", "label", "12V_IN"), ("2", "label", "12V_PROT")],
    },
    {
        "lib_id": "Custom:MP1584EN",
        "ref": "U4",
        "value": "MP1584EN",
        "cx": 115.0,
        "cy": 85.0,
        "rotation": 0,
        "footprint": "Package_SO:SOP-8_3.9x4.9mm_P1.27mm",
        "pin_nets": [
            ("1", "label", "12V_PROT"),
            ("2", "label", "12V_PROT"),
            ("3", "label", "SW_NODE"),
            ("4", "label", "12V_PROT"),
            ("5", "power", "GND"),
            ("6", "power", "GND"),
            ("7", "label", "FB_5V"),
            ("8", "label", "COMP_5V"),
        ],
    },
    {
        "lib_id": "Device:L",
        "ref": "L1",
        "value": "10uH",
        "cx": 140.0,
        "cy": 75.0,
        "rotation": 0,
        "footprint": "",
        "pin_nets": [("1", "label", "SW_NODE"), ("2", "power", "+5V")],
    },
    {
        "lib_id": "Device:R",
        "ref": "R7",
        "value": "100k",
        "cx": 140.0,
        "cy": 90.0,
        "rotation": 0,
        "footprint": "",
        "pin_nets": [("1", "power", "+5V"), ("2", "label", "FB_5V")],
    },
    {
        "lib_id": "Device:R",
        "ref": "R8",
        "value": "39k",
        "cx": 140.0,
        "cy": 100.0,
        "rotation": 0,
        "footprint": "",
        "pin_nets": [("1", "label", "FB_5V"), ("2", "power", "GND")],
    },
    {
        "lib_id": "Device:C",
        "ref": "C6",
        "value": "10uF",
        "cx": 110.0,
        "cy": 95.0,
        "rotation": 0,
        "footprint": "",
        "pin_nets": [("1", "label", "12V_PROT"), ("2", "power", "GND")],
    },
    {
        "lib_id": "Device:C",
        "ref": "C4",
        "value": "22uF",
        "cx": 155.0,
        "cy": 75.0,
        "rotation": 0,
        "footprint": "",
        "pin_nets": [("1", "power", "+5V"), ("2", "power", "GND")],
    },
    {
        "lib_id": "Custom:TP4056",
        "ref": "U2",
        "value": "TP4056",
        "cx": 115.0,
        "cy": 130.0,
        "rotation": 0,
        "footprint": "Package_SO:SOP-8_3.9x4.9mm_P1.27mm",
        "pin_nets": [
            ("1", "power", "GND"),
            ("2", "label", "PROG_1A"),
            ("3", "power", "GND"),
            ("4", "power", "+5V"),
            ("5", "label", "VBATT"),
            ("6", "nc", ""),
            ("7", "nc", ""),
            ("8", "power", "+5V"),
        ],
    },
    {
        "lib_id": "Device:R",
        "ref": "R5",
        "value": "1.2k",
        "cx": 95.0,
        "cy": 132.0,
        "rotation": 0,
        "footprint": "",
        "pin_nets": [("1", "label", "PROG_1A"), ("2", "power", "GND")],
    },
    {
        "lib_id": "Device:Battery",
        "ref": "BT1",
        "value": "18650",
        "cx": 155.0,
        "cy": 130.0,
        "rotation": 0,
        "footprint": "",
        "pin_nets": [("1", "label", "VBATT"), ("2", "power", "GND")],
    },
    {
        "lib_id": "Transistor_FET:AO3401A",
        "ref": "Q1",
        "value": "AO3401A",
        "cx": 180.0,
        "cy": 100.0,
        "rotation": 0,
        "footprint": "Package_TO_SOT_SMD:SOT-23",
        "pin_nets": [("1", "label", "Q1_GATE"), ("2", "power", "+5V"), ("3", "label", "VBATT")],
    },
    {
        "lib_id": "Device:R",
        "ref": "R6",
        "value": "100k",
        "cx": 168.0,
        "cy": 100.0,
        "rotation": 90,
        "footprint": "",
        "pin_nets": [("1", "power", "+5V"), ("2", "label", "Q1_GATE")],
    },
    {
        "lib_id": "Regulator_Linear:AMS1117-3.3",
        "ref": "U3",
        "value": "AMS1117-3.3",
        "cx": 220.0,
        "cy": 100.0,
        "rotation": 0,
        "footprint": "Package_TO_SOT_SMD:SOT-223-3_TabPin2",
        "pin_nets": [("1", "power", "GND"), ("2", "power", "+3V3"), ("3", "power", "+5V")],
    },
    {
        "lib_id": "Device:C",
        "ref": "C1",
        "value": "10uF",
        "cx": 213.0,
        "cy": 113.0,
        "rotation": 0,
        "footprint": "",
        "pin_nets": [("1", "power", "+5V"), ("2", "power", "GND")],
    },
    {
        "lib_id": "Device:C",
        "ref": "C2",
        "value": "10uF",
        "cx": 228.0,
        "cy": 113.0,
        "rotation": 0,
        "footprint": "",
        "pin_nets": [("1", "power", "+3V3"), ("2", "power", "GND")],
    },
    {
        "lib_id": "Device:C",
        "ref": "C3",
        "value": "100nF",
        "cx": 228.0,
        "cy": 170.0,
        "rotation": 0,
        "footprint": "",
        "pin_nets": [("1", "power", "+3V3"), ("2", "power", "GND")],
    },
    {
        "lib_id": "Connector_Generic:Conn_01x04",
        "ref": "J3",
        "value": "NeoTrellis",
        "cx": 280.0,
        "cy": 170.0,
        "rotation": 0,
        "footprint": "",
        "pin_nets": [
            ("1", "power", "+3V3"),
            ("2", "power", "GND"),
            ("3", "label", "SDA"),
            ("4", "label", "SCL"),
        ],
    },
    {
        "lib_id": "Device:R",
        "ref": "R3",
        "value": "4.7k",
        "cx": 245.0,
        "cy": 150.0,
        "rotation": 0,
        "footprint": "",
        "pin_nets": [("1", "power", "+3V3"), ("2", "label", "SDA")],
    },
    {
        "lib_id": "Device:R",
        "ref": "R4",
        "value": "4.7k",
        "cx": 245.0,
        "cy": 165.0,
        "rotation": 0,
        "footprint": "",
        "pin_nets": [("1", "power", "+3V3"), ("2", "label", "SCL")],
    },
    {
        "lib_id": "Device:R",
        "ref": "R1",
        "value": "100k",
        "cx": 175.0,
        "cy": 155.0,
        "rotation": 0,
        "footprint": "",
        "pin_nets": [("1", "label", "VBATT"), ("2", "label", "BATT_ADC")],
    },
    {
        "lib_id": "Device:R",
        "ref": "R2",
        "value": "100k",
        "cx": 175.0,
        "cy": 180.0,
        "rotation": 0,
        "footprint": "",
        "pin_nets": [("1", "label", "BATT_ADC"), ("2", "power", "GND")],
    },
    {
        "lib_id": "Custom:ESP32-C3-Super-Mini",
        "ref": "U1",
        "value": "ESP32-C3-Super-Mini",
        "cx": 200.0,
        "cy": 170.0,
        "rotation": 0,
        "footprint": "",
        "pin_nets": [
            ("1", "nc", ""),
            ("2", "nc", ""),
            ("3", "label", "SCL"),
            ("4", "nc", ""),
            ("5", "nc", ""),
            ("6", "nc", ""),
            ("7", "nc", ""),
            ("8", "nc", ""),
            ("9", "nc", ""),
            ("10", "power", "GND"),
            ("11", "power", "+3V3"),
            ("12", "nc", ""),
            ("13", "label", "BATT_ADC"),
            ("14", "nc", ""),
            ("15", "nc", ""),
            ("16", "label", "SDA"),
        ],
    },
]

PWR_FLAGS = [("+5V", 50.0, 40.0), ("GND", 50.0, 45.0)]


def gen_uid() -> str:
    return str(uuid.uuid4())


def fmt(value: float) -> str:
    return f"{value:.3f}".rstrip("0").rstrip(".")


def indent_block(block: str, prefix: str = "    ") -> str:
    return "\n".join(prefix + line if line else line for line in block.splitlines())


def extract_balanced(text: str, start: int) -> str:
    depth = 0
    in_string = False
    escape = False
    for idx in range(start, len(text)):
        char = text[idx]
        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start : idx + 1]

    raise ValueError("unterminated s-expression")


def split_symbol_block(block: str) -> tuple[str, list[str]]:
    newline = block.find("\n")
    if newline == -1:
        return block[:-1], []
    header = block[:newline]
    children: list[str] = []
    idx = newline + 1
    end = len(block) - 1
    while idx < end:
        while idx < end and block[idx].isspace():
            idx += 1
        if idx >= end:
            break
        child = extract_balanced(block, idx)
        children.append(child)
        idx += len(child)
    return header, children


def rename_top_symbol(block: str, old_name: str, new_name: str) -> str:
    return block.replace(f'(symbol "{old_name}"', f'(symbol "{new_name}"', 1)


def rename_nested_symbol(block: str, old_prefix: str, new_prefix: str) -> str:
    return re.sub(
        rf'^\(symbol "{re.escape(old_prefix)}([^"]+)"',
        rf'(symbol "{new_prefix}\1"',
        block,
        count=1,
    )


def rewrite_symbol_block(block: str, lib_name: str, lib_text: str) -> str:
    match = re.match(r'\(symbol "([^"]+)"', block)
    if not match:
        raise ValueError("invalid symbol block")
    name = match.group(1)
    extend_match = re.search(r'\(extends "([^"]+)"\)', block)
    if not extend_match:
        return rename_top_symbol(block, name, f"{lib_name}:{name}")

    parent_name = extend_match.group(1)
    parent_marker = f'(symbol "{parent_name}"'
    parent_start = lib_text.find(parent_marker)
    if parent_start == -1:
        raise ValueError(f"parent symbol {parent_name} not found in {lib_name}")
    parent_block = extract_balanced(lib_text, parent_start)

    child_header, child_children = split_symbol_block(block)
    child_header = child_header.replace(
        f'(symbol "{name}"',
        f'(symbol "{lib_name}:{name}"',
        1,
    )
    child_header = re.sub(r'\s+\(extends "[^"]+"\)', '', child_header, count=1)

    _, parent_children = split_symbol_block(parent_block)
    merged_children = [child for child in child_children if child.startswith('(property ')]
    for child in parent_children:
        if child.startswith('(symbol "'):
            merged_children.append(rename_nested_symbol(child, f"{parent_name}_", f"{name}_"))

    lines = [child_header]
    for child in merged_children:
        lines.extend('  ' + line for line in child.splitlines())
    lines.append(')')
    return '\n'.join(lines)


def extract_symbol(lib_path: Path, sym_name: str, seen: OrderedDict[str, str] | None = None) -> OrderedDict[str, str]:
    lib_name = lib_path.stem
    if seen is None:
        seen = OrderedDict()
    key = f"{lib_name}:{sym_name}"
    if key in seen:
        return seen

    lib_text = lib_path.read_text()
    marker = f'(symbol "{sym_name}"'
    start = lib_text.find(marker)
    if start == -1:
        raise ValueError(f"symbol {sym_name} not found in {lib_path}")

    block = extract_balanced(lib_text, start)
    seen[key] = rewrite_symbol_block(block, lib_name, lib_text)
    return seen


def make_power(net_name: str, x: float, y: float) -> str:
    global POWER_COUNTER
    POWER_COUNTER += 1
    ref = f"#PWR{POWER_COUNTER:02d}"
    uid = gen_uid()
    pin_uid = gen_uid()
    value_y = y + 3.81 if net_name == "GND" else y - 3.81
    return textwrap.dedent(
        f"""
          (symbol (lib_id "power:{net_name}") (at {fmt(x)} {fmt(y)} 0) (unit 1)
            (in_bom no) (on_board no) (dnp no)
            (uuid "{uid}")
            (property "Reference" "{ref}" (at {fmt(x)} {fmt(y + 6.35)} 0)
              (effects (font (size 1.27 1.27)) hide)
            )
            (property "Value" "{net_name}" (at {fmt(x)} {fmt(value_y)} 0)
              (effects (font (size 1.27 1.27)))
            )
            (property "Footprint" "" (at {fmt(x)} {fmt(y)} 0)
              (effects (font (size 1.27 1.27)) hide)
            )
            (property "Datasheet" "" (at {fmt(x)} {fmt(y)} 0)
              (effects (font (size 1.27 1.27)) hide)
            )
            (pin "1" (uuid "{pin_uid}"))
            (instances
              (project "{PROJECT_NAME}"
                (path "/{SHEET_UUID}"
                  (reference "{ref}") (unit 1)
                )
              )
            )
          )
        """
    ).strip()


def make_label(name: str, x: float, y: float, justify: str = "left") -> str:
    return textwrap.dedent(
        f"""
          (label "{name}" (at {fmt(x)} {fmt(y)} 0) (fields_autoplaced)
            (effects (font (size 1.27 1.27)) (justify {justify}))
            (uuid "{gen_uid()}")
          )
        """
    ).strip()


def make_no_connect(x: float, y: float) -> str:
    return f'  (no_connect (at {fmt(x)} {fmt(y)}) (uuid "{gen_uid()}"))'


def pin_offsets(lib_id: str, rotation: int) -> dict[str, tuple[float, float]]:
    key = (lib_id, rotation)
    if key not in PIN_ENDPOINTS:
        raise ValueError(f"missing pin offsets for {lib_id} rotation {rotation}")
    return PIN_ENDPOINTS[key]


def label_justify(rel_x: float) -> str:
    return "right" if rel_x < 0 else "left"


def make_component(
    lib_id: str,
    ref: str,
    value: str,
    cx: float,
    cy: float,
    rotation: int,
    footprint: str,
    pin_nets: list[tuple[str, str, str]],
) -> tuple[str, list[str]]:
    offsets = pin_offsets(lib_id, rotation)
    pin_lines = []
    attachments: list[str] = []
    for pin_number, net_type, net_name in pin_nets:
        if pin_number not in offsets:
            raise ValueError(f"pin {pin_number} missing from {lib_id}")
        rel_x, rel_y = offsets[pin_number]
        abs_x = cx + rel_x
        abs_y = cy - rel_y
        pin_lines.append(f'    (pin "{pin_number}" (uuid "{gen_uid()}"))')
        if net_type == "power":
            attachments.append(make_power(net_name, abs_x, abs_y))
        elif net_type == "label":
            attachments.append(make_label(net_name, abs_x, abs_y, label_justify(rel_x)))
        elif net_type == "nc":
            attachments.append(make_no_connect(abs_x, abs_y))
        else:
            raise ValueError(f"unsupported net type {net_type}")

    block = textwrap.dedent(
        f"""
          (symbol (lib_id "{lib_id}") (at {fmt(cx)} {fmt(cy)} {rotation}) (unit 1)
            (in_bom yes) (on_board yes) (dnp no)
            (uuid "{gen_uid()}")
            (property "Reference" "{ref}" (at {fmt(cx)} {fmt(cy + 6.35)} 0)
              (effects (font (size 1.27 1.27)))
            )
            (property "Value" "{value}" (at {fmt(cx)} {fmt(cy - 6.35)} 0)
              (effects (font (size 1.27 1.27)))
            )
            (property "Footprint" "{footprint}" (at {fmt(cx)} {fmt(cy)} 0)
              (effects (font (size 1.27 1.27)) hide)
            )
            (property "Datasheet" "" (at {fmt(cx)} {fmt(cy)} 0)
              (effects (font (size 1.27 1.27)) hide)
            )
        """
    ).strip("\n")
    block = "\n".join([block, *pin_lines])
    block += textwrap.dedent(
        f"""
            (instances
              (project "{PROJECT_NAME}"
                (path "/{SHEET_UUID}"
                  (reference "{ref}") (unit 1)
                )
              )
            )
          )
        """
    )
    return block.strip(), attachments


def make_pwr_flag(net_name: str, x: float, y: float) -> tuple[str, list[str]]:
    global FLAG_COUNTER
    FLAG_COUNTER += 1
    ref = f"#FLG{FLAG_COUNTER:02d}"
    block = textwrap.dedent(
        f"""
          (symbol (lib_id "power:PWR_FLAG") (at {fmt(x)} {fmt(y)} 0) (unit 1)
            (in_bom no) (on_board no) (dnp no)
            (uuid "{gen_uid()}")
            (property "Reference" "{ref}" (at {fmt(x)} {fmt(y + 6.35)} 0)
              (effects (font (size 1.27 1.27)) hide)
            )
            (property "Value" "PWR_FLAG" (at {fmt(x)} {fmt(y - 3.81)} 0)
              (effects (font (size 1.27 1.27)))
            )
            (property "Footprint" "" (at {fmt(x)} {fmt(y)} 0)
              (effects (font (size 1.27 1.27)) hide)
            )
            (property "Datasheet" "" (at {fmt(x)} {fmt(y)} 0)
              (effects (font (size 1.27 1.27)) hide)
            )
            (pin "1" (uuid "{gen_uid()}"))
            (instances
              (project "{PROJECT_NAME}"
                (path "/{SHEET_UUID}"
                  (reference "{ref}") (unit 1)
                )
              )
            )
          )
        """
    ).strip()
    return block, [make_power(net_name, x, y)]


def write_custom_library() -> None:
    SYMBOL_DIR.mkdir(parents=True, exist_ok=True)
    blocks = "\n".join(indent_block(block, "  ") for block in CUSTOM_SYMBOLS.values())
    content = "\n".join(
        [
            "(kicad_symbol_lib (version 20220914) (generator generate_schematic)",
            blocks,
            ")",
            "",
        ]
    )
    CUSTOM_LIB_PATH.write_text(content)


def write_project_file() -> None:
    project = {
        "board": {},
        "cvpcb": {},
        "erc": {},
        "libraries": {"pinned_footprint_libs": [], "pinned_symbol_libs": []},
        "meta": {"filename": PROJECT_PATH.name, "version": 1},
        "net_settings": {},
        "pcbnew": {},
        "schematic": {"legacy_lib_dir": "", "legacy_lib_list": []},
        "sheets": [],
        "text_variables": {},
    }
    PROJECT_PATH.write_text(json.dumps(project, indent=2) + "\n")


def build_lib_symbols() -> list[str]:
    symbols: OrderedDict[str, str] = OrderedDict()
    for lib_name, sym_name in SYSTEM_SYMBOLS:
        lib_path = SYSTEM_SYMBOL_DIR / f"{lib_name}.kicad_sym"
        extract_symbol(lib_path, sym_name, symbols)
    for sym_name in CUSTOM_SYMBOLS:
        extract_symbol(CUSTOM_LIB_PATH, sym_name, symbols)
    return list(symbols.values())


def write_schematic() -> None:
    lib_symbols = build_lib_symbols()
    component_blocks: list[str] = []
    attachment_blocks: list[str] = []

    for spec in COMPONENTS:
        block, attachments = make_component(**spec)
        component_blocks.append(block)
        attachment_blocks.extend(attachments)

    for net_name, x, y in PWR_FLAGS:
        block, attachments = make_pwr_flag(net_name, x, y)
        component_blocks.append(block)
        attachment_blocks.extend(attachments)

    lib_section = "\n".join(indent_block(block, "    ") for block in lib_symbols)
    attachments = "\n\n".join(attachment_blocks)
    components = "\n\n".join(component_blocks)

    schematic = "\n".join(
        [
            "(kicad_sch (version 20230121) (generator generate_schematic)",
            "",
            f"  (uuid {PROJECT_UUID})",
            "",
            '  (paper "A3")',
            "",
            "  (title_block",
            '    (title "ESP32 NeoTrellis Box")',
            '    (company "tsayles")',
            "  )",
            "",
            "  (lib_symbols",
            lib_section,
            "  )",
            "",
            attachments,
            "",
            components,
            "",
            "  (sheet_instances",
            '    (path "/" (page "1"))',
            "  )",
            ")",
            "",
        ]
    )
    SCHEMATIC_PATH.write_text(schematic)


def main() -> None:
    global PROJECT_UUID, SHEET_UUID, POWER_COUNTER, FLAG_COUNTER
    PROJECT_UUID = gen_uid()
    SHEET_UUID = gen_uid()
    POWER_COUNTER = 0
    FLAG_COUNTER = 0
    write_custom_library()
    write_project_file()
    write_schematic()


if __name__ == "__main__":
    main()
