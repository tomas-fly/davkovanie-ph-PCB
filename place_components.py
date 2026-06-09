#!/usr/bin/env python3
"""
Place components in KiCad PCB file into logical module groups.
Modifies footprint (at X Y [angle]) coordinates and adds Edge.Cuts board outline.
"""

import re
import uuid

PCB_PATH = "/Users/ing.tomaslaso/Documents/kiCad/ph-verzion-01/ktualizacia dosky - doplnenie 12v do pcb/ph-verzion-01.kicad_pcb"

# Component placement dictionary: reference -> (x, y) or (x, y, angle)
# Board: 190x120mm, corners (25,25) to (215,145)
#
# Layout (top to bottom, left to right):
#   Top-left:     AC-DC Power (U1 = 51x24mm, needs big space!)
#   Top-center:   Buck 12V->5V
#   Top-right:    LDO 3.3V
#   Center-left:  Peripheral connectors
#   Center:       ESP32 module
#   Center-right: ADC
#   Right edge:   pH frontend (top) + ORP frontend (bottom), BNC on edge
#   Bottom:       MOSFET outputs + Relay
#
PLACEMENTS = {
    # ── Module 1: AC-DC Power Supply ──
    # U1 (HLK-30M12) is ~51x24mm. Place at top-left, isolated.
    # Input components (J1, F1, MOV1) LEFT of U1, output (J12, C1) RIGHT of U1
    "U1": (52, 40),        # center of big module, body ~27-77 x, ~28-52 y
    "J1": (30, 62),        # AC input terminal, BELOW U1 on left edge
    "F1": (30, 72),        # fuse below J1
    "MOV1": (44, 62),      # varistor next to J1
    "J12": (62, 62),       # 12V output terminal, below U1 right side
    "C1": (72, 62),        # output filter cap
    "R1": (56, 72),        # LED resistor
    "D1": (60, 72),        # power LED

    # ── Module 2: Buck Converter 12V→5V ──
    # Right of U1, top area
    "U2": (100, 35),       # LM2596 buck IC (TO-263-5)
    "L1": (100, 48),       # 10mm inductor below U2
    "D2": (90, 48),        # Schottky flyback diode
    "C2": (88, 33),        # input electrolytic (10mm radial)
    "C3": (112, 33),       # output electrolytic (8mm radial)
    "C5": (112, 42),       # output ceramic 1206
    "FB1": (112, 48),      # output ferrite bead

    # ── Module 3: LDO 5V→3.3V ──
    # Right of buck, top area
    "U3": (130, 35),       # AMS1117 (SOT-223)
    "C4": (124, 30),       # input cap
    "C6": (136, 30),       # output cap

    # ── Module 4: ESP32 Module ──
    # Center of board
    "U11": (85, 90),       # ESP32-WROOM-32E (18x25.5mm), center
    "C7": (72, 78),        # bypass cap
    "C8": (72, 82),        # bypass cap
    "C9": (72, 105),       # bypass cap bottom
    "R16": (100, 78),      # pull-up/down resistors right of ESP
    "R17": (100, 81),
    "R18": (100, 84),
    "R19": (100, 87),
    "J8": (100, 74),       # debug/programming header
    "J2": (68, 90, 0),     # expansion header, left of ESP32

    # ── Module 5: pH Analog Frontend ──
    # Right side of board, top half. BNC on right edge.
    # Keep analog section away from digital (ESP32) and power (MOSFET)
    "P1": (208, 52, 270),  # BNC on RIGHT edge, pointing outward
    "U6": (155, 35),       # pH buffer op-amp (DIP-8, ~10mm wide)
    "U7": (155, 50),       # pH gain stage (DIP-8)
    "R2": (145, 32),       # resistors column
    "R3": (145, 35),
    "R4": (168, 42),       # pH cal trim pot (Bourns 3214W ~5mm)
    "R5": (145, 38),
    "R6": (145, 41),
    "R7": (145, 44),
    "R8": (145, 47),
    "C10": (172, 32),      # decoupling caps (6.3mm radial)
    "C11": (178, 32),      # 0805 caps
    "C12": (178, 35),
    "C13": (178, 38),
    "C14": (178, 41),
    "C15": (182, 32),
    "C16": (182, 35),
    "C17": (182, 38),
    "C29": (160, 60),      # large film cap 18mm

    # ── Module 6: ORP Analog Frontend ──
    # Right side, bottom half. BNC on right edge.
    "P2": (208, 92, 270),  # BNC on RIGHT edge
    "U8": (155, 75),       # ORP buffer op-amp (DIP-8)
    "U9": (155, 90),       # ORP gain stage (DIP-8)
    "R9": (145, 72),
    "R10": (145, 75),
    "R11": (168, 82),      # ORP cal trim pot
    "R12": (145, 78),
    "R13": (145, 81),
    "R14": (145, 84),
    "R15": (145, 87),
    "L2": (172, 72),       # 0805 inductor
    "FB2": (172, 75),      # 0805 ferrite
    "C18": (178, 72),
    "C19": (178, 75),
    "C20": (178, 78),
    "C21": (178, 81),
    "C22": (182, 72),
    "C23": (182, 75),
    "C24": (182, 78),
    "C25": (182, 81),
    "C26": (186, 72),
    "C27": (186, 75),
    "C28": (186, 78),

    # ── Module 7: ADC ──
    # Between ESP32 and analog frontends
    "U4": (125, 65),       # ADC (TO-263-2)
    "U5": (118, 70),       # voltage reference (SOT-23-5)
    "U10": (125, 55),      # ADC (MSOP-10)

    # ── Module 8: Peripheral Connectors ──
    # Left side, below power section
    "J3": (32, 82),        # JST 3-pin connectors
    "J4": (32, 90),
    "J5": (32, 98),
    "J6": (32, 106),
    "J7": (48, 92),        # 2x10 pin header (expansion)

    # ── Module 9: MOSFET Outputs & Relay ──
    # Bottom of board, spread across width
    "Q1": (72, 118),       # MOSFET (TO-252)
    "Q2": (84, 118),
    "Q3": (96, 118),
    "Q4": (108, 118),
    "R20": (72, 124),      # gate resistors
    "R21": (72, 127),
    "R22": (84, 124),
    "R23": (84, 127),
    "R24": (96, 124),
    "R25": (96, 127),
    "R26": (108, 124),
    "R27": (108, 127),
    "R28": (118, 124),
    "R29": (118, 127),
    "R30": (128, 124),
    "R31": (128, 127),
    "D3": (75, 131),       # flyback diodes
    "D4": (87, 131),
    "D5": (99, 131),
    "D6": (111, 131),
    "D7": (121, 131),
    "J9": (75, 138),       # output terminals
    "J10": (93, 138),
    "J11": (112, 138),
    "RLY1": (140, 130),    # relay (29x13mm) — far right of MOSFET area
    "U12": (120, 118),     # optocoupler near relay
}


