#!/usr/bin/env python3
"""
PCB Component Placement Script for pH/ORP Monitor Board
========================================================
Reads ph-verzion-01.kicad_pcb, updates component positions,
writes result to ph-verzion-01.kicad_pcb (overwrites).

Board size: ~130 x 90 mm (2-layer, fits Hammond 1554 box ~150x100mm)
Origin: top-left corner at (30, 30) mm

Layout zones (left to right):
  ZONE 1 (x=30-60):  230V HIGH VOLTAGE — AC input, fuse, PSU, relay, AC output
  ZONE 2 (x=62-90):  POWER — buck, LDO, analog regulators
  ZONE 3 (x=62-90):  DIGITAL — ESP32, ADC
  ZONE 4 (x=92-155): ANALOG FRONT-END — pH + ORP signal chains
  CONNECTORS:         Edges of board

6mm clearance between HV zone and LV zones.
AGND star-point near ADC.
"""

import re
import sys
import os

PCB_FILE = os.path.join(os.path.dirname(__file__), "ph-verzion-01.kicad_pcb")

# ============================================================
# COMPONENT PLACEMENT TABLE
# Format: "REF": (x_mm, y_mm, rotation_deg)
# Origin approx top-left of board area
# Board area: x=30..160, y=30..120 (130x90mm)
# ============================================================

# --- Board geometry ---
BX = 30   # board origin X
BY = 30   # board origin Y
BW = 135  # board width
BH = 90   # board height

PLACEMENT = {}

# ============================================================
# ZONE 1: 230V HIGH VOLTAGE (left side, x=30..58)
# Isolated from rest by 6mm gap
# ============================================================

# AC input connector — top-left edge
PLACEMENT["J1"]   = (BX + 5,  BY + 10, 0)       # 3-pin terminal block, AC in

# Fuse
PLACEMENT["F1"]   = (BX + 5,  BY + 22, 0)       # Fuse holder 5x20mm

# HLK-30M12 AC-DC converter (large module ~50x30mm area)
PLACEMENT["U1"]   = (BX + 15, BY + 40, 0)       # HLK-30M12

# C1: 100nF bypass on PSU output
PLACEMENT["C1"]   = (BX + 15, BY + 55, 0)

# LED power indicator
PLACEMENT["D1"]   = (BX + 5,  BY + 55, 0)       # LED blue
PLACEMENT["R1"]   = (BX + 5,  BY + 58, 0)       # 1k LED resistor

# Relay section (bottom of HV zone)
PLACEMENT["RLY1"] = (BX + 15, BY + 68, 0)       # Finder 40.52 relay (large)

# Relay drive components
PLACEMENT["U12"]  = (BX + 5,  BY + 65, 0)       # LTV-356T optocoupler
PLACEMENT["R28"]  = (BX + 5,  BY + 68, 0)       # 330R opto input
PLACEMENT["R29"]  = (BX + 5,  BY + 71, 0)       # 1k opto output

# Relay protection
PLACEMENT["D7"]   = (BX + 8,  BY + 75, 0)       # M7 flyback diode
PLACEMENT["R30"]  = (BX + 12, BY + 80, 0)       # 100R snubber
PLACEMENT["C29"]  = (BX + 18, BY + 80, 0)       # 100nF X2 snubber
PLACEMENT["MOV1"] = (BX + 24, BY + 80, 0)       # Varistor

# AC output connector — bottom-left edge
PLACEMENT["J11"]  = (BX + 5,  BY + 85, 0)       # 3-pin terminal block, AC out

# ============================================================
# ZONE 2: POWER SUPPLY (center-left, x=62..92)
# ============================================================

# --- Buck 12V → 5V ---
PLACEMENT["U2"]   = (BX + 38, BY + 8,  0)       # LM2596S TO-263-5
PLACEMENT["C2"]   = (BX + 32, BY + 8,  0)       # 680µF input cap
PLACEMENT["C3"]   = (BX + 44, BY + 15, 0)       # 220µF output cap
PLACEMENT["L1"]   = (BX + 44, BY + 8,  0)       # 33µH inductor (Bourns SRN1060)
PLACEMENT["D2"]   = (BX + 38, BY + 15, 0)       # SS34 Schottky SMC

# --- LDO 5V → 3.3V ---
PLACEMENT["U3"]   = (BX + 38, BY + 24, 0)       # LD1117 SOT-223
PLACEMENT["C4"]   = (BX + 34, BY + 28, 0)       # 10µF LDO in
PLACEMENT["C10"]  = (BX + 42, BY + 28, 0)       # 22µF LDO out (THT)

