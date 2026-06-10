#!/usr/bin/env python3
"""Compact layout — squeeze components closer, shrink board."""
import re
import uuid as uuid_mod

PCB = "/Users/ing.tomaslaso/Documents/kiCad/ph-verzion-01/ph-verzion-01.kicad_pcb"

with open(PCB, "r") as f:
    content = f.read()

# ============================================================
# NEW COMPACT LAYOUT
# Target board: ~175x115mm
# Board origin: (25,25), corners (25,25)→(200,140)
# ============================================================
#
# Layout plan (top to bottom):
#
#  Row 1 (y=28-60): Power supply chain left→right
#    [U1 AC-DC 60x36mm] [Buck U2+L1+D2] [LDO U3] [Analog pwr U4,U5]
#    Below U1: J1, F1, MOV1, J12
#
#  Row 2 (y=62-95): Analog frontends (right) + ESP32 (center-left)
#    [J connectors] [ESP32 U11] [ADC U10] [pH: U6,U7,R,C] [BNC P1]
#                                         [ORP: U8,U9,R,C] [BNC P2]
#
#  Row 3 (y=98-135): MOSFETs, relay, output terminals
#    [Q1-Q4 + R + D] [RLY1 + U12] [J9 J10 J11]
#

# Get current positions
blocks = content.split('\n\t(footprint ')
current = {}
for b in blocks[1:]:
    ref_m = re.search(r'\(property "Reference" "([^"]+)"', b)
    at_m = re.search(r'\(at ([\d.\-]+) ([\d.\-]+)( ([\d.\-]+))?\)', b)
    if ref_m and at_m:
        ref = ref_m.group(1)
        x, y = float(at_m.group(1)), float(at_m.group(2))
        a = float(at_m.group(4)) if at_m.group(4) else 0
        current[ref] = (x, y, a)

NEW = {}

# ── ROW 1: POWER SUPPLY (y=28-58) ──

# U1 AC-DC (60x36mm, origin offset left) at top-left
# Body: x=origin-5..origin+55, y=origin-22..origin+14
NEW["U1"]  = (32, 48, 0)    # body: 27..87, 26..62

# Input components BELOW U1
NEW["J1"]  = (32, 68, 0)    # AC input
NEW["F1"]  = (50, 68, 0)    # fuse
NEW["MOV1"]= (66, 68, 0)    # varistor
NEW["J12"] = (32, 80, 0)    # 12V output terminal
NEW["C1"]  = (48, 80, 0)    # filter cap
NEW["R1"]  = (56, 80, 0)    # LED resistor
NEW["D1"]  = (60, 80, 0)    # LED

# Buck converter (right of U1, x=90+)
NEW["C2"]  = (92, 30, 0)    # input cap 10mm
NEW["U2"]  = (106, 30, 0)   # LM2596 TO-263
NEW["C3"]  = (120, 30, 0)   # output cap 8mm
NEW["D2"]  = (98, 42, 0)    # Schottky
NEW["L1"]  = (110, 42, 0)   # inductor 11mm
NEW["C5"]  = (122, 42, 0)   # ceramic cap
NEW["FB1"] = (130, 42, 0)   # ferrite

# LDO (right of buck, same row)
NEW["U3"]  = (140, 30, 0)   # AMS1117 SOT-223
NEW["C4"]  = (134, 26, 0)   # input cap
NEW["C6"]  = (148, 26, 0)   # output cap

# Analog power (below buck, x=92+)
NEW["U4"]  = (106, 54, 0)   # LM7805 TO-263
NEW["C7"]  = (94, 52, 0)    # input cap
NEW["C8"]  = (94, 58, 0)    # bypass
NEW["C9"]  = (118, 52, 0)   # output cap
NEW["C10"] = (118, 58, 0)   # output cap
NEW["FB2"] = (126, 52, 0)   # ferrite
NEW["L2"]  = (126, 58, 0)   # inductor
NEW["U5"]  = (106, 64, 0)   # TPS60400 charge pump
NEW["C11"] = (96, 64, 0)
NEW["C12"] = (116, 64, 0)

