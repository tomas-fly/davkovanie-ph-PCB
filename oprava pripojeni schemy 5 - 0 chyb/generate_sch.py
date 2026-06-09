#!/usr/bin/env python3
"""
pH/ORP Monitor v1.0 — KiCad Schematic Generator
Generates .kicad_sch file step by step.
"""

import uuid

def uid():
    return str(uuid.uuid4())

def snap(v):
    """Snap a coordinate to the nearest mil (0.0254mm) to match KiCad's internal grid."""
    mils = round(v / 0.0254)
    return round(mils * 0.0254, 4)

# ============================================================
# LIB SYMBOL DEFINITIONS
# ============================================================

def lib_symbol_power(name):
    """Generate a power symbol like +12V, +5V, +3V3, +5V_AN, -5V_AN"""
    is_negative = name.startswith("-")
    if is_negative:
        # Negative power symbol (arrow pointing down)
        gfx = f"""
    (symbol "{name}_0_1"
      (polyline
        (pts (xy -0.762 -1.27) (xy 0 -2.54))
        (stroke (width 0) (type default)) (fill (type none))
      )
      (polyline
        (pts (xy 0 -2.54) (xy 0.762 -1.27))
        (stroke (width 0) (type default)) (fill (type none))
      )
      (polyline
        (pts (xy 0 0) (xy 0 -2.54))
        (stroke (width 0) (type default)) (fill (type none))
      )
    )
    (symbol "{name}_1_1"
      (pin power_in line (at 0 0 270) (length 0)
        (name "" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
    )"""
    else:
        gfx = f"""
    (symbol "{name}_0_1"
      (polyline
        (pts (xy -0.762 1.27) (xy 0 2.54))
        (stroke (width 0) (type default)) (fill (type none))
      )
      (polyline
        (pts (xy 0 2.54) (xy 0.762 1.27))
        (stroke (width 0) (type default)) (fill (type none))
      )
      (polyline
        (pts (xy 0 0) (xy 0 2.54))
        (stroke (width 0) (type default)) (fill (type none))
      )
    )
    (symbol "{name}_1_1"
      (pin power_in line (at 0 0 90) (length 0)
        (name "" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
    )"""

    return f"""(symbol "power:{name}" (power) (pin_names (offset 0)) (in_bom yes) (on_board yes)
    (property "Reference" "#PWR" (at 0 -3.81 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Value" "{name}" (at 0 3.556 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Datasheet" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Description" "Power symbol creates a global label with name \\"{name}\\"" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "ki_keywords" "global power" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    ){gfx}
    (embedded_fonts no)
  )"""


LIB_GND = """(symbol "power:GND" (power) (pin_names (offset 0)) (in_bom yes) (on_board yes)
    (property "Reference" "#PWR" (at 0 -6.35 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Value" "GND" (at 0 -3.81 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Datasheet" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Description" "Power symbol creates a global label with name \\"GND\\"" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "ki_keywords" "global power" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (symbol "GND_0_1"
      (polyline
        (pts (xy 0 0) (xy 0 -1.27) (xy 1.27 -1.27) (xy 0 -2.54) (xy -1.27 -1.27) (xy 0 -1.27))
        (stroke (width 0) (type default)) (fill (type none))
      )
    )
    (symbol "GND_1_1"
      (pin power_in line (at 0 0 270) (length 0)
        (name "" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
    )
    (embedded_fonts no)
  )"""

LIB_PWR_FLAG = """(symbol "power:PWR_FLAG" (power) (pin_names (offset 0)) (in_bom yes) (on_board yes)
    (property "Reference" "#FLG" (at 0 1.905 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Value" "PWR_FLAG" (at 0 3.81 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Datasheet" "~" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Description" "Special symbol for telling ERC where power comes from" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "ki_keywords" "flag power" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (symbol "PWR_FLAG_0_0"
      (pin power_out line (at 0 0 90) (length 0)
        (name "" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
    )
    (symbol "PWR_FLAG_0_1"
      (polyline
        (pts (xy 0 0) (xy 0 1.27) (xy 1.016 1.778) (xy 0 2.286) (xy -1.016 1.778) (xy 0 1.27))
        (stroke (width 0) (type default)) (fill (type none))
      )
    )
    (embedded_fonts no)
  )"""

LIB_R = """(symbol "Device:R" (pin_numbers (hide yes)) (pin_names (offset 0))
    (exclude_from_sim no) (in_bom yes) (on_board yes)
    (property "Reference" "R" (at 2.032 0 90)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "R" (at -1.778 0 90)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at -1.778 0 90)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Datasheet" "~" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Description" "Resistor" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (symbol "R_0_1"
      (rectangle (start -1.016 2.54) (end 1.016 -2.54)
        (stroke (width 0.254) (type default)) (fill (type none))
      )
    )
    (symbol "R_1_1"
      (pin passive line (at 0 3.81 270) (length 1.27)
        (name "~" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at 0 -3.81 90) (length 1.27)
        (name "~" (effects (font (size 1.27 1.27))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
    )
    (embedded_fonts no)
  )"""

LIB_C = """(symbol "Device:C" (pin_numbers (hide yes)) (pin_names (offset 0.254))
    (exclude_from_sim no) (in_bom yes) (on_board yes)
    (property "Reference" "C" (at 0.635 2.54 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Value" "C" (at 0.635 -2.54 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Footprint" "" (at 0.9652 -3.81 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Datasheet" "~" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Description" "Unpolarized capacitor" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (symbol "C_0_1"
      (polyline
        (pts (xy -2.032 -0.762) (xy 2.032 -0.762))
        (stroke (width 0.508) (type default)) (fill (type none))
      )
      (polyline
        (pts (xy -2.032 0.762) (xy 2.032 0.762))
        (stroke (width 0.508) (type default)) (fill (type none))
      )
    )
    (symbol "C_1_1"
      (pin passive line (at 0 3.81 270) (length 2.794)
        (name "~" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at 0 -3.81 90) (length 2.794)
        (name "~" (effects (font (size 1.27 1.27))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
    )
    (embedded_fonts no)
  )"""

LIB_LED = """(symbol "Device:LED" (pin_numbers (hide yes)) (pin_names (offset 1.016) (hide yes))
    (exclude_from_sim no) (in_bom yes) (on_board yes)
    (property "Reference" "D" (at 0 2.54 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "LED" (at 0 -2.54 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Datasheet" "~" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Description" "Light emitting diode" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (symbol "LED_0_1"
      (polyline
        (pts (xy -1.27 -1.27) (xy -1.27 1.27))
        (stroke (width 0.254) (type default)) (fill (type none))
      )
      (polyline
        (pts (xy -1.27 0) (xy 1.27 0))
        (stroke (width 0) (type default)) (fill (type none))
      )
      (polyline
        (pts (xy 1.27 -1.27) (xy 1.27 1.27) (xy -1.27 0) (xy 1.27 -1.27))
        (stroke (width 0.254) (type default)) (fill (type none))
      )
      (polyline
        (pts (xy -3.048 -0.762) (xy -4.572 -2.286))
        (stroke (width 0) (type default)) (fill (type none))
      )
      (polyline
        (pts (xy -1.778 -0.762) (xy -3.302 -2.286))
        (stroke (width 0) (type default)) (fill (type none))
      )
      (polyline
        (pts (xy -3.048 -2.286) (xy -3.556 -1.778) (xy -3.556 -2.286) (xy -3.048 -2.286))
        (stroke (width 0) (type default)) (fill (type none))
      )
      (polyline
        (pts (xy -1.778 -2.286) (xy -2.286 -1.778) (xy -2.286 -2.286) (xy -1.778 -2.286))
        (stroke (width 0) (type default)) (fill (type none))
      )
    )
    (symbol "LED_1_1"
      (pin passive line (at -3.81 0 0) (length 2.54)
        (name "K" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at 3.81 0 180) (length 2.54)
        (name "A" (effects (font (size 1.27 1.27))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
    )
    (embedded_fonts no)
  )"""

LIB_FUSE = """(symbol "Device:Fuse" (pin_numbers (hide yes)) (pin_names (offset 1.016))
    (exclude_from_sim no) (in_bom yes) (on_board yes)
    (property "Reference" "F" (at 2.032 0 90)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "Fuse" (at -1.905 0 90)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at -1.778 0 90)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Datasheet" "~" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Description" "Fuse" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (symbol "Fuse_0_1"
      (rectangle (start -0.762 -2.54) (end 0.762 2.54)
        (stroke (width 0.254) (type default)) (fill (type none))
      )
      (polyline
        (pts (xy 0 2.54) (xy 0 -2.54))
        (stroke (width 0) (type default)) (fill (type none))
      )
    )
    (symbol "Fuse_1_1"
      (pin passive line (at 0 3.81 270) (length 1.27)
        (name "~" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at 0 -3.81 90) (length 1.27)
        (name "~" (effects (font (size 1.27 1.27))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
    )
    (embedded_fonts no)
  )"""

LIB_CONN_01x03 = """(symbol "Connector_Generic:Conn_01x03" (pin_names (offset 1.016) (hide yes))
    (exclude_from_sim no) (in_bom yes) (on_board yes)
    (property "Reference" "J" (at 0 5.08 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "Conn_01x03" (at 0 -5.08 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Datasheet" "~" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Description" "Generic connector, single row, 01x03" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (symbol "Conn_01x03_1_1"
      (rectangle (start -1.27 3.81) (end 1.27 -3.81)
        (stroke (width 0.254) (type default)) (fill (type background))
      )
      (pin passive line (at -3.81 2.54 0) (length 2.54)
        (name "Pin_1" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at -3.81 0 0) (length 2.54)
        (name "Pin_2" (effects (font (size 1.27 1.27))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at -3.81 -2.54 0) (length 2.54)
        (name "Pin_3" (effects (font (size 1.27 1.27))))
        (number "3" (effects (font (size 1.27 1.27))))
      )
    )
    (embedded_fonts no)
  )"""

# HLK-30M12 custom symbol: AC-DC module
# Pins: 1=AC_L, 2=AC_N, 3=+12V, 4=GND
LIB_HLK_30M12 = """(symbol "Custom:HLK-30M12" (pin_names (offset 1.016))
    (exclude_from_sim no) (in_bom yes) (on_board yes)
    (property "Reference" "U" (at 0 8.89 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "HLK-30M12" (at 0 -8.89 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Datasheet" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Description" "AC-DC Power Module 230VAC to 12VDC 2.5A 30W" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (symbol "HLK-30M12_0_1"
      (rectangle (start -7.62 7.62) (end 7.62 -7.62)
        (stroke (width 0.254) (type default)) (fill (type background))
      )
      (text "AC/DC" (at 0 0 0)
        (effects (font (size 2.54 2.54)))
      )
      (text "230V~12V" (at 0 -3.81 0)
        (effects (font (size 1.27 1.27)))
      )
    )
    (symbol "HLK-30M12_1_1"
      (pin input line (at -11.43 3.81 0) (length 3.81)
        (name "AC_L" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin input line (at -11.43 -3.81 0) (length 3.81)
        (name "AC_N" (effects (font (size 1.27 1.27))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
      (pin power_out line (at 11.43 3.81 180) (length 3.81)
        (name "+12V" (effects (font (size 1.27 1.27))))
        (number "3" (effects (font (size 1.27 1.27))))
      )
      (pin power_out line (at 11.43 -3.81 180) (length 3.81)
        (name "GND" (effects (font (size 1.27 1.27))))
        (number "6" (effects (font (size 1.27 1.27))))
      )
    )
    (embedded_fonts no)
  )"""


# ============================================================
# HELPER: Footprint lookup
# ============================================================

# Default footprints by lib_id
_FP_DEFAULTS = {
    # Standard passives
    "Device:R":                "Resistor_SMD:R_0805_2012Metric",
    "Device:C":                "Capacitor_SMD:C_0805_2012Metric",
    "Device:C_Polarized":      "Capacitor_THT:CP_Radial_D6.3mm_P2.50mm",
    "Device:LED":              "LED_SMD:LED_0805_2012Metric",
    "Device:D":                "Diode_SMD:D_SMA",
    "Device:L":                "Inductor_SMD:L_0805_2012Metric",
    "Device:Fuse":             "Fuse:Fuseholder_Cylinder-5x20mm_Schurter_FPG4_Vertical_Closed",
    "Device:FerriteBead":      "Inductor_SMD:L_0805_2012Metric",
    "Device:Varistor":         "Varistor:RV_Disc_D12mm_W4.2mm_P7.5mm",
    "Device:R_Potentiometer":  "Potentiometer_SMD:Potentiometer_Bourns_3214W_Vertical",
    "Device:Q_NMOS_GDS":       "Package_TO_SOT_SMD:TO-252-2",
    # Custom ICs
    "Custom:LD1117AS33TR":     "Package_TO_SOT_SMD:SOT-223-3_TabPin2",
    "Custom:L7805ABD2T":       "Package_TO_SOT_SMD:TO-263-2",
    "Custom:TPS60400DBVR":     "Package_TO_SOT_SMD:SOT-23-5",
    "Custom:CA3140EZ":         "Package_DIP:DIP-8_W7.62mm",
    "Custom:TL071IP":          "Package_DIP:DIP-8_W7.62mm",
    "Custom:ADS1115IDGSR":     "Package_SO:MSOP-10_3x3mm_P0.5mm",
    "Custom:ESP32-WROOM-32E":  "RF_Module:ESP32-WROOM-32E",
    "Custom:LTV-356T":         "Package_SO:SOP-4_3.8x4.1mm_P2.54mm",
    "Custom:Relay_DPDT":       "Relay_THT:Relay_DPDT_Finder_40.52",
    "Custom:HLK-30M12":        "Converter_ACDC:Converter_ACDC_Hi-Link_HLK-30Mxx",
    "Custom:LM2596S-5.0":      "Package_TO_SOT_SMD:TO-263-5_TabPin3",
    # Connectors
    "Connector:Conn_Coaxial":                   "Connector_Coaxial:BNC_Amphenol_B6252HB-NPP3G-50_Horizontal",
    "Connector_Generic:Conn_01x02":             "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal",
    "Connector_Generic:Conn_01x03":             "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical",
    "Connector_Generic:Conn_01x04":             "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical",
    "Connector_Generic:Conn_01x14":             "Connector_PinHeader_2.54mm:PinHeader_1x14_P2.54mm_Vertical",
    "Connector_Generic:Conn_02x10_Odd_Even":    "Connector_PinHeader_2.54mm:PinHeader_2x10_P2.54mm_Vertical",
}

# Per-reference overrides (components that differ from lib_id default)
_FP_OVERRIDES = {
    # Electrolytic caps — different sizes
    "C2":  "Capacitor_THT:CP_Radial_D10.0mm_P5.00mm",    # 680µF/25V
    "C3":  "Capacitor_THT:CP_Radial_D8.0mm_P3.50mm",     # 220µF/10V
    "C5":  "Capacitor_SMD:C_1206_3216Metric",             # 22µF ceramic (1206)
    "C10": "Capacitor_THT:CP_Radial_D6.3mm_P2.50mm",     # 47µF/16V
    # D2 is SMC (3A Schottky), rest are SMA
    "D2":  "Diode_SMD:D_SMC",
    # L1 is power inductor (33µH/3A), not 0805
    "L1":  "Inductor_SMD:L_Bourns-SRN1060",
    # Screw terminals 230V (3-pin, 5.08mm pitch)
    "J1":  "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-3-5.08_1x03_P5.08mm_Horizontal",
    "J11": "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-3-5.08_1x03_P5.08mm_Horizontal",
    # X2 safety capacitor (snubber)
    "C29": "Capacitor_THT:C_Rect_L18.0mm_W5.0mm_P15.00mm_FKS3_FKP3",
}


def get_footprint(lib_id, ref):
    """Determine correct KiCad footprint for a component."""
    # Power symbols — no footprint
    if lib_id.startswith("power:"):
        return ""
    # Strip # from power refs
    ref_clean = ref.lstrip('#')
    # Per-ref override first
    if ref_clean in _FP_OVERRIDES:
        return _FP_OVERRIDES[ref_clean]
    # Default by lib_id
    return _FP_DEFAULTS.get(lib_id, "")


# ============================================================
# HELPER: Symbol instance
# ============================================================

def make_symbol(lib_id, ref, value, x, y, angle=0, mirror=None, unit=1,
                extra_props=None, project_name="ph-verzion-01",
                project_uuid="54ccc777-3789-41c0-b4eb-6807475564db",
                pin_count=2, pin_numbers=None):
    """Generate a symbol instance S-expression."""
    x, y = snap(x), snap(y)
    sym_uuid = uid()

    mirror_str = ""
    if mirror == "x":
        mirror_str = "\n\t\t(mirror x)"
    elif mirror == "y":
        mirror_str = "\n\t\t(mirror y)"

    # Generate pin entries
    pins = ""
    if pin_numbers:
        for pn in pin_numbers:
            pins += f'\n\t\t(pin "{pn}" (uuid "{uid()}"))'
    else:
        for i in range(1, pin_count + 1):
            pins += f'\n\t\t(pin "{i}" (uuid "{uid()}"))'

    # Property positions (relative to symbol position)
    ref_y = snap(y - 2.54)
    val_y = snap(y + 2.54)

    ref_x = snap(x + 2.54)
    props = f"""
\t\t(property "Reference" "{ref}" (at {ref_x} {ref_y} 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify left))
\t\t)
\t\t(property "Value" "{value}" (at {ref_x} {val_y} 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify left))
\t\t)
\t\t(property "Footprint" "{get_footprint(lib_id, ref)}" (at {x} {y} 0)
\t\t\t(effects (font (size 1.27 1.27)) (hide yes))
\t\t)
\t\t(property "Datasheet" "~" (at {x} {y} 0)
\t\t\t(effects (font (size 1.27 1.27)) (hide yes))
\t\t)
\t\t(property "Description" "" (at {x} {y} 0)
\t\t\t(effects (font (size 1.27 1.27)) (hide yes))
\t\t)"""

    if extra_props:
        for k, v in extra_props.items():
            props += f"""
\t\t(property "{k}" "{v}" (at {x} {y} 0)
\t\t\t(effects (font (size 1.27 1.27)) (hide yes))
\t\t)"""

    return f"""\t(symbol
\t\t(lib_id "{lib_id}")
\t\t(at {x} {y} {angle}){mirror_str}
\t\t(unit {unit})
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{sym_uuid}")
{props}{pins}
\t\t(instances
\t\t\t(project "{project_name}"
\t\t\t\t(path "/{project_uuid}"
\t\t\t\t\t(reference "{ref}")
\t\t\t\t\t(unit {unit})
\t\t\t\t)
\t\t\t)
\t\t)
\t)"""


def make_wire(x1, y1, x2, y2):
    """Generate a wire S-expression."""
    x1, y1, x2, y2 = snap(x1), snap(y1), snap(x2), snap(y2)
    return f"""\t(wire
\t\t(pts
\t\t\t(xy {x1} {y1}) (xy {x2} {y2})
\t\t)
\t\t(stroke (width 0) (type default))
\t\t(uuid "{uid()}")
\t)"""


def make_junction(x, y):
    """Generate a junction S-expression."""
    x, y = snap(x), snap(y)
    return f"""\t(junction
\t\t(at {x} {y})
\t\t(diameter 0)
\t\t(color 0 0 0 0)
\t\t(uuid "{uid()}")
\t)"""


def make_label(name, x, y, angle=0):
    """Generate a net label S-expression."""
    x, y = snap(x), snap(y)
    return f"""\t(label "{name}"
\t\t(at {x} {y} {angle})
\t\t(effects
\t\t\t(font (size 1.27 1.27))
\t\t\t(justify left bottom)
\t\t)
\t\t(uuid "{uid()}")
\t)"""


def make_text(content, x, y, size=2.54):
    """Generate a text annotation S-expression."""
    return f"""\t(text "{content}"
\t\t(exclude_from_sim no)
\t\t(at {x} {y} 0)
\t\t(effects
\t\t\t(font (size {size} {size}))
\t\t\t(justify left bottom)
\t\t)
\t\t(uuid "{uid()}")
\t)"""


def make_no_connect(x, y):
    x, y = snap(x), snap(y)
    return f"""\t(no_connect
\t\t(at {x} {y})
\t\t(uuid "{uid()}")
\t)"""


# ============================================================
# MORE LIB SYMBOL DEFINITIONS (Step 2+)
# ============================================================

LIB_C_POLARIZED = """(symbol "Device:C_Polarized" (pin_numbers (hide yes)) (pin_names (offset 0.254))
    (exclude_from_sim no) (in_bom yes) (on_board yes)
    (property "Reference" "C" (at 0.635 2.54 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Value" "C_Polarized" (at 0.635 -2.54 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Footprint" "" (at 0.9652 -3.81 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Datasheet" "~" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Description" "Polarized capacitor" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (symbol "C_Polarized_0_1"
      (polyline
        (pts (xy -2.032 0.762) (xy 2.032 0.762))
        (stroke (width 0.508) (type default)) (fill (type none))
      )
      (polyline
        (pts (xy -1.524 2.286) (xy -0.508 2.286))
        (stroke (width 0) (type default)) (fill (type none))
      )
      (polyline
        (pts (xy -1.016 1.778) (xy -1.016 2.794))
        (stroke (width 0) (type default)) (fill (type none))
      )
      (rectangle (start -2.032 -1.27) (end 2.032 -0.508)
        (stroke (width 0) (type default)) (fill (type outline))
      )
    )
    (symbol "C_Polarized_1_1"
      (pin passive line (at 0 3.81 270) (length 2.794)
        (name "~" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at 0 -3.81 90) (length 2.794)
        (name "~" (effects (font (size 1.27 1.27))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
    )
    (embedded_fonts no)
  )"""

LIB_L = """(symbol "Device:L" (pin_numbers (hide yes)) (pin_names (offset 1.016) (hide yes))
    (exclude_from_sim no) (in_bom yes) (on_board yes)
    (property "Reference" "L" (at -1.27 0 90)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "L" (at 1.905 0 90)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Datasheet" "~" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Description" "Inductor" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (symbol "L_0_1"
      (arc (start 0 -2.54) (mid 0.6323 -1.905) (end 0 -1.27)
        (stroke (width 0) (type default)) (fill (type none))
      )
      (arc (start 0 -1.27) (mid 0.6323 -0.635) (end 0 0)
        (stroke (width 0) (type default)) (fill (type none))
      )
      (arc (start 0 0) (mid 0.6323 0.635) (end 0 1.27)
        (stroke (width 0) (type default)) (fill (type none))
      )
      (arc (start 0 1.27) (mid 0.6323 1.905) (end 0 2.54)
        (stroke (width 0) (type default)) (fill (type none))
      )
    )
    (symbol "L_1_1"
      (pin passive line (at 0 3.81 270) (length 1.27)
        (name "1" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at 0 -3.81 90) (length 1.27)
        (name "2" (effects (font (size 1.27 1.27))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
    )
    (embedded_fonts no)
  )"""