# --- Analog power 12V → +5V_AN ---
PLACEMENT["U4"]   = (BX + 38, BY + 38, 0)       # L7805ABD2T D2PAK
PLACEMENT["C6"]   = (BX + 32, BY + 38, 0)       # 100nF in
PLACEMENT["C7"]   = (BX + 32, BY + 42, 0)       # 10µF in
PLACEMENT["C8"]   = (BX + 44, BY + 38, 0)       # 100nF out
PLACEMENT["C9"]   = (BX + 44, BY + 42, 0)       # 10µF out
PLACEMENT["FB1"]  = (BX + 48, BY + 40, 0)       # Ferrite bead +5V_AN
PLACEMENT["L2"]   = (BX + 48, BY + 44, 0)       # LC filter inductor

# --- Charge pump +5V_AN → -5V_AN ---
PLACEMENT["U5"]   = (BX + 38, BY + 50, 0)       # TPS60400 SOT-23-5
PLACEMENT["C11"]  = (BX + 34, BY + 52, 0)       # 1µF flying cap
PLACEMENT["C12"]  = (BX + 42, BY + 52, 0)       # 10µF output cap
PLACEMENT["FB2"]  = (BX + 48, BY + 52, 0)       # Ferrite bead -5V_AN

# ============================================================
# ZONE 3: DIGITAL (center, x=62..92, y=55..90)
# ============================================================

# ESP32 module (large, ~18x25mm)
PLACEMENT["U11"]  = (BX + 55, BY + 68, 0)       # ESP32-WROOM-32E
PLACEMENT["C27"]  = (BX + 50, BY + 60, 0)       # 100nF ESP32 bypass
PLACEMENT["C28"]  = (BX + 53, BY + 60, 0)       # 10µF ESP32 bypass
PLACEMENT["R18"]  = (BX + 50, BY + 63, 0)       # 10k EN pull-up
PLACEMENT["C26"]  = (BX + 53, BY + 63, 0)       # 100nF EN cap
PLACEMENT["R19"]  = (BX + 50, BY + 66, 0)       # 10k IO0 pull-up

# ADS1115 ADC (between ESP32 and analog section)
PLACEMENT["U10"]  = (BX + 75, BY + 52, 0)       # ADS1115 MSOP-10
PLACEMENT["C25"]  = (BX + 75, BY + 48, 0)       # 100nF ADC bypass
PLACEMENT["R16"]  = (BX + 80, BY + 48, 0)       # 4.7k SDA pull-up
PLACEMENT["R17"]  = (BX + 80, BY + 52, 0)       # 4.7k SCL pull-up

# ============================================================
# ZONE 4: pH ANALOG FRONT-END (right side, x=92..155, top half)
# ============================================================

# BNC pH input — right edge
PLACEMENT["P1"]   = (BX + 120, BY + 10, 0)      # BNC connector

# pH Buffer (CA3140EZ) — DIP-8
PLACEMENT["U6"]   = (BX + 100, BY + 10, 0)      # CA3140 buffer
PLACEMENT["R2"]   = (BX + 112, BY + 8,  0)      # 4.7M input R
PLACEMENT["C13"]  = (BX + 112, BY + 12, 0)      # 2.2nF input filter
PLACEMENT["C14"]  = (BX + 95,  BY + 6,  0)      # 100nF V+ bypass
PLACEMENT["C15"]  = (BX + 95,  BY + 14, 0)      # 100nF V- bypass
PLACEMENT["R3"]   = (BX + 95,  BY + 18, 0)      # 2.2k feedback
PLACEMENT["R4"]   = (BX + 99,  BY + 18, 0)      # 5k trimer
PLACEMENT["R5"]   = (BX + 103, BY + 18, 0)      # 1k bias
PLACEMENT["C16"]  = (BX + 107, BY + 18, 0)      # 1µF feedback cap

# pH Amplifier (TL071IP) — DIP-8
PLACEMENT["U7"]   = (BX + 85,  BY + 10, 0)      # TL071 amplifier
PLACEMENT["C17"]  = (BX + 80,  BY + 6,  0)      # 100nF V+ bypass
PLACEMENT["C18"]  = (BX + 80,  BY + 14, 0)      # 100nF V- bypass
PLACEMENT["R6"]   = (BX + 80,  BY + 18, 0)      # 30k input R
PLACEMENT["R7"]   = (BX + 84,  BY + 18, 0)      # 30k feedback R
PLACEMENT["R8"]   = (BX + 88,  BY + 18, 0)      # 75k offset R

# ============================================================
# ZONE 5: ORP ANALOG FRONT-END (right side, x=92..155, bottom half)
# Mirror of pH, shifted down by ~28mm
# ============================================================

DY_ORP = 30  # vertical offset from pH

# BNC ORP input — right edge
PLACEMENT["P2"]   = (BX + 120, BY + 10 + DY_ORP, 0)   # BNC connector

