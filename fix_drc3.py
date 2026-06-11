#!/usr/bin/env python3
"""Fix MOSFET zone spacing + J6/J2 overlap."""
import re

PCB = "/Users/ing.tomaslaso/Documents/kiCad/ph-verzion-01/ph-verzion-01.kicad_pcb"

with open(PCB, "r") as f:
    content = f.read()

# R20-R31 at y=142 overlap D3-D7 at y=142
# Fix: move D3-D7 down to y=148 (6mm gap), R20-R31 stay at y=142
# Also spread R20-R31 more: each MOSFET pair (Rgate+Rpulldown) needs 6mm spacing
# Q1-Q4 at y=134, R pairs below at y=142, D below at y=148, terminals at y=155

# J6 at (28,140) overlaps J2 at (28,118) — J2 is 33mm tall → extends to y=151!
# Fix: move J6 far away from J2

FIXES = {
    # Diodes — move DOWN from y=142 to y=149
    "D3":  (80, 149),
    "D4":  (94, 149),
    "D5":  (108, 149),
    "D6":  (122, 149),
    "D7":  (134, 149),

    # Resistors — spread out so each pair has 6mm between them
    # Currently R20/R21 at (78,142)/(82,142) — that's 4mm, fine for 0805
    # But they overlap with D3 at (80,142)! D3 is SMA = 5.4x2.6mm
    # R20 pad at 77-79, D3 pad at 78-82 — OVERLAP
    # Fix: shift R pairs to be exactly BETWEEN their MOSFET and diode
    "R20": (76, 140),   # Q1 gate resistors
    "R21": (76, 143),
    "R22": (90, 140),   # Q2 gate resistors
    "R23": (90, 143),
    "R24": (104, 140),  # Q3 gate resistors
    "R25": (104, 143),
    "R26": (118, 140),  # Q4 gate resistors
    "R27": (118, 143),
    "R28": (132, 140),  # relay/extra resistors
    "R29": (132, 143),
    "R30": (140, 140),

    # J6 at (28,140) — J2 extends from y=118 to y=151, so J6 overlaps
    # Move J6 to left-bottom area, below J5
    "J6":  (28, 155),

    # Also J3-J5 — check they don't overlap J2 either
    # J2 at (28,118,0): pins from y=118 to y=151
    # J3 at (30,98): should be fine (above J2)
    # J5 at (30,118): overlaps J2 start!
    "J3":  (30, 92),
    "J4":  (30, 100),
    "J5":  (30, 108),
}

for ref, pos in FIXES.items():
    new_x, new_y = pos[0], pos[1]
    explicit_angle = pos[2] if len(pos) == 3 else None

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
        old_at = at_match.group(0)
        if explicit_angle is not None:
            new_at = f"(at {new_x} {new_y} {explicit_angle})"
        elif at_match.group(3):
            new_at = f"(at {new_x} {new_y}{at_match.group(3)})"
        else:
            new_at = f"(at {new_x} {new_y})"

        abs_start = fp_start + at_match.start()
        abs_end = fp_start + at_match.end()
        content = content[:abs_start] + new_at + content[abs_end:]
        print(f"  {ref}: {old_at} → {new_at}")

with open(PCB, "w") as f:
    f.write(content)

print("\nDone. Revert in KiCad and re-run DRC.")
