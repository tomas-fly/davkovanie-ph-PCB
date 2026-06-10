#!/usr/bin/env python3
"""Place components on PCB into logical module groups. Simple position update."""

import re
import uuid

PCB_FILE = "/Users/ing.tomaslaso/Documents/kiCad/ph-verzion-01/ph-verzion-01.kicad_pcb"

# ============================================================
# Component sizes (from footprints):
#   U1  HLK-30M12:  60x36mm (origin offset! body extends +55 right, +14 down from center)
#   U11 ESP32:      19x26mm
#   RLY1 Finder:    30x13mm
#   P1/P2 BNC:      36x16mm (at 270°: ~16x36mm tall, extends ~17mm left from center)
#   U6-U9 DIP-8:    12x10mm
#   U2/U4 TO-263:   17x11mm
#   J1/J11 terminal 3-pin: 16x11mm
#   J9/J10/J12 terminal 2-pin: 11x11mm
#   F1 fuse:        13x13mm
#   C29 film cap:   18x5mm
#   C2 elcap 10mm radial, C3 elcap 8mm radial, C7/C9/C10 elcap 6.3mm
#   L1 Bourns SRN1060: 11x11mm
#   J2 1x14 header: 4x37mm
#   J7 2x10 header: 6x26mm
#   0805 SMD:       ~3x2mm
# ============================================================

# Board: 210x140mm, origin (20,20), corners (20,20)→(230,160)
BX, BY = 20, 20
BW, BH = 210, 140