# ORP Buffer (CA3140EZ) — DIP-8
PLACEMENT["U8"]   = (BX + 100, BY + 10 + DY_ORP, 0)   # CA3140 buffer
PLACEMENT["R9"]   = (BX + 112, BY + 8  + DY_ORP, 0)   # 4.7M input R
PLACEMENT["C19"]  = (BX + 112, BY + 12 + DY_ORP, 0)   # 2.2nF input filter
PLACEMENT["C20"]  = (BX + 95,  BY + 6  + DY_ORP, 0)   # 100nF V+ bypass
PLACEMENT["C21"]  = (BX + 95,  BY + 14 + DY_ORP, 0)   # 100nF V- bypass
PLACEMENT["R10"]  = (BX + 95,  BY + 18 + DY_ORP, 0)   # 2.2k feedback
PLACEMENT["R11"]  = (BX + 99,  BY + 18 + DY_ORP, 0)   # 5k trimer
PLACEMENT["R12"]  = (BX + 103, BY + 18 + DY_ORP, 0)   # 1k bias
PLACEMENT["C22"]  = (BX + 107, BY + 18 + DY_ORP, 0)   # 1µF feedback cap

# ORP Amplifier (TL071IP) — DIP-8
PLACEMENT["U9"]   = (BX + 85,  BY + 10 + DY_ORP, 0)   # TL071 amplifier
PLACEMENT["C23"]  = (BX + 80,  BY + 6  + DY_ORP, 0)   # 100nF V+ bypass
PLACEMENT["C24"]  = (BX + 80,  BY + 14 + DY_ORP, 0)   # 100nF V- bypass
PLACEMENT["R13"]  = (BX + 80,  BY + 18 + DY_ORP, 0)   # 30k input R
PLACEMENT["R14"]  = (BX + 84,  BY + 18 + DY_ORP, 0)   # 30k feedback R
PLACEMENT["R15"]  = (BX + 88,  BY + 18 + DY_ORP, 0)   # 75k offset R

# ============================================================
# MOSFET OUTPUTS (bottom-center, x=62..92)
# ============================================================

# Q1 — Pump MOSFET
PLACEMENT["Q1"]   = (BX + 38, BY + 62, 0)
PLACEMENT["R20"]  = (BX + 34, BY + 62, 0)       # 100R gate
PLACEMENT["R24"]  = (BX + 34, BY + 65, 0)       # 10k pull-down
PLACEMENT["D3"]   = (BX + 42, BY + 62, 0)       # SS14 flyback

# Q2 — Relay coil MOSFET (driven by opto)
PLACEMENT["Q2"]   = (BX + 38, BY + 72, 0)
PLACEMENT["R21"]  = (BX + 34, BY + 72, 0)       # 100R gate
PLACEMENT["R25"]  = (BX + 34, BY + 75, 0)       # 10k pull-down
PLACEMENT["D4"]   = (BX + 42, BY + 72, 0)       # SS14 flyback

# Q3 — External MOSFET 3
PLACEMENT["Q3"]   = (BX + 55, BY + 85, 0)
PLACEMENT["R22"]  = (BX + 51, BY + 85, 0)       # 100R gate
PLACEMENT["R26"]  = (BX + 51, BY + 88, 0)       # 10k pull-down
PLACEMENT["D5"]   = (BX + 59, BY + 85, 0)       # SS14 flyback
PLACEMENT["J3"]   = (BX + 65, BY + 85, 0)       # 2-pin terminal block

# Q4 — External MOSFET 4
PLACEMENT["Q4"]   = (BX + 75, BY + 85, 0)
PLACEMENT["R23"]  = (BX + 71, BY + 85, 0)       # 100R gate
PLACEMENT["R27"]  = (BX + 71, BY + 88, 0)       # 10k pull-down
PLACEMENT["D6"]   = (BX + 79, BY + 85, 0)       # SS14 flyback
PLACEMENT["J4"]   = (BX + 85, BY + 85, 0)       # 2-pin terminal block

# ============================================================
# CONNECTORS (board edges)
# ============================================================

# Display connector (14-pin header) — top edge
PLACEMENT["J6"]   = (BX + 75, BY + 3, 0)        # 1x14 pin header

# 1-Wire connectors (4× JST-XH 3-pin) — bottom edge
PLACEMENT["J2"]   = (BX + 90,  BY + 85, 0)      # 1-Wire #1
PLACEMENT["J5"]   = (BX + 98,  BY + 85, 0)      # 1-Wire #2
PLACEMENT["J9"]   = (BX + 106, BY + 85, 0)      # 1-Wire #3
PLACEMENT["J10"]  = (BX + 114, BY + 85, 0)      # 1-Wire #4
PLACEMENT["R31"]  = (BX + 90,  BY + 82, 0)      # 4.7k 1-Wire pull-up

