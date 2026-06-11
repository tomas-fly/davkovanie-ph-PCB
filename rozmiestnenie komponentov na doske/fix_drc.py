#!/usr/bin/env python3
"""
Fix DRC issues:
1. Separate J2 and J7 (shorting - too close together)
2. Fix board outline (remove all old Edge.Cuts, write clean rectangle)
3. Move components away from board edges (J9,J10,J11,RLY1,P1,P2)
4. Fix courtyard overlaps (C7/U4, D3-D7 vs J9-J11 area)
"""

import re
import uuid

PCB_FILE = "/Users/ing.tomaslaso/Documents/kiCad/ph-verzion-01/ph-verzion-01.kicad_pcb"

# Only move components that have DRC issues
# Format: ref -> (new_x, new_y) or (new_x, new_y, new_angle)
FIXES = {
    # J2 (1x14 pin header, 4x37mm at 90°) and J7 (2x10 header, 6x26mm at 90°)
    # Currently at x=31.48/41.48, y=145, both at 90°
    # They overlap because J2 is ~37mm long (rotated = tall) and J7 is ~26mm long
    # Separate them: J2 stays left, J7 moves right with 12mm gap
    "J2":  (30, 130, 90),    # display header, left side
    "J7":  (48, 130, 90),    # GPIO header, 18mm right of J2

    # R16, R17 were colliding with J7 — move them away
    "R16": (64, 128),
    "R17": (64, 134),

    # J9, J10, J11 at y=155 = ON board edge (board ends at y=165)
    # Terminal blocks are ~11mm tall, so pads at y=155 extend to y~161
    # Need at least 0.5mm from edge at y=165 → move to y=152
    "J9":  (80, 152),
    "J10": (98, 152),
    "J11": (118, 152),

    # RLY1 (30x13mm) at (148,148) — bottom pads at y~155 too close to edge
    "RLY1": (148, 144),

    # P1, P2 BNC at x=224 — GND pads at x=229, board edge at x=230
    # Need 0.5mm clearance → move BNC to x=220
    "P1":  (220, 42, 270),
    "P2":  (220, 90, 270),

    # C7 (6.3mm radial electrolytic) at (96,56) overlaps U4 at (108,58)
    # U4 is TO-263 (17x11mm) — left edge at ~100mm
    # Move C7 left
    "C7":  (90, 56),

    # C2 (10mm radial) at (92,30) overlaps U2 area
    "C2":  (88, 30),

    # D3-D7 at y=148 may overlap with J9-J11 at y=152
    # Move diodes up a bit
    "D3":  (80, 145),
    "D4":  (94, 145),
    "D5":  (108, 145),
    "D6":  (122, 145),
    "D7":  (134, 145),
}


def main():
    with open(PCB_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")

    # --- Update component positions ---
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

    fixed = 0
    for block_start, block_end in fp_blocks:
        ref = None
        for li in range(block_start, min(block_end, len(lines))):
            m = ref_re.search(lines[li])
            if m:
                ref = m.group(1)
                break
        if ref is None or ref not in FIXES:
            continue

        fix = FIXES[ref]
        new_x, new_y = fix[0], fix[1]
        explicit_angle = fix[2] if len(fix) == 3 else None

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
                fixed += 1
                print(f"  Fixed {ref}: -> ({new_x}, {new_y})")
                break

    # --- Fix board outline ---
    # Remove ALL existing Edge.Cuts and Dwgs.User gr_line/gr_rect
    new_lines = []
    for l in lines:
        if re.search(r'gr_(line|rect).*"Edge\.Cuts"', l):
            continue  # skip old edge cuts
        if re.search(r'gr_line.*"Dwgs\.User"', l):
            continue  # skip old drawings user lines
        new_lines.append(l)
    lines = new_lines

    # Add clean board outline: rectangle with generous margins
    # Board: 210x145mm at (20,20) → (230,165)
    x1, y1 = 20, 20
    x2, y2 = 230, 165
    edge_lines = [
        f'\t(gr_line (start {x1} {y1}) (end {x2} {y1}) (stroke (width 0.05) (type solid)) (layer "Edge.Cuts") (uuid "{uuid.uuid4()}"))',
        f'\t(gr_line (start {x2} {y1}) (end {x2} {y2}) (stroke (width 0.05) (type solid)) (layer "Edge.Cuts") (uuid "{uuid.uuid4()}"))',
        f'\t(gr_line (start {x2} {y2}) (end {x1} {y2}) (stroke (width 0.05) (type solid)) (layer "Edge.Cuts") (uuid "{uuid.uuid4()}"))',
        f'\t(gr_line (start {x1} {y2}) (end {x1} {y1}) (stroke (width 0.05) (type solid)) (layer "Edge.Cuts") (uuid "{uuid.uuid4()}"))',
    ]

    # Find insertion point (before last closing paren)
    insert_idx = len(lines) - 1
    while insert_idx >= 0 and lines[insert_idx].strip() != ")":
        insert_idx -= 1
    if insert_idx >= 0:
        for j, el in enumerate(edge_lines):
            lines.insert(insert_idx + j, el)

    # Write back
    with open(PCB_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\nFixed {fixed} component positions")
    print(f"Board outline: clean rectangle ({x1},{y1})→({x2},{y2}) = {x2-x1}x{y2-y1}mm")
    print(f"Edge.Cuts lines: 4 (all old removed)")


if __name__ == "__main__":
    main()
