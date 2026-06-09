#!/usr/bin/env python3
"""
Comprehensive schematic fixer.
1. Compute exact pin positions using correct KiCad formula
2. Snap nearby wire endpoints to exact pin positions
3. Add no_connect markers for unused pins
4. Add missing GND connections
"""
import re, math, uuid

def uid():
    return str(uuid.uuid4())

SCH = "ph-verzion-01.kicad_sch"
with open(SCH) as f:
    sch = f.read()

# === Parse lib_symbols section ===
lib_pos = sch.find("(lib_symbols")
depth = 0; lib_end = lib_pos
for i in range(lib_pos, len(sch)):
    if sch[i] == '(': depth += 1
    elif sch[i] == ')':
        depth -= 1
        if depth == 0: lib_end = i + 1; break

lib_section = sch[lib_pos:lib_end]
main = sch[lib_end:]
MAIN_OFF = lib_end

# === 1. Parse lib symbol pins ===
pin_by_symbol = {}  # parent_name -> [(pin_num, lx, ly, pin_name)]
for sym_m in re.finditer(r'\(symbol\s+"([^"]+)"\s*\n', lib_section):
    sym_name = sym_m.group(1)
    parent = re.sub(r'_\d+_\d+$', '', sym_name)
    start = sym_m.start()
    d = 0; end = start
    for i in range(start, min(start + 100000, len(lib_section))):
        if lib_section[i] == '(': d += 1
        elif lib_section[i] == ')':
            d -= 1
            if d == 0: end = i; break
    block = lib_section[start:end]
    for pm in re.finditer(r'\(pin\s+\w+\s+\w+\s*\n?\s*\(at\s+([\d.-]+)\s+([\d.-]+)\s+(\d+)\)', block):
        px, py = float(pm.group(1)), float(pm.group(2))
        after = block[pm.end():pm.end()+300]
        nm = re.search(r'\(number\s+"([^"]+)"', after)
        name_m = re.search(r'\(name\s+"([^"]*)"', after)
        if not nm: continue
        pnum = nm.group(1)
        pname = name_m.group(1) if name_m else ""
        if parent not in pin_by_symbol: pin_by_symbol[parent] = []
        entry = (pnum, px, py, pname)
        if entry not in pin_by_symbol[parent]:
            pin_by_symbol[parent].append(entry)

print(f"Library symbols with pins: {len(pin_by_symbol)}")

# === 2. Parse placed symbols ===
placed = []
for m in re.finditer(r'\(symbol\n\t\t\(lib_id "([^"]+)"\)\n\t\t\(at ([\d.]+) ([\d.]+)( \d+)?\)', main):
    lib_id = m.group(1)
    sx, sy = float(m.group(2)), float(m.group(3))
    angle = int(m.group(4).strip()) if m.group(4) else 0
    block = main[m.start():m.start()+2000]
    ref_m = re.search(r'"Reference" "([^"]+)"', block)
    ref = ref_m.group(1) if ref_m else "?"
    my = "(mirror y)" in block[:300]
    mx = "(mirror x)" in block[:300]
    short_id = lib_id.split(':')[-1] if ':' in lib_id else lib_id
    placed.append((short_id, sx, sy, angle, ref, mx, my))

print(f"Placed symbols: {len(placed)}")

# === 3. Compute global pin positions using CORRECT formula ===
def pin_global(lx, ly, angle, sx, sy, mx=False, my=False):
    """Compute global pin position from lib local coordinates.
    Formula: standard rotation, then negate Y (lib Y-up → schematic Y-down).
    """
    if my: lx = -lx
    if mx: ly = -ly
    rad = math.radians(angle)
    rx = lx * math.cos(rad) - ly * math.sin(rad)
    ry = lx * math.sin(rad) + ly * math.cos(rad)
    return (round(sx + rx, 4), round(sy - ry, 4))

all_pins = {}  # (gx, gy) -> [(ref, pin_num, pin_name)]
for short_id, sx, sy, angle, ref, mx, my in placed:
    if short_id in pin_by_symbol:
        for pnum, lx, ly, pname in pin_by_symbol[short_id]:
            gx, gy = pin_global(lx, ly, angle, sx, sy, mx, my)
            key = (gx, gy)
            if key not in all_pins: all_pins[key] = []
            all_pins[key].append((ref, pnum, pname))

print(f"Unique pin positions: {len(all_pins)}")

# === 4. Parse all endpoints (wires, labels, junctions, no_connects) ===
wire_xys = []  # [(x, y, abs_pos, original_text)]
for m in re.finditer(r'\(xy ([\d.]+) ([\d.]+)\)', main):
    x, y = float(m.group(1)), float(m.group(2))
    abs_pos = m.start() + MAIN_OFF
    wire_xys.append((x, y, abs_pos, m.group(0)))

# Also track label positions
label_positions = set()
for m in re.finditer(r'\(label "[^"]+"\n\t\t\(at ([\d.]+) ([\d.]+)', main):
    label_positions.add((round(float(m.group(1)), 4), round(float(m.group(2)), 4)))

