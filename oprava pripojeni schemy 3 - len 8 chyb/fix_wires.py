#!/usr/bin/env python3
"""Snap all off-grid wire endpoints to nearest component pins."""
import re, math

SCH = "ph-verzion-01.kicad_sch"
with open(SCH) as f:
    sch = f.read()

# Find end of lib_symbols block (it's at the beginning of the file)
pos = sch.find("(lib_symbols")
depth = 0
lib_end = pos
for i in range(pos, len(sch)):
    if sch[i] == '(':
        depth += 1
    elif sch[i] == ')':
        depth -= 1
        if depth == 0:
            lib_end = i + 1
            break

lib_section = sch[pos:lib_end]
main = sch[lib_end:]  # everything AFTER lib_symbols
main_offset = lib_end  # offset to convert main positions to sch positions

print(f"lib_symbols: {pos}-{lib_end}, main section: {len(main)} chars")

# === 1. Parse placed symbols ===
placed = []
for m in re.finditer(r'\(symbol\n\t\t\(lib_id "([^"]+)"\)\n\t\t\(at ([\d.]+) ([\d.]+)( \d+)?\)', main):
    lib_id = m.group(1)
    sx, sy = float(m.group(2)), float(m.group(3))
    angle = int(m.group(4).strip()) if m.group(4) else 0
    block = main[m.start():m.start() + 2000]
    ref_m = re.search(r'"Reference" "([^"]+)"', block)
    ref = ref_m.group(1) if ref_m else "?"
    my = "(mirror y)" in block[:300]
    mx = "(mirror x)" in block[:300]
    placed.append((lib_id, sx, sy, angle, ref, mx, my))

print(f"Placed symbols: {len(placed)}")

# === 2. Parse lib symbol pins ===
symbol_pins = {}
for m in re.finditer(r'\(symbol "([^"]+)"\n', lib_section):
    sym_name = m.group(1)
    parent = re.sub(r'_\d+_\d+$', '', sym_name)

    start = m.start()
    d = 0
    end = start
    for i in range(start, min(start + 100000, len(lib_section))):
        if lib_section[i] == '(':
            d += 1
        elif lib_section[i] == ')':
            d -= 1
            if d == 0:
                end = i
                break

    block = lib_section[start:end]
    for pm in re.finditer(r'\(pin \w+ \w+\n\s+\(at ([\d.-]+) ([\d.-]+) (\d+)\).*?\(number "([^"]+)"\)', block, re.DOTALL):
        px, py = float(pm.group(1)), float(pm.group(2))
        pnum = pm.group(4)
        if parent not in symbol_pins:
            symbol_pins[parent] = []
        if not any(p[0] == pnum and p[1] == px and p[2] == py for p in symbol_pins[parent]):
            symbol_pins[parent].append((pnum, px, py))

print(f"Library symbols with pins: {len(symbol_pins)}")

# === 3. Calculate global pin positions ===
def rot(lx, ly, angle, mx=False, my=False):
    if my:
        lx = -lx
    if mx:
        ly = -ly
    rad = math.radians(angle)
    return (lx * math.cos(rad) - ly * math.sin(rad),
            lx * math.sin(rad) + ly * math.cos(rad))

all_pins = []
for lib_id, sx, sy, angle, ref, mx, my in placed:
    if lib_id in symbol_pins:
        for pn, lx, ly in symbol_pins[lib_id]:
            dx, dy = rot(lx, ly, angle, mx, my)
            all_pins.append((round(sx + dx, 2), round(sy + dy, 2), ref, pn))

print(f"Global pins: {len(all_pins)}")

# === 4. Parse wires ===
wires = []
for m in re.finditer(r'\(xy ([\d.]+) ([\d.]+)\) \(xy ([\d.]+) ([\d.]+)\)', main):
    x1, y1 = float(m.group(1)), float(m.group(2))
    x2, y2 = float(m.group(3)), float(m.group(4))
    # Store position relative to sch (not main)
    wires.append((x1, y1, x2, y2, m.start() + main_offset))

print(f"Wires: {len(wires)}")

# === 5. Find and fix near-miss connections ===
SNAP_MAX = 2.5
SNAP_MIN = 0.005
fixes = []

for px, py, ref, pn in all_pins:
    best_d = 999
    best = None
    for x1, y1, x2, y2, ws in wires:
        d1 = math.sqrt((px - x1) ** 2 + (py - y1) ** 2)
        d2 = math.sqrt((px - x2) ** 2 + (py - y2) ** 2)
        if SNAP_MIN < d1 < best_d:
            best_d = d1
            best = (x1, y1, ws)
        if SNAP_MIN < d2 < best_d:
            best_d = d2
            best = (x2, y2, ws)

    if best and best_d < SNAP_MAX:
        wx, wy, fpos = best
        fixes.append((wx, wy, px, py, ref, pn, best_d, fpos))

print(f"\nFixes needed: {len(fixes)}")

# Apply from end to start
fixes.sort(key=lambda x: x[7], reverse=True)
applied = 0
for wx, wy, px, py, ref, pn, dist, fpos in fixes:
    old = f"(xy {wx} {wy})"
    new = f"(xy {px} {py})"
    if old == new:
        continue
    idx = sch.find(old, max(0, fpos - 50), fpos + 200)
    if idx >= 0:
        sch = sch[:idx] + new + sch[idx + len(old):]
        applied += 1

print(f"Applied: {applied}")

refs = {}
for _, _, _, _, ref, pn, dist, _ in fixes:
    if ref not in refs:
        refs[ref] = []
    refs[ref].append(f"p{pn}({dist:.2f})")
for r in sorted(refs.keys()):
    print(f"  {r}: {', '.join(refs[r])}")

with open(SCH, 'w') as f:
    f.write(sch)
print("\nDone!")
