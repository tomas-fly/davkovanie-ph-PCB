#!/usr/bin/env python3
"""
pH/ORP Monitor v1.0 — KiCad Schematic Generator
Generates .kicad_sch file step by step.
"""

import uuid

def uid():
    return str(uuid.uuid4())

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
      (rectangle (start -1.016 3.81) (end 1.016 -3.81)
        (stroke (width 0.254) (type default)) (fill (type none))
      )
    )
    (symbol "R_1_1"
      (pin passive line (at 0 5.08 270) (length 1.27)
        (name "~" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at 0 -5.08 90) (length 1.27)
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
        (number "4" (effects (font (size 1.27 1.27))))
      )
    )
    (embedded_fonts no)
  )"""


# ============================================================
# HELPER: Symbol instance
# ============================================================

def make_symbol(lib_id, ref, value, x, y, angle=0, mirror=None, unit=1,
                extra_props=None, project_name="ph-verzion-01",
                project_uuid="54ccc777-3789-41c0-b4eb-6807475564db",
                pin_count=2):
    """Generate a symbol instance S-expression."""
    sym_uuid = uid()

    mirror_str = ""
    if mirror == "x":
        mirror_str = "\n\t\t(mirror x)"
    elif mirror == "y":
        mirror_str = "\n\t\t(mirror y)"

    # Generate pin entries
    pins = ""
    for i in range(1, pin_count + 1):
        pins += f'\n\t\t(pin "{i}" (uuid "{uid()}"))'

    # Property positions (relative to symbol position)
    ref_y = y - 2.54
    val_y = y + 2.54

    props = f"""
\t\t(property "Reference" "{ref}" (at {x + 2.54} {ref_y} 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify left))
\t\t)
\t\t(property "Value" "{value}" (at {x + 2.54} {val_y} 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify left))
\t\t)
\t\t(property "Footprint" "" (at {x} {y} 0)
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
    return f"""\t(wire
\t\t(pts
\t\t\t(xy {x1} {y1}) (xy {x2} {y2})
\t\t)
\t\t(stroke (width 0) (type default))
\t\t(uuid "{uid()}")
\t)"""


def make_junction(x, y):
    """Generate a junction S-expression."""
    return f"""\t(junction
\t\t(at {x} {y})
\t\t(diameter 0)
\t\t(color 0 0 0 0)
\t\t(uuid "{uid()}")
\t)"""


def make_label(name, x, y, angle=0):
    """Generate a net label S-expression."""
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
    return f"""\t(no_connect
\t\t(at {x} {y})
\t\t(uuid "{uid()}")
\t)"""


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
    # Fuse pin 1 (top) at y-5.08, pin 2 (bottom) at y+5.08 from center
    # Place at (55, 62.46) rotated 90 degrees (horizontal)
    symbols.append(make_symbol("Device:Fuse", "F1", "2A/250V",
                               55, 62.46, 90, pin_count=2))

    # Wire: J1 pin 1 (L) → F1 pin 1
    # J1 pin 1 exits at (36.19, 62.46), F1 at 90° has pin1 at (55-5.08, 62.46)=(49.92, 62.46)
    wires.append(make_wire(36.19, 62.46, 49.92, 62.46))

    # F1 pin 2 exits at (55+5.08, 62.46) = (60.08, 62.46)
    # HLK-30M12 at (85, 65)
    # HLK AC_L pin at (-11.43 from center + 3.81 up) = (85-11.43, 65-3.81) = (73.57, 61.19)
    # Wait, pin is at (at -11.43 3.81 0) meaning offset from symbol center
    # So AC_L absolute: (85-11.43, 65-3.81) = (73.57, 61.19)
    # AC_N absolute: (85-11.43, 65+3.81) = (73.57, 68.81)
    # +12V absolute: (85+11.43, 65-3.81) = (96.43, 61.19)
    # GND absolute: (85+11.43, 65+3.81) = (96.43, 68.81)

    symbols.append(make_symbol("Custom:HLK-30M12", "U1", "HLK-30M12",
                               85, 65, 0, pin_count=4))

    # Wire: F1 pin 2 → HLK AC_L
    wires.append(make_wire(60.08, 62.46, 73.57, 62.46))
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
    # Actually R has pin1 at y-5.08 and pin2 at y+5.08 from center
    symbols.append(make_symbol("Device:R", "R1", "1k",
                               140, 62, 0, pin_count=2))
    # R1 pin1 at (140, 62-5.08)=(140, 56.92), pin2 at (140, 62+5.08)=(140, 67.08)

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
    wires.append(make_wire(140, 53, 140, 56.92))

    # R1 bottom to LED anode
    wires.append(make_wire(140, 67.08, 140, 68.19))

    # LED cathode to GND
    symbols.append(make_symbol("power:GND", "#PWR04", "GND",
                               140, 78, 0, pin_count=1))
    wires.append(make_wire(140, 75.81, 140, 78))

    # PWR_FLAGs
    # PWR_FLAG on +12V rail
    symbols.append(make_symbol("power:PWR_FLAG", "#FLG01", "PWR_FLAG",
                               120, 56.19, 0, pin_count=1))
    wires.append(make_wire(120, 56.19, 120, 61.19))
    junctions.append(make_junction(120, 61.19))

    # PWR_FLAG on GND rail
    symbols.append(make_symbol("power:PWR_FLAG", "#FLG02", "PWR_FLAG",
                               120, 73.81, 180, pin_count=1))
    wires.append(make_wire(120, 73.81, 120, 68.81))
    junctions.append(make_junction(120, 68.81))

    # Net labels for connection to next steps
    labels.append(make_label("+12V", 130, 61.19))

    return lib_symbols, symbols, wires, junctions, labels, texts


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