# ── ROW 2: ESP32 + ANALOG FRONTENDS (y=62-95) ──

# Connectors (far left)
NEW["J2"]  = (28, 90, 0)    # display 1x14 vertical (33mm tall)
NEW["J7"]  = (38, 90, 0)    # GPIO 2x10 vertical (23mm tall)
NEW["J3"]  = (28, 70, 0)    # 1-Wire JSTs
NEW["J4"]  = (28, 78, 0)
NEW["J5"]  = (38, 70, 0)
NEW["J6"]  = (38, 78, 0)

# ESP32 (center, below analog power)
# ESP32 origin at bottom-center, body extends UP ~25mm
# Courtyard: ~x±12, y-28..+2
NEW["U11"] = (70, 94, 0)    # origin at bottom, body spans y=66..96
NEW["R16"] = (56, 72, 0)    # pull resistors LEFT of ESP32
NEW["R17"] = (56, 76, 0)
NEW["R18"] = (56, 80, 0)
NEW["R19"] = (56, 84, 0)
NEW["C26"] = (84, 72, 0)    # bypass caps RIGHT of ESP32
NEW["C27"] = (84, 76, 0)
NEW["C28"] = (84, 80, 0)
NEW["J8"]  = (84, 96, 0)    # UART header

# ADC (between ESP32 and analog frontend)
NEW["U10"] = (96, 72, 0)    # ADS1115 MSOP-10
NEW["C25"] = (96, 66, 0)
NEW["R31"] = (104, 72, 0)

# pH analog frontend (right side, top half)
NEW["U6"]  = (150, 66, 0)   # CA3140 DIP-8
NEW["U7"]  = (150, 80, 0)   # TL071 DIP-8
NEW["R2"]  = (140, 64, 0)
NEW["R3"]  = (140, 68, 0)
NEW["R4"]  = (164, 72, 0)   # trimpot
NEW["R5"]  = (140, 72, 0)
NEW["R6"]  = (140, 76, 0)
NEW["R7"]  = (140, 80, 0)
NEW["R8"]  = (140, 84, 0)
NEW["C13"] = (164, 64, 0)
NEW["C14"] = (164, 68, 0)
NEW["C15"] = (168, 64, 0)
NEW["C16"] = (168, 68, 0)
NEW["C17"] = (168, 72, 0)
NEW["C29"] = (150, 90, 0)   # 18mm film cap
NEW["P1"]  = (192, 74, 270) # BNC right edge

# ORP analog frontend (right side, bottom half)
NEW["U8"]  = (120, 90, 0)   # CA3140 DIP-8
NEW["U9"]  = (120, 104, 0)  # TL071 DIP-8
NEW["R9"]  = (110, 88, 0)
NEW["R10"] = (110, 92, 0)
NEW["R11"] = (134, 96, 0)   # trimpot
NEW["R12"] = (110, 96, 0)
NEW["R13"] = (110, 100, 0)
NEW["R14"] = (110, 104, 0)
NEW["R15"] = (110, 108, 0)
NEW["C18"] = (134, 88, 0)
NEW["C19"] = (134, 92, 0)
NEW["C20"] = (138, 88, 0)
NEW["C21"] = (138, 92, 0)
NEW["C22"] = (138, 96, 0)
NEW["C23"] = (142, 88, 0)
NEW["C24"] = (142, 92, 0)
NEW["P2"]  = (192, 98, 270) # BNC right edge

# ── ROW 3: MOSFET OUTPUTS + RELAY (y=112-135) ──