LIB_D = """(symbol "Device:D" (pin_numbers (hide yes)) (pin_names (offset 1.016) (hide yes))
    (exclude_from_sim no) (in_bom yes) (on_board yes)
    (property "Reference" "D" (at 0 2.54 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "D" (at 0 -2.54 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Datasheet" "~" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Description" "Diode" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (symbol "D_0_1"
      (polyline
        (pts (xy -1.27 1.27) (xy -1.27 -1.27))
        (stroke (width 0.254) (type default)) (fill (type none))
      )
      (polyline
        (pts (xy 1.27 0) (xy -1.27 0))
        (stroke (width 0) (type default)) (fill (type none))
      )
      (polyline
        (pts (xy 1.27 -1.27) (xy 1.27 1.27) (xy -1.27 0) (xy 1.27 -1.27))
        (stroke (width 0.254) (type default)) (fill (type none))
      )
    )
    (symbol "D_1_1"
      (pin passive line (at -3.81 0 0) (length 2.54)
        (name "K" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at 3.81 0 180) (length 2.54)
        (name "A" (effects (font (size 1.27 1.27))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
    )
    (embedded_fonts no)
  )"""

# LM2596S-5.0 custom symbol
# Pin 1: VIN, Pin 2: OUTPUT (switch), Pin 3: GND, Pin 4: FB, Pin 5: ON/OFF
LIB_LM2596 = """(symbol "Custom:LM2596S-5.0" (pin_names (offset 1.016))
    (exclude_from_sim no) (in_bom yes) (on_board yes)
    (property "Reference" "U" (at 0 8.89 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "LM2596S-5.0" (at 0 -8.89 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Datasheet" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Description" "Step-Down Voltage Regulator, 5V fixed, 3A, TO-263-5" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (symbol "LM2596S-5.0_0_1"
      (rectangle (start -7.62 7.62) (end 7.62 -7.62)
        (stroke (width 0.254) (type default)) (fill (type background))
      )
      (text "BUCK" (at 0 0 0)
        (effects (font (size 2.54 2.54)))
      )
      (text "LM2596" (at 0 -3.81 0)
        (effects (font (size 1.27 1.27)))
      )
    )
    (symbol "LM2596S-5.0_1_1"
      (pin power_in line (at -11.43 5.08 0) (length 3.81)
        (name "VIN" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin output line (at 11.43 5.08 180) (length 3.81)
        (name "OUT" (effects (font (size 1.27 1.27))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
      (pin power_in line (at 0 -11.43 90) (length 3.81)
        (name "GND" (effects (font (size 1.27 1.27))))
        (number "3" (effects (font (size 1.27 1.27))))
      )
      (pin input line (at 11.43 -2.54 180) (length 3.81)
        (name "FB" (effects (font (size 1.27 1.27))))
        (number "4" (effects (font (size 1.27 1.27))))
      )
      (pin input line (at -11.43 -2.54 0) (length 3.81)
        (name "ON/OFF" (effects (font (size 1.27 1.27))))
        (number "5" (effects (font (size 1.27 1.27))))
      )
    )
    (embedded_fonts no)
  )"""


# AMS1117-3.3 LDO custom symbol
# Pin 1: GND/Adjust, Pin 2: VOUT, Pin 3: VIN
LIB_AMS1117 = """(symbol "Custom:LD1117AS33TR" (pin_names (offset 1.016))
    (exclude_from_sim no) (in_bom yes) (on_board yes)
    (property "Reference" "U" (at 0 6.35 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "LD1117AS33TR" (at 0 -6.35 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "Package_TO_SOT_SMD:SOT-223-3_TabPin2" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Datasheet" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Description" "1A Low Dropout Voltage Regulator, 3.3V, SOT-223" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (symbol "LD1117AS33TR_0_1"
      (rectangle (start -6.35 5.08) (end 6.35 -5.08)
        (stroke (width 0.254) (type default)) (fill (type background))
      )
      (text "LDO" (at 0 0 0)
        (effects (font (size 2.54 2.54)))
      )
      (text "3.3V" (at 0 -2.54 0)
        (effects (font (size 1.27 1.27)))
      )
    )
    (symbol "LD1117AS33TR_1_1"
      (pin power_in line (at -10.16 2.54 0) (length 3.81)
        (name "VIN" (effects (font (size 1.27 1.27))))
        (number "3" (effects (font (size 1.27 1.27))))
      )
      (pin power_out line (at 10.16 2.54 180) (length 3.81)
        (name "VOUT" (effects (font (size 1.27 1.27))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
      (pin power_in line (at 0 -8.89 90) (length 3.81)
        (name "GND" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
    )
    (embedded_fonts no)
  )"""

# L7805ABD2T-TR linear regulator (D2PAK SMD)
# Pin 1: IN, Pin 2: GND, Pin 3: OUT
LIB_LM7805 = """(symbol "Custom:L7805ABD2T" (pin_names (offset 1.016))
    (exclude_from_sim no) (in_bom yes) (on_board yes)
    (property "Reference" "U" (at 0 6.35 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "L7805ABD2T" (at 0 -6.35 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "Package_TO_SOT_SMD:TO-263-2" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Datasheet" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Description" "Linear Voltage Regulator, 5V, 1.5A, D2PAK SMD" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (symbol "L7805ABD2T_0_1"
      (rectangle (start -6.35 5.08) (end 6.35 -5.08)
        (stroke (width 0.254) (type default)) (fill (type background))
      )
      (text "7805" (at 0 0 0)
        (effects (font (size 2.54 2.54)))
      )
      (text "LINEAR" (at 0 -2.54 0)
        (effects (font (size 1.27 1.27)))
      )
    )
    (symbol "L7805ABD2T_1_1"
      (pin power_in line (at -10.16 2.54 0) (length 3.81)
        (name "IN" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin power_in line (at 0 -8.89 90) (length 3.81)
        (name "GND" (effects (font (size 1.27 1.27))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
      (pin power_out line (at 10.16 2.54 180) (length 3.81)
        (name "OUT" (effects (font (size 1.27 1.27))))
        (number "3" (effects (font (size 1.27 1.27))))
      )
    )
    (embedded_fonts no)
  )"""

# TPS60400DBVR charge pump (SOT-23-5)
# Pin 1: IN, Pin 2: GND, Pin 3: C+, Pin 4: C-, Pin 5: OUT
LIB_TPS60400 = """(symbol "Custom:TPS60400DBVR" (pin_names (offset 1.016))
    (exclude_from_sim no) (in_bom yes) (on_board yes)
    (property "Reference" "U" (at 0 8.89 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "TPS60400DBVR" (at 0 -8.89 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Datasheet" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Description" "Unregulated Charge Pump Voltage Inverter, 60mA, SOT-23-5" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (symbol "TPS60400DBVR_0_1"
      (rectangle (start -7.62 7.62) (end 7.62 -7.62)
        (stroke (width 0.254) (type default)) (fill (type background))
      )
      (text "CHARGE" (at 0 1.27 0)
        (effects (font (size 1.78 1.78)))
      )
      (text "PUMP" (at 0 -1.27 0)
        (effects (font (size 1.78 1.78)))
      )
    )
    (symbol "TPS60400DBVR_1_1"
      (pin power_in line (at -11.43 5.08 0) (length 3.81)
        (name "IN" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin power_in line (at 0 -11.43 90) (length 3.81)
        (name "GND" (effects (font (size 1.27 1.27))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at 11.43 5.08 180) (length 3.81)
        (name "C+" (effects (font (size 1.27 1.27))))
        (number "3" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at 11.43 0 180) (length 3.81)
        (name "C-" (effects (font (size 1.27 1.27))))
        (number "4" (effects (font (size 1.27 1.27))))
      )
      (pin power_out line (at 11.43 -5.08 180) (length 3.81)
        (name "OUT" (effects (font (size 1.27 1.27))))
        (number "5" (effects (font (size 1.27 1.27))))
      )
    )
    (embedded_fonts no)
  )"""

# Ferrite bead symbol
LIB_FB = """(symbol "Device:FerriteBead" (pin_numbers (hide yes)) (pin_names (offset 1.016) (hide yes))
    (exclude_from_sim no) (in_bom yes) (on_board yes)
    (property "Reference" "FB" (at -1.27 0 90)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "FerriteBead" (at 1.905 0 90)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Datasheet" "~" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Description" "Ferrite bead" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (symbol "FerriteBead_0_1"
      (polyline
        (pts (xy 0 -2.54) (xy 0 -1.27) (xy 0.762 -0.635) (xy -0.762 0.635) (xy 0 1.27) (xy 0 2.54))
        (stroke (width 0) (type default)) (fill (type none))
      )
      (polyline
        (pts (xy -0.762 -0.635) (xy 0.762 -0.635))
        (stroke (width 0) (type default)) (fill (type none))
      )
    )
    (symbol "FerriteBead_1_1"
      (pin passive line (at 0 3.81 270) (length 1.27)
        (name "~" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at 0 -3.81 90) (length 1.27)
        (name "~" (effects (font (size 1.27 1.27))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
    )
    (embedded_fonts no)
  )"""

# Standard 8-pin DIP op-amp (used for CA3140EZ)
# Pin 1: Offset N1, Pin 2: IN-, Pin 3: IN+, Pin 4: V-
# Pin 5: Offset N2, Pin 6: OUT, Pin 7: V+, Pin 8: Strobe/NC
LIB_OPAMP_DIP8 = """(symbol "Custom:CA3140EZ" (pin_names (offset 1.016))
    (exclude_from_sim no) (in_bom yes) (on_board yes)
    (property "Reference" "U" (at 0 7.62 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "CA3140EZ" (at 0 -7.62 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Datasheet" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Description" "4.5MHz CMOS Op-Amp, Zin>1TOhm, DIP-8" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (symbol "CA3140EZ_0_1"
      (polyline
        (pts (xy -5.08 5.08) (xy 5.08 0) (xy -5.08 -5.08) (xy -5.08 5.08))
        (stroke (width 0.254) (type default)) (fill (type background))
      )
      (text "+" (at -3.81 -1.905 0)
        (effects (font (size 1.27 1.27)))
      )
      (text "-" (at -3.81 1.905 0)
        (effects (font (size 1.27 1.27)))
      )
    )
    (symbol "CA3140EZ_1_1"
      (pin input line (at -8.89 2.54 0) (length 3.81)
        (name "IN-" (effects (font (size 1.016 1.016))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
      (pin input line (at -8.89 -2.54 0) (length 3.81)
        (name "IN+" (effects (font (size 1.016 1.016))))
        (number "3" (effects (font (size 1.27 1.27))))
      )
      (pin power_in line (at -1.27 -8.89 90) (length 3.81)
        (name "V-" (effects (font (size 1.016 1.016))))
        (number "4" (effects (font (size 1.27 1.27))))
      )
      (pin power_in line (at -1.27 8.89 270) (length 3.81)
        (name "V+" (effects (font (size 1.016 1.016))))
        (number "7" (effects (font (size 1.27 1.27))))
      )
      (pin output line (at 8.89 0 180) (length 3.81)
        (name "OUT" (effects (font (size 1.016 1.016))))
        (number "6" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at -8.89 5.08 0) (length 3.81)
        (name "N1" (effects (font (size 1.016 1.016))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at -8.89 -5.08 0) (length 3.81)
        (name "N2" (effects (font (size 1.016 1.016))))
        (number "5" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at 8.89 -5.08 180) (length 3.81)
        (name "STR" (effects (font (size 1.016 1.016))))
        (number "8" (effects (font (size 1.27 1.27))))
      )
    )
    (embedded_fonts no)
  )"""

# TL071IP DIP-8 op-amp (same pinout as CA3140)
LIB_OPAMP_TL081 = """(symbol "Custom:TL071IP" (pin_names (offset 1.016))
    (exclude_from_sim no) (in_bom yes) (on_board yes)
    (property "Reference" "U" (at 0 7.62 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "TL071IP" (at 0 -7.62 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Datasheet" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Description" "Low-Noise JFET-Input Op-Amp, DIP-8" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (symbol "TL071IP_0_1"
      (polyline
        (pts (xy -5.08 5.08) (xy 5.08 0) (xy -5.08 -5.08) (xy -5.08 5.08))
        (stroke (width 0.254) (type default)) (fill (type background))
      )
      (text "+" (at -3.81 -1.905 0)
        (effects (font (size 1.27 1.27)))
      )
      (text "-" (at -3.81 1.905 0)
        (effects (font (size 1.27 1.27)))
      )
    )
    (symbol "TL071IP_1_1"
      (pin input line (at -8.89 2.54 0) (length 3.81)
        (name "IN-" (effects (font (size 1.016 1.016))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
      (pin input line (at -8.89 -2.54 0) (length 3.81)
        (name "IN+" (effects (font (size 1.016 1.016))))
        (number "3" (effects (font (size 1.27 1.27))))
      )
      (pin power_in line (at -1.27 -8.89 90) (length 3.81)
        (name "V-" (effects (font (size 1.016 1.016))))
        (number "4" (effects (font (size 1.27 1.27))))
      )
      (pin power_in line (at -1.27 8.89 270) (length 3.81)
        (name "V+" (effects (font (size 1.016 1.016))))
        (number "7" (effects (font (size 1.27 1.27))))
      )
      (pin output line (at 8.89 0 180) (length 3.81)
        (name "OUT" (effects (font (size 1.016 1.016))))
        (number "6" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at -8.89 5.08 0) (length 3.81)
        (name "N1" (effects (font (size 1.016 1.016))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at -8.89 -5.08 0) (length 3.81)
        (name "N2" (effects (font (size 1.016 1.016))))
        (number "5" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at 8.89 -5.08 180) (length 3.81)
        (name "N2B" (effects (font (size 1.016 1.016))))
        (number "8" (effects (font (size 1.27 1.27))))
      )
    )
    (embedded_fonts no)
  )"""

# BNC connector (2-pin: signal + shield/GND)
LIB_BNC = """(symbol "Connector:Conn_Coaxial" (pin_names (offset 1.016) (hide yes))
    (exclude_from_sim no) (in_bom yes) (on_board yes)
    (property "Reference" "P" (at 0.254 3.048 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "BNC" (at 0.254 -2.794 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Datasheet" "~" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Description" "Coaxial connector (BNC)" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (symbol "Conn_Coaxial_0_1"
      (circle (center 0 0) (radius 1.778)
        (stroke (width 0.254) (type default)) (fill (type none))
      )
    )
    (symbol "Conn_Coaxial_1_1"
      (pin passive line (at -3.81 0 0) (length 2.032)
        (name "Signal" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at 0 -3.81 90) (length 2.032)
        (name "Shield" (effects (font (size 1.27 1.27))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
    )
    (embedded_fonts no)
  )"""

# Potentiometer / trimmer (3-pin: 1, wiper, 2)
LIB_POT = """(symbol "Device:R_Potentiometer" (pin_names (offset 1.016) (hide yes))
    (exclude_from_sim no) (in_bom yes) (on_board yes)
    (property "Reference" "R" (at 2.032 0 90)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "R_Potentiometer" (at -3.81 0 90)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Datasheet" "~" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Description" "Potentiometer" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (symbol "R_Potentiometer_0_1"
      (rectangle (start -1.016 2.54) (end 1.016 -2.54)
        (stroke (width 0.254) (type default)) (fill (type none))
      )
      (polyline
        (pts (xy 1.27 0) (xy 2.54 0))
        (stroke (width 0) (type default)) (fill (type none))
      )
      (polyline
        (pts (xy 1.524 0.508) (xy 1.27 0) (xy 1.524 -0.508))
        (stroke (width 0.254) (type default)) (fill (type none))
      )
    )
    (symbol "R_Potentiometer_1_1"
      (pin passive line (at 0 3.81 270) (length 1.27)
        (name "1" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at 3.81 0 180) (length 1.27)
        (name "2" (effects (font (size 1.27 1.27))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at 0 -3.81 90) (length 1.27)
        (name "3" (effects (font (size 1.27 1.27))))
        (number "3" (effects (font (size 1.27 1.27))))
      )
    )
    (embedded_fonts no)
  )"""


# ============================================================
# STEP 1: 230VAC INPUT + HLK-30M12 → 12V
# ============================================================

def generate_step1():
    """Generate Step 1: 230V input, fuse, HLK-30M12, LED indicator, power flags."""

    lib_symbols = []
    symbols = []
    wires = []
    junctions = []
    labels = []
    texts = []

    # --- Lib symbols needed ---
    lib_symbols.append(LIB_CONN_01x03)
    lib_symbols.append(LIB_FUSE)
    lib_symbols.append(LIB_HLK_30M12)
    lib_symbols.append(LIB_C)
    lib_symbols.append(LIB_R)
    lib_symbols.append(LIB_LED)
    lib_symbols.append(LIB_GND)
    lib_symbols.append(lib_symbol_power("+12V"))
    lib_symbols.append(LIB_PWR_FLAG)

    # --- Layout ---
    # Left to right: J_AC_IN → F1 → HLK-30M12 → C_PSU / LED circuit
    # Y baseline around 80mm from top

    # Section title
    texts.append(make_text("POWER SUPPLY — 230VAC INPUT", 25, 30, 3.0))
    texts.append(make_text("WARNING: 230V MAINS — MIN 6mm CREEPAGE", 25, 35, 1.5))

    # J_AC_IN: 3-pin screw terminal at (40, 65)
    # Connector pins come out to the right at -3.81 offset
    # Pin 1 (L) at y=62.46, Pin 2 (N) at y=65, Pin 3 (PE) at y=67.54
    symbols.append(make_symbol("Connector_Generic:Conn_01x03", "J1", "230V_IN",
                               40, 65, 0, pin_count=3))

    # Labels on connector pins
    labels.append(make_label("AC_L", 36.19, 62.46))
    labels.append(make_label("AC_N", 36.19, 65))
    labels.append(make_label("PE", 36.19, 67.54))

    # F1: Fuse (vertical) — between connector L and HLK AC_L
    # Fuse pin 1 at (0, 3.81), pin 2 at (0, -3.81) in lib coords
    # Place at (55, 62.46) rotated 90 degrees (horizontal)
    # At 90°: pin1 at (55-3.81, 62.46)=(51.19, 62.46), pin2 at (55+3.81, 62.46)=(58.81, 62.46)
    symbols.append(make_symbol("Device:Fuse", "F1", "2A/250V",
                               55, 62.46, 90, pin_count=2))

    # Wire: J1 pin 1 (L) → F1 pin 1
    wires.append(make_wire(36.19, 62.46, 51.19, 62.46))

    # F1 pin 2 exits at (58.81, 62.46)
    # HLK-30M12 at (85, 65)
    # HLK AC_L pin at (-11.43 from center + 3.81 up) = (85-11.43, 65-3.81) = (73.57, 61.19)
    # Wait, pin is at (at -11.43 3.81 0) meaning offset from symbol center
    # So AC_L absolute: (85-11.43, 65-3.81) = (73.57, 61.19)
    # AC_N absolute: (85-11.43, 65+3.81) = (73.57, 68.81)
    # +12V absolute: (85+11.43, 65-3.81) = (96.43, 61.19)
    # GND absolute: (85+11.43, 65+3.81) = (96.43, 68.81)

    symbols.append(make_symbol("Custom:HLK-30M12", "U1", "HLK-30M12",
                               85, 65, 0, pin_numbers=["1", "2", "3", "6"]))

    # Wire: F1 pin 2 → HLK AC_L
    wires.append(make_wire(58.81, 62.46, 73.57, 62.46))
    wires.append(make_wire(73.57, 62.46, 73.57, 61.19))

    # Wire: J1 pin 2 (N) → HLK AC_N
    wires.append(make_wire(36.19, 65, 36.19, 68.81))
    wires.append(make_wire(36.19, 68.81, 73.57, 68.81))

    # PE label — just goes to a net label (will be connected to chassis/box)
    labels.append(make_label("PE", 36.19, 67.54))

    # +12V output from HLK
    # +12V pin at (96.43, 61.19)
    # Wire to the right, then up to +12V power symbol
    wires.append(make_wire(96.43, 61.19, 115, 61.19))

    # +12V power symbol at (115, 56)
    symbols.append(make_symbol("power:+12V", "#PWR01", "+12V",
                               115, 56.19, 0, pin_count=1))
    wires.append(make_wire(115, 61.19, 115, 56.19))

    # GND from HLK
    # GND pin at (96.43, 68.81)
    wires.append(make_wire(96.43, 68.81, 115, 68.81))

    # GND power symbol at (115, 73)
    symbols.append(make_symbol("power:GND", "#PWR02", "GND",
                               115, 73.81, 0, pin_count=1))
    wires.append(make_wire(115, 68.81, 115, 73.81))

    # Junction at (115, 61.19) for +12V bus
    junctions.append(make_junction(115, 61.19))
    # Junction at (115, 68.81) for GND bus
    junctions.append(make_junction(115, 68.81))

    # C_PSU: 100nF bypass capacitor on 12V output
    # Place vertically at (125, 65) — pin 1 (top) connects to +12V, pin 2 (bottom) to GND
    # C pin 1 at (125, 65-3.81)=(125, 61.19), C pin 2 at (125, 65+3.81)=(125, 68.81)
    symbols.append(make_symbol("Device:C", "C1", "100nF",
                               125, 65, 0, pin_count=2))
    wires.append(make_wire(115, 61.19, 125, 61.19))
    wires.append(make_wire(115, 68.81, 125, 68.81))

    # LED power indicator circuit: +12V → R_LED (1kΩ) → LED → GND
    # Place at right side: R at (140, 61.19), LED at (140, 68.81)
    # R vertical: pin1 at (140, 56.11), pin2 at (140, 66.27)
    # Actually R has pin1 at y-3.81 and pin2 at y+3.81 from center
    symbols.append(make_symbol("Device:R", "R1", "1k",
                               140, 62, 0, pin_count=2))
    # R1 pin1 at (140, 62-3.81)=(140, 58.19), pin2 at (140, 62+3.81)=(140, 65.81)

    # LED horizontal: place at (140, 71) - but LED is horizontal by default
    # LED pin1 (K/cathode) at x-3.81, pin2 (A/anode) at x+3.81
    # Let's make it vertical: rotate 90 degrees
    # At 90°: pin1 at (140, 71-3.81)=(140, 67.19), pin2 at (140, 71+3.81)=(140, 74.81)
    # Actually with 90° rotation, pins swap positions
    # Let's place LED at (140, 72), rotated 270° so anode is up
    symbols.append(make_symbol("Device:LED", "D1", "Blue",
                               140, 72, 270, pin_count=2))
    # At 270°: pin2 (A) at top (140, 72-3.81)=(140, 68.19), pin1 (K) at bottom (140, 72+3.81)=(140, 75.81)

    # +12V to R1 top
    symbols.append(make_symbol("power:+12V", "#PWR03", "+12V",
                               140, 53, 0, pin_count=1))
    wires.append(make_wire(140, 53, 140, 58.19))

    # R1 bottom to LED anode
    wires.append(make_wire(140, 65.81, 140, 68.19))

    # LED cathode to GND
    symbols.append(make_symbol("power:GND", "#PWR04", "GND",
                               140, 78, 0, pin_count=1))
    wires.append(make_wire(140, 75.81, 140, 78))

    # PWR_FLAGs removed — +12V and GND nets are already driven by HLK power_out pins

    # Net labels for connection to next steps
    wires.append(make_wire(125, 61.19, 130, 61.19))
    labels.append(make_label("+12V", 130, 61.19))

    return lib_symbols, symbols, wires, junctions, labels, texts


# ============================================================
# STEP 2: BUCK 12V → 5V (LM2596S-5.0)
# ============================================================