# Placement: ref -> (x, y) or (x, y, angle)
P = {
    # ══════════════════════════════════════════════
    # MODULE 1: AC-DC Power Supply (top-left)
    # U1 body extends from (cx-4.5) to (cx+55.5) in X, (cy-22) to (cy+14) in Y
    # So at (28, 48): body spans x=23..83, y=26..62
    # ══════════════════════════════════════════════
    "U1":   (28, 48),
    "J1":   (32, 70),       # AC input terminal, BELOW U1
    "F1":   (52, 70),       # fuse next to J1
    "MOV1": (70, 70),       # varistor
    "J12":  (32, 84),       # 12V output terminal
    "C1":   (48, 84),       # output bypass cap
    "R1":   (56, 84),       # LED resistor
    "D1":   (62, 84),       # power LED

    # ══════════════════════════════════════════════
    # MODULE 2: Buck Converter 12V→5V (top-center, RIGHT of U1)
    # U1 body ends at x~83, start buck at x=92
    # ══════════════════════════════════════════════
    "C2":   (92, 30),       # input electrolytic 10mm
    "U2":   (108, 30),      # LM2596 TO-263 (17x11mm)
    "C3":   (126, 30),      # output electrolytic 8mm
    "D2":   (100, 44),      # Schottky diode SMC
    "L1":   (114, 44),      # inductor 11mm
    "C5":   (126, 44),      # output ceramic 1206
    "FB1":  (134, 44),      # ferrite bead 0805

    # ══════════════════════════════════════════════
    # MODULE 3: LDO 5V→3.3V (top, right of buck)
    # ══════════════════════════════════════════════
    "U3":   (148, 30),      # AMS1117 SOT-223
    "C4":   (140, 26),      # input cap
    "C6":   (156, 26),      # output cap

    # ══════════════════════════════════════════════
    # MODULE 4: Analog Power (LM7805 + charge pump)
    # ══════════════════════════════════════════════
    "U4":   (108, 58),      # LM7805 TO-263 (analog +5V)
    "C7":   (96, 56),       # input electrolytic
    "C8":   (96, 64),       # bypass
    "C9":   (122, 56),      # output electrolytic
    "C10":  (122, 64),      # output electrolytic pH
    "FB2":  (130, 56),      # ferrite
    "L2":   (130, 64),      # inductor
    # TPS60400 charge pump (-5V)
    "U5":   (108, 72),      # SOT-23-5
    "C11":  (98, 72),       # input
    "C12":  (118, 72),      # output
    "FB1":  (134, 44),      # (already placed above)

    # ══════════════════════════════════════════════
    # MODULE 5: ESP32 (center-left, below power)
    # ESP32 is 19x26mm
    # ══════════════════════════════════════════════
    "U11":  (92, 100),      # ESP32
    "C27":  (80, 90),       # bypass caps
    "C28":  (80, 96),
    "R18":  (80, 102),      # pull resistors
    "C26":  (80, 108),
    "R19":  (108, 90),
    "R16":  (108, 96),
    "R17":  (108, 102),
    "J8":   (108, 110),     # UART header
    # ADS1115 ADC (near ESP32)
    "U10":  (122, 90),      # MSOP-10
    "C25":  (122, 84),
    "R31":  (130, 90),

    # ══════════════════════════════════════════════
    # MODULE 6: pH Analog Frontend (right side, top)
    # BNC at 270° extends ~17mm LEFT from center, ~18mm up/down
    # P1 at x=222: body spans x=205..222, y=24..60
    # ══════════════════════════════════════════════
    "P1":   (224, 42, 270), # BNC RIGHT edge
    "U6":   (180, 30),      # CA3140 DIP-8 (12x10mm)
    "U7":   (180, 46),      # TL071 DIP-8
    "C13":  (170, 28),      # caps
    "C14":  (170, 34),
    "C15":  (170, 40),
    "C16":  (170, 46),
    "C17":  (170, 52),
    "R2":   (196, 28),      # resistors near BNC
    "R3":   (196, 32),
    "R4":   (196, 40),      # trimpot (6mm)
    "R5":   (196, 48),
    "R6":   (200, 28),
    "R7":   (200, 34),
    "R8":   (200, 40),
    "C29":  (180, 58),      # large film cap 18x5mm

    # ══════════════════════════════════════════════
    # MODULE 7: ORP Analog Frontend (right side, bottom)
    # P2 at x=224: body like P1 but shifted down
    # ══════════════════════════════════════════════
    "P2":   (224, 90, 270), # BNC RIGHT edge
    "U8":   (180, 78),      # CA3140 DIP-8
    "U9":   (180, 94),      # TL071 DIP-8
    "C18":  (170, 76),
    "C19":  (170, 82),
    "C20":  (170, 88),
    "C21":  (170, 94),
    "C22":  (170, 100),
    "R9":   (196, 76),
    "R10":  (196, 80),
    "R11":  (196, 88),      # trimpot
    "R12":  (196, 96),
    "R13":  (200, 76),
    "R14":  (200, 82),
    "R15":  (200, 88),
    "C23":  (204, 76),
    "C24":  (204, 82),

    # ══════════════════════════════════════════════
    # MODULE 8: Peripheral Connectors (left side, bottom)
    # ══════════════════════════════════════════════
    "J3":   (30, 98),       # JST 3-pin (8x7mm each)
    "J4":   (30, 108),
    "J5":   (30, 118),
    "J6":   (30, 128),
    "J2":   (48, 100),      # display header 1x14 (4x37mm)
    "J7":   (58, 100),      # GPIO 2x10 header (6x26mm)

    # ══════════════════════════════════════════════
    # MODULE 9: MOSFET Outputs & Relay (bottom center)
    # ══════════════════════════════════════════════
    "Q1":   (80, 124),      # TO-252 MOSFETs
    "Q2":   (94, 124),
    "Q3":   (108, 124),
    "Q4":   (122, 124),
    "R20":  (78, 132),      # gate/pulldown resistors
    "R21":  (82, 132),
    "R22":  (92, 132),
    "R23":  (96, 132),
    "R24":  (106, 132),
    "R25":  (110, 132),
    "R26":  (120, 132),
    "R27":  (124, 132),
    "R28":  (132, 132),
    "R29":  (136, 132),
    "R30":  (142, 132),
    "D3":   (80, 138),      # flyback diodes
    "D4":   (94, 138),
    "D5":   (108, 138),
    "D6":   (122, 138),
    "D7":   (134, 138),
    "J9":   (80, 148),      # output terminals
    "J10":  (98, 148),
    "J11":  (118, 148),     # AC output 3-pin
    "RLY1": (148, 140),     # Finder relay 30x13mm
    "U12":  (136, 124),     # optocoupler SOP-4
}