NEW["Q1"]  = (50, 115, 0)
NEW["Q2"]  = (64, 115, 0)
NEW["Q3"]  = (78, 115, 0)
NEW["Q4"]  = (92, 115, 0)
NEW["R20"] = (48, 122, 0)
NEW["R21"] = (48, 125, 0)
NEW["R22"] = (62, 122, 0)
NEW["R23"] = (62, 125, 0)
NEW["R24"] = (76, 122, 0)
NEW["R25"] = (76, 125, 0)
NEW["R26"] = (90, 122, 0)
NEW["R27"] = (90, 125, 0)
NEW["R28"] = (102, 122, 0)
NEW["R29"] = (102, 125, 0)
NEW["R30"] = (110, 122, 0)
NEW["D3"]  = (52, 130, 0)
NEW["D4"]  = (66, 130, 0)
NEW["D5"]  = (80, 130, 0)
NEW["D6"]  = (94, 130, 0)
NEW["D7"]  = (106, 130, 0)
NEW["J9"]  = (52, 136, 0)   # output terminals
NEW["J10"] = (72, 136, 0)
NEW["J11"] = (94, 136, 0)   # AC output 3-pin
NEW["U12"] = (114, 115, 0)  # optocoupler
NEW["RLY1"]= (130, 125, 0)  # relay 30x13mm

# ============================================================
# Apply all positions
# ============================================================

for ref, pos in NEW.items():
    new_x, new_y = pos[0], pos[1]
    angle = pos[2] if len(pos) == 3 else None

    pattern = rf'(\(property "Reference" "{re.escape(ref)}")'
    ref_match = re.search(pattern, content)
    if not ref_match:
        print(f"  {ref}: NOT FOUND")
        continue

    fp_start = content.rfind("\t(footprint ", 0, ref_match.start())
    if fp_start == -1:
        continue

    region = content[fp_start:ref_match.start()]
    at_match = re.search(r'\(at ([-\d.]+) ([-\d.]+)( [-\d.]+)?\)', region)
    if at_match:
        if angle is not None:
            new_at = f"(at {new_x} {new_y} {angle})"
        elif at_match.group(3):
            new_at = f"(at {new_x} {new_y}{at_match.group(3)})"
        else:
            new_at = f"(at {new_x} {new_y})"

        abs_start = fp_start + at_match.start()
        abs_end = fp_start + at_match.end()
        content = content[:abs_start] + new_at + content[abs_end:]

# ============================================================
# Fix board outline — 175x115mm
# ============================================================
# Remove old
content = re.sub(r'\t\(gr_line \(start[^)]+\)[^\n]*\(layer "(Edge\.Cuts|Dwgs\.User)"\)[^\n]*\)\n', '', content)
content = re.sub(
    r'\t\(gr_line\n(?:\t\t[^\n]+\n)*?\t\t\(layer "(Edge\.Cuts|Dwgs\.User)"\)\n(?:\t\t[^\n]+\n)*?\t\)\n',
    '', content
)

x1, y1 = 22, 22
x2, y2 = 200, 142
outline = f"""\t(gr_line (start {x1} {y1}) (end {x2} {y1}) (stroke (width 0.05) (type solid)) (layer "Edge.Cuts") (uuid "{uuid_mod.uuid4()}"))
\t(gr_line (start {x2} {y1}) (end {x2} {y2}) (stroke (width 0.05) (type solid)) (layer "Edge.Cuts") (uuid "{uuid_mod.uuid4()}"))
\t(gr_line (start {x2} {y2}) (end {x1} {y2}) (stroke (width 0.05) (type solid)) (layer "Edge.Cuts") (uuid "{uuid_mod.uuid4()}"))
\t(gr_line (start {x1} {y2}) (end {x1} {y1}) (stroke (width 0.05) (type solid)) (layer "Edge.Cuts") (uuid "{uuid_mod.uuid4()}"))
"""

last_paren = content.rfind(")")
content = content[:last_paren] + outline + content[last_paren:]

with open(PCB, "w") as f:
    f.write(content)

placed = len([r for r in NEW if r in current])
print(f"Placed {placed}/{len(NEW)} components")
print(f"Board: {x2-x1}x{y2-y1}mm ({x1},{y1})→({x2},{y2})")
missing = [r for r in NEW if r not in current]
if missing:
    print(f"NOT in PCB: {missing}")