def generate_step2():
    """Generate Step 2: LM2596 buck converter 12V → 5V digital."""

    lib_symbols = []
    symbols = []
    wires = []
    junctions = []
    labels = []
    texts = []

    # --- Lib symbols needed (new ones not in step 1) ---
    lib_symbols.append(LIB_LM2596)
    lib_symbols.append(LIB_C_POLARIZED)
    lib_symbols.append(LIB_L)
    lib_symbols.append(LIB_D)
    lib_symbols.append(lib_symbol_power("+5V"))

    # --- Layout ---
    # Place below step 1, Y baseline ~100mm
    # Flow: +12V → C_in → LM2596 → L1 → +5V → C_out
    #                        ↓
    #                  D2 (cathode to OUT, anode to GND)

    base_x = 25
    base_y = 95

    texts.append(make_text("BUCK CONVERTER — 12V to 5V (Digital)", base_x, base_y, 2.0))

    # LM2596 center position
    lm_x = 80
    lm_y = base_y + 20  # = 115

    # LM2596 pin positions (from symbol definition):
    # Pin 1 (VIN):    left side, (lm_x - 11.43, lm_y - 5.08)  = (68.57, 109.92)
    # Pin 2 (OUT):    right side, (lm_x + 11.43, lm_y - 5.08) = (91.43, 109.92)
    # Pin 3 (GND):    bottom, (lm_x, lm_y + 11.43)            = (80, 126.43)
    # Pin 4 (FB):     right side, (lm_x + 11.43, lm_y + 2.54) = (91.43, 117.54)
    # Pin 5 (ON/OFF): left side, (lm_x - 11.43, lm_y + 2.54)  = (68.57, 117.54)

    symbols.append(make_symbol("Custom:LM2596S-5.0", "U2", "LM2596S-5.0",
                               lm_x, lm_y, 0, pin_count=5))

    # +12V power symbol → wire to VIN
    vin_x = 50
    vin_y = lm_y - 5.08  # 109.92

    symbols.append(make_symbol("power:+12V", "#PWR05", "+12V",
                               vin_x, vin_y - 5, 0, pin_count=1))
    wires.append(make_wire(vin_x, vin_y - 5, vin_x, vin_y))

    # C2: 680µF/25V input capacitor (polarized) at (55, 115)
    # Pin 1 (+) at top: (55, 115 - 3.81) = (55, 111.19)
    # Pin 2 (-) at bottom: (55, 115 + 3.81) = (55, 118.81)
    c2_x = 55
    c2_y = lm_y
    symbols.append(make_symbol("Device:C_Polarized", "C2", "680uF/25V",
                               c2_x, c2_y, 0, pin_count=2))

    # Wire +12V rail → C2 pin1 → LM2596 VIN
    wires.append(make_wire(vin_x, vin_y, c2_x, vin_y))
    wires.append(make_wire(c2_x, c2_y - 3.81, c2_x, vin_y))
    wires.append(make_wire(c2_x, vin_y, 68.57, vin_y))
    junctions.append(make_junction(c2_x, vin_y))

    # C2 pin2 → GND
    symbols.append(make_symbol("power:GND", "#PWR06", "GND",
                               c2_x, c2_y + 8, 0, pin_count=1))
    wires.append(make_wire(c2_x, c2_y + 3.81, c2_x, c2_y + 8))

    # ON/OFF pin → GND (always on)
    # ON/OFF at (68.57, 117.54)
    wires.append(make_wire(68.57, 117.54, 63, 117.54))
    symbols.append(make_symbol("power:GND", "#PWR07", "GND",
                               63, 120, 0, pin_count=1))
    wires.append(make_wire(63, 117.54, 63, 120))

    # GND pin of LM2596 at (80, 126.43)
    symbols.append(make_symbol("power:GND", "#PWR08", "GND",
                               lm_x, lm_y + 15, 0, pin_count=1))
    wires.append(make_wire(lm_x, lm_y + 11.43, lm_x, lm_y + 15))

    # OUT pin at (91.43, 109.92)
    # D2: SS34 Schottky diode — cathode connects to OUT node, anode to GND
    # Place D2 vertical at (97, 117) rotated 90° (cathode up)
    # D at 90°: pin1 (K) at top = (97, 117-3.81)=(97, 113.19)
    #           pin2 (A) at bottom = (97, 117+3.81)=(97, 120.81)
    # Actually D rotated 270° to have cathode at top:
    # At 270°: pin1 (K) at (97, 117-3.81), pin2 (A) at (97, 117+3.81)
    d2_x = 97
    d2_y = 117
    symbols.append(make_symbol("Device:D", "D2", "SS34",
                               d2_x, d2_y, 270, pin_count=2))
    # D at 270°: pin2 (A) at top (d2_x, d2_y - 3.81), pin1 (K) at bottom (d2_x, d2_y + 3.81)
    # Wait, for 270° rotation: original horizontal pin1(K) at left(-3.81,0) → rotated to (0, +3.81) = bottom
    # pin2(A) at right(+3.81,0) → rotated to (0, -3.81) = top
    # So A is at top, K is at bottom... that's wrong for our circuit.
    # We need cathode UP (connected to switching node), anode DOWN (to GND)
    # So use 90° rotation: pin1(K) at left → rotates to top, pin2(A) at right → rotates to bottom
    # 90°: pin1(K) at (d2_x, d2_y - 3.81), pin2(A) at (d2_x, d2_y + 3.81)
    # That means cathode at top, anode at bottom - correct!

    # Fix D2 rotation
    symbols[-1] = make_symbol("Device:D", "D2", "SS34",
                              d2_x, d2_y, 90, pin_count=2)
    # 90°: pin1(K) at (d2_x, d2_y - 3.81) = (97, 113.19) — connects to OUT/switching node
    #       pin2(A) at (d2_x, d2_y + 3.81) = (97, 120.81) — connects to GND

    # Wire OUT → D2 cathode & L1
    out_node_y = vin_y  # 109.92
    wires.append(make_wire(91.43, out_node_y, d2_x, out_node_y))
    wires.append(make_wire(d2_x, out_node_y, d2_x, d2_y - 3.81))
    junctions.append(make_junction(d2_x, out_node_y))

    # D2 anode → GND
    symbols.append(make_symbol("power:GND", "#PWR09", "GND",
                               d2_x, d2_y + 8, 0, pin_count=1))
    wires.append(make_wire(d2_x, d2_y + 3.81, d2_x, d2_y + 8))

    # L1: 33µH inductor at (110, out_node_y) horizontal → rotated 90°
    # At 90°: pin1 at (l1_x, out_node_y - 3.81), pin2 at (l1_x, out_node_y + 3.81)
    # Actually I want L horizontal, so don't rotate
    # L vertical: pin1 at top (l1_x, l1_y - 3.81), pin2 at bottom (l1_x, l1_y + 3.81)
    # I want L horizontal: left pin connects to switching node, right pin to +5V output
    # Place at 90° rotation to make it horizontal
    l1_x = 110
    l1_y = out_node_y
    symbols.append(make_symbol("Device:L", "L1", "33uH",
                               l1_x, l1_y, 90, pin_count=2))
    # At 90°: pin1 at (l1_x - 3.81, l1_y) = (106.19, 109.92) — connects to switching node
    #         pin2 at (l1_x + 3.81, l1_y) = (113.81, 109.92) — connects to +5V output

    # Wire from OUT/D2 junction to L1 pin1
    wires.append(make_wire(d2_x, out_node_y, 106.19, out_node_y))

    # +5V output node
    out_5v_x = 130
    out_5v_y = out_node_y

    # Wire L1 pin2 → +5V output
    wires.append(make_wire(113.81, out_node_y, out_5v_x, out_node_y))

    # C3: 220µF/10V output capacitor (polarized) at (130, 115)
    c3_x = out_5v_x
    c3_y = lm_y
    symbols.append(make_symbol("Device:C_Polarized", "C3", "220uF/10V",
                               c3_x, c3_y, 0, pin_count=2))
    # C3 pin1 (+) at (130, 115-3.81) = (130, 111.19)
    # C3 pin2 (-) at (130, 115+3.81) = (130, 118.81)
    wires.append(make_wire(c3_x, c3_y - 3.81, c3_x, out_5v_y))
    junctions.append(make_junction(c3_x, out_5v_y))

    # C3 pin2 → GND
    symbols.append(make_symbol("power:GND", "#PWR10", "GND",
                               c3_x, c3_y + 8, 0, pin_count=1))
    wires.append(make_wire(c3_x, c3_y + 3.81, c3_x, c3_y + 8))

    # +5V power symbol
    symbols.append(make_symbol("power:+5V", "#PWR11", "+5V",
                               out_5v_x, out_5v_y - 5, 0, pin_count=1))
    wires.append(make_wire(out_5v_x, out_5v_y - 5, out_5v_x, out_5v_y))

    # FB pin at (91.43, 117.54) → connect to +5V output
    # Wire from FB → right → up → to output
    fb_x = 91.43
    fb_y = 117.54
    wires.append(make_wire(fb_x, fb_y, out_5v_x + 5, fb_y))
    wires.append(make_wire(out_5v_x + 5, fb_y, out_5v_x + 5, out_5v_y))
    wires.append(make_wire(out_5v_x, out_5v_y, out_5v_x + 5, out_5v_y))
    junctions.append(make_junction(out_5v_x + 5, out_5v_y))

    # PWR_FLAG on +5V
    symbols.append(make_symbol("power:PWR_FLAG", "#FLG03", "PWR_FLAG",
                               out_5v_x + 10, out_5v_y - 5, 0, pin_count=1))
    wires.append(make_wire(out_5v_x + 10, out_5v_y - 5, out_5v_x + 10, out_5v_y))
    wires.append(make_wire(out_5v_x, out_5v_y, out_5v_x + 10, out_5v_y))

    # Net label — place on the +5V wire at output node level
    wires.append(make_wire(out_5v_x, out_5v_y, out_5v_x + 3, out_5v_y))
    labels.append(make_label("+5V", out_5v_x + 3, out_5v_y))
    junctions.append(make_junction(out_5v_x, out_5v_y))

    return lib_symbols, symbols, wires, junctions, labels, texts


# ============================================================
# STEP 3: LDO 5V → 3.3V (AMS1117-3.3)
# ============================================================

def generate_step3():
    """Generate Step 3: AMS1117-3.3 LDO for ESP32 3.3V supply."""

    lib_symbols = []
    symbols = []
    wires = []
    junctions = []
    labels = []
    texts = []

    # --- Lib symbols needed ---
    lib_symbols.append(LIB_AMS1117)
    lib_symbols.append(lib_symbol_power("+3V3"))

    # --- Layout ---
    # Place below step 2, Y baseline ~140mm
    base_x = 25
    base_y = 140

    texts.append(make_text("LDO — 5V to 3.3V (ESP32)", base_x, base_y, 2.0))

    # AMS1117 center position
    u3_x = 80
    u3_y = base_y + 15  # = 155

    # AMS1117 pin positions (from symbol definition):
    # Pin 3 (VIN):  left,   (u3_x - 10.16, u3_y - 2.54) = (69.84, 152.46)
    # Pin 2 (VOUT): right,  (u3_x + 10.16, u3_y - 2.54) = (90.16, 152.46)
    # Pin 1 (GND):  bottom, (u3_x, u3_y + 8.89)         = (80, 163.89)

    symbols.append(make_symbol("Custom:LD1117AS33TR", "U3", "LD1117AS33TR",
                               u3_x, u3_y, 0, pin_count=3))

    # +5V input
    vin_x = 55
    vin_y = u3_y - 2.54  # 152.46

    symbols.append(make_symbol("power:+5V", "#PWR12", "+5V",
                               vin_x, vin_y - 5, 0, pin_count=1))
    wires.append(make_wire(vin_x, vin_y - 5, vin_x, vin_y))

    # C4: 10µF input capacitor at (60, 155)
    c4_x = 60
    c4_y = u3_y
    symbols.append(make_symbol("Device:C", "C4", "10uF",
                               c4_x, c4_y, 0, pin_count=2))
    # C4 pin1 at (60, 155-3.81)=(60, 151.19), pin2 at (60, 155+3.81)=(60, 158.81)

    # Wire: +5V → C4 pin1 → AMS1117 VIN
    wires.append(make_wire(vin_x, vin_y, c4_x, vin_y))
    wires.append(make_wire(c4_x, c4_y - 3.81, c4_x, vin_y))
    wires.append(make_wire(c4_x, vin_y, 69.84, vin_y))
    junctions.append(make_junction(c4_x, vin_y))

    # C4 pin2 → GND
    symbols.append(make_symbol("power:GND", "#PWR13", "GND",
                               c4_x, c4_y + 7, 0, pin_count=1))
    wires.append(make_wire(c4_x, c4_y + 3.81, c4_x, c4_y + 7))

    # GND pin of AMS1117 at (80, 163.89)
    symbols.append(make_symbol("power:GND", "#PWR14", "GND",
                               u3_x, u3_y + 12, 0, pin_count=1))
    wires.append(make_wire(u3_x, u3_y + 8.89, u3_x, u3_y + 12))

    # VOUT at (90.16, 152.46)
    vout_x = 110
    vout_y = vin_y  # 152.46

    # C5: 22µF output capacitor at (105, 155)
    c5_x = 105
    c5_y = u3_y
    symbols.append(make_symbol("Device:C", "C5", "22uF",
                               c5_x, c5_y, 0, pin_count=2))
    # C5 pin1 at (105, 151.19), pin2 at (105, 158.81)

    # Wire: AMS1117 VOUT → C5 pin1 → +3V3 output
    wires.append(make_wire(90.16, vout_y, c5_x, vout_y))
    wires.append(make_wire(c5_x, c5_y - 3.81, c5_x, vout_y))
    wires.append(make_wire(c5_x, vout_y, vout_x, vout_y))
    junctions.append(make_junction(c5_x, vout_y))

    # C5 pin2 → GND
    symbols.append(make_symbol("power:GND", "#PWR15", "GND",
                               c5_x, c5_y + 7, 0, pin_count=1))
    wires.append(make_wire(c5_x, c5_y + 3.81, c5_x, c5_y + 7))

    # +3V3 power symbol
    symbols.append(make_symbol("power:+3V3", "#PWR16", "+3V3",
                               vout_x, vout_y - 5, 0, pin_count=1))
    wires.append(make_wire(vout_x, vout_y - 5, vout_x, vout_y))

    # PWR_FLAG removed — +3V3 net is driven by AMS1117 VOUT power_out pin

    return lib_symbols, symbols, wires, junctions, labels, texts


# ============================================================
# STEP 4: Analógové napájanie (+5V_AN, -5V_AN)
# ============================================================

def generate_step4():
    """Generate Step 4: LM7805 linear reg (+5V_AN) + TPS60400 charge pump (-5V_AN)."""

    lib_symbols = []
    symbols = []
    wires = []
    junctions = []
    labels = []
    texts = []

    # --- Lib symbols needed ---
    lib_symbols.append(LIB_LM7805)
    lib_symbols.append(LIB_TPS60400)
    lib_symbols.append(LIB_FB)
    lib_symbols.append(lib_symbol_power("+5V_AN"))
    lib_symbols.append(lib_symbol_power("-5V_AN"))

    # --- Layout ---
    # Place right of step 3 or below. Let's use right half of sheet.
    # A3 = 420mm wide, so plenty of space. Place at X ~200, Y ~95 (same row as step 2)
    base_x = 200
    base_y = 95

    texts.append(make_text("ANALOG POWER — +5V_AN / -5V_AN (Clean)", base_x, base_y, 2.0))

    # ---- LM7805 section ----
    u4_x = 240
    u4_y = base_y + 18  # = 113

    # LM7805 pin positions:
    # Pin 1 (IN):  left,   (u4_x - 10.16, u4_y - 2.54) = (229.84, 110.46)
    # Pin 2 (GND): bottom, (u4_x, u4_y + 8.89)         = (240, 121.89)
    # Pin 3 (OUT): right,  (u4_x + 10.16, u4_y - 2.54) = (250.16, 110.46)

    symbols.append(make_symbol("Custom:L7805ABD2T", "U4", "L7805ABD2T",
                               u4_x, u4_y, 0, pin_count=3))

    # +12V input
    vin_y = u4_y - 2.54  # 110.46
    symbols.append(make_symbol("power:+12V", "#PWR17", "+12V",
                               215, vin_y - 5, 0, pin_count=1))
    wires.append(make_wire(215, vin_y - 5, 215, vin_y))

    # C6: 100nF input ceramic at (220, 113)
    c6_x = 220
    symbols.append(make_symbol("Device:C", "C6", "100nF",
                               c6_x, u4_y, 0, pin_count=2))
    # C6 pin1 at (220, 109.19), pin2 at (220, 116.81)

    # C7: 10µF input electrolytic at (225, 113)
    c7_x = 226
    symbols.append(make_symbol("Device:C_Polarized", "C7", "10uF/25V",
                               c7_x, u4_y, 0, pin_count=2))

    # Wire: +12V → C6 → C7 → LM7805 IN
    wires.append(make_wire(215, vin_y, c6_x, vin_y))
    wires.append(make_wire(c6_x, u4_y - 3.81, c6_x, vin_y))
    junctions.append(make_junction(c6_x, vin_y))
    wires.append(make_wire(c6_x, vin_y, c7_x, vin_y))
    wires.append(make_wire(c7_x, u4_y - 3.81, c7_x, vin_y))
    junctions.append(make_junction(c7_x, vin_y))
    wires.append(make_wire(c7_x, vin_y, 229.84, vin_y))

    # C6, C7 bottom → GND
    gnd_y = u4_y + 7
    symbols.append(make_symbol("power:GND", "#PWR18", "GND",
                               c6_x, gnd_y, 0, pin_count=1))
    wires.append(make_wire(c6_x, u4_y + 3.81, c6_x, gnd_y))

    symbols.append(make_symbol("power:GND", "#PWR19", "GND",
                               c7_x, gnd_y, 0, pin_count=1))
    wires.append(make_wire(c7_x, u4_y + 3.81, c7_x, gnd_y))

    # LM7805 GND
    symbols.append(make_symbol("power:GND", "#PWR20", "GND",
                               u4_x, u4_y + 12, 0, pin_count=1))
    wires.append(make_wire(u4_x, u4_y + 8.89, u4_x, u4_y + 12))

    # Output side: LM7805 OUT → C8 (100nF) → C9 (10µF) → FB1 → +5V_AN
    out_y = vin_y  # 110.46

    # C8: 100nF output ceramic at (255, 113)
    c8_x = 255
    symbols.append(make_symbol("Device:C", "C8", "100nF",
                               c8_x, u4_y, 0, pin_count=2))
    wires.append(make_wire(250.16, out_y, c8_x, out_y))
    wires.append(make_wire(c8_x, u4_y - 3.81, c8_x, out_y))
    junctions.append(make_junction(c8_x, out_y))

    # C9: 10µF output electrolytic at (261, 113)
    c9_x = 261
    symbols.append(make_symbol("Device:C_Polarized", "C9", "10uF/16V",
                               c9_x, u4_y, 0, pin_count=2))
    wires.append(make_wire(c8_x, out_y, c9_x, out_y))
    wires.append(make_wire(c9_x, u4_y - 3.81, c9_x, out_y))
    junctions.append(make_junction(c9_x, out_y))

    # C8, C9 bottom → GND
    symbols.append(make_symbol("power:GND", "#PWR21", "GND",
                               c8_x, gnd_y, 0, pin_count=1))
    wires.append(make_wire(c8_x, u4_y + 3.81, c8_x, gnd_y))

    symbols.append(make_symbol("power:GND", "#PWR22", "GND",
                               c9_x, gnd_y, 0, pin_count=1))
    wires.append(make_wire(c9_x, u4_y + 3.81, c9_x, gnd_y))

    # LC filter: L2 (10µH) + C10 (47µF)
    # L2 horizontal at (271, out_y), rotated 90°
    l2_x = 271
    symbols.append(make_symbol("Device:L", "L2", "10uH",
                               l2_x, out_y, 90, pin_count=2))
    # L2 at 90°: pin1 at (267.19, out_y), pin2 at (274.81, out_y)
    wires.append(make_wire(c9_x, out_y, 267.19, out_y))

    # C10: 47µF at (278, 113)
    c10_x = 278
    symbols.append(make_symbol("Device:C_Polarized", "C10", "47uF/16V",
                               c10_x, u4_y, 0, pin_count=2))
    wires.append(make_wire(274.81, out_y, c10_x, out_y))
    wires.append(make_wire(c10_x, u4_y - 3.81, c10_x, out_y))
    junctions.append(make_junction(c10_x, out_y))

    symbols.append(make_symbol("power:GND", "#PWR23", "GND",
                               c10_x, gnd_y, 0, pin_count=1))
    wires.append(make_wire(c10_x, u4_y + 3.81, c10_x, gnd_y))

    # FB1: ferrite bead horizontal at (286, out_y)
    fb1_x = 286
    symbols.append(make_symbol("Device:FerriteBead", "FB1", "600R@100MHz",
                               fb1_x, out_y, 90, pin_count=2))
    # FB1 at 90°: pin1 at (282.19, out_y), pin2 at (289.81, out_y)
    wires.append(make_wire(c10_x, out_y, 282.19, out_y))

    # +5V_AN power symbol
    v5an_x = 295
    symbols.append(make_symbol("power:+5V_AN", "#PWR24", "+5V_AN",
                               v5an_x, out_y - 5, 0, pin_count=1))
    wires.append(make_wire(289.81, out_y, v5an_x, out_y))
    wires.append(make_wire(v5an_x, out_y - 5, v5an_x, out_y))

    # ---- TPS60400 section ----
    # Place below LM7805, at Y ~140
    u5_x = 250
    u5_y = base_y + 50  # = 145

    texts.append(make_text("CHARGE PUMP — +5V_AN to -5V_AN", base_x, base_y + 37, 1.5))

    # TPS60400 pin positions:
    # Pin 1 (IN):  left,   (u5_x - 11.43, u5_y - 5.08) = (238.57, 139.92)
    # Pin 2 (GND): bottom, (u5_x, u5_y + 11.43)        = (250, 156.43)
    # Pin 3 (C+):  right,  (u5_x + 11.43, u5_y - 5.08) = (261.43, 139.92)
    # Pin 4 (C-):  right,  (u5_x + 11.43, u5_y)        = (261.43, 145)
    # Pin 5 (OUT): right,  (u5_x + 11.43, u5_y + 5.08) = (261.43, 150.08)

    symbols.append(make_symbol("Custom:TPS60400DBVR", "U5", "TPS60400",
                               u5_x, u5_y, 0, pin_count=5))

    # +5V_AN input
    in_y = u5_y - 5.08  # 139.92
    symbols.append(make_symbol("power:+5V_AN", "#PWR25", "+5V_AN",
                               230, in_y - 5, 0, pin_count=1))
    wires.append(make_wire(230, in_y - 5, 230, in_y))
    wires.append(make_wire(230, in_y, 238.57, in_y))

    # GND
    symbols.append(make_symbol("power:GND", "#PWR26", "GND",
                               u5_x, u5_y + 15, 0, pin_count=1))
    wires.append(make_wire(u5_x, u5_y + 11.43, u5_x, u5_y + 15))

    # C11: 1µF flying capacitor between C+ and C-
    # Place at (270, 142.5) vertical
    c11_x = 270
    c11_y = (139.92 + 145) / 2  # between C+ and C- = 142.46
    symbols.append(make_symbol("Device:C", "C11", "1uF",
                               c11_x, c11_y, 0, pin_count=2))
    # C11 pin1 at (270, 138.65), pin2 at (270, 146.27)

    # Wire C+ → C11 pin1
    wires.append(make_wire(261.43, 139.92, c11_x, 139.92))
    wires.append(make_wire(c11_x, c11_y - 3.81, c11_x, 139.92))

    # Wire C- → C11 pin2
    wires.append(make_wire(261.43, 145, c11_x, 145))
    wires.append(make_wire(c11_x, c11_y + 3.81, c11_x, 145))

    # OUT pin at (261.43, 150.08)
    # C12: 10µF output cap at (270, 152)
    c12_x = 270
    c12_y = 152
    symbols.append(make_symbol("Device:C", "C12", "10uF",
                               c12_x, c12_y, 0, pin_count=2))
    # C12 pin1 at (270, 148.19), pin2 at (270, 155.81)

    wires.append(make_wire(261.43, 150.08, c12_x, 150.08))
    wires.append(make_wire(c12_x, c12_y - 3.81, c12_x, 150.08))
    junctions.append(make_junction(c12_x, 150.08))

    # C12 pin2 → GND
    symbols.append(make_symbol("power:GND", "#PWR27", "GND",
                               c12_x, c12_y + 6, 0, pin_count=1))
    wires.append(make_wire(c12_x, c12_y + 3.81, c12_x, c12_y + 6))

    # FB2: ferrite bead horizontal at (280, 150.08)
    fb2_x = 280
    symbols.append(make_symbol("Device:FerriteBead", "FB2", "600R@100MHz",
                               fb2_x, 150.08, 90, pin_count=2))
    # FB2 at 90°: pin1 at (276.19, 150.08), pin2 at (283.81, 150.08)
    wires.append(make_wire(c12_x, 150.08, 276.19, 150.08))

    # -5V_AN power symbol
    v5an_neg_x = 290
    symbols.append(make_symbol("power:-5V_AN", "#PWR28", "-5V_AN",
                               v5an_neg_x, 150.08 + 5, 0, pin_count=1))
    wires.append(make_wire(283.81, 150.08, v5an_neg_x, 150.08))
    wires.append(make_wire(v5an_neg_x, 150.08, v5an_neg_x, 150.08 + 5))

    # PWR_FLAGs for +5V_AN and -5V_AN nets
    symbols.append(make_symbol("power:PWR_FLAG", "#FLG05", "PWR_FLAG",
                               v5an_x + 5, out_y - 5, 0, pin_count=1))
    wires.append(make_wire(v5an_x + 5, out_y - 5, v5an_x + 5, out_y))
    wires.append(make_wire(v5an_x, out_y, v5an_x + 5, out_y))
    junctions.append(make_junction(v5an_x, out_y))

    symbols.append(make_symbol("power:PWR_FLAG", "#FLG06", "PWR_FLAG",
                               v5an_neg_x + 5, 150.08 - 5, 0, pin_count=1))
    wires.append(make_wire(v5an_neg_x + 5, 150.08 - 5, v5an_neg_x + 5, 150.08))
    wires.append(make_wire(v5an_neg_x, 150.08, v5an_neg_x + 5, 150.08))
    junctions.append(make_junction(v5an_neg_x, 150.08))

    return lib_symbols, symbols, wires, junctions, labels, texts