def main():
    with open(PCB_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")

    # --- Find footprint blocks and update positions ---
    fp_start_re = re.compile(r'^\t\(footprint "')
    at_re = re.compile(r'^(\s*\(at\s+)[\d.\-]+\s+[\d.\-]+(\s+[\d.\-]+)?(\).*)$')
    ref_re = re.compile(r'\(property "Reference" "([^"]+)"')

    fp_blocks = []
    i = 0
    while i < len(lines):
        if fp_start_re.match(lines[i]):
            start = i
            j = i + 1
            while j < len(lines):
                if fp_start_re.match(lines[j]):
                    break
                if lines[j].strip() == ")" and lines[j].startswith("\t") and not lines[j].startswith("\t\t"):
                    j += 1
                    break
                j += 1
            fp_blocks.append((start, j))
            i = j
        else:
            i += 1

    placed = 0
    found = set()
    for block_start, block_end in fp_blocks:
        ref = None
        for li in range(block_start, min(block_end, len(lines))):
            m = ref_re.search(lines[li])
            if m:
                ref = m.group(1)
                break
        if ref is None or ref not in P:
            continue

        found.add(ref)
        placement = P[ref]
        new_x, new_y = placement[0], placement[1]
        explicit_angle = placement[2] if len(placement) == 3 else None

        for li in range(block_start, min(block_start + 6, block_end)):
            m = at_re.match(lines[li])
            if m:
                prefix = m.group(1)
                old_angle = m.group(2)
                suffix = m.group(3)
                if explicit_angle is not None:
                    angle_str = f" {explicit_angle}"
                elif old_angle is not None:
                    angle_str = old_angle
                else:
                    angle_str = ""
                lines[li] = f"{prefix}{new_x} {new_y}{angle_str}{suffix}"
                placed += 1
                break

    # --- Remove existing Edge.Cuts ---
    edge_re = re.compile(r'^\s*\(gr_line\s.*\(layer "Edge\.Cuts"\).*\)$')
    dwgs_re = re.compile(r'^\s*\(gr_line\s.*\(layer "Dwgs\.User"\).*\)$')
    lines = [l for l in lines if not edge_re.match(l) and not dwgs_re.match(l)]

    # --- Add board outline ---
    x1, y1 = BX, BY
    x2, y2 = BX + BW, BY + BH
    edge_lines = [
        f'\t(gr_line (start {x1} {y1}) (end {x2} {y1}) (stroke (width 0.05) (type solid)) (layer "Edge.Cuts") (uuid "{uuid.uuid4()}"))',
        f'\t(gr_line (start {x2} {y1}) (end {x2} {y2}) (stroke (width 0.05) (type solid)) (layer "Edge.Cuts") (uuid "{uuid.uuid4()}"))',
        f'\t(gr_line (start {x2} {y2}) (end {x1} {y2}) (stroke (width 0.05) (type solid)) (layer "Edge.Cuts") (uuid "{uuid.uuid4()}"))',
        f'\t(gr_line (start {x1} {y2}) (end {x1} {y1}) (stroke (width 0.05) (type solid)) (layer "Edge.Cuts") (uuid "{uuid.uuid4()}"))',
    ]

    insert_idx = len(lines) - 1
    while insert_idx >= 0 and lines[insert_idx].strip() != ")":
        insert_idx -= 1
    if insert_idx >= 0:
        for j, el in enumerate(edge_lines):
            lines.insert(insert_idx + j, el)

    with open(PCB_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    missing = [r for r in P if r not in found]
    print(f"Placed: {placed} / {len(P)}")
    if missing:
        print(f"NOT found in PCB: {missing}")
    else:
        print("All references found.")
    print(f"Board outline: {BW}x{BH}mm at ({x1},{y1})→({x2},{y2})")


if __name__ == "__main__":
    main()