# GPIO extension header (2x10) — bottom-right
PLACEMENT["J7"]   = (BX + 125, BY + 75, 0)      # 2x10 pin header

# UART debug header (1x4) — bottom edge
PLACEMENT["J8"]   = (BX + 125, BY + 85, 0)      # 1x4 pin header

# Extra 100nF cap (C5) — near analog section
PLACEMENT["C5"]   = (BX + 48, BY + 48, 0)


# ============================================================
# MAIN: Parse and update PCB file
# ============================================================

def parse_and_update(pcb_path):
    with open(pcb_path, "r") as f:
        content = f.read()

    # Find all footprint blocks and update positions
    updated = 0
    skipped = []

    for ref, (x, y, rot) in PLACEMENT.items():
        # Pattern to find the footprint block for this reference
        # We look for (property "Reference" "REF") inside a (footprint ...) block
        # and update the (at X Y [angle]) right after the footprint line

        # First find the reference property to locate which footprint block
        ref_pattern = rf'(\(property "Reference" "{re.escape(ref)}")'
        ref_matches = list(re.finditer(ref_pattern, content))

        if not ref_matches:
            skipped.append(ref)
            continue

        # For each match, find the enclosing footprint block's (at ...) line
        for ref_match in ref_matches:
            pos = ref_match.start()

            # Search backwards to find the footprint line
            # Find the last "(footprint " before this position
            fp_start = content.rfind("\t(footprint ", 0, pos)
            if fp_start == -1:
                continue

            # Find the (at X Y [angle]) within this footprint block
            # It should be right after the first line
            at_pattern = r'\(at ([-\d.]+) ([-\d.]+)( [-\d.]+)?\)'
            # Search from footprint start to reference position
            search_region = content[fp_start:pos]
            at_match = re.search(at_pattern, search_region)
            if at_match:
                old_at = at_match.group(0)
                if rot != 0:
                    new_at = f"(at {x} {y} {rot})"
                else:
                    new_at = f"(at {x} {y})"
                # Replace only this specific occurrence
                abs_start = fp_start + at_match.start()
                abs_end = fp_start + at_match.end()
                content = content[:abs_start] + new_at + content[abs_end:]
                updated += 1
                break

    # Add board outline on Edge.Cuts layer
    # Remove existing edge cuts lines first
    content = re.sub(r'\t\(gr_line \(start [^)]+\) \(end [^)]+\).*?\(layer "Edge\.Cuts"\).*?\)\n', '', content)
    content = re.sub(r'\t\(gr_rect \(start [^)]+\) \(end [^)]+\).*?\(layer "Edge\.Cuts"\).*?\)\n', '', content)

    # Add board outline rectangle before the closing parenthesis
    x1, y1 = BX, BY
    x2, y2 = BX + BW, BY + BH
    corner_r = 3  # 3mm corner radius

    board_outline = f"""
\t(gr_line (start {x1} {y1}) (end {x2} {y1})
\t\t(stroke (width 0.1) (type default)) (layer "Edge.Cuts") (uuid "b0a00001-0000-0000-0000-000000000001"))
\t(gr_line (start {x2} {y1}) (end {x2} {y2})
\t\t(stroke (width 0.1) (type default)) (layer "Edge.Cuts") (uuid "b0a00002-0000-0000-0000-000000000002"))
\t(gr_line (start {x2} {y2}) (end {x1} {y2})
\t\t(stroke (width 0.1) (type default)) (layer "Edge.Cuts") (uuid "b0a00003-0000-0000-0000-000000000003"))
\t(gr_line (start {x1} {y2}) (end {x1} {y1})
\t\t(stroke (width 0.1) (type default)) (layer "Edge.Cuts") (uuid "b0a00004-0000-0000-0000-000000000004"))
"""

    # Add isolation line between HV and LV zones (on User.Drawings for reference)
    hv_boundary_x = BX + 30  # 30mm from left = HV zone boundary
    isolation_line = f"""
\t(gr_line (start {hv_boundary_x} {y1}) (end {hv_boundary_x} {y2})
\t\t(stroke (width 0.3) (type dash)) (layer "Dwgs.User") (uuid "b0a00005-0000-0000-0000-000000000005"))
"""

    # Insert before the last closing paren
    last_paren = content.rfind(")")
    content = content[:last_paren] + board_outline + isolation_line + content[last_paren:]

    with open(pcb_path, "w") as f:
        f.write(content)

    print(f"Updated {updated} component positions")
    if skipped:
        print(f"Skipped (not found in PCB): {skipped}")
    print(f"Board outline: {BW}x{BH}mm at ({BX},{BY})")
    print(f"HV isolation line at x={BX + 30}mm")


if __name__ == "__main__":
    parse_and_update(PCB_FILE)