# ============================================================
# STEP 5: pH front-end (CA3140 + TL081)
# ============================================================

def generate_step5():
    """Generate Step 5: pH sensor analog front-end.
    BNC → R2(4.7M) → CA3140 buffer → TL081 inverting amp → pH_OUT
    """

    lib_symbols = []
    symbols = []
    wires = []
    junctions = []
    labels = []
    texts = []
    no_connects = []

    # --- Lib symbols needed ---
    lib_symbols.append(LIB_OPAMP_DIP8)
    lib_symbols.append(LIB_OPAMP_TL081)
    lib_symbols.append(LIB_BNC)
    lib_symbols.append(LIB_POT)

    # --- Layout ---
    # Place on right side of sheet, row 2 (below analog power)
    # X ~200, Y ~175
    base_x = 195
    base_y = 170

    texts.append(make_text("pH SENSOR — Analog Front-End", base_x, base_y, 2.0))

    # ======== BNC CONNECTOR ========
    # P1: BNC at (210, 195)
    # Pin 1 (Signal) exits left at (210-3.81, 195) = (206.19, 195)
    # Pin 2 (Shield) exits bottom at (210, 195+3.81) = (210, 198.81)
    p1_x = 210
    p1_y = 195
    symbols.append(make_symbol("Connector:Conn_Coaxial", "P1", "pH_BNC",
                               p1_x, p1_y, 180, pin_count=2))
    # At 180°: pin1 (Signal) exits right at (213.81, 195)
    # pin2 (Shield) exits top... no wait.
    # 180° rotation: pin1 at left(-3.81,0) rotates to right(+3.81,0) = (213.81, 195)
    # pin2 at bottom(0,-3.81) rotates to top(0,+3.81)... no, (0,-3.81) at 180° = (0, 3.81)
    # Actually for 180°: x→-x, y→-y. So pin1 at (-3.81,0)→(3.81,0), pin2 at (0,-3.81)→(0,3.81)
    # pin2 shield at (210, 195-3.81) = (210, 191.19)... that's up. Let me just not rotate.
    # Default (0°): pin1 at (-3.81, 0) → left, pin2 at (0, -3.81) → down
    # So pin1 Signal at (206.19, 195), pin2 Shield at (210, 198.81) — GND below

    symbols[-1] = make_symbol("Connector:Conn_Coaxial", "P1", "pH_BNC",
                              p1_x, p1_y, 0, pin_count=2)
    # pin1 at (206.19, 195) — will wire to the left, but we need signal going right
    # Let's mirror or use 180°.
    # With 180°: pin1 at (213.81, 195) going right — good
    # pin2 at (210, 191.19) going up — we'll wire GND down from there
    # Actually at 180°: pin2 at (0, -3.81) → (0, 3.81), so absolute (210, 195+3.81)=(210, 198.81)
    # Hmm wait. 180° rotation: point (x,y) → (-x,-y)
    # pin1 at (-3.81, 0) → (3.81, 0) → absolute (213.81, 195) - signal goes right ✓
    # pin2 at (0, -3.81) → (0, 3.81) → absolute (210, 198.81) - shield goes down? No, +3.81 means up
    # Actually in KiCad Y increases downward, so (0, 3.81) after rotation means down. Let me just test.
    # For simplicity: place BNC facing right (180° rotation), connect as needed

    symbols[-1] = make_symbol("Connector:Conn_Coaxial", "P1", "pH_BNC",
                              p1_x, p1_y, 180, pin_count=2)
    # Signal at (213.81, 195), Shield at (210, 198.81) — going down = GND ✓ (KiCad Y+ = down)

    # Shield at 180° is at (p1_x, p1_y - 3.81) = (210, 191.19)
    # Wire from shield pin down to GND symbol below BNC
    symbols.append(make_symbol("power:GND", "#PWR29", "GND",
                               p1_x, p1_y + 7, 0, pin_count=1))
    wires.append(make_wire(p1_x, p1_y - 3.81, p1_x, p1_y + 7))

    # ======== R2: 4.7MΩ input bias ========
    # Horizontal, connecting BNC signal to U6 IN+
    r2_x = 222
    r2_y = p1_y
    symbols.append(make_symbol("Device:R", "R2", "4.7M",
                               r2_x, r2_y, 90, pin_count=2))
    # R at 90°: pin1 at (r2_x-3.81, r2_y)=(218.19, 195), pin2 at (r2_x+3.81, r2_y)=(225.81, 195)

    # Wire BNC signal → R2 pin1
    wires.append(make_wire(213.81, p1_y, 218.19, p1_y))

    # ======== C13: 2.2nF VF filter (from R2/U6 junction to GND) ========
    c13_x = 230
    c13_y = p1_y + 7
    symbols.append(make_symbol("Device:C", "C13", "2.2nF",
                               c13_x, c13_y, 0, pin_count=2))
    # C13 pin1 at (230, 195+7-3.81)=(230, 198.19), pin2 at (230, 195+7+3.81)=(230, 205.81)

    # Junction at R2 output / C13 / U6 IN+ node
    node_in_x = 230
    node_in_y = p1_y  # 195
    wires.append(make_wire(225.81, p1_y, node_in_x, node_in_y))
    wires.append(make_wire(c13_x, c13_y - 3.81, c13_x, node_in_y))
    junctions.append(make_junction(node_in_x, node_in_y))

    # C13 → GND
    symbols.append(make_symbol("power:GND", "#PWR30", "GND",
                               c13_x, c13_y + 7, 0, pin_count=1))
    wires.append(make_wire(c13_x, c13_y + 3.81, c13_x, c13_y + 7))

    # ======== U6: CA3140EZ (buffer) ========
    u6_x = 250
    u6_y = 190

    symbols.append(make_symbol("Custom:CA3140EZ", "U6", "CA3140EZ",
                               u6_x, u6_y, 0, pin_count=8))

    # CA3140 pin positions (from symbol):
    # Pin 2 (IN-): left at (u6_x-8.89, u6_y-2.54) = (241.11, 187.46) — wait, IN- is at +2.54 offset
    # Actually in the symbol: IN- at (at -8.89 2.54 0) → y offset +2.54 from center
    # IN+ at (at -8.89 -2.54 0) → y offset -2.54 from center
    # In KiCad, Y+ is down, so:
    # Pin 2 (IN-) at (241.11, 190+2.54) = (241.11, 192.54) — BELOW center
    # Pin 3 (IN+) at (241.11, 190-2.54) = (241.11, 187.46) — ABOVE center
    # Wait, that's counterintuitive. In the triangle symbol, - is top, + is bottom.
    # Let me re-check: the symbol has text "-" at y=1.905 (upper) and "+" at y=-1.905 (lower).
    # In KiCad Y+ down: y=1.905 is below center, y=-1.905 is above center.
    # So "-" is below, "+" is above... that's wrong for standard op-amp.
    # Actually standard op-amp: IN- at top (non-inverting below).
    # In KiCad: "above center" = smaller Y value. My symbol has:
    # IN- pin at y_offset=2.54 → in KiCad = below center (larger Y)
    # IN+ pin at y_offset=-2.54 → in KiCad = above center (smaller Y)
    # So IN+ is above (smaller Y), IN- is below (larger Y) — this is INVERTED from standard.
    # But that's fine because the triangle text shows + below and - above.
    # Let me just be consistent with pin positions.

    # Pin positions absolute:
    # Pin 2 (IN-):  (241.11, 192.54)
    # Pin 3 (IN+):  (241.11, 187.46)
    # Pin 4 (V-):   (248.73, 198.89)  — bottom
    # Pin 7 (V+):   (248.73, 181.11)  — top
    # Pin 6 (OUT):  (258.89, 190)     — right
    # Pin 1 (N1):   (241.11, 184.92)  — left top (offset null)
    # Pin 5 (N2):   (241.11, 195.08)  — left bottom (offset null)
    # Pin 8 (STR):  (258.89, 195.08)  — right bottom (strobe)

    pin2_x, pin2_y = 241.11, 192.54  # IN-
    pin3_x, pin3_y = 241.11, 187.46  # IN+
    pin4_x, pin4_y = 248.73, 198.89  # V-
    pin7_x, pin7_y = 248.73, 181.11  # V+
    pin6_x, pin6_y = 258.89, 190     # OUT
    pin1_x, pin1_y = 241.11, 184.92  # N1
    pin5_x, pin5_y = 241.11, 195.08  # N2
    pin8_x, pin8_y = 258.89, 195.08  # STR

    # Wire IN+ ← pH signal from R2/C13 junction
    wires.append(make_wire(node_in_x, node_in_y, node_in_x, pin3_y))
    wires.append(make_wire(node_in_x, pin3_y, pin3_x, pin3_y))

    # V+ → +5V_AN
    symbols.append(make_symbol("power:+5V_AN", "#PWR31", "+5V_AN",
                               pin7_x, pin7_y - 5, 0, pin_count=1))
    wires.append(make_wire(pin7_x, pin7_y - 5, pin7_x, pin7_y))

    # V- → -5V_AN
    symbols.append(make_symbol("power:-5V_AN", "#PWR32", "-5V_AN",
                               pin4_x, pin4_y + 5, 0, pin_count=1))
    wires.append(make_wire(pin4_x, pin4_y, pin4_x, pin4_y + 5))

    # Bypass caps C15 (100nF on V+) and C16 (100nF on V-)
    c15_x = pin7_x + 7
    symbols.append(make_symbol("Device:C", "C15", "100nF",
                               c15_x, pin7_y - 2, 0, pin_count=2))
    wires.append(make_wire(pin7_x, pin7_y, c15_x, pin7_y))
    wires.append(make_wire(c15_x, pin7_y - 2 - 3.81, c15_x, pin7_y))
    junctions.append(make_junction(pin7_x, pin7_y))
    symbols.append(make_symbol("power:GND", "#PWR33", "GND",
                               c15_x, pin7_y + 3, 0, pin_count=1))
    wires.append(make_wire(c15_x, pin7_y - 2 + 3.81, c15_x, pin7_y + 3))

    c16_x = pin4_x + 7
    symbols.append(make_symbol("Device:C", "C16", "100nF",
                               c16_x, pin4_y + 2, 0, pin_count=2))
    wires.append(make_wire(pin4_x, pin4_y, c16_x, pin4_y))
    wires.append(make_wire(c16_x, pin4_y + 2 - 3.81, c16_x, pin4_y))
    junctions.append(make_junction(pin4_x, pin4_y))
    symbols.append(make_symbol("power:GND", "#PWR34", "GND",
                               c16_x, pin4_y + 9, 0, pin_count=1))
    wires.append(make_wire(c16_x, pin4_y + 2 + 3.81, c16_x, pin4_y + 9))

    # NC on pin 1 (N1), pin 5 (N2), pin 8 (STR)
    no_connects.append(make_no_connect(pin1_x, pin1_y))
    no_connects.append(make_no_connect(pin5_x, pin5_y))
    no_connects.append(make_no_connect(pin8_x, pin8_y))

    # ======== Feedback network on IN- (pin 2) ========
    # From original schematic: C2(1µF) + R4(2.2kΩ) feedback, R5(5kΩ trimer), R6(1kΩ)
    # Simplified: IN- connects to output via feedback network
    # R3 (2.2kΩ) from IN- to GND (via R5 trimer wiper)
    # C14 (1µF) from IN- to output (AC feedback)
    # R5 (5kΩ pot) for calibration

    # Feedback: C14 (1µF) from OUT to IN-
    c14_x = u6_x
    c14_y = pin2_y + 10  # below U6
    symbols.append(make_symbol("Device:C", "C14", "1uF",
                               c14_x, c14_y, 90, pin_count=2))
    # C14 at 90°: pin1 at (c14_x-3.81, c14_y)=(246.19, 202.54), pin2 at (c14_x+3.81, c14_y)=(253.81, 202.54)

    # Wire IN- down to C14 pin1
    wires.append(make_wire(pin2_x, pin2_y, pin2_x, c14_y))
    wires.append(make_wire(pin2_x, c14_y, c14_x - 3.81, c14_y))

    # Wire OUT down to C14 pin2
    out_node_x = pin6_x
    out_node_y = pin6_y
    wires.append(make_wire(out_node_x, out_node_y, out_node_x, c14_y))
    wires.append(make_wire(out_node_x, c14_y, c14_x + 3.81, c14_y))
    junctions.append(make_junction(out_node_x, out_node_y))

    # R3 (2.2kΩ) from IN- junction down to R5 wiper
    r3_x = pin2_x - 5
    r3_y = c14_y + 8
    symbols.append(make_symbol("Device:R", "R3", "2.2k",
                               r3_x, r3_y, 0, pin_count=2))
    # R3 pin1 at (r3_x, r3_y-3.81), pin2 at (r3_x, r3_y+3.81)
    wires.append(make_wire(pin2_x, c14_y, r3_x, c14_y))
    wires.append(make_wire(r3_x, r3_y - 3.81, r3_x, c14_y))
    junctions.append(make_junction(pin2_x, c14_y))

    # R4 (5kΩ trimer) - potentiometer
    r4_x = r3_x
    r4_y = r3_y + 12
    symbols.append(make_symbol("Device:R_Potentiometer", "R4", "5k",
                               r4_x, r4_y, 0, pin_count=3))
    # Pot: pin1 at (r4_x, r4_y-3.81), pin2(wiper) at (r4_x+3.81, r4_y), pin3 at (r4_x, r4_y+3.81)
    wires.append(make_wire(r3_x, r3_y + 3.81, r4_x, r4_y - 3.81))

    # R5 (1kΩ) from pot pin3 to GND
    r5_x = r4_x
    r5_y = r4_y + 10
    symbols.append(make_symbol("Device:R", "R5", "1k",
                               r5_x, r5_y, 0, pin_count=2))
    wires.append(make_wire(r4_x, r4_y + 3.81, r5_x, r5_y - 3.81))

    symbols.append(make_symbol("power:GND", "#PWR35", "GND",
                               r5_x, r5_y + 8, 0, pin_count=1))
    wires.append(make_wire(r5_x, r5_y + 3.81, r5_x, r5_y + 8))

    # Pot wiper (pin2) at (r4_x + 3.81, r4_y) — unused, mark no_connect
    no_connects.append(make_no_connect(r4_x + 3.81, r4_y))

    # ======== U7: TL071IP (output stage, inverting amplifier) ========
    u7_x = 290
    u7_y = 190

    symbols.append(make_symbol("Custom:TL071IP", "U7", "TL071IP",
                               u7_x, u7_y, 0, pin_count=8))

    # TL081 pin positions (same layout as CA3140):
    u7_pin2_x, u7_pin2_y = u7_x - 8.89, u7_y + 2.54   # IN- = (281.11, 192.54)
    u7_pin3_x, u7_pin3_y = u7_x - 8.89, u7_y - 2.54   # IN+ = (281.11, 187.46)
    u7_pin4_x, u7_pin4_y = u7_x - 1.27, u7_y + 8.89   # V-  = (288.73, 198.89)
    u7_pin7_x, u7_pin7_y = u7_x - 1.27, u7_y - 8.89   # V+  = (288.73, 181.11)
    u7_pin6_x, u7_pin6_y = u7_x + 8.89, u7_y           # OUT = (298.89, 190)
    u7_pin1_x, u7_pin1_y = u7_x - 8.89, u7_y - 5.08   # N1
    u7_pin5_x, u7_pin5_y = u7_x - 8.89, u7_y + 5.08   # N2
    u7_pin8_x, u7_pin8_y = u7_x + 8.89, u7_y + 5.08   # N2B

    # R7 (30kΩ) input resistor: U6 OUT → U7 IN-
    r7_x = 270
    r7_y = u7_pin2_y  # 192.54
    symbols.append(make_symbol("Device:R", "R7", "30k",
                               r7_x, r7_y, 90, pin_count=2))
    # R7 at 90°: pin1 at (266.19, 192.54), pin2 at (273.81, 192.54)

    # Wire U6 OUT → R7 pin1
    wires.append(make_wire(out_node_x, out_node_y, out_node_x, r7_y))
    wires.append(make_wire(out_node_x, r7_y, 266.19, r7_y))
    junctions.append(make_junction(out_node_x, r7_y))

    # Wire R7 pin2 → U7 IN-
    wires.append(make_wire(273.81, r7_y, u7_pin2_x, u7_pin2_y))

    # R6 (30kΩ) feedback: U7 OUT → U7 IN-
    r6_x = u7_x
    r6_y = u7_pin2_y + 10  # below U7
    symbols.append(make_symbol("Device:R", "R6", "30k",
                               r6_x, r6_y, 90, pin_count=2))
    # R6 at 90°: pin1 at (r6_x-3.81, r6_y)=(286.19, 202.54), pin2 at (r6_x+3.81, r6_y)=(293.81, 202.54)

    # Wire from IN- pin to feedback junction, then down to R6 pin1
    fb_junct_x = u7_pin2_x + 2
    fb_junct_y = u7_pin2_y
    wires.append(make_wire(u7_pin2_x, u7_pin2_y, fb_junct_x, fb_junct_y))
    junctions.append(make_junction(u7_pin2_x, u7_pin2_y))
    wires.append(make_wire(fb_junct_x, fb_junct_y, fb_junct_x, r6_y))
    wires.append(make_wire(fb_junct_x, r6_y, r6_x - 3.81, r6_y))

    # Wire R6 pin2 → U7 OUT (via junction)
    wires.append(make_wire(r6_x + 3.81, r6_y, u7_pin6_x, r6_y))
    wires.append(make_wire(u7_pin6_x, r6_y, u7_pin6_x, u7_pin6_y))
    junctions.append(make_junction(u7_pin6_x, u7_pin6_y))

    # R8 (75kΩ) from IN+ to GND (offset/bias)
    r8_x = u7_pin3_x - 5
    r8_y = u7_pin3_y
    symbols.append(make_symbol("Device:R", "R8", "75k",
                               r8_x, r8_y, 0, pin_count=2))
    # R8 vertical: pin1 at (r8_x, r8_y-3.81), pin2 at (r8_x, r8_y+3.81)
    wires.append(make_wire(r8_x, r8_y - 3.81, r8_x, u7_pin3_y))
    wires.append(make_wire(r8_x, u7_pin3_y, u7_pin3_x, u7_pin3_y))

    symbols.append(make_symbol("power:GND", "#PWR36", "GND",
                               r8_x, r8_y + 8, 0, pin_count=1))
    wires.append(make_wire(r8_x, r8_y + 3.81, r8_x, r8_y + 8))

    # U7 V+ → +5V_AN
    symbols.append(make_symbol("power:+5V_AN", "#PWR37", "+5V_AN",
                               u7_pin7_x, u7_pin7_y - 5, 0, pin_count=1))
    wires.append(make_wire(u7_pin7_x, u7_pin7_y - 5, u7_pin7_x, u7_pin7_y))

    # U7 V- → -5V_AN
    symbols.append(make_symbol("power:-5V_AN", "#PWR38", "-5V_AN",
                               u7_pin4_x, u7_pin4_y + 5, 0, pin_count=1))
    wires.append(make_wire(u7_pin4_x, u7_pin4_y, u7_pin4_x, u7_pin4_y + 5))

    # Bypass caps C17, C18 for U7
    c17_x = u7_pin7_x + 7
    symbols.append(make_symbol("Device:C", "C17", "100nF",
                               c17_x, u7_pin7_y - 2, 0, pin_count=2))
    wires.append(make_wire(u7_pin7_x, u7_pin7_y, c17_x, u7_pin7_y))
    wires.append(make_wire(c17_x, u7_pin7_y - 2 - 3.81, c17_x, u7_pin7_y))
    junctions.append(make_junction(u7_pin7_x, u7_pin7_y))
    symbols.append(make_symbol("power:GND", "#PWR39", "GND",
                               c17_x, u7_pin7_y + 3, 0, pin_count=1))
    wires.append(make_wire(c17_x, u7_pin7_y - 2 + 3.81, c17_x, u7_pin7_y + 3))

    c18_x = u7_pin4_x + 7
    symbols.append(make_symbol("Device:C", "C18", "100nF",
                               c18_x, u7_pin4_y + 2, 0, pin_count=2))
    wires.append(make_wire(u7_pin4_x, u7_pin4_y, c18_x, u7_pin4_y))
    wires.append(make_wire(c18_x, u7_pin4_y + 2 - 3.81, c18_x, u7_pin4_y))
    junctions.append(make_junction(u7_pin4_x, u7_pin4_y))
    symbols.append(make_symbol("power:GND", "#PWR40", "GND",
                               c18_x, u7_pin4_y + 9, 0, pin_count=1))
    wires.append(make_wire(c18_x, u7_pin4_y + 2 + 3.81, c18_x, u7_pin4_y + 9))

    # NC on U7 unused pins
    no_connects.append(make_no_connect(u7_pin1_x, u7_pin1_y))
    no_connects.append(make_no_connect(u7_pin5_x, u7_pin5_y))
    no_connects.append(make_no_connect(u7_pin8_x, u7_pin8_y))

    # ======== OUTPUT: pH_OUT label ========
    labels.append(make_label("pH_OUT", u7_pin6_x + 2, u7_pin6_y))
    wires.append(make_wire(u7_pin6_x, u7_pin6_y, u7_pin6_x + 15, u7_pin6_y))

    return lib_symbols, symbols, wires, junctions, labels, texts, no_connects