# And no_connect positions
nc_positions = set()
for m in re.finditer(r'\(no_connect\n\t\t\(at ([\d.]+) ([\d.]+)\)', main):
    nc_positions.add((round(float(m.group(1)), 4), round(float(m.group(2)), 4)))

# Build set of all endpoints
all_endpoints = set()
for x, y, _, _ in wire_xys:
    all_endpoints.add((round(x, 4), round(y, 4)))
all_endpoints |= label_positions | nc_positions

print(f"Wire endpoints: {len(wire_xys)}, Labels: {len(label_positions)}, No-connects: {len(nc_positions)}")
print(f"Total unique endpoints: {len(all_endpoints)}")

# === 5. Check pin connectivity ===
connected_pins = []
close_pins = []  # within snap distance
unconnected_pins = []

SNAP_DIST = 3.0  # mm

for (gx, gy), ref_list in all_pins.items():
    if (gx, gy) in all_endpoints:
        connected_pins.append((gx, gy, ref_list))
    else:
        # Find nearest endpoint
        best_d = 999
        best_ep = None
        for ex, ey in all_endpoints:
            d = math.sqrt((gx - ex)**2 + (gy - ey)**2)
            if d < best_d:
                best_d = d
                best_ep = (ex, ey)

        if best_d < SNAP_DIST:
            close_pins.append((gx, gy, ref_list, best_d, best_ep))
        else:
            unconnected_pins.append((gx, gy, ref_list, best_d))

print(f"\nConnected: {len(connected_pins)}")
print(f"Close (<{SNAP_DIST}mm): {len(close_pins)}")
print(f"Unconnected: {len(unconnected_pins)}")

# === 6. Snap close wire endpoints to pin positions ===
print("\n=== Snapping close wire endpoints ===")
fixes = []
for gx, gy, ref_list, dist, (bx, by) in sorted(close_pins, key=lambda x: x[3]):
    ref_info = ref_list[0]
    old_text = f"(xy {bx} {by})"
    new_text = f"(xy {gx} {gy})"
    if old_text != new_text:
        print(f"  {ref_info[0]} pin {ref_info[1]} ({ref_info[2]}): ({bx},{by}) → ({gx},{gy}) dist={dist:.3f}mm")
        fixes.append((old_text, new_text, dist, ref_info[0], ref_info[1]))

# Apply fixes to the actual schematic
# We need to be careful not to snap wrong endpoints
# For each fix, find the closest occurrence to the pin position and snap it
applied = 0
for old_text, new_text, dist, ref, pn in fixes:
    # Find the old_text occurrence that's closest to where we expect it
    idx = sch.find(old_text)
    count = 0
    while idx >= 0:
        count += 1
        idx = sch.find(old_text, idx + 1)

    if count == 1:
        # Only one occurrence - safe to replace
        sch = sch.replace(old_text, new_text, 1)
        applied += 1
    else:
        # Multiple occurrences - need to find the right one
        # For now, skip if ambiguous (will handle in post-processing)
        print(f"    WARNING: {old_text} has {count} occurrences - skipping (ambiguous)")

print(f"Applied {applied} wire snaps")

# === 7. Add no_connect markers for unused pins ===
print("\n=== Pins needing no_connect markers ===")
no_connect_pins = []
for gx, gy, ref_list, dist in unconnected_pins:
    for ref, pn, pname in ref_list:
        if ref.startswith('#'):
            continue  # skip power symbols
        # Determine if this pin should be no_connect or needs a wire
        needs_nc = False
        if pname in ('NC', 'NC1', 'NC2'):
            needs_nc = True
        elif pname in ('SD0', 'SD1', 'SD2', 'SD3', 'CMD', 'CLK'):
            needs_nc = True  # unused SD card pins
        elif ref == 'RLY1' and pn in ('12', '21', '22', '24'):
            needs_nc = True  # unused relay contacts

        if needs_nc:
            no_connect_pins.append((gx, gy, ref, pn, pname))
            print(f"  NC: {ref} pin {pn} ({pname}) at ({gx},{gy})")

# Find insertion point for no_connect markers (before the first symbol)
# In the generated file, no_connects come after junctions
nc_insert_marker = "\n\t(junction"
nc_insert_pos = sch.find(nc_insert_marker)
if nc_insert_pos < 0:
    nc_insert_marker = "\n\t(wire"
    nc_insert_pos = sch.find(nc_insert_marker)

nc_additions = ""
for gx, gy, ref, pn, pname in no_connect_pins:
    # Check if there's already a no_connect at this position
    if (round(gx, 4), round(gy, 4)) not in nc_positions:
        nc_additions += f"""\n\t(no_connect
\t\t(at {gx} {gy})
\t\t(uuid "{uid()}")
\t)"""

if nc_additions and nc_insert_pos >= 0:
    sch = sch[:nc_insert_pos] + nc_additions + sch[nc_insert_pos:]
    print(f"Added {len(no_connect_pins)} no_connect markers")

# === 8. Add GND connections for ESP32 ground pins ===
print("\n=== Adding GND connections for ESP32 ===")
gnd_additions = ""
esp32_gnd_pins = []
for gx, gy, ref_list, dist in unconnected_pins:
    for ref, pn, pname in ref_list:
        if ref == 'U11' and pname in ('GND', 'GND_PAD'):
            esp32_gnd_pins.append((gx, gy, ref, pn, pname))

