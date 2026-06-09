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
LIB_AMS1117 = """(symbol "Custom:AMS1117-3.3" (pin_names (offset 1.016))
    (exclude_from_sim no) (in_bom yes) (on_board yes)
    (property "Reference" "U" (at 0 6.35 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "AMS1117-3.3" (at 0 -6.35 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Datasheet" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Description" "1A Low Dropout Voltage Regulator, 3.3V, SOT-223" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (symbol "AMS1117-3.3_0_1"
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
    (symbol "AMS1117-3.3_1_1"
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

# LM7805 linear regulator (TO-220)
# Pin 1: IN, Pin 2: GND, Pin 3: OUT
LIB_LM7805 = """(symbol "Custom:LM7805" (pin_names (offset 1.016))
    (exclude_from_sim no) (in_bom yes) (on_board yes)
    (property "Reference" "U" (at 0 6.35 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "LM7805" (at 0 -6.35 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Datasheet" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (property "Description" "Linear Voltage Regulator, 5V, 1.5A, TO-220" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (hide yes))
    )
    (symbol "LM7805_0_1"
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
    (symbol "LM7805_1_1"
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

    # PWR_FLAG on +5V
    symbols.append(make_symbol("power:PWR_FLAG", "#FLG03", "PWR_FLAG",
                               out_5v_x + 10, out_5v_y - 5, 0, pin_count=1))
    wires.append(make_wire(out_5v_x + 10, out_5v_y - 5, out_5v_x + 10, out_5v_y))
    wires.append(make_wire(out_5v_x, out_5v_y, out_5v_x + 10, out_5v_y))

    # Net label
    labels.append(make_label("+5V", out_5v_x + 3, out_5v_y - 3))

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

    symbols.append(make_symbol("Custom:AMS1117-3.3", "U3", "AMS1117-3.3",
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

    # PWR_FLAG on +3V3
    symbols.append(make_symbol("power:PWR_FLAG", "#FLG04", "PWR_FLAG",
                               vout_x + 8, vout_y - 5, 0, pin_count=1))
    wires.append(make_wire(vout_x + 8, vout_y - 5, vout_x + 8, vout_y))
    wires.append(make_wire(vout_x, vout_y, vout_x + 8, vout_y))

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

    symbols.append(make_symbol("Custom:LM7805", "U4", "LM7805",
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