# ============================================================
# STEP 6: ORP front-end (CA3140 + TL081) — copy of Step 5
# ============================================================

def generate_step6():
    """Generate Step 6: ORP sensor analog front-end.
    BNC → R9(4.7M) → CA3140 buffer → TL081 inverting amp → ORP_OUT
    Identical topology to Step 5, offset Y+70, different refs.
    """

    lib_symbols = []
    symbols = []
    wires = []
    junctions = []
    labels = []
    texts = []
    no_connects = []

    # No new lib symbols needed — CA3140, TL081, BNC, POT already defined in step 5

    # --- Section label ---
    texts.append(make_text("ORP FRONT-END", 205, 240, size=3))

    # Y offset from pH: +70
    dy = 70

    # ======== BNC CONNECTOR ========
    p2_x = 210
    p2_y = 195 + dy  # 265
    symbols.append(make_symbol("Connector:Conn_Coaxial", "P2", "ORP_BNC",
                               p2_x, p2_y, 180, pin_count=2))
    # 180°: Signal at (213.81, 265), Shield at (210, 268.81)

    # Shield at 180° is at (p2_x, p2_y - 3.81) = (210, 261.19)
    symbols.append(make_symbol("power:GND", "#PWR41", "GND",
                               p2_x, p2_y + 7, 0, pin_count=1))
    wires.append(make_wire(p2_x, p2_y - 3.81, p2_x, p2_y + 7))

    # ======== R9: 4.7MΩ input bias ========
    r9_x = 222
    r9_y = p2_y
    symbols.append(make_symbol("Device:R", "R9", "4.7M",
                               r9_x, r9_y, 90, pin_count=2))
    # pin1 at (218.19, 265), pin2 at (225.81, 265)

    # Wire BNC signal → R9 pin1
    wires.append(make_wire(213.81, p2_y, 218.19, p2_y))

    # ======== C19: 2.2nF VF filter ========
    c19_x = 230
    c19_y = p2_y + 7
    symbols.append(make_symbol("Device:C", "C19", "2.2nF",
                               c19_x, c19_y, 0, pin_count=2))

    # Junction at R9 output / C19 / U8 IN+
    node_in_x = 230
    node_in_y = p2_y
    wires.append(make_wire(225.81, p2_y, node_in_x, node_in_y))
    wires.append(make_wire(c19_x, c19_y - 3.81, c19_x, node_in_y))
    junctions.append(make_junction(node_in_x, node_in_y))

    # C19 → GND
    symbols.append(make_symbol("power:GND", "#PWR42", "GND",
                               c19_x, c19_y + 7, 0, pin_count=1))
    wires.append(make_wire(c19_x, c19_y + 3.81, c19_x, c19_y + 7))

    # ======== U8: CA3140EZ (buffer) ========
    u8_x = 250
    u8_y = 190 + dy  # 260

    symbols.append(make_symbol("Custom:CA3140EZ", "U8", "CA3140EZ",
                               u8_x, u8_y, 0, pin_count=8))

    # Pin positions absolute (same offsets as U6):
    pin2_x, pin2_y = u8_x - 8.89, u8_y + 2.54   # IN-  (241.11, 262.54)
    pin3_x, pin3_y = u8_x - 8.89, u8_y - 2.54   # IN+  (241.11, 257.46)
    pin4_x, pin4_y = u8_x - 1.27, u8_y + 8.89   # V-   (248.73, 268.89)
    pin7_x, pin7_y = u8_x - 1.27, u8_y - 8.89   # V+   (248.73, 251.11)
    pin6_x, pin6_y = u8_x + 8.89, u8_y           # OUT  (258.89, 260)
    pin1_x, pin1_y = u8_x - 8.89, u8_y - 5.08   # N1   (241.11, 254.92)
    pin5_x, pin5_y = u8_x - 8.89, u8_y + 5.08   # N2   (241.11, 265.08)
    pin8_x, pin8_y = u8_x + 8.89, u8_y + 5.08   # STR  (258.89, 265.08)

    # Wire IN+ ← ORP signal from R9/C19 junction
    wires.append(make_wire(node_in_x, node_in_y, node_in_x, pin3_y))
    wires.append(make_wire(node_in_x, pin3_y, pin3_x, pin3_y))

    # V+ → +5V_AN
    symbols.append(make_symbol("power:+5V_AN", "#PWR43", "+5V_AN",
                               pin7_x, pin7_y - 5, 0, pin_count=1))
    wires.append(make_wire(pin7_x, pin7_y - 5, pin7_x, pin7_y))

    # V- → -5V_AN
    symbols.append(make_symbol("power:-5V_AN", "#PWR44", "-5V_AN",
                               pin4_x, pin4_y + 5, 0, pin_count=1))
    wires.append(make_wire(pin4_x, pin4_y, pin4_x, pin4_y + 5))

    # Bypass caps C21 (100nF on V+) and C22 (100nF on V-)
    c21_x = pin7_x + 7
    symbols.append(make_symbol("Device:C", "C21", "100nF",
                               c21_x, pin7_y - 2, 0, pin_count=2))
    wires.append(make_wire(pin7_x, pin7_y, c21_x, pin7_y))
    wires.append(make_wire(c21_x, pin7_y - 2 - 3.81, c21_x, pin7_y))
    junctions.append(make_junction(pin7_x, pin7_y))
    symbols.append(make_symbol("power:GND", "#PWR45", "GND",
                               c21_x, pin7_y + 3, 0, pin_count=1))
    wires.append(make_wire(c21_x, pin7_y - 2 + 3.81, c21_x, pin7_y + 3))

    c22_x = pin4_x + 7
    symbols.append(make_symbol("Device:C", "C22", "100nF",
                               c22_x, pin4_y + 2, 0, pin_count=2))
    wires.append(make_wire(pin4_x, pin4_y, c22_x, pin4_y))
    wires.append(make_wire(c22_x, pin4_y + 2 - 3.81, c22_x, pin4_y))
    junctions.append(make_junction(pin4_x, pin4_y))
    symbols.append(make_symbol("power:GND", "#PWR46", "GND",
                               c22_x, pin4_y + 9, 0, pin_count=1))
    wires.append(make_wire(c22_x, pin4_y + 2 + 3.81, c22_x, pin4_y + 9))

    # NC on pin 1 (N1), pin 5 (N2), pin 8 (STR)
    no_connects.append(make_no_connect(pin1_x, pin1_y))
    no_connects.append(make_no_connect(pin5_x, pin5_y))
    no_connects.append(make_no_connect(pin8_x, pin8_y))

    # ======== Feedback network on IN- (pin 2) ========
    # C20 (1µF) from OUT to IN-
    c20_x = u8_x
    c20_y = pin2_y + 10
    symbols.append(make_symbol("Device:C", "C20", "1uF",
                               c20_x, c20_y, 90, pin_count=2))

    # Wire IN- down to C20 pin1
    wires.append(make_wire(pin2_x, pin2_y, pin2_x, c20_y))
    wires.append(make_wire(pin2_x, c20_y, c20_x - 3.81, c20_y))

    # Wire OUT down to C20 pin2
    out_node_x = pin6_x
    out_node_y = pin6_y
    wires.append(make_wire(out_node_x, out_node_y, out_node_x, c20_y))
    wires.append(make_wire(out_node_x, c20_y, c20_x + 3.81, c20_y))
    junctions.append(make_junction(out_node_x, out_node_y))

    # R10 (2.2kΩ) from IN- junction down to R11 wiper
    r10_x = pin2_x - 5
    r10_y = c20_y + 8
    symbols.append(make_symbol("Device:R", "R10", "2.2k",
                               r10_x, r10_y, 0, pin_count=2))
    wires.append(make_wire(pin2_x, c20_y, r10_x, c20_y))
    wires.append(make_wire(r10_x, r10_y - 3.81, r10_x, c20_y))
    junctions.append(make_junction(pin2_x, c20_y))

    # R11 (5kΩ trimer) - potentiometer
    r11_x = r10_x
    r11_y = r10_y + 12
    symbols.append(make_symbol("Device:R_Potentiometer", "R11", "5k",
                               r11_x, r11_y, 0, pin_count=3))
    wires.append(make_wire(r10_x, r10_y + 3.81, r11_x, r11_y - 3.81))

    # R12 (1kΩ) from pot pin3 to GND
    r12_x = r11_x
    r12_y = r11_y + 10
    symbols.append(make_symbol("Device:R", "R12", "1k",
                               r12_x, r12_y, 0, pin_count=2))
    wires.append(make_wire(r11_x, r11_y + 3.81, r12_x, r12_y - 3.81))

    symbols.append(make_symbol("power:GND", "#PWR47", "GND",
                               r12_x, r12_y + 8, 0, pin_count=1))
    wires.append(make_wire(r12_x, r12_y + 3.81, r12_x, r12_y + 8))

    # Pot R11 wiper (pin2) at (r11_x + 3.81, r11_y) — unused, mark no_connect
    no_connects.append(make_no_connect(r11_x + 3.81, r11_y))

    # ======== U9: TL071IP (inverting amplifier) ========
    u9_x = 290
    u9_y = 190 + dy  # 260

    symbols.append(make_symbol("Custom:TL071IP", "U9", "TL071IP",
                               u9_x, u9_y, 0, pin_count=8))

    u9_pin2_x, u9_pin2_y = u9_x - 8.89, u9_y + 2.54   # IN-
    u9_pin3_x, u9_pin3_y = u9_x - 8.89, u9_y - 2.54   # IN+
    u9_pin4_x, u9_pin4_y = u9_x - 1.27, u9_y + 8.89   # V-
    u9_pin7_x, u9_pin7_y = u9_x - 1.27, u9_y - 8.89   # V+
    u9_pin6_x, u9_pin6_y = u9_x + 8.89, u9_y           # OUT
    u9_pin1_x, u9_pin1_y = u9_x - 8.89, u9_y - 5.08   # N1
    u9_pin5_x, u9_pin5_y = u9_x - 8.89, u9_y + 5.08   # N2
    u9_pin8_x, u9_pin8_y = u9_x + 8.89, u9_y + 5.08   # N2B

    # R14 (30kΩ) input resistor: U8 OUT → U9 IN-
    r14_x = 270
    r14_y = u9_pin2_y
    symbols.append(make_symbol("Device:R", "R14", "30k",
                               r14_x, r14_y, 90, pin_count=2))

    # Wire U8 OUT → R14 pin1
    wires.append(make_wire(out_node_x, out_node_y, out_node_x, r14_y))
    wires.append(make_wire(out_node_x, r14_y, 266.19, r14_y))
    junctions.append(make_junction(out_node_x, r14_y))

    # Wire R14 pin2 → U9 IN-
    wires.append(make_wire(273.81, r14_y, u9_pin2_x, u9_pin2_y))

    # R13 (30kΩ) feedback: U9 OUT → U9 IN-
    r13_x = u9_x
    r13_y = u9_pin2_y + 10
    symbols.append(make_symbol("Device:R", "R13", "30k",
                               r13_x, r13_y, 90, pin_count=2))

    # Wire from IN- pin to feedback junction, then down to R13 pin1
    fb_junct_x = u9_pin2_x + 2
    fb_junct_y = u9_pin2_y
    wires.append(make_wire(u9_pin2_x, u9_pin2_y, fb_junct_x, fb_junct_y))
    junctions.append(make_junction(u9_pin2_x, u9_pin2_y))
    wires.append(make_wire(fb_junct_x, fb_junct_y, fb_junct_x, r13_y))
    wires.append(make_wire(fb_junct_x, r13_y, r13_x - 3.81, r13_y))

    # Wire R13 pin2 → U9 OUT
    wires.append(make_wire(r13_x + 3.81, r13_y, u9_pin6_x, r13_y))
    wires.append(make_wire(u9_pin6_x, r13_y, u9_pin6_x, u9_pin6_y))
    junctions.append(make_junction(u9_pin6_x, u9_pin6_y))

    # R15 (75kΩ) from IN+ to GND
    r15_x = u9_pin3_x - 5
    r15_y = u9_pin3_y
    symbols.append(make_symbol("Device:R", "R15", "75k",
                               r15_x, r15_y, 0, pin_count=2))
    wires.append(make_wire(r15_x, r15_y - 3.81, r15_x, u9_pin3_y))
    wires.append(make_wire(r15_x, u9_pin3_y, u9_pin3_x, u9_pin3_y))

    symbols.append(make_symbol("power:GND", "#PWR48", "GND",
                               r15_x, r15_y + 8, 0, pin_count=1))
    wires.append(make_wire(r15_x, r15_y + 3.81, r15_x, r15_y + 8))

    # U9 V+ → +5V_AN
    symbols.append(make_symbol("power:+5V_AN", "#PWR49", "+5V_AN",
                               u9_pin7_x, u9_pin7_y - 5, 0, pin_count=1))
    wires.append(make_wire(u9_pin7_x, u9_pin7_y - 5, u9_pin7_x, u9_pin7_y))

    # U9 V- → -5V_AN
    symbols.append(make_symbol("power:-5V_AN", "#PWR50", "-5V_AN",
                               u9_pin4_x, u9_pin4_y + 5, 0, pin_count=1))
    wires.append(make_wire(u9_pin4_x, u9_pin4_y, u9_pin4_x, u9_pin4_y + 5))

    # Bypass caps C23, C24 for U9
    c23_x = u9_pin7_x + 7
    symbols.append(make_symbol("Device:C", "C23", "100nF",
                               c23_x, u9_pin7_y - 2, 0, pin_count=2))
    wires.append(make_wire(u9_pin7_x, u9_pin7_y, c23_x, u9_pin7_y))
    wires.append(make_wire(c23_x, u9_pin7_y - 2 - 3.81, c23_x, u9_pin7_y))
    junctions.append(make_junction(u9_pin7_x, u9_pin7_y))
    symbols.append(make_symbol("power:GND", "#PWR51", "GND",
                               c23_x, u9_pin7_y + 3, 0, pin_count=1))
    wires.append(make_wire(c23_x, u9_pin7_y - 2 + 3.81, c23_x, u9_pin7_y + 3))

    c24_x = u9_pin4_x + 7
    symbols.append(make_symbol("Device:C", "C24", "100nF",
                               c24_x, u9_pin4_y + 2, 0, pin_count=2))
    wires.append(make_wire(u9_pin4_x, u9_pin4_y, c24_x, u9_pin4_y))
    wires.append(make_wire(c24_x, u9_pin4_y + 2 - 3.81, c24_x, u9_pin4_y))
    junctions.append(make_junction(u9_pin4_x, u9_pin4_y))
    symbols.append(make_symbol("power:GND", "#PWR52", "GND",
                               c24_x, u9_pin4_y + 9, 0, pin_count=1))
    wires.append(make_wire(c24_x, u9_pin4_y + 2 + 3.81, c24_x, u9_pin4_y + 9))

    # NC on U9 unused pins
    no_connects.append(make_no_connect(u9_pin1_x, u9_pin1_y))
    no_connects.append(make_no_connect(u9_pin5_x, u9_pin5_y))
    no_connects.append(make_no_connect(u9_pin8_x, u9_pin8_y))

    # ======== OUTPUT: ORP_OUT label ========
    labels.append(make_label("ORP_OUT", u9_pin6_x + 2, u9_pin6_y))
    wires.append(make_wire(u9_pin6_x, u9_pin6_y, u9_pin6_x + 15, u9_pin6_y))

    return lib_symbols, symbols, wires, junctions, labels, texts, no_connects


# ============================================================
# STEP 7: ADS1115 ADC
# ============================================================

# ADS1115IDGSR MSOP-10 lib symbol
# Pin 1: ADDR, Pin 2: ALRT/RDY, Pin 3: GND, Pin 4: AIN0, Pin 5: AIN1
# Pin 6: AIN2, Pin 7: AIN3, Pin 8: VDD, Pin 9: SDA, Pin 10: SCL
LIB_ADS1115 = """(symbol "Custom:ADS1115IDGSR"
\t\t(pin_names (offset 1.016))
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(property "Reference" "U"
\t\t\t(at 0 13.97 0)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Value" "ADS1115IDGSR"
\t\t\t(at 0 -13.97 0)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Footprint" "Package_SO:MSOP-10_3x3mm_P0.5mm"
\t\t\t(at 0 -16.51 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(symbol "ADS1115IDGSR_0_1"
\t\t\t(rectangle (start -10.16 12.7) (end 10.16 -12.7)
\t\t\t\t(stroke (width 0.254) (type default))
\t\t\t\t(fill (type background))
\t\t\t)
\t\t)
\t\t(symbol "ADS1115IDGSR_1_1"
\t\t\t(pin input line (at -13.97 7.62 0) (length 3.81)
\t\t\t\t(name "AIN0" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "4" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin input line (at -13.97 5.08 0) (length 3.81)
\t\t\t\t(name "AIN1" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "5" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin input line (at -13.97 2.54 0) (length 3.81)
\t\t\t\t(name "AIN2" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "6" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin input line (at -13.97 0 0) (length 3.81)
\t\t\t\t(name "AIN3" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "7" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin input line (at -13.97 -5.08 0) (length 3.81)
\t\t\t\t(name "ADDR" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "1" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin power_in line (at 0 15.24 270) (length 2.54)
\t\t\t\t(name "VDD" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "8" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin power_in line (at 0 -15.24 90) (length 2.54)
\t\t\t\t(name "GND" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "3" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin bidirectional line (at 13.97 5.08 180) (length 3.81)
\t\t\t\t(name "SDA" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "9" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin output line (at 13.97 2.54 180) (length 3.81)
\t\t\t\t(name "SCL" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "10" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin open_collector line (at 13.97 -5.08 180) (length 3.81)
\t\t\t\t(name "ALRT" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "2" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t)
\t)"""


def generate_step7():
    """Generate Step 7: ADS1115 16-bit ADC with I2C pull-ups.
    pH_OUT → AIN0, ORP_OUT → AIN1, SDA/SCL → ESP32
    """

    lib_symbols = []
    symbols = []
    wires = []
    junctions = []
    labels = []
    texts = []
    no_connects = []

    lib_symbols.append(LIB_ADS1115)

    # --- Section label ---
    texts.append(make_text("ADC — ADS1115", 330, 170, size=3))

    # ======== U10: ADS1115 ========
    # Place to the right of the analog front-ends
    u10_x = 355
    u10_y = 200

    symbols.append(make_symbol("Custom:ADS1115IDGSR", "U10", "ADS1115",
                               u10_x, u10_y, 0, pin_count=10))

    # Pin positions (from lib symbol definition):
    # AIN0 (pin 4): left at (u10_x - 13.97, u10_y - 7.62) — wait, y offset 7.62 from center
    # In symbol: AIN0 at (at -13.97 7.62 0) → KiCad coords: x_abs = u10_x - 13.97, y_abs = u10_y - 7.62
    # (KiCad Y+ = down, symbol Y+ = up, so symbol y=7.62 → absolute y = center - 7.62)
    # Wait — in KiCad lib symbols, Y is screen Y (down positive)? No.
    # In KiCad symbol definitions, Y axis is inverted vs schematic. Symbol y+ = up, schematic y+ = down.
    # So symbol position (x, y) → schematic absolute (u10_x + x, u10_y - y)
    ain0_x, ain0_y = u10_x - 13.97, u10_y - 7.62   # (341.03, 192.38)
    ain1_x, ain1_y = u10_x - 13.97, u10_y - 5.08   # (341.03, 194.92)
    ain2_x, ain2_y = u10_x - 13.97, u10_y - 2.54   # (341.03, 197.46)
    ain3_x, ain3_y = u10_x - 13.97, u10_y           # (341.03, 200)
    addr_x, addr_y = u10_x - 13.97, u10_y + 5.08   # (341.03, 205.08)
    vdd_x, vdd_y   = u10_x, u10_y - 15.24           # (355, 184.76)
    gnd_x, gnd_y   = u10_x, u10_y + 15.24           # (355, 215.24)
    sda_x, sda_y   = u10_x + 13.97, u10_y - 5.08   # (368.97, 194.92)
    scl_x, scl_y   = u10_x + 13.97, u10_y - 2.54   # (368.97, 197.46)
    alrt_x, alrt_y = u10_x + 13.97, u10_y + 5.08   # (368.97, 205.08)

    # AIN0 ← pH_OUT (net label)
    labels.append(make_label("pH_OUT", ain0_x - 5, ain0_y, angle=180))
    wires.append(make_wire(ain0_x - 5, ain0_y, ain0_x, ain0_y))

    # AIN1 ← ORP_OUT (net label)
    labels.append(make_label("ORP_OUT", ain1_x - 5, ain1_y, angle=180))
    wires.append(make_wire(ain1_x - 5, ain1_y, ain1_x, ain1_y))

    # AIN2, AIN3 — no connect (voľný, vyvedený na pad — but for schematic, NC)
    no_connects.append(make_no_connect(ain2_x, ain2_y))
    no_connects.append(make_no_connect(ain3_x, ain3_y))

    # ADDR → GND (I2C address 0x48)
    symbols.append(make_symbol("power:GND", "#PWR53", "GND",
                               addr_x - 5, addr_y, 90, pin_count=1))
    wires.append(make_wire(addr_x - 5, addr_y, addr_x, addr_y))

    # ALRT/RDY → NC
    no_connects.append(make_no_connect(alrt_x, alrt_y))

    # VDD → +3V3
    symbols.append(make_symbol("power:+3V3", "#PWR54", "+3V3",
                               vdd_x, vdd_y - 3, 0, pin_count=1))
    wires.append(make_wire(vdd_x, vdd_y - 3, vdd_x, vdd_y))

    # GND
    symbols.append(make_symbol("power:GND", "#PWR55", "GND",
                               gnd_x, gnd_y + 3, 0, pin_count=1))
    wires.append(make_wire(gnd_x, gnd_y, gnd_x, gnd_y + 3))

    # C25: 100nF bypass on VDD
    c25_x = vdd_x + 8
    c25_y = vdd_y
    symbols.append(make_symbol("Device:C", "C25", "100nF",
                               c25_x, c25_y, 0, pin_count=2))
    # Wire from VDD net to C25 top
    wires.append(make_wire(vdd_x, vdd_y, c25_x, vdd_y))
    wires.append(make_wire(c25_x, c25_y - 3.81, c25_x, vdd_y))
    junctions.append(make_junction(vdd_x, vdd_y))
    # C25 bottom → GND
    symbols.append(make_symbol("power:GND", "#PWR56", "GND",
                               c25_x, c25_y + 5, 0, pin_count=1))
    wires.append(make_wire(c25_x, c25_y + 3.81, c25_x, c25_y + 5))

    # SDA net label + R16 pull-up
    sda_label_x = sda_x + 3
    labels.append(make_label("SDA", sda_label_x, sda_y))
    wires.append(make_wire(sda_x, sda_y, sda_label_x + 10, sda_y))

    # R16: 4.7kΩ pull-up SDA → +3V3
    r16_x = sda_label_x + 5
    r16_y = sda_y - 8
    symbols.append(make_symbol("Device:R", "R16", "4.7k",
                               r16_x, r16_y, 0, pin_count=2))
    # pin1 at (r16_x, r16_y-3.81), pin2 at (r16_x, r16_y+3.81)
    wires.append(make_wire(r16_x, r16_y + 3.81, r16_x, sda_y))
    junctions.append(make_junction(r16_x, sda_y))
    symbols.append(make_symbol("power:+3V3", "#PWR57", "+3V3",
                               r16_x, r16_y - 8, 0, pin_count=1))
    wires.append(make_wire(r16_x, r16_y - 3.81, r16_x, r16_y - 8))

    # SCL net label + R17 pull-up
    scl_label_x = scl_x + 3
    labels.append(make_label("SCL", scl_label_x, scl_y))
    wires.append(make_wire(scl_x, scl_y, scl_label_x + 10, scl_y))

    # R17: 4.7kΩ pull-up SCL → +3V3
    r17_x = scl_label_x + 10
    r17_y = scl_y - 8
    symbols.append(make_symbol("Device:R", "R17", "4.7k",
                               r17_x, r17_y, 0, pin_count=2))
    wires.append(make_wire(r17_x, r17_y + 3.81, r17_x, scl_y))
    junctions.append(make_junction(r17_x, scl_y))
    symbols.append(make_symbol("power:+3V3", "#PWR58", "+3V3",
                               r17_x, r17_y - 8, 0, pin_count=1))
    wires.append(make_wire(r17_x, r17_y - 3.81, r17_x, r17_y - 8))

    return lib_symbols, symbols, wires, junctions, labels, texts, no_connects