if esp32_gnd_pins:
    # Find ESP32 position
    for short_id, sx, sy, angle, ref, mx, my in placed:
        if ref == 'U11':
            esp_x, esp_y = sx, sy
            break

    # Add GND power symbol below the leftmost GND pin
    # Sort by x to find leftmost
    esp32_gnd_pins.sort(key=lambda p: p[0])

    # GND power symbol position
    gnd_sym_x = esp32_gnd_pins[0][0] - 5
    gnd_sym_y = esp32_gnd_pins[0][1] + 5

    # Wire from each GND pin down to a common GND point
    wire_insert = sch.rfind("\n\t(wire")
    if wire_insert < 0:
        wire_insert = sch.rfind("\n\t(label")

    gnd_wires = ""
    for i, (gx, gy, ref, pn, pname) in enumerate(esp32_gnd_pins):
        # Wire from pin straight down
        gnd_wires += f"""\n\t(wire
\t\t(pts
\t\t\t(xy {gx} {gy}) (xy {gx} {gy + 3})
\t\t)
\t\t(stroke (width 0) (type default))
\t\t(uuid "{uid()}")
\t)"""
        # Horizontal wire to common GND point
        gnd_wires += f"""\n\t(wire
\t\t(pts
\t\t\t(xy {gx} {gy + 3}) (xy {gnd_sym_x} {gy + 3})
\t\t)
\t\t(stroke (width 0) (type default))
\t\t(uuid "{uid()}")
\t)"""
        if i > 0:
            gnd_wires += f"""\n\t(junction
\t\t(at {gnd_sym_x} {gy + 3})
\t\t(diameter 0)
\t\t(color 0 0 0 0)
\t\t(uuid "{uid()}")
\t)"""
        print(f"  GND wire: {ref} pin {pn} ({pname}) at ({gx},{gy})")

    # GND power symbol
    sym_insert = sch.rfind("\n\t(symbol")
    gnd_sym = f"""\n\t(symbol
\t\t(lib_id "power:GND")
\t\t(at {gnd_sym_x} {gnd_sym_y} 0)
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{uid()}")
\t\t(property "Reference" "#PWR_FIX1" (at {gnd_sym_x + 2.54} {gnd_sym_y - 2.54} 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify left))
\t\t)
\t\t(property "Value" "GND" (at {gnd_sym_x + 2.54} {gnd_sym_y + 2.54} 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify left))
\t\t)
\t\t(property "Footprint" "" (at {gnd_sym_x} {gnd_sym_y} 0)
\t\t\t(effects (font (size 1.27 1.27)) (hide yes))
\t\t)
\t\t(property "Datasheet" "~" (at {gnd_sym_x} {gnd_sym_y} 0)
\t\t\t(effects (font (size 1.27 1.27)) (hide yes))
\t\t)
\t\t(property "Description" "" (at {gnd_sym_x} {gnd_sym_y} 0)
\t\t\t(effects (font (size 1.27 1.27)) (hide yes))
\t\t)
\t\t(pin "1" (uuid "{uid()}"))
\t\t(instances
\t\t\t(project "ph-verzion-01"
\t\t\t\t(path "/54ccc777-3789-41c0-b4eb-6807475564db"
\t\t\t\t\t(reference "#PWR_FIX1")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)"""

    # Wire from common point down to GND symbol
    common_y = esp32_gnd_pins[0][1] + 3
    gnd_wires += f"""\n\t(wire
\t\t(pts
\t\t\t(xy {gnd_sym_x} {common_y}) (xy {gnd_sym_x} {gnd_sym_y})
\t\t)
\t\t(stroke (width 0) (type default))
\t\t(uuid "{uid()}")
\t)"""

    if wire_insert >= 0 and sym_insert >= 0:
        # Insert wires first (before symbols), then symbol
        sch = sch[:wire_insert] + gnd_wires + sch[wire_insert:]
        # Recalculate sym_insert after wire insertion
        sym_insert = sch.rfind("\n\t(symbol")
        sch = sch[:sym_insert] + gnd_sym + sch[sym_insert:]
        print(f"Added GND connections for {len(esp32_gnd_pins)} ESP32 pins")

# === 9. Report remaining unconnected pins ===
print("\n=== Remaining unconnected pins (need manual wiring) ===")
for gx, gy, ref_list, dist in sorted(unconnected_pins, key=lambda x: x[0]):
    for ref, pn, pname in ref_list:
        if ref.startswith('#'):
            continue
        # Skip pins we already handled
        handled = False
        for _, _, r, p, _ in no_connect_pins:
            if r == ref and p == pn: handled = True
        for _, _, r, p, _ in esp32_gnd_pins:
            if r == ref and p == pn: handled = True
        if not handled:
            print(f"  {ref} pin {pn} ({pname}) at ({gx},{gy}) nearest={dist:.1f}mm")

# === Write output ===
with open(SCH, 'w') as f:
    f.write(sch)

print(f"\nDone! Written to {SCH}")
