#!/usr/bin/env python3
"""
Comprehensive fix: snap ALL wire endpoints to exact pin positions.
Strategy:
1. Parse all pin global positions
2. Parse all wire endpoints
3. For each wire endpoint, if a pin is within snap distance, move endpoint to exact pin pos
4. This ensures every wire that's "close" to a pin actually connects
"""
import re, math, uuid

SCH = "ph-verzion-01.kicad_sch"
with open(SCH) as f:
    sch = f.read()

# Find lib_symbols boundaries
lib_pos = sch.find("(lib_symbols")
depth = 0
lib_end = lib_pos
for i in range(lib_pos, len(sch)):
    if sch[i] == '(': depth += 1
    elif sch[i] == ')':
        depth -= 1
        if depth == 0:
            lib_end = i + 1
            break

lib_section = sch[lib_pos:lib_end]
main = sch[lib_end:]
MAIN_OFF = lib_end

# === 1. Parse lib symbol pins ===
pin_by_symbol = {}  # short_name -> [(pin_num, local_x, local_y)]
pin_matches = list(re.finditer(r'\(pin \w+ \w+\n\t+\(at ([\d.-]+) ([\d.-]+) (\d+)\)', lib_section))
for m in pin_matches:
    after = lib_section[m.end():m.end()+400]
    nm = re.search(r'number "([^"]+)"', after)
    if not nm:
        continue
    before = lib_section[max(0, m.start()-15000):m.start()]
    sym_matches = list(re.finditer(r'\(symbol "([^"]+)"', before))
    if sym_matches:
        sym_name = sym_matches[-1].group(1)
        parent = re.sub(r'_\d+_\d+$', '', sym_name)
        if parent not in pin_by_symbol:
            pin_by_symbol[parent] = []
        entry = (nm.group(1), float(m.group(1)), float(m.group(2)))
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

# === 3. Calculate ALL global pin positions ===
def rot(lx, ly, angle, mx=False, my=False):
    if my: lx = -lx
    if mx: ly = -ly
    rad = math.radians(angle)
    return (round(lx * math.cos(rad) - ly * math.sin(rad), 4),
            round(lx * math.sin(rad) + ly * math.cos(rad), 4))

all_pins = {}  # (x, y) -> [(ref, pin_num)]
for short_id, sx, sy, angle, ref, mx, my in placed:
    if short_id in pin_by_symbol:
        for pn, lx, ly in pin_by_symbol[short_id]:
            dx, dy = rot(lx, ly, angle, mx, my)
            gx = round(sx + dx, 2)
            gy = round(sy + dy, 2)
            key = (gx, gy)
            if key not in all_pins:
                all_pins[key] = []
            all_pins[key].append((ref, pn))

print(f"Unique pin positions: {len(all_pins)}")

# Build a spatial lookup for pins
pin_list = list(all_pins.keys())

# === 4. Parse ALL wire endpoint positions in main section ===
# Find every (xy X Y) occurrence in wires
# Each wire has format: (xy X1 Y1) (xy X2 Y2)
wire_xys = []  # [(x, y, start_pos_in_sch, original_text)]
for m in re.finditer(r'\(xy ([\d.]+) ([\d.]+)\)', main):
    x, y = float(m.group(1)), float(m.group(2))
    abs_pos = m.start() + MAIN_OFF
    wire_xys.append((x, y, abs_pos, m.group(0)))

print(f"Wire xy points: {len(wire_xys)}")

# === 5. For each wire endpoint, find nearest pin and snap ===
SNAP_MAX = 3.0  # mm - generous snap distance
SNAP_MIN = 0.001  # ignore exact matches

fixes = []  # [(old_text, new_text, abs_pos, dist, ref, pin)]
for wx, wy, wpos, orig_text in wire_xys:
    best_d = 999
    best_pin = None
    for px, py in pin_list:
        d = math.sqrt((wx - px)**2 + (wy - py)**2)
        if SNAP_MIN < d < best_d:
            best_d = d
            best_pin = (px, py)

    if best_pin and best_d < SNAP_MAX:
        px, py = best_pin
        new_text = f"(xy {px} {py})"
        if orig_text != new_text:
            ref_info = all_pins[best_pin][0]
            fixes.append((orig_text, new_text, wpos, best_d, ref_info[0], ref_info[1]))

print(f"\nWire endpoints to snap: {len(fixes)}")

# Sort by position descending (fix from end to preserve earlier positions)
fixes.sort(key=lambda x: x[2], reverse=True)

applied = 0
for old_text, new_text, abs_pos, dist, ref, pin in fixes:
    # Search near expected position
    search_start = max(0, abs_pos - 20)
    search_end = min(len(sch), abs_pos + len(old_text) + 20)
    idx = sch.find(old_text, search_start, search_end)
    if idx >= 0:
        sch = sch[:idx] + new_text + sch[idx + len(old_text):]
        applied += 1

print(f"Applied: {applied}")

# Summary
refs = {}
for _, _, _, dist, ref, pin in fixes:
    if ref not in refs:
        refs[ref] = []
    refs[ref].append(f"p{pin}({dist:.2f})")

print(f"\nFixed components ({len(refs)}):")
for r in sorted(refs.keys()):
    print(f"  {r}: {', '.join(refs[r])}")

# === 6. Check for pins with NO wire nearby at all (need new wires) ===
print("\n=== Pins with NO wire within 5mm ===")
no_wire_pins = []
for (px, py), ref_list in all_pins.items():
    best_d = 999
    for wx, wy, _, _ in wire_xys:
        d = math.sqrt((wx - px)**2 + (wy - py)**2)
        if d < best_d:
            best_d = d
    if best_d > 5.0:
        for ref, pn in ref_list:
            if not ref.startswith('#'):  # skip power symbols
                no_wire_pins.append((px, py, ref, pn, best_d))
                print(f"  {ref} pin {pn} at ({px},{py}) - nearest wire: {best_d:.1f}mm")

with open(SCH, 'w') as f:
    f.write(sch)

print(f"\nDone! Applied {applied} wire endpoint fixes.")