# ============================================================
# STEP 8: ESP32-WROOM-32E
# ============================================================

# ESP32-WROOM-32E-N4 lib symbol (38 pins)
# Left side: power + inputs, Right side: GPIOs
# Using standard ESP32-WROOM-32E pinout
LIB_ESP32 = """(symbol "Custom:ESP32-WROOM-32E"
\t\t(pin_names (offset 1.016))
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(property "Reference" "U"
\t\t\t(at 0 29.21 0)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Value" "ESP32-WROOM-32E"
\t\t\t(at 0 -29.21 0)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Footprint" "RF_Module:ESP32-WROOM-32E"
\t\t\t(at 0 -31.75 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(symbol "ESP32-WROOM-32E_0_1"
\t\t\t(rectangle (start -15.24 27.94) (end 15.24 -27.94)
\t\t\t\t(stroke (width 0.254) (type default))
\t\t\t\t(fill (type background))
\t\t\t)
\t\t)
\t\t(symbol "ESP32-WROOM-32E_1_1"
\t\t\t(pin power_in line (at 0 30.48 270) (length 2.54)
\t\t\t\t(name "3V3" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "2" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin input line (at -17.78 25.4 0) (length 2.54)
\t\t\t\t(name "EN" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "3" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin bidirectional line (at 17.78 25.4 180) (length 2.54)
\t\t\t\t(name "IO0" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "25" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin bidirectional line (at 17.78 22.86 180) (length 2.54)
\t\t\t\t(name "IO1/TX" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "35" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin bidirectional line (at 17.78 20.32 180) (length 2.54)
\t\t\t\t(name "IO2" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "24" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin bidirectional line (at 17.78 17.78 180) (length 2.54)
\t\t\t\t(name "IO3/RX" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "34" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin bidirectional line (at 17.78 15.24 180) (length 2.54)
\t\t\t\t(name "IO4" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "26" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin bidirectional line (at 17.78 12.7 180) (length 2.54)
\t\t\t\t(name "IO5" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "29" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin bidirectional line (at 17.78 7.62 180) (length 2.54)
\t\t\t\t(name "IO12" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "14" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin bidirectional line (at 17.78 5.08 180) (length 2.54)
\t\t\t\t(name "IO13" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "16" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin bidirectional line (at 17.78 2.54 180) (length 2.54)
\t\t\t\t(name "IO14" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "13" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin bidirectional line (at 17.78 0 180) (length 2.54)
\t\t\t\t(name "IO15" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "23" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin bidirectional line (at 17.78 -2.54 180) (length 2.54)
\t\t\t\t(name "IO16" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "27" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin bidirectional line (at 17.78 -5.08 180) (length 2.54)
\t\t\t\t(name "IO17" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "28" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin bidirectional line (at 17.78 -7.62 180) (length 2.54)
\t\t\t\t(name "IO18" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "30" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin bidirectional line (at 17.78 -10.16 180) (length 2.54)
\t\t\t\t(name "IO19" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "31" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin bidirectional line (at 17.78 -12.7 180) (length 2.54)
\t\t\t\t(name "IO21" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "33" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin bidirectional line (at 17.78 -15.24 180) (length 2.54)
\t\t\t\t(name "IO22" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "36" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin bidirectional line (at 17.78 -17.78 180) (length 2.54)
\t\t\t\t(name "IO23" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "37" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin bidirectional line (at -17.78 22.86 0) (length 2.54)
\t\t\t\t(name "IO25" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "10" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin bidirectional line (at -17.78 20.32 0) (length 2.54)
\t\t\t\t(name "IO26" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "11" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin bidirectional line (at -17.78 17.78 0) (length 2.54)
\t\t\t\t(name "IO27" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "12" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin bidirectional line (at -17.78 12.7 0) (length 2.54)
\t\t\t\t(name "IO32" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "8" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin bidirectional line (at -17.78 10.16 0) (length 2.54)
\t\t\t\t(name "IO33" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "9" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin input line (at -17.78 5.08 0) (length 2.54)
\t\t\t\t(name "IO34" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "6" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin input line (at -17.78 2.54 0) (length 2.54)
\t\t\t\t(name "IO35" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "7" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin input line (at -17.78 0 0) (length 2.54)
\t\t\t\t(name "SVP/IO36" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "4" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin input line (at -17.78 -2.54 0) (length 2.54)
\t\t\t\t(name "SVN/IO39" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "5" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin power_in line (at 0 -30.48 90) (length 2.54)
\t\t\t\t(name "GND" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "1" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin power_in line (at -2.54 -30.48 90) (length 2.54)
\t\t\t\t(name "GND" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "15" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin power_in line (at -5.08 -30.48 90) (length 2.54)
\t\t\t\t(name "GND" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "38" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin power_in line (at -7.62 -30.48 90) (length 2.54)
\t\t\t\t(name "GND_PAD" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "39" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -17.78 -7.62 0) (length 2.54)
\t\t\t\t(name "SD2" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "17" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -17.78 -10.16 0) (length 2.54)
\t\t\t\t(name "SD3" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "18" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -17.78 -12.7 0) (length 2.54)
\t\t\t\t(name "CMD" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "19" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -17.78 -15.24 0) (length 2.54)
\t\t\t\t(name "CLK" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "20" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -17.78 -17.78 0) (length 2.54)
\t\t\t\t(name "SD0" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "21" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -17.78 -20.32 0) (length 2.54)
\t\t\t\t(name "SD1" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "22" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 17.78 10.16 180) (length 2.54)
\t\t\t\t(name "NC" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "32" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t)
\t)"""


def generate_step8():
    """Generate Step 8: ESP32-WROOM-32E-N4 MCU with boot circuit and GPIO net labels."""

    lib_symbols = []
    symbols = []
    wires = []
    junctions = []
    labels = []
    texts = []
    no_connects = []

    lib_symbols.append(LIB_ESP32)

    # --- Section label ---
    texts.append(make_text("ESP32 MCU", 80, 240, size=3))

    # ======== U11: ESP32-WROOM-32E ========
    u11_x = 110
    u11_y = 290

    symbols.append(make_symbol("Custom:ESP32-WROOM-32E", "U11", "ESP32-WROOM-32E-N4",
                               u11_x, u11_y, 0,
                               pin_numbers=[str(i) for i in range(1, 40)]))

    # Pin positions — symbol Y inverted to schematic Y:
    # 3V3 (pin 2): top, (u11_x, u11_y - 30.48)
    v33_x, v33_y = u11_x, u11_y - 30.48               # (110, 259.52)
    # GND (pin 1): bottom, (u11_x, u11_y + 30.48)
    gnd_pin_x, gnd_pin_y = u11_x, u11_y + 30.48       # (110, 320.48)
    # EN (pin 3): left, (u11_x - 17.78, u11_y - 25.4)
    en_x, en_y = u11_x - 17.78, u11_y - 25.4          # (92.22, 264.6)

    # Right-side GPIOs (x = u11_x + 17.78 = 127.78):
    rx = u11_x + 17.78  # 127.78
    io0_y  = u11_y - 25.4   # 264.6
    io1_y  = u11_y - 22.86  # 267.14  (TX)
    io2_y  = u11_y - 20.32  # 269.68
    io3_y  = u11_y - 17.78  # 272.22  (RX)
    io4_y  = u11_y - 15.24  # 274.76
    io5_y  = u11_y - 12.7   # 277.3
    io12_y = u11_y - 7.62   # 282.38
    io13_y = u11_y - 5.08   # 284.92
    io14_y = u11_y - 2.54   # 287.46
    io15_y = u11_y           # 290
    io16_y = u11_y + 2.54   # 292.54
    io17_y = u11_y + 5.08   # 295.08
    io18_y = u11_y + 7.62   # 297.62
    io19_y = u11_y + 10.16  # 300.16
    io21_y = u11_y + 12.7   # 302.7
    io22_y = u11_y + 15.24  # 305.24
    io23_y = u11_y + 17.78  # 307.78

    # Left-side GPIOs (x = u11_x - 17.78 = 92.22):
    lx = u11_x - 17.78  # 92.22
    io25_y = u11_y - 22.86  # 267.14
    io26_y = u11_y - 20.32  # 269.68
    io27_y = u11_y - 17.78  # 272.22
    io32_y = u11_y - 12.7   # 277.3
    io33_y = u11_y - 10.16  # 279.84
    io34_y = u11_y - 5.08   # 284.92
    io35_y = u11_y - 2.54   # 287.46
    io36_y = u11_y           # 290
    io39_y = u11_y + 2.54   # 292.54

    # ======== Power: 3V3 ========
    symbols.append(make_symbol("power:+3V3", "#PWR59", "+3V3",
                               v33_x, v33_y - 3, 0, pin_count=1))
    wires.append(make_wire(v33_x, v33_y - 3, v33_x, v33_y))

    # ======== Power: GND ========
    symbols.append(make_symbol("power:GND", "#PWR60", "GND",
                               gnd_pin_x, gnd_pin_y + 3, 0, pin_count=1))
    wires.append(make_wire(gnd_pin_x, gnd_pin_y, gnd_pin_x, gnd_pin_y + 3))

    # ======== C26: 100nF bypass ========
    c26_x = v33_x + 8
    c26_y = v33_y
    symbols.append(make_symbol("Device:C", "C26", "100nF",
                               c26_x, c26_y, 0, pin_count=2))
    wires.append(make_wire(v33_x, v33_y, c26_x, v33_y))
    wires.append(make_wire(c26_x, c26_y - 3.81, c26_x, v33_y))
    junctions.append(make_junction(v33_x, v33_y))
    symbols.append(make_symbol("power:GND", "#PWR61", "GND",
                               c26_x, c26_y + 5, 0, pin_count=1))
    wires.append(make_wire(c26_x, c26_y + 3.81, c26_x, c26_y + 5))

    # ======== C27: 10µF bypass ========
    c27_x = v33_x + 16
    c27_y = v33_y
    symbols.append(make_symbol("Device:C", "C27", "10uF",
                               c27_x, c27_y, 0, pin_count=2))
    wires.append(make_wire(c26_x, v33_y, c27_x, v33_y))
    wires.append(make_wire(c27_x, c27_y - 3.81, c27_x, v33_y))
    junctions.append(make_junction(c26_x, v33_y))
    symbols.append(make_symbol("power:GND", "#PWR62", "GND",
                               c27_x, c27_y + 5, 0, pin_count=1))
    wires.append(make_wire(c27_x, c27_y + 3.81, c27_x, c27_y + 5))

    # ======== EN pin: R18 (10kΩ pull-up) + C28 (100nF RC filter) ========
    # R18: pull-up EN → +3V3
    r18_x = en_x - 7
    r18_y = en_y - 7
    symbols.append(make_symbol("Device:R", "R18", "10k",
                               r18_x, r18_y, 0, pin_count=2))
    # R18 pin2 → EN
    wires.append(make_wire(r18_x, r18_y + 3.81, r18_x, en_y))
    wires.append(make_wire(r18_x, en_y, en_x, en_y))
    # R18 pin1 → +3V3
    symbols.append(make_symbol("power:+3V3", "#PWR63", "+3V3",
                               r18_x, r18_y - 8, 0, pin_count=1))
    wires.append(make_wire(r18_x, r18_y - 3.81, r18_x, r18_y - 8))

    # C28: EN → GND (RC delay for stable boot)
    c28_x = r18_x
    c28_y = en_y + 7
    symbols.append(make_symbol("Device:C", "C28", "100nF",
                               c28_x, c28_y, 0, pin_count=2))
    wires.append(make_wire(c28_x, c28_y - 3.81, c28_x, en_y))
    junctions.append(make_junction(r18_x, en_y))
    symbols.append(make_symbol("power:GND", "#PWR64", "GND",
                               c28_x, c28_y + 5, 0, pin_count=1))
    wires.append(make_wire(c28_x, c28_y + 3.81, c28_x, c28_y + 5))

    # ======== IO0: R19 (10kΩ pull-up for boot) ========
    r19_x = rx + 7
    r19_y = io0_y - 7
    symbols.append(make_symbol("Device:R", "R19", "10k",
                               r19_x, r19_y, 0, pin_count=2))
    wires.append(make_wire(rx, io0_y, r19_x, io0_y))
    wires.append(make_wire(r19_x, r19_y + 3.81, r19_x, io0_y))
    symbols.append(make_symbol("power:+3V3", "#PWR65", "+3V3",
                               r19_x, r19_y - 8, 0, pin_count=1))
    wires.append(make_wire(r19_x, r19_y - 3.81, r19_x, r19_y - 8))

    # ======== GPIO net labels (right side) ========
    lbl_offset = 5  # wire length from pin to label

    # IO1/TX → UART_TX
    labels.append(make_label("UART_TX", rx + lbl_offset, io1_y))
    wires.append(make_wire(rx, io1_y, rx + lbl_offset + 10, io1_y))

    # IO2 → TFT_DC
    labels.append(make_label("TFT_DC", rx + lbl_offset, io2_y))
    wires.append(make_wire(rx, io2_y, rx + lbl_offset + 10, io2_y))

    # IO3/RX → UART_RX
    labels.append(make_label("UART_RX", rx + lbl_offset, io3_y))
    wires.append(make_wire(rx, io3_y, rx + lbl_offset + 10, io3_y))

    # IO4 → TFT_RST
    labels.append(make_label("TFT_RST", rx + lbl_offset, io4_y))
    wires.append(make_wire(rx, io4_y, rx + lbl_offset + 10, io4_y))

    # IO5 → ONEWIRE_DATA
    labels.append(make_label("ONEWIRE_DATA", rx + lbl_offset, io5_y))
    wires.append(make_wire(rx, io5_y, rx + lbl_offset + 10, io5_y))

    # IO12 → voľný (J7) — no label needed, will be in step 10
    labels.append(make_label("GPIO12", rx + lbl_offset, io12_y))
    wires.append(make_wire(rx, io12_y, rx + lbl_offset + 10, io12_y))

    # IO13 → MOSFET3_GATE
    labels.append(make_label("MOSFET3_GATE", rx + lbl_offset, io13_y))
    wires.append(make_wire(rx, io13_y, rx + lbl_offset + 10, io13_y))

    # IO14 → MOSFET4_GATE
    labels.append(make_label("MOSFET4_GATE", rx + lbl_offset, io14_y))
    wires.append(make_wire(rx, io14_y, rx + lbl_offset + 10, io14_y))

    # IO15 → TFT_CS
    labels.append(make_label("TFT_CS", rx + lbl_offset, io15_y))
    wires.append(make_wire(rx, io15_y, rx + lbl_offset + 10, io15_y))

    # IO16 → voľný (J7)
    labels.append(make_label("GPIO16", rx + lbl_offset, io16_y))
    wires.append(make_wire(rx, io16_y, rx + lbl_offset + 10, io16_y))

    # IO17 → voľný (J7)
    labels.append(make_label("GPIO17", rx + lbl_offset, io17_y))
    wires.append(make_wire(rx, io17_y, rx + lbl_offset + 10, io17_y))

    # IO18 → SPI_SCK
    labels.append(make_label("SPI_SCK", rx + lbl_offset, io18_y))
    wires.append(make_wire(rx, io18_y, rx + lbl_offset + 10, io18_y))

    # IO19 → SPI_MISO
    labels.append(make_label("SPI_MISO", rx + lbl_offset, io19_y))
    wires.append(make_wire(rx, io19_y, rx + lbl_offset + 10, io19_y))

    # IO21 → TOUCH_CS
    labels.append(make_label("TOUCH_CS", rx + lbl_offset, io21_y))
    wires.append(make_wire(rx, io21_y, rx + lbl_offset + 10, io21_y))

    # IO22 → voľný (J7)
    labels.append(make_label("GPIO22", rx + lbl_offset, io22_y))
    wires.append(make_wire(rx, io22_y, rx + lbl_offset + 10, io22_y))

    # IO23 → SPI_MOSI
    labels.append(make_label("SPI_MOSI", rx + lbl_offset, io23_y))
    wires.append(make_wire(rx, io23_y, rx + lbl_offset + 10, io23_y))

    # ======== GPIO net labels (left side) ========
    # IO25 → RELAY_CTRL
    labels.append(make_label("RELAY_CTRL", lx - 15, io25_y, angle=180))
    wires.append(make_wire(lx - 15, io25_y, lx, io25_y))

    # IO26 → SDA
    labels.append(make_label("SDA", lx - 10, io26_y, angle=180))
    wires.append(make_wire(lx - 10, io26_y, lx, io26_y))

    # IO27 → SCL
    labels.append(make_label("SCL", lx - 10, io27_y, angle=180))
    wires.append(make_wire(lx - 10, io27_y, lx, io27_y))

    # IO32 → TFT_BL
    labels.append(make_label("TFT_BL", lx - 12, io32_y, angle=180))
    wires.append(make_wire(lx - 12, io32_y, lx, io32_y))

    # IO33 → MOSFET1_GATE
    labels.append(make_label("MOSFET1_GATE", lx - 15, io33_y, angle=180))
    wires.append(make_wire(lx - 15, io33_y, lx, io33_y))

    # IO34 → voľný (J7, input only)
    labels.append(make_label("GPIO34", lx - 12, io34_y, angle=180))
    wires.append(make_wire(lx - 12, io34_y, lx, io34_y))

    # IO35 → voľný (J7, input only)
    labels.append(make_label("GPIO35", lx - 12, io35_y, angle=180))
    wires.append(make_wire(lx - 12, io35_y, lx, io35_y))

    # IO36/SVP → voľný (J7, input only)
    labels.append(make_label("GPIO36", lx - 12, io36_y, angle=180))
    wires.append(make_wire(lx - 12, io36_y, lx, io36_y))

    # IO39/SVN → TOUCH_IRQ
    labels.append(make_label("TOUCH_IRQ", lx - 15, io39_y, angle=180))
    wires.append(make_wire(lx - 15, io39_y, lx, io39_y))

    # ======== Unused SD card pins (left side) — no_connect ========
    # Pins 17-22: SD2, SD3, CMD, CLK, SD0, SD1
    sd_pin_ys = [
        u11_y + 7.62,   # pin 17 SD2
        u11_y + 10.16,  # pin 18 SD3
        u11_y + 12.70,  # pin 19 CMD
        u11_y + 15.24,  # pin 20 CLK
        u11_y + 17.78,  # pin 21 SD0
        u11_y + 20.32,  # pin 22 SD1
    ]
    for sd_y in sd_pin_ys:
        no_connects.append(make_no_connect(lx, sd_y))

    # NC pin 32 (right side)
    nc32_y = u11_y - 10.16  # 279.84
    no_connects.append(make_no_connect(rx, nc32_y))

    # ======== Extra GND pins (15, 38, 39) — wire to existing GND ========
    # GND pin 1 at (110, 320.48) is already connected
    # GND pin 15 at (107.46, 320.48), pin 38 at (104.92, 320.48), pin 39 GND_PAD at (102.38, 320.48)
    gnd15_x = u11_x - 2.54   # 107.46
    gnd38_x = u11_x - 5.08   # 104.92
    gnd39_x = u11_x - 7.62   # 102.38
    # Wire all to pin 1 GND at (110, 320.48)
    wires.append(make_wire(gnd39_x, gnd_pin_y, gnd_pin_x, gnd_pin_y))
    junctions.append(make_junction(gnd15_x, gnd_pin_y))
    junctions.append(make_junction(gnd38_x, gnd_pin_y))

    return lib_symbols, symbols, wires, junctions, labels, texts, no_connects


# ============================================================
# STEP 9: Outputs (4× MOSFET + PC817 + Relay + 230V out)
# ============================================================

# N-MOSFET lib symbol (IRLR2905TRPBF DPAK)
# Pin 1: Gate (left), Pin 2: Drain (top), Pin 3: Source (bottom)
LIB_NMOS = """(symbol "Device:Q_NMOS_GDS"
\t\t(pin_names (offset 0) (hide yes))
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(property "Reference" "Q"
\t\t\t(at 5.08 1.905 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify left))
\t\t)
\t\t(property "Value" "Q_NMOS_GDS"
\t\t\t(at 5.08 0 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify left))
\t\t)
\t\t(property "Footprint" "Package_TO_SOT_SMD:TO-252-2"
\t\t\t(at 5.08 -1.905 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(symbol "Q_NMOS_GDS_0_1"
\t\t\t(polyline (pts (xy 0.254 0) (xy -2.54 0)) (stroke (width 0) (type default)) (fill (type none)))
\t\t\t(polyline (pts (xy 0.254 1.905) (xy 0.254 -1.905)) (stroke (width 0.254) (type default)) (fill (type none)))
\t\t\t(polyline (pts (xy 0.762 -1.27) (xy 0.762 -2.286)) (stroke (width 0.254) (type default)) (fill (type none)))
\t\t\t(polyline (pts (xy 0.762 0.508) (xy 0.762 -0.508)) (stroke (width 0.254) (type default)) (fill (type none)))
\t\t\t(polyline (pts (xy 0.762 2.286) (xy 0.762 1.27)) (stroke (width 0.254) (type default)) (fill (type none)))
\t\t\t(polyline (pts (xy 2.54 2.54) (xy 2.54 1.778)) (stroke (width 0) (type default)) (fill (type none)))
\t\t\t(polyline (pts (xy 2.54 -2.54) (xy 2.54 0) (xy 0.762 0)) (stroke (width 0) (type default)) (fill (type none)))
\t\t\t(polyline (pts (xy 0.762 -1.778) (xy 3.302 -1.778) (xy 3.302 1.778) (xy 0.762 1.778)) (stroke (width 0) (type default)) (fill (type none)))
\t\t\t(polyline (pts (xy 1.016 0) (xy 2.032 0.381) (xy 2.032 -0.381) (xy 1.016 0)) (stroke (width 0) (type default)) (fill (type outline)))
\t\t)
\t\t(symbol "Q_NMOS_GDS_1_1"
\t\t\t(pin input line (at -5.08 0 0) (length 2.54)
\t\t\t\t(name "G" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "1" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 2.54 5.08 270) (length 2.54)
\t\t\t\t(name "D" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "2" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 2.54 -5.08 90) (length 2.54)
\t\t\t\t(name "S" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "3" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t)
\t)"""

