#!/usr/bin/env python3
"""
Fix remaining DRC issues:
1. Remove ALL duplicate Edge.Cuts + Dwgs.User gr_lines, keep only 1 clean rectangle
2. Separate J2 and J7 much more (J2 is 1x14=33mm long at 90°, J7 is 2x10=26mm)
3. Move R16/R17 away from J7
4. Fix courtyard overlaps for remaining components
"""

import re
import uuid as uuid_mod

PCB = "/Users/ing.tomaslaso/Documents/kiCad/ph-verzion-01/ph-verzion-01.kicad_pcb"

with open(PCB, "r") as f:
    content = f.read()

# ============================================================
# STEP 1: Remove ALL gr_line/gr_rect on Edge.Cuts and Dwgs.User
# These are multi-line blocks like:
#   (gr_line
#       (start X Y)
#       (end X Y)
#       ...
#       (layer "Edge.Cuts")
#       ...
#   )
# And single-line:
#   (gr_line (start ...) ... (layer "Edge.Cuts") ...)
# ============================================================

# Remove single-line gr_lines on Edge.Cuts or Dwgs.User
content = re.sub(r'\t\(gr_line \(start[^)]+\)[^\n]*\(layer "(Edge\.Cuts|Dwgs\.User)"\)[^\n]*\)\n', '', content)

# Remove multi-line gr_line blocks on Edge.Cuts or Dwgs.User
# Pattern: \t(gr_line\n ... (layer "Edge.Cuts") ... \t)
content = re.sub(
    r'\t\(gr_line\n(?:\t\t[^\n]+\n)*?\t\t\(layer "(Edge\.Cuts|Dwgs\.User)"\)\n(?:\t\t[^\n]+\n)*?\t\)\n',
    '',
    content
)

# Verify no Edge.Cuts gr_lines remain (except layer definition)
remaining = re.findall(r'gr_line.*Edge\.Cuts', content)
print(f"Edge.Cuts gr_lines after cleanup: {len(remaining)}")

# ============================================================
# STEP 2: Add single clean board outline
# ============================================================
x1, y1 = 20, 20
x2, y2 = 230, 165

outline = f"""\t(gr_line (start {x1} {y1}) (end {x2} {y1}) (stroke (width 0.05) (type solid)) (layer "Edge.Cuts") (uuid "{uuid_mod.uuid4()}"))
\t(gr_line (start {x2} {y1}) (end {x2} {y2}) (stroke (width 0.05) (type solid)) (layer "Edge.Cuts") (uuid "{uuid_mod.uuid4()}"))
\t(gr_line (start {x2} {y2}) (end {x1} {y2}) (stroke (width 0.05) (type solid)) (layer "Edge.Cuts") (uuid "{uuid_mod.uuid4()}"))
\t(gr_line (start {x1} {y2}) (end {x1} {y1}) (stroke (width 0.05) (type solid)) (layer "Edge.Cuts") (uuid "{uuid_mod.uuid4()}"))
"""

# Insert before last )
last_paren = content.rfind(")")
content = content[:last_paren] + outline + content[last_paren:]

# ============================================================
# STEP 3: Fix component positions
# J2 (1x14 header at 90°) = 33.02mm long, 2.54mm wide
# J7 (2x10 header at 90°) = 22.86mm long, 5.08mm wide
# At 90° rotation, length goes vertical, width goes horizontal
# J2 width at 90° = 2.54mm → extends ±1.27mm in X from center
# J7 width at 90° = 5.08mm → extends ±2.54mm in X from center
# Min gap between them: J2 right edge + 1mm + J7 left edge
# J2 at x=30: right edge at ~31.27
# J7 needs left edge at 32.27 → center at 34.81
# But J7 is 2x10 = two rows, wider. Let me put J7 further right.
#
# Actually the problem is MUCH bigger: at 90° the 14-pin header
# has its pins spread in Y direction, 33mm. J2 at (30,130,90)
# and J7 at (48,130,90) — the issue is that J2 and J7 pin rows
# are only 18mm apart horizontally but the 2x10 header J7 has
# pins at x±1.27 from center. J2 has pins at x=center.
# So J2 rightmost pin at 30mm, J7 leftmost at 48-1.27=46.73
# That's 16.73mm gap — should be enough!
#
# Wait, looking at the DRC: pads overlap AT y=130, x=47.78 (J2 pad8)
# vs x=48.0 (J7 pad1). So J2 pin 8 is at x=47.78 and J7 pin 1
# at x=48. This means J2 at 90° extends its pins in X direction,
# not Y! A 1x14 header at 90°: pins are along X axis.
# Pin 1 at origin, pin 14 at origin + 13*2.54 = 33.02mm in X
# So J2 at (30,130,90) has pins from x=30 to x=30+33=63!
# J7 at (48,130,90) has pins from x=48 to x=48+22.86=71!
# THEY COMPLETELY OVERLAP in X!
#
# Fix: Put J2 and J7 in DIFFERENT areas entirely.
# J2 (display header): along left edge, NOT rotated (vertical)
# J7 (GPIO header): along bottom edge, NOT rotated (vertical)
# ============================================================

FIXES = {
    # J2 1x14 header — put it vertical (0°) along left side
    # At 0°: pins go in Y direction, 33mm tall, ~2.5mm wide
    "J2":  (28, 118, 0),    # vertical, left edge

    # J7 2x10 header — put it separate, vertical
    # At 0°: pins go in Y direction, 22.86mm tall, ~5mm wide
    "J7":  (38, 118, 0),    # vertical, 10mm right of J2

    # R16, R17 — move well away from J2/J7 area
    "R16": (50, 114),
    "R17": (50, 120),

    # D3-D7 still overlapping J9-J11 area — move up more
    "D3":  (80, 142),
    "D4":  (94, 142),
    "D5":  (108, 142),
    "D6":  (122, 142),
    "D7":  (134, 142),

    # J6 at (30,128) may overlap J2 — move down
    "J6":  (28, 140),
}

# Apply fixes
for ref, pos in FIXES.items():
    new_x, new_y = pos[0], pos[1]
    explicit_angle = pos[2] if len(pos) == 3 else None

    # Find the footprint block with this reference
    pattern = rf'(\(property "Reference" "{re.escape(ref)}")'
    ref_match = re.search(pattern, content)
    if not ref_match:
        print(f"  {ref}: NOT FOUND")
        continue

    # Find the footprint start before this reference
    fp_start = content.rfind("\t(footprint ", 0, ref_match.start())
    if fp_start == -1:
        continue

    # Find the (at ...) in the region between fp_start and reference
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

# Verify
with open(PCB) as f:
    verify = f.read()
edge_lines = re.findall(r'gr_line.*Edge\.Cuts', verify)
print(f"\nFinal Edge.Cuts gr_lines: {len(edge_lines)}")
print(f"Board: {x2-x1}x{y2-y1}mm at ({x1},{y1})→({x2},{y2})")