def main():
    with open(PCB_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")

    # --- Step 1: Find footprint blocks and update positions ---
    # We identify footprint blocks by finding lines that start with \t(footprint "
    # Then within each block, find the reference and the (at ...) line

    placed_count = 0
    not_found_refs = []
    found_refs = set()

    # Pattern to match footprint block start
    fp_start_re = re.compile(r'^\t\(footprint "')
    # Pattern to match (at X Y) or (at X Y angle)
    at_re = re.compile(r'^(\s*\(at\s+)[\d.\-]+\s+[\d.\-]+(\s+[\d.\-]+)?(\).*)$')
    # Pattern to match reference property
    ref_re = re.compile(r'\(property "Reference" "([^"]+)"')

    # First pass: identify footprint block ranges (start_line, end_line)
    fp_blocks = []
    i = 0
    while i < len(lines):
        if fp_start_re.match(lines[i]):
            start = i
            # Find the end of this block: next footprint start at same indent level,
            # or a line that starts with \t( but not a continuation
            j = i + 1
            depth = 1  # we're inside the opening (footprint
            while j < len(lines):
                # Count parens to track depth
                line = lines[j]
                if fp_start_re.match(line):
                    # Next footprint block at same level
                    break
                # Check if we've exited the footprint block
                # A footprint block at indent level 1 ends with a line "\t)"
                if line.strip() == ")" and line.startswith("\t") and not line.startswith("\t\t"):
                    j += 1  # include the closing line
                    break
                j += 1
            fp_blocks.append((start, j))
            i = j
        else:
            i += 1

    # Process each footprint block
    for block_start, block_end in fp_blocks:
        # Find reference in this block
        ref = None
        for li in range(block_start, min(block_end, len(lines))):
            m = ref_re.search(lines[li])
            if m:
                ref = m.group(1)
                break

        if ref is None or ref not in PLACEMENTS:
            continue

        found_refs.add(ref)
        placement = PLACEMENTS[ref]
        new_x = placement[0]
        new_y = placement[1]
        explicit_angle = placement[2] if len(placement) == 3 else None

        # Find the (at ...) line within first 5 lines of block
        for li in range(block_start, min(block_start + 6, block_end)):
            m = at_re.match(lines[li])
            if m:
                prefix = m.group(1)       # e.g. "\t\t(at "
                old_angle = m.group(2)     # e.g. " 90" or None
                suffix = m.group(3)        # e.g. ")"

                if explicit_angle is not None:
                    angle_str = f" {explicit_angle}"
                elif old_angle is not None:
                    angle_str = old_angle  # keep existing angle
                else:
                    angle_str = ""

                lines[li] = f"{prefix}{new_x} {new_y}{angle_str}{suffix}"
                placed_count += 1
                break

    # Check which refs from PLACEMENTS were not found
    for ref in PLACEMENTS:
        if ref not in found_refs:
            not_found_refs.append(ref)

    # --- Step 2: Remove existing Edge.Cuts gr_line entries ---
    edge_cuts_re = re.compile(r'^\s*\(gr_line\s.*\(layer "Edge\.Cuts"\).*\)$')
    lines = [l for l in lines if not edge_cuts_re.match(l)]

    # --- Step 3: Add board outline on Edge.Cuts layer ---
    # Board: 190mm x 120mm, corners at (25,25), (215,25), (215,145), (25,145)
    edge_lines = [
        f'\t(gr_line (start 25 25) (end 215 25) (stroke (width 0.05) (type solid)) (layer "Edge.Cuts") (uuid "{uuid.uuid4()}"))',
        f'\t(gr_line (start 215 25) (end 215 145) (stroke (width 0.05) (type solid)) (layer "Edge.Cuts") (uuid "{uuid.uuid4()}"))',
        f'\t(gr_line (start 215 145) (end 25 145) (stroke (width 0.05) (type solid)) (layer "Edge.Cuts") (uuid "{uuid.uuid4()}"))',
        f'\t(gr_line (start 25 145) (end 25 25) (stroke (width 0.05) (type solid)) (layer "Edge.Cuts") (uuid "{uuid.uuid4()}"))',
    ]

    # Insert edge lines before the last closing paren of the file
    # Find the last line that is just ")"
    insert_idx = len(lines) - 1
    while insert_idx >= 0 and lines[insert_idx].strip() != ")":
        insert_idx -= 1

    if insert_idx >= 0:
        for j, el in enumerate(edge_lines):
            lines.insert(insert_idx + j, el)

    # --- Step 4: Write back ---
    with open(PCB_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    # --- Summary ---
    print(f"Components placed: {placed_count} / {len(PLACEMENTS)}")
    if not_found_refs:
        print(f"References NOT found in PCB: {sorted(not_found_refs)}")
    else:
        print("All references found and placed.")
    print(f"Edge.Cuts board outline added (190x120mm, corners 25,25 to 215,145)")


if __name__ == "__main__":
    main()