# LTV-356T optocoupler lib symbol (SOP-4 SMD)
LIB_PC817 = """(symbol "Custom:LTV-356T"
\t\t(pin_names (offset 1.016))
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(property "Reference" "U"
\t\t\t(at 0 8.89 0)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Value" "LTV-356T"
\t\t\t(at 0 -8.89 0)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Footprint" "Package_SO:SOP-4_4.4x2.6mm_P1.27mm"
\t\t\t(at 0 -11.43 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(symbol "LTV-356T_0_1"
\t\t\t(rectangle (start -6.35 7.62) (end 6.35 -7.62)
\t\t\t\t(stroke (width 0.254) (type default))
\t\t\t\t(fill (type background))
\t\t\t)
\t\t)
\t\t(symbol "LTV-356T_1_1"
\t\t\t(pin passive line (at -8.89 5.08 0) (length 2.54)
\t\t\t\t(name "A" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "1" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -8.89 -5.08 0) (length 2.54)
\t\t\t\t(name "K" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "2" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 8.89 -5.08 180) (length 2.54)
\t\t\t\t(name "E" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "3" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 8.89 5.08 180) (length 2.54)
\t\t\t\t(name "C" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "4" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t)
\t)"""

# Relay lib symbol (Finder 40.52, simplified 4-pin)
LIB_RELAY = """(symbol "Custom:Relay_DPDT"
\t\t(pin_names (offset 1.016))
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(property "Reference" "RLY"
\t\t\t(at 0 10.16 0)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Value" "Relay_DPDT"
\t\t\t(at 0 -10.16 0)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Footprint" ""
\t\t\t(at 0 -12.7 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(symbol "Relay_DPDT_0_1"
\t\t\t(rectangle (start -7.62 8.89) (end 7.62 -8.89)
\t\t\t\t(stroke (width 0.254) (type default))
\t\t\t\t(fill (type background))
\t\t\t)
\t\t)
\t\t(symbol "Relay_DPDT_1_1"
\t\t\t(pin passive line (at -10.16 5.08 0) (length 2.54)
\t\t\t\t(name "COIL+" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "A1" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -10.16 -5.08 0) (length 2.54)
\t\t\t\t(name "COIL-" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "A2" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 10.16 5.08 180) (length 2.54)
\t\t\t\t(name "COM" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "11" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 10.16 -5.08 180) (length 2.54)
\t\t\t\t(name "NO1" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "14" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 10.16 -2.54 180) (length 2.54)
\t\t\t\t(name "NC1" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "12" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 10.16 -10.16 180) (length 2.54)
\t\t\t\t(name "COM2" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "21" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 10.16 -12.7 180) (length 2.54)
\t\t\t\t(name "NC2" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "22" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 10.16 -15.24 180) (length 2.54)
\t\t\t\t(name "NO2" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "24" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t)
\t)"""

# Varistor lib symbol
LIB_VARISTOR = """(symbol "Device:Varistor"
\t\t(pin_numbers (hide yes))
\t\t(pin_names (offset 0) (hide yes))
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(property "Reference" "MOV"
\t\t\t(at 2.54 0 90)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Value" "Varistor"
\t\t\t(at -2.54 0 90)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Footprint" ""
\t\t\t(at 0 0 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(symbol "Varistor_0_1"
\t\t\t(polyline (pts (xy -1.016 3.556) (xy 1.016 -3.556)) (stroke (width 0) (type default)) (fill (type none)))
\t\t\t(rectangle (start -0.762 3.81) (end 0.762 -3.81)
\t\t\t\t(stroke (width 0.254) (type default))
\t\t\t\t(fill (type none))
\t\t\t)
\t\t)
\t\t(symbol "Varistor_1_1"
\t\t\t(pin passive line (at 0 6.35 270) (length 2.54)
\t\t\t\t(name "~" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "1" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 0 -6.35 90) (length 2.54)
\t\t\t\t(name "~" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "2" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t)
\t)"""

# 2-pin connector
LIB_CONN_01x02 = """(symbol "Connector_Generic:Conn_01x02"
\t\t(pin_names (offset 1.016) (hide yes))
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(property "Reference" "J"
\t\t\t(at 0 2.54 0)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Value" "Conn_01x02"
\t\t\t(at 0 -5.08 0)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Footprint" "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical"
\t\t\t(at 0 0 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(symbol "Conn_01x02_1_1"
\t\t\t(rectangle (start -1.27 -2.413) (end 0 -2.667))
\t\t\t(rectangle (start -1.27 0.127) (end 0 -0.127))
\t\t\t(rectangle (start -1.27 1.27) (end 1.27 -3.81)
\t\t\t\t(stroke (width 0.254) (type default))
\t\t\t\t(fill (type background))
\t\t\t)
\t\t\t(pin passive line (at -3.81 0 0) (length 2.54)
\t\t\t\t(name "Pin_1" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "1" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -3.81 -2.54 0) (length 2.54)
\t\t\t\t(name "Pin_2" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "2" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t)
\t)"""


def generate_step9():
    """Generate Step 9: 4x MOSFET channels + PC817 + Relay + 230V output."""

    lib_symbols = []
    symbols = []
    wires = []
    junctions = []
    labels = []
    texts = []
    no_connects = []

    lib_symbols.append(LIB_NMOS)
    lib_symbols.append(LIB_PC817)
    lib_symbols.append(LIB_RELAY)
    lib_symbols.append(LIB_VARISTOR)
    lib_symbols.append(LIB_CONN_01x02)

    # --- Section label ---
    texts.append(make_text("MOSFET OUTPUTS + RELAY", 15, 340, size=3))

    # ================================================================
    # Helper: place one MOSFET channel
    # ================================================================
    def mosfet_channel(q_ref, q_val, rg_ref, rpd_ref, d_ref,
                       gate_label, x, y, pwr_base):
        """Place MOSFET channel at (x,y).
        Gate at left, Drain at top, Source at bottom.
        """
        symbols.append(make_symbol("Device:Q_NMOS_GDS", q_ref, q_val,
                                   x, y, 0, pin_count=3))
        gate_x, gate_y = x - 5.08, y
        drain_x, drain_y = x + 2.54, y - 5.08
        source_x, source_y = x + 2.54, y + 5.08

        # Source → GND
        symbols.append(make_symbol("power:GND", f"#PWR{pwr_base}", "GND",
                                   source_x, source_y + 3, 0, pin_count=1))
        wires.append(make_wire(source_x, source_y, source_x, source_y + 3))

        # R_gate (100Ω)
        rg_x = gate_x - 7
        symbols.append(make_symbol("Device:R", rg_ref, "100R",
                                   rg_x, gate_y, 90, pin_count=2))
        wires.append(make_wire(rg_x + 3.81, gate_y, gate_x, gate_y))
        labels.append(make_label(gate_label, rg_x - 3.81, gate_y, angle=180))

        # R_pd (10kΩ) pull-down
        rpd_x = gate_x
        rpd_y = gate_y + 7
        symbols.append(make_symbol("Device:R", rpd_ref, "10k",
                                   rpd_x, rpd_y, 0, pin_count=2))
        wires.append(make_wire(rpd_x, rpd_y - 3.81, rpd_x, gate_y))
        wires.append(make_wire(rpd_x, gate_y, gate_x, gate_y))
        junctions.append(make_junction(gate_x, gate_y))
        symbols.append(make_symbol("power:GND", f"#PWR{pwr_base+1}", "GND",
                                   rpd_x, rpd_y + 8, 0, pin_count=1))
        wires.append(make_wire(rpd_x, rpd_y + 3.81, rpd_x, rpd_y + 8))

        # D: SS14 flyback (90° makes horizontal pins vertical)
        # At 90°: K(pin1) at (d_x, d_y+3.81), A(pin2) at (d_x, d_y-3.81)
        d_x = drain_x + 7
        d_y = drain_y - 2
        symbols.append(make_symbol("Device:D", d_ref, "SS14",
                                   d_x, d_y, 90, pin_count=2))
        wires.append(make_wire(drain_x, drain_y, d_x, drain_y))
        wires.append(make_wire(d_x, d_y + 3.81, d_x, drain_y))
        junctions.append(make_junction(drain_x, drain_y))
        junctions.append(make_junction(d_x, drain_y))
        symbols.append(make_symbol("power:+12V", f"#PWR{pwr_base+2}", "+12V",
                                   d_x, d_y - 7, 0, pin_count=1))
        wires.append(make_wire(d_x, d_y - 3.81, d_x, d_y - 7))

        return drain_x, drain_y

    # ================================================================
    # Q1: Pump (MOSFET1_GATE, GPIO33) — internal, no connector
    # ================================================================
    q1_x, q1_y = 40, 370
    q1_drain_x, q1_drain_y = mosfet_channel(
        "Q1", "IRLR2905", "R20", "R24", "D3",
        "MOSFET1_GATE", q1_x, q1_y, pwr_base=66)
    symbols.append(make_symbol("power:+12V", "#PWR69", "+12V",
                               q1_drain_x, q1_drain_y - 5, 0, pin_count=1))
    wires.append(make_wire(q1_drain_x, q1_drain_y, q1_drain_x, q1_drain_y - 5))

    # ================================================================
    # Q2: Relay coil (driven by PC817)
    # ================================================================
    q2_x, q2_y = 100, 370
    q2_drain_x, q2_drain_y = mosfet_channel(
        "Q2", "IRLR2905", "R21", "R25", "D4",
        "MOSFET2_GATE", q2_x, q2_y, pwr_base=70)

    # ================================================================
    # PC817 optocoupler (U12)
    # ================================================================
    u12_x = 73
    u12_y = 350

    symbols.append(make_symbol("Custom:LTV-356T", "U12", "LTV-356T",
                               u12_x, u12_y, 0, pin_count=4))

    opto_a_x, opto_a_y = u12_x - 8.89, u12_y - 5.08   # Anode
    opto_k_x, opto_k_y = u12_x - 8.89, u12_y + 5.08   # Cathode
    opto_e_x, opto_e_y = u12_x + 8.89, u12_y + 5.08   # Emitter
    opto_c_x, opto_c_y = u12_x + 8.89, u12_y - 5.08   # Collector

    # R28 (330Ω): RELAY_CTRL → Anode
    r28_x = opto_a_x - 8
    symbols.append(make_symbol("Device:R", "R28", "330R",
                               r28_x, opto_a_y, 90, pin_count=2))
    wires.append(make_wire(r28_x + 3.81, opto_a_y, opto_a_x, opto_a_y))
    labels.append(make_label("RELAY_CTRL", r28_x - 3.81, opto_a_y, angle=180))

    # Cathode → GND
    symbols.append(make_symbol("power:GND", "#PWR73", "GND",
                               opto_k_x, opto_k_y + 3, 0, pin_count=1))
    wires.append(make_wire(opto_k_x, opto_k_y, opto_k_x, opto_k_y + 3))

    # Emitter → GND
    symbols.append(make_symbol("power:GND", "#PWR74", "GND",
                               opto_e_x, opto_e_y + 3, 0, pin_count=1))
    wires.append(make_wire(opto_e_x, opto_e_y, opto_e_x, opto_e_y + 3))

    # R29 (1kΩ): +12V → Collector
    r29_x = opto_c_x + 7
    r29_y = opto_c_y - 7
    symbols.append(make_symbol("Device:R", "R29", "1k",
                               r29_x, r29_y, 0, pin_count=2))
    wires.append(make_wire(r29_x, r29_y + 3.81, r29_x, opto_c_y))
    wires.append(make_wire(opto_c_x, opto_c_y, r29_x, opto_c_y))
    junctions.append(make_junction(r29_x, opto_c_y))
    symbols.append(make_symbol("power:+12V", "#PWR75", "+12V",
                               r29_x, r29_y - 8, 0, pin_count=1))
    wires.append(make_wire(r29_x, r29_y - 3.81, r29_x, r29_y - 8))

    # Collector → MOSFET2_GATE
    labels.append(make_label("MOSFET2_GATE", r29_x + 3, opto_c_y))
    wires.append(make_wire(r29_x, opto_c_y, r29_x + 12, opto_c_y))

    # ================================================================
    # RLY1: Finder 40.52 relay
    # ================================================================
    rly_x = 130
    rly_y = 350

    symbols.append(make_symbol("Custom:Relay_DPDT", "RLY1", "Finder_40.52",
                               rly_x, rly_y, 0, pin_numbers=["A1", "A2", "11", "12", "14", "21", "22", "24"]))

    coil_p_x, coil_p_y = rly_x - 10.16, rly_y - 5.08
    coil_n_x, coil_n_y = rly_x - 10.16, rly_y + 5.08
    com_x, com_y = rly_x + 10.16, rly_y - 5.08
    no_x, no_y = rly_x + 10.16, rly_y + 5.08

    # COIL+ → +12V
    symbols.append(make_symbol("power:+12V", "#PWR76", "+12V",
                               coil_p_x, coil_p_y - 5, 0, pin_count=1))
    wires.append(make_wire(coil_p_x, coil_p_y - 5, coil_p_x, coil_p_y))

    # COIL- → Q2 drain
    wires.append(make_wire(coil_n_x, coil_n_y, coil_n_x, q2_drain_y))
    wires.append(make_wire(coil_n_x, q2_drain_y, q2_drain_x, q2_drain_y))
    junctions.append(make_junction(q2_drain_x, q2_drain_y))

    # D7 (M7, SMD ekvivalent 1N4007) flyback across coil
    # At 90°: K(pin1) at (d7_x, d7_y+3.81), A(pin2) at (d7_x, d7_y-3.81)
    d7_x = coil_p_x - 7
    d7_y = rly_y
    symbols.append(make_symbol("Device:D", "D7", "M7",
                               d7_x, d7_y, 90, pin_count=2))
    wires.append(make_wire(d7_x, d7_y - 3.81, d7_x, coil_p_y))
    wires.append(make_wire(d7_x, coil_p_y, coil_p_x, coil_p_y))
    junctions.append(make_junction(coil_p_x, coil_p_y))
    wires.append(make_wire(d7_x, d7_y + 3.81, d7_x, coil_n_y))
    wires.append(make_wire(d7_x, coil_n_y, coil_n_x, coil_n_y))
    junctions.append(make_junction(coil_n_x, coil_n_y))

    # NO → AC_L
    labels.append(make_label("AC_L", no_x + 3, no_y))
    wires.append(make_wire(no_x, no_y, no_x + 12, no_y))

    # COM → L_OUT
    labels.append(make_label("L_OUT", com_x + 3, com_y))
    wires.append(make_wire(com_x, com_y, com_x + 12, com_y))

    # RC snubber: R30 + C29 across COM-NO
    r30_x = rly_x + 22
    r30_y = rly_y - 3
    symbols.append(make_symbol("Device:R", "R30", "100R",
                               r30_x, r30_y, 0, pin_count=2))
    wires.append(make_wire(r30_x, r30_y - 3.81, r30_x, com_y))
    wires.append(make_wire(com_x, com_y, r30_x, com_y))
    junctions.append(make_junction(com_x, com_y))

    c29_x = r30_x
    c29_y = rly_y + 3
    symbols.append(make_symbol("Device:C", "C29", "100nF_X2",
                               c29_x, c29_y, 0, pin_count=2))
    wires.append(make_wire(r30_x, r30_y + 3.81, c29_x, c29_y - 3.81))
    wires.append(make_wire(c29_x, c29_y + 3.81, c29_x, no_y))
    wires.append(make_wire(no_x, no_y, c29_x, no_y))
    junctions.append(make_junction(no_x, no_y))

    # Unused relay pins: 12(NC1), 21(COM2), 22(NC2), 24(NO2)
    # Pin positions at (rly_x + 10.16, rly_y - ry) where ry negates lib y
    no_connects.append(make_no_connect(140.16, 352.54))   # pin 12 NC1
    no_connects.append(make_no_connect(140.16, 360.16))   # pin 21 COM2
    no_connects.append(make_no_connect(140.16, 362.70))   # pin 22 NC2
    no_connects.append(make_no_connect(140.16, 365.24))   # pin 24 NO2

    # MOV1: 275V varistor across COM-NO
    mov_x = rly_x + 30
    mov_y = rly_y
    symbols.append(make_symbol("Device:Varistor", "MOV1", "275V",
                               mov_x, mov_y, 0, pin_count=2))
    wires.append(make_wire(mov_x, mov_y - 6.35, mov_x, com_y))
    wires.append(make_wire(r30_x, com_y, mov_x, com_y))
    junctions.append(make_junction(r30_x, com_y))
    wires.append(make_wire(mov_x, mov_y + 6.35, mov_x, no_y))
    wires.append(make_wire(c29_x, no_y, mov_x, no_y))
    junctions.append(make_junction(c29_x, no_y))

    # ================================================================
    # Q3: Free output (MOSFET3_GATE) + J9
    # ================================================================
    q3_x, q3_y = 190, 370
    q3_drain_x, q3_drain_y = mosfet_channel(
        "Q3", "IRLR2905", "R22", "R26", "D5",
        "MOSFET3_GATE", q3_x, q3_y, pwr_base=77)

    j9_x = q3_drain_x + 15
    j9_y = q3_drain_y
    symbols.append(make_symbol("Connector_Generic:Conn_01x02", "J9", "OUT3",
                               j9_x, j9_y, 0, pin_count=2))
    symbols.append(make_symbol("power:+12V", "#PWR80", "+12V",
                               j9_x - 3.81 - 5, j9_y, 0, pin_count=1))
    wires.append(make_wire(j9_x - 3.81 - 5, j9_y, j9_x - 3.81, j9_y))
    junctions.append(make_junction(j9_x - 3.81 - 5, j9_y))
    wires.append(make_wire(j9_x - 3.81, j9_y + 2.54, q3_drain_x, j9_y + 2.54))
    wires.append(make_wire(q3_drain_x, q3_drain_y, q3_drain_x, j9_y + 2.54))
    junctions.append(make_junction(q3_drain_x, q3_drain_y))

    # ================================================================
    # Q4: Free output (MOSFET4_GATE) + J10
    # ================================================================
    q4_x, q4_y = 250, 370
    q4_drain_x, q4_drain_y = mosfet_channel(
        "Q4", "IRLR2905", "R23", "R27", "D6",
        "MOSFET4_GATE", q4_x, q4_y, pwr_base=81)

    j10_x = q4_drain_x + 15
    j10_y = q4_drain_y
    symbols.append(make_symbol("Connector_Generic:Conn_01x02", "J10", "OUT4",
                               j10_x, j10_y, 0, pin_count=2))
    symbols.append(make_symbol("power:+12V", "#PWR84", "+12V",
                               j10_x - 3.81 - 5, j10_y, 0, pin_count=1))
    wires.append(make_wire(j10_x - 3.81 - 5, j10_y, j10_x - 3.81, j10_y))
    junctions.append(make_junction(j10_x - 3.81 - 5, j10_y))
    wires.append(make_wire(j10_x - 3.81, j10_y + 2.54, q4_drain_x, j10_y + 2.54))
    wires.append(make_wire(q4_drain_x, q4_drain_y, q4_drain_x, j10_y + 2.54))
    junctions.append(make_junction(q4_drain_x, q4_drain_y))

    # ================================================================
    # J11: 230V output — 3-pin screw terminal
    # ================================================================
    j11_x = 175
    j11_y = 345

    symbols.append(make_symbol("Connector_Generic:Conn_01x03", "J11", "AC_OUT_230V",
                               j11_x, j11_y, 0, pin_count=3))

    # Conn_01x03 pins: Pin1 at (jpx, jy-2.54), Pin2 at (jpx, jy), Pin3 at (jpx, jy+2.54)
    # Pin 1: L_OUT
    labels.append(make_label("L_OUT", j11_x - 3.81 - 7, j11_y - 2.54, angle=180))
    wires.append(make_wire(j11_x - 3.81 - 7, j11_y - 2.54, j11_x - 3.81, j11_y - 2.54))

    # Pin 2: N
    labels.append(make_label("AC_N", j11_x - 3.81 - 7, j11_y, angle=180))
    wires.append(make_wire(j11_x - 3.81 - 7, j11_y, j11_x - 3.81, j11_y))

    # Pin 3: PE
    labels.append(make_label("PE", j11_x - 3.81 - 7, j11_y + 2.54, angle=180))
    wires.append(make_wire(j11_x - 3.81 - 7, j11_y + 2.54, j11_x - 3.81, j11_y + 2.54))

    return lib_symbols, symbols, wires, junctions, labels, texts, no_connects


# ============================================================
# STEP 10: Peripherals (Display, 1-Wire, GPIO header, UART)
# ============================================================

# 14-pin connector (display)
LIB_CONN_01x14 = """(symbol "Connector_Generic:Conn_01x14"
\t\t(pin_names (offset 1.016) (hide yes))
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(property "Reference" "J"
\t\t\t(at 0 17.78 0)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Value" "Conn_01x14"
\t\t\t(at 0 -19.05 0)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Footprint" "Connector_PinHeader_2.54mm:PinHeader_1x14_P2.54mm_Vertical"
\t\t\t(at 0 0 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(symbol "Conn_01x14_0_1"
\t\t\t(rectangle (start -1.27 16.51) (end 1.27 -17.78)
\t\t\t\t(stroke (width 0.254) (type default))
\t\t\t\t(fill (type background))
\t\t\t)
\t\t)
\t\t(symbol "Conn_01x14_1_1"
\t\t\t(pin passive line (at -3.81 15.24 0) (length 2.54)
\t\t\t\t(name "Pin_1" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "1" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -3.81 12.7 0) (length 2.54)
\t\t\t\t(name "Pin_2" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "2" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -3.81 10.16 0) (length 2.54)
\t\t\t\t(name "Pin_3" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "3" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -3.81 7.62 0) (length 2.54)
\t\t\t\t(name "Pin_4" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "4" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -3.81 5.08 0) (length 2.54)
\t\t\t\t(name "Pin_5" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "5" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -3.81 2.54 0) (length 2.54)
\t\t\t\t(name "Pin_6" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "6" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -3.81 0 0) (length 2.54)
\t\t\t\t(name "Pin_7" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "7" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -3.81 -2.54 0) (length 2.54)
\t\t\t\t(name "Pin_8" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "8" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -3.81 -5.08 0) (length 2.54)
\t\t\t\t(name "Pin_9" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "9" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -3.81 -7.62 0) (length 2.54)
\t\t\t\t(name "Pin_10" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "10" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -3.81 -10.16 0) (length 2.54)
\t\t\t\t(name "Pin_11" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "11" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -3.81 -12.7 0) (length 2.54)
\t\t\t\t(name "Pin_12" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "12" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -3.81 -15.24 0) (length 2.54)
\t\t\t\t(name "Pin_13" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "13" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -3.81 -17.78 0) (length 2.54)
\t\t\t\t(name "Pin_14" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "14" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t)
\t)"""

# 4-pin connector (UART)
LIB_CONN_01x04 = """(symbol "Connector_Generic:Conn_01x04"
\t\t(pin_names (offset 1.016) (hide yes))
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(property "Reference" "J"
\t\t\t(at 0 5.08 0)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Value" "Conn_01x04"
\t\t\t(at 0 -7.62 0)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Footprint" "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical"
\t\t\t(at 0 0 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(symbol "Conn_01x04_1_1"
\t\t\t(rectangle (start -1.27 3.81) (end 1.27 -6.35)
\t\t\t\t(stroke (width 0.254) (type default))
\t\t\t\t(fill (type background))
\t\t\t)
\t\t\t(pin passive line (at -3.81 2.54 0) (length 2.54)
\t\t\t\t(name "Pin_1" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "1" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -3.81 0 0) (length 2.54)
\t\t\t\t(name "Pin_2" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "2" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -3.81 -2.54 0) (length 2.54)
\t\t\t\t(name "Pin_3" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "3" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -3.81 -5.08 0) (length 2.54)
\t\t\t\t(name "Pin_4" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "4" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t)
\t)"""

# 2x10 connector (GPIO header)
LIB_CONN_02x10 = """(symbol "Connector_Generic:Conn_02x10_Odd_Even"
\t\t(pin_names (offset 1.016) (hide yes))
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(property "Reference" "J"
\t\t\t(at 0 13.97 0)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Value" "Conn_02x10_Odd_Even"
\t\t\t(at 0 -13.97 0)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Footprint" "Connector_PinHeader_2.54mm:PinHeader_2x10_P2.54mm_Vertical"
\t\t\t(at 0 0 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(symbol "Conn_02x10_Odd_Even_0_1"
\t\t\t(rectangle (start -1.27 12.7) (end 1.27 -12.7)
\t\t\t\t(stroke (width 0.254) (type default))
\t\t\t\t(fill (type background))
\t\t\t)
\t\t)
\t\t(symbol "Conn_02x10_Odd_Even_1_1"
\t\t\t(pin passive line (at -3.81 11.43 0) (length 2.54)
\t\t\t\t(name "Pin_1" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "1" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 3.81 11.43 180) (length 2.54)
\t\t\t\t(name "Pin_2" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "2" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -3.81 8.89 0) (length 2.54)
\t\t\t\t(name "Pin_3" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "3" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 3.81 8.89 180) (length 2.54)
\t\t\t\t(name "Pin_4" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "4" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -3.81 6.35 0) (length 2.54)
\t\t\t\t(name "Pin_5" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "5" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 3.81 6.35 180) (length 2.54)
\t\t\t\t(name "Pin_6" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "6" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -3.81 3.81 0) (length 2.54)
\t\t\t\t(name "Pin_7" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "7" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 3.81 3.81 180) (length 2.54)
\t\t\t\t(name "Pin_8" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "8" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -3.81 1.27 0) (length 2.54)
\t\t\t\t(name "Pin_9" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "9" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 3.81 1.27 180) (length 2.54)
\t\t\t\t(name "Pin_10" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "10" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -3.81 -1.27 0) (length 2.54)
\t\t\t\t(name "Pin_11" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "11" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 3.81 -1.27 180) (length 2.54)
\t\t\t\t(name "Pin_12" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "12" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -3.81 -3.81 0) (length 2.54)
\t\t\t\t(name "Pin_13" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "13" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 3.81 -3.81 180) (length 2.54)
\t\t\t\t(name "Pin_14" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "14" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -3.81 -6.35 0) (length 2.54)
\t\t\t\t(name "Pin_15" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "15" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 3.81 -6.35 180) (length 2.54)
\t\t\t\t(name "Pin_16" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "16" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -3.81 -8.89 0) (length 2.54)
\t\t\t\t(name "Pin_17" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "17" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 3.81 -8.89 180) (length 2.54)
\t\t\t\t(name "Pin_18" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "18" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at -3.81 -11.43 0) (length 2.54)
\t\t\t\t(name "Pin_19" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "19" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t\t(pin passive line (at 3.81 -11.43 180) (length 2.54)
\t\t\t\t(name "Pin_20" (effects (font (size 1.27 1.27))))
\t\t\t\t(number "20" (effects (font (size 1.27 1.27))))
\t\t\t)
\t\t)
\t)"""


def generate_step10():
    """Generate Step 10: Peripherals — Display, 1-Wire, GPIO header, UART."""

    lib_symbols = []
    symbols = []
    wires = []
    junctions = []
    labels = []
    texts = []
    no_connects = []

    lib_symbols.append(LIB_CONN_01x14)
    lib_symbols.append(LIB_CONN_01x04)
    lib_symbols.append(LIB_CONN_02x10)

    # ================================================================
    # J2: Display connector 1×14 (ILI9488 + XPT2046)
    # ================================================================
    texts.append(make_text("DISPLAY CONNECTOR", 310, 240, size=3))

    j2_x = 330
    j2_y = 280

    symbols.append(make_symbol("Connector_Generic:Conn_01x14", "J2", "DISPLAY",
                               j2_x, j2_y, 0, pin_count=14))

    # Pin positions: pin1 at (j2_x-3.81, j2_y-15.24), each +2.54 down
    # Pin n at y = j2_y - 15.24 + (n-1)*2.54
    j2_px = j2_x - 3.81  # 326.19
    def j2_py(n):
        return j2_y - 15.24 + (n - 1) * 2.54

    # Pin 1: +3V3
    symbols.append(make_symbol("power:+3V3", "#PWR85", "+3V3",
                               j2_px - 5, j2_py(1), 90, pin_count=1))
    wires.append(make_wire(j2_px - 5, j2_py(1), j2_px, j2_py(1)))

    # Pin 2: GND
    symbols.append(make_symbol("power:GND", "#PWR86", "GND",
                               j2_px - 5, j2_py(2), 90, pin_count=1))
    wires.append(make_wire(j2_px - 5, j2_py(2), j2_px, j2_py(2)))

    # Pin 3: TFT_CS
    labels.append(make_label("TFT_CS", j2_px - 10, j2_py(3), angle=180))
    wires.append(make_wire(j2_px - 10, j2_py(3), j2_px, j2_py(3)))

    # Pin 4: TFT_RST
    labels.append(make_label("TFT_RST", j2_px - 10, j2_py(4), angle=180))
    wires.append(make_wire(j2_px - 10, j2_py(4), j2_px, j2_py(4)))

    # Pin 5: TFT_DC
    labels.append(make_label("TFT_DC", j2_px - 10, j2_py(5), angle=180))
    wires.append(make_wire(j2_px - 10, j2_py(5), j2_px, j2_py(5)))

    # Pin 6: SPI_MOSI
    labels.append(make_label("SPI_MOSI", j2_px - 10, j2_py(6), angle=180))
    wires.append(make_wire(j2_px - 10, j2_py(6), j2_px, j2_py(6)))

    # Pin 7: SPI_SCK
    labels.append(make_label("SPI_SCK", j2_px - 10, j2_py(7), angle=180))
    wires.append(make_wire(j2_px - 10, j2_py(7), j2_px, j2_py(7)))

    # Pin 8: TFT_BL
    labels.append(make_label("TFT_BL", j2_px - 10, j2_py(8), angle=180))
    wires.append(make_wire(j2_px - 10, j2_py(8), j2_px, j2_py(8)))

    # Pin 9: SPI_MISO
    labels.append(make_label("SPI_MISO", j2_px - 10, j2_py(9), angle=180))
    wires.append(make_wire(j2_px - 10, j2_py(9), j2_px, j2_py(9)))

    # Pin 10: SPI_SCK (shared)
    labels.append(make_label("SPI_SCK", j2_px - 10, j2_py(10), angle=180))
    wires.append(make_wire(j2_px - 10, j2_py(10), j2_px, j2_py(10)))

    # Pin 11: TOUCH_CS
    labels.append(make_label("TOUCH_CS", j2_px - 10, j2_py(11), angle=180))
    wires.append(make_wire(j2_px - 10, j2_py(11), j2_px, j2_py(11)))

    # Pin 12: SPI_MOSI (shared)
    labels.append(make_label("SPI_MOSI", j2_px - 10, j2_py(12), angle=180))
    wires.append(make_wire(j2_px - 10, j2_py(12), j2_px, j2_py(12)))

    # Pin 13: SPI_MISO (shared)
    labels.append(make_label("SPI_MISO", j2_px - 10, j2_py(13), angle=180))
    wires.append(make_wire(j2_px - 10, j2_py(13), j2_px, j2_py(13)))

    # Pin 14: TOUCH_IRQ
    labels.append(make_label("TOUCH_IRQ", j2_px - 10, j2_py(14), angle=180))
    wires.append(make_wire(j2_px - 10, j2_py(14), j2_px, j2_py(14)))

    # ================================================================
    # J3-J6: 1-Wire connectors (JST-XH 3-pin) + R31 pull-up
    # ================================================================
    texts.append(make_text("1-WIRE SENSORS", 310, 310, size=3))

    ow_base_x = 330
    ow_base_y = 325

    for i, jref in enumerate(["J3", "J4", "J5", "J6"]):
        jx = ow_base_x + i * 20
        jy = ow_base_y

        symbols.append(make_symbol("Connector_Generic:Conn_01x03", jref, f"1W_{i+1}",
                                   jx, jy, 0, pin_count=3))
        jpx = jx - 3.81
        # Conn_01x03 pins: Pin1 at (jpx, jy-2.54), Pin2 at (jpx, jy), Pin3 at (jpx, jy+2.54)
        # Pin 1: +3V3
        symbols.append(make_symbol("power:+3V3", f"#PWR{87+i*2}", "+3V3",
                                   jpx - 5, jy - 2.54, 90, pin_count=1))
        wires.append(make_wire(jpx - 5, jy - 2.54, jpx, jy - 2.54))

        # Pin 2: ONEWIRE_DATA
        labels.append(make_label("ONEWIRE_DATA", jpx - 10, jy, angle=180))
        wires.append(make_wire(jpx - 10, jy, jpx, jy))

        # Pin 3: GND
        symbols.append(make_symbol("power:GND", f"#PWR{88+i*2}", "GND",
                                   jpx - 5, jy + 2.54, 90, pin_count=1))
        wires.append(make_wire(jpx - 5, jy + 2.54, jpx, jy + 2.54))

    # R31: 4.7kΩ pull-up ONEWIRE_DATA → +3V3
    r31_x = ow_base_x - 10
    r31_y = ow_base_y - 5
    symbols.append(make_symbol("Device:R", "R31", "4.7k",
                               r31_x, r31_y, 0, pin_count=2))
    labels.append(make_label("ONEWIRE_DATA", r31_x, r31_y + 8, angle=0))
    wires.append(make_wire(r31_x, r31_y + 3.81, r31_x, r31_y + 8))
    symbols.append(make_symbol("power:+3V3", "#PWR95", "+3V3",
                               r31_x, r31_y - 8, 0, pin_count=1))
    wires.append(make_wire(r31_x, r31_y - 3.81, r31_x, r31_y - 8))

    # ================================================================
    # J7: GPIO expansion header 2×10
    # ================================================================
    texts.append(make_text("GPIO HEADER", 355, 240, size=3))

    j7_x = 380
    j7_y = 280

    symbols.append(make_symbol("Connector_Generic:Conn_02x10_Odd_Even", "J7", "GPIO_EXT",
                               j7_x, j7_y, 0, pin_count=20))

    # Left pins (odd): GPIO signals at (j7_x - 3.81, ...)
    # Right pins (even): GND at (j7_x + 3.81, ...)
    j7_lx = j7_x - 3.81  # 376.19
    j7_rx = j7_x + 3.81  # 383.81

    # y positions: pin1/2 at j7_y-11.43, each pair +2.54 down
    def j7_ly(row):  # row 0-9
        return j7_y - 11.43 + row * 2.54

    # Row 0 (pin 1/2): GPIO12 / GND
    labels.append(make_label("GPIO12", j7_lx - 10, j7_ly(0), angle=180))
    wires.append(make_wire(j7_lx - 10, j7_ly(0), j7_lx, j7_ly(0)))
    symbols.append(make_symbol("power:GND", "#PWR96", "GND",
                               j7_rx + 5, j7_ly(0), 270, pin_count=1))
    wires.append(make_wire(j7_rx, j7_ly(0), j7_rx + 5, j7_ly(0)))

    # Row 1 (pin 3/4): GPIO16 / GND
    labels.append(make_label("GPIO16", j7_lx - 10, j7_ly(1), angle=180))
    wires.append(make_wire(j7_lx - 10, j7_ly(1), j7_lx, j7_ly(1)))
    symbols.append(make_symbol("power:GND", "#PWR97", "GND",
                               j7_rx + 5, j7_ly(1), 270, pin_count=1))
    wires.append(make_wire(j7_rx, j7_ly(1), j7_rx + 5, j7_ly(1)))

    # Row 2 (pin 5/6): GPIO17 / GND
    labels.append(make_label("GPIO17", j7_lx - 10, j7_ly(2), angle=180))
    wires.append(make_wire(j7_lx - 10, j7_ly(2), j7_lx, j7_ly(2)))
    symbols.append(make_symbol("power:GND", "#PWR98", "GND",
                               j7_rx + 5, j7_ly(2), 270, pin_count=1))
    wires.append(make_wire(j7_rx, j7_ly(2), j7_rx + 5, j7_ly(2)))

    # Row 3 (pin 7/8): GPIO22 / GND
    labels.append(make_label("GPIO22", j7_lx - 10, j7_ly(3), angle=180))
    wires.append(make_wire(j7_lx - 10, j7_ly(3), j7_lx, j7_ly(3)))
    symbols.append(make_symbol("power:GND", "#PWR99", "GND",
                               j7_rx + 5, j7_ly(3), 270, pin_count=1))
    wires.append(make_wire(j7_rx, j7_ly(3), j7_rx + 5, j7_ly(3)))

    # Row 4 (pin 9/10): GPIO34 / GND
    labels.append(make_label("GPIO34", j7_lx - 10, j7_ly(4), angle=180))
    wires.append(make_wire(j7_lx - 10, j7_ly(4), j7_lx, j7_ly(4)))
    symbols.append(make_symbol("power:GND", "#PWR100", "GND",
                               j7_rx + 5, j7_ly(4), 270, pin_count=1))
    wires.append(make_wire(j7_rx, j7_ly(4), j7_rx + 5, j7_ly(4)))

    # Row 5 (pin 11/12): GPIO35 / GND
    labels.append(make_label("GPIO35", j7_lx - 10, j7_ly(5), angle=180))
    wires.append(make_wire(j7_lx - 10, j7_ly(5), j7_lx, j7_ly(5)))
    symbols.append(make_symbol("power:GND", "#PWR101", "GND",
                               j7_rx + 5, j7_ly(5), 270, pin_count=1))
    wires.append(make_wire(j7_rx, j7_ly(5), j7_rx + 5, j7_ly(5)))

    # Row 6 (pin 13/14): GPIO36 / GND
    labels.append(make_label("GPIO36", j7_lx - 10, j7_ly(6), angle=180))
    wires.append(make_wire(j7_lx - 10, j7_ly(6), j7_lx, j7_ly(6)))
    symbols.append(make_symbol("power:GND", "#PWR102", "GND",
                               j7_rx + 5, j7_ly(6), 270, pin_count=1))
    wires.append(make_wire(j7_rx, j7_ly(6), j7_rx + 5, j7_ly(6)))

    # Row 7 (pin 15/16): +3V3 / +5V
    symbols.append(make_symbol("power:+3V3", "#PWR103", "+3V3",
                               j7_lx - 5, j7_ly(7), 90, pin_count=1))
    wires.append(make_wire(j7_lx - 5, j7_ly(7), j7_lx, j7_ly(7)))
    symbols.append(make_symbol("power:+5V", "#PWR104", "+5V",
                               j7_rx + 5, j7_ly(7), 270, pin_count=1))
    wires.append(make_wire(j7_rx, j7_ly(7), j7_rx + 5, j7_ly(7)))

    # Row 8 (pin 17/18): +12V / GND
    symbols.append(make_symbol("power:+12V", "#PWR105", "+12V",
                               j7_lx - 5, j7_ly(8), 90, pin_count=1))
    wires.append(make_wire(j7_lx - 5, j7_ly(8), j7_lx, j7_ly(8)))
    symbols.append(make_symbol("power:GND", "#PWR106", "GND",
                               j7_rx + 5, j7_ly(8), 270, pin_count=1))
    wires.append(make_wire(j7_rx, j7_ly(8), j7_rx + 5, j7_ly(8)))

    # Row 9 (pin 19/20): GND / GND
    symbols.append(make_symbol("power:GND", "#PWR107", "GND",
                               j7_lx - 5, j7_ly(9), 90, pin_count=1))
    wires.append(make_wire(j7_lx - 5, j7_ly(9), j7_lx, j7_ly(9)))
    symbols.append(make_symbol("power:GND", "#PWR108", "GND",
                               j7_rx + 5, j7_ly(9), 270, pin_count=1))
    wires.append(make_wire(j7_rx, j7_ly(9), j7_rx + 5, j7_ly(9)))

    # ================================================================
    # J8: Debug UART 1×4 (3V3, TX, RX, GND)
    # ================================================================
    texts.append(make_text("DEBUG UART", 310, 345, size=3))

    j8_x = 330
    j8_y = 360

    symbols.append(make_symbol("Connector_Generic:Conn_01x04", "J8", "UART",
                               j8_x, j8_y, 0, pin_count=4))

    j8_px = j8_x - 3.81  # 326.19
    # Pin 1 at (j8_px, j8_y - 2.54), pin 2 at (j8_px, j8_y), pin 3 at (j8_px, j8_y + 2.54), pin 4 at (j8_px, j8_y + 5.08)

    # Pin 1: +3V3
    symbols.append(make_symbol("power:+3V3", "#PWR109", "+3V3",
                               j8_px - 5, j8_y - 2.54, 90, pin_count=1))
    wires.append(make_wire(j8_px - 5, j8_y - 2.54, j8_px, j8_y - 2.54))

    # Pin 2: UART_TX
    labels.append(make_label("UART_TX", j8_px - 10, j8_y, angle=180))
    wires.append(make_wire(j8_px - 10, j8_y, j8_px, j8_y))

    # Pin 3: UART_RX
    labels.append(make_label("UART_RX", j8_px - 10, j8_y + 2.54, angle=180))
    wires.append(make_wire(j8_px - 10, j8_y + 2.54, j8_px, j8_y + 2.54))

    # Pin 4: GND
    symbols.append(make_symbol("power:GND", "#PWR110", "GND",
                               j8_px - 5, j8_y + 5.08, 90, pin_count=1))
    wires.append(make_wire(j8_px - 5, j8_y + 5.08, j8_px, j8_y + 5.08))

    return lib_symbols, symbols, wires, junctions, labels, texts, no_connects


# ============================================================
# ASSEMBLE SCHEMATIC
# ============================================================

def build_schematic():
    """Build the complete .kicad_sch file."""

    project_uuid = "54ccc777-3789-41c0-b4eb-6807475564db"

    # Gather all elements from all steps
    all_lib_symbols = []
    all_symbols = []
    all_wires = []
    all_junctions = []
    all_labels = []
    all_texts = []

    # Step 1
    ls, sym, w, j, lbl, txt = generate_step1()
    all_lib_symbols.extend(ls)
    all_symbols.extend(sym)
    all_wires.extend(w)
    all_junctions.extend(j)
    all_labels.extend(lbl)
    all_texts.extend(txt)

    # Step 2
    ls, sym, w, j, lbl, txt = generate_step2()
    all_lib_symbols.extend(ls)
    all_symbols.extend(sym)
    all_wires.extend(w)
    all_junctions.extend(j)
    all_labels.extend(lbl)
    all_texts.extend(txt)

    # Step 3
    ls, sym, w, j, lbl, txt = generate_step3()
    all_lib_symbols.extend(ls)
    all_symbols.extend(sym)
    all_wires.extend(w)
    all_junctions.extend(j)
    all_labels.extend(lbl)
    all_texts.extend(txt)

    # Step 4
    ls, sym, w, j, lbl, txt = generate_step4()
    all_lib_symbols.extend(ls)
    all_symbols.extend(sym)
    all_wires.extend(w)
    all_junctions.extend(j)
    all_labels.extend(lbl)
    all_texts.extend(txt)

    all_no_connects = []

    # Step 5
    ls, sym, w, j, lbl, txt, nc = generate_step5()
    all_lib_symbols.extend(ls)
    all_symbols.extend(sym)
    all_wires.extend(w)
    all_junctions.extend(j)
    all_labels.extend(lbl)
    all_texts.extend(txt)
    all_no_connects.extend(nc)

    # Step 6
    ls, sym, w, j, lbl, txt, nc = generate_step6()
    all_lib_symbols.extend(ls)
    all_symbols.extend(sym)
    all_wires.extend(w)
    all_junctions.extend(j)
    all_labels.extend(lbl)
    all_texts.extend(txt)
    all_no_connects.extend(nc)

    # Step 7
    ls, sym, w, j, lbl, txt, nc = generate_step7()
    all_lib_symbols.extend(ls)
    all_symbols.extend(sym)
    all_wires.extend(w)
    all_junctions.extend(j)
    all_labels.extend(lbl)
    all_texts.extend(txt)
    all_no_connects.extend(nc)

    # Step 8
    ls, sym, w, j, lbl, txt, nc = generate_step8()
    all_lib_symbols.extend(ls)
    all_symbols.extend(sym)
    all_wires.extend(w)
    all_junctions.extend(j)
    all_labels.extend(lbl)
    all_texts.extend(txt)
    all_no_connects.extend(nc)

    # Step 9
    ls, sym, w, j, lbl, txt, nc = generate_step9()
    all_lib_symbols.extend(ls)
    all_symbols.extend(sym)
    all_wires.extend(w)
    all_junctions.extend(j)
    all_labels.extend(lbl)
    all_texts.extend(txt)
    all_no_connects.extend(nc)

    # Step 10
    ls, sym, w, j, lbl, txt, nc = generate_step10()
    all_lib_symbols.extend(ls)
    all_symbols.extend(sym)
    all_wires.extend(w)
    all_junctions.extend(j)
    all_labels.extend(lbl)
    all_texts.extend(txt)
    all_no_connects.extend(nc)

    # Build the S-expression
    lib_section = "\n\t\t".join(all_lib_symbols)

    content = f"""(kicad_sch
\t(version 20260306)
\t(generator "eeschema")
\t(generator_version "10.0")
\t(uuid "{project_uuid}")
\t(paper "A3")
\t(lib_symbols
\t\t{lib_section}
\t)

{chr(10).join(all_texts)}

{chr(10).join(all_no_connects)}

{chr(10).join(all_junctions)}

{chr(10).join(all_wires)}

{chr(10).join(all_labels)}

{chr(10).join(all_symbols)}

\t(sheet_instances
\t\t(path "/"
\t\t\t(page "1")
\t\t)
\t)
\t(embedded_fonts no)
)"""

    return content


if __name__ == "__main__":
    sch = build_schematic()
    output_path = "/Users/ing.tomaslaso/Documents/kiCad/ph-verzion-01/ph-verzion-01.kicad_sch"
    with open(output_path, 'w') as f:
        f.write(sch)
    print(f"Schematic written to {output_path}")
    print(f"File size: {len(sch)} bytes")
