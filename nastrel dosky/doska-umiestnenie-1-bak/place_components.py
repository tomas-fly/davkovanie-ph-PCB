#!/usr/bin/env python3
"""
PCB Placement v4 — automatic overlap resolution.

1. Place components in approximate zones
2. Extract actual bounding boxes from PCB footprints
3. Iteratively push overlapping components apart
4. Write updated positions back to PCB
"""

import re, os, math, sys

PCB_FILE = os.path.join(os.path.dirname(__file__), "ph-verzion-01.kicad_pcb")

BX, BY = 20, 20
BW, BH = 230, 145
# Board edges: x=20..250, y=20..165

HV_BOUNDARY = BX + 65  # HV/LV boundary

# ================================================================
# INITIAL PLACEMENT — v5, generous spacing based on actual sizes
# Actual sizes: U1=60×36, U11=19×26, RLY1=30×13, DIP-8=12×10,
#   TO-263=17×11, BNC=11×11, J1/J11=16×11, F1=13×13, J7=6×26,
#   J2=4×37, TO-220=10×15, JST=8×7, electro cap=10-13mm
# ================================================================

PLACEMENT = {}

# --- HV ZONE (x=20..85) ---
# U1 HLK-30M12 (60×36mm) — top of HV zone
PLACEMENT["J1"]   = (BX + 10, BY + 10, 0)     # AC in 16×11mm
PLACEMENT["F1"]   = (BX + 30, BY + 10, 0)     # Fuse 13×13mm

PLACEMENT["U1"]   = (BX + 32, BY + 40, 0)     # 60×36mm, extends x=2..62, y=22..58

PLACEMENT["C1"]   = (BX + 10, BY + 62, 0)     # PSU bypass below HLK
PLACEMENT["D1"]   = (BX + 18, BY + 62, 0)     # LED
PLACEMENT["R1"]   = (BX + 26, BY + 62, 0)     # LED R

# Relay + opto (bottom of HV zone)
PLACEMENT["U12"]  = (BX + 5,  BY + 74, 0)     # PC817
PLACEMENT["R28"]  = (BX + 5,  BY + 82, 0)
PLACEMENT["R29"]  = (BX + 14, BY + 82, 0)

PLACEMENT["RLY1"] = (BX + 32, BY + 82, 0)     # 30×13mm

PLACEMENT["Q2"]   = (BX + 8,  BY + 92, 0)     # TO-220 10×15mm
PLACEMENT["R21"]  = (BX + 3,  BY + 100, 0)
PLACEMENT["R25"]  = (BX + 11, BY + 100, 0)
PLACEMENT["D4"]   = (BX + 19, BY + 100, 0)

PLACEMENT["D7"]   = (BX + 3,  BY + 108, 0)
PLACEMENT["R30"]  = (BX + 11, BY + 108, 0)
PLACEMENT["C29"]  = (BX + 24, BY + 108, 0)    # 18mm film cap
PLACEMENT["MOV1"] = (BX + 44, BY + 108, 0)    # 14mm varistor

PLACEMENT["J11"]  = (BX + 10, BY + 122, 0)    # AC out 16×11mm

# --- POWER ZONE (x=90..135) ---
PX = BX + 88

# Buck 12V→5V
PLACEMENT["C2"]   = (PX,      BY + 10, 0)     # 12mm electro cap
PLACEMENT["U2"]   = (PX + 16, BY + 10, 0)     # TO-263 17×11mm
PLACEMENT["L1"]   = (PX + 34, BY + 10, 0)     # 11mm inductor
PLACEMENT["D2"]   = (PX + 16, BY + 24, 0)     # SS34 SMC
PLACEMENT["C3"]   = (PX + 34, BY + 24, 0)     # 10mm electro cap

# LDO 5V→3.3V
PLACEMENT["C4"]   = (PX,      BY + 38, 0)
PLACEMENT["U3"]   = (PX + 12, BY + 38, 0)     # SOT-223
PLACEMENT["C10"]  = (PX + 24, BY + 38, 0)

# Analog 12V→+5V_AN (LM7805 TO-263 17×11mm)
PLACEMENT["C6"]   = (PX,      BY + 52, 0)
PLACEMENT["C7"]   = (PX + 10, BY + 52, 0)
PLACEMENT["U4"]   = (PX + 22, BY + 52, 0)     # D2PAK 17×11mm
PLACEMENT["C8"]   = (PX + 38, BY + 52, 0)
PLACEMENT["C9"]   = (PX + 38, BY + 60, 0)
PLACEMENT["FB1"]  = (PX + 46, BY + 52, 0)
PLACEMENT["L2"]   = (PX + 46, BY + 60, 0)

# Charge pump TPS60400
PLACEMENT["C11"]  = (PX,      BY + 68, 0)
PLACEMENT["U5"]   = (PX + 10, BY + 68, 0)     # SOT-23-5
PLACEMENT["C12"]  = (PX + 20, BY + 68, 0)
PLACEMENT["FB2"]  = (PX + 28, BY + 68, 0)
PLACEMENT["C5"]   = (PX + 36, BY + 68, 0)

# --- DIGITAL ZONE ---

# ESP32 (19×26mm) — center of digital area
PLACEMENT["U11"]  = (PX + 10, BY + 88, 0)
PLACEMENT["C27"]  = (PX - 4,  BY + 80, 0)
PLACEMENT["C28"]  = (PX - 4,  BY + 86, 0)
PLACEMENT["R18"]  = (PX - 4,  BY + 92, 0)
PLACEMENT["C26"]  = (PX - 4,  BY + 98, 0)
PLACEMENT["R19"]  = (PX + 26, BY + 80, 0)

# ADS1115 ADC
PLACEMENT["U10"]  = (PX + 36, BY + 82, 0)
PLACEMENT["C25"]  = (PX + 36, BY + 76, 0)
PLACEMENT["R16"]  = (PX + 44, BY + 76, 0)
PLACEMENT["R17"]  = (PX + 44, BY + 82, 0)

# --- MOSFETs (bottom, under HV + power, NOT extending into analog) ---
MX = BX + 70  # MOSFET zone starts at x=70
PLACEMENT["Q1"]   = (MX,      BY + 114, 0)    # TO-220 10×15mm
PLACEMENT["R20"]  = (MX - 8,  BY + 114, 0)
PLACEMENT["R24"]  = (MX - 8,  BY + 122, 0)
PLACEMENT["D3"]   = (MX + 8,  BY + 122, 0)

PLACEMENT["Q3"]   = (MX + 30, BY + 114, 0)
PLACEMENT["R22"]  = (MX + 18, BY + 114, 0)
PLACEMENT["R26"]  = (MX + 18, BY + 122, 0)
PLACEMENT["D5"]   = (MX + 38, BY + 122, 0)
PLACEMENT["J9"]   = (MX + 42, BY + 100, 0)    # Terminal OUT3

PLACEMENT["Q4"]   = (MX + 60, BY + 114, 0)
PLACEMENT["R23"]  = (MX + 48, BY + 114, 0)
PLACEMENT["R27"]  = (MX + 48, BY + 122, 0)
PLACEMENT["D6"]   = (MX + 68, BY + 122, 0)
PLACEMENT["J10"]  = (MX + 72, BY + 100, 0)    # Terminal OUT4

# --- ANALOG FRONT-END (x=155..230) ---
AX = BX + 148

# pH section (BNC 11×11, DIP-8 12×10, spread generously)
PLACEMENT["P1"]   = (AX + 68, BY + 16, 0)     # BNC far right
PLACEMENT["R2"]   = (AX + 54, BY + 12, 0)
PLACEMENT["C13"]  = (AX + 54, BY + 20, 0)
PLACEMENT["U6"]   = (AX + 38, BY + 16, 0)     # CA3140 DIP-8 12×10mm
PLACEMENT["C14"]  = (AX + 28, BY + 8,  0)
PLACEMENT["C15"]  = (AX + 28, BY + 24, 0)
PLACEMENT["R3"]   = (AX + 28, BY + 34, 0)
PLACEMENT["R4"]   = (AX + 38, BY + 34, 0)     # trimpot 6mm
PLACEMENT["R5"]   = (AX + 48, BY + 34, 0)
PLACEMENT["C16"]  = (AX + 58, BY + 34, 0)
PLACEMENT["U7"]   = (AX + 12, BY + 16, 0)     # TL071 DIP-8
PLACEMENT["C17"]  = (AX + 2,  BY + 8,  0)
PLACEMENT["C18"]  = (AX + 2,  BY + 24, 0)
PLACEMENT["R6"]   = (AX + 2,  BY + 34, 0)
PLACEMENT["R7"]   = (AX + 12, BY + 34, 0)
PLACEMENT["R8"]   = (AX + 22, BY + 34, 0)

# ORP section (shifted down 50mm for clearance)
DY = 50
PLACEMENT["P2"]   = (AX + 68, BY + 16 + DY, 0)  # BNC far right
PLACEMENT["R9"]   = (AX + 54, BY + 12 + DY, 0)
PLACEMENT["C19"]  = (AX + 54, BY + 20 + DY, 0)
PLACEMENT["U8"]   = (AX + 38, BY + 16 + DY, 0)
PLACEMENT["C20"]  = (AX + 28, BY + 8  + DY, 0)
PLACEMENT["C21"]  = (AX + 28, BY + 24 + DY, 0)
PLACEMENT["R10"]  = (AX + 28, BY + 34 + DY, 0)
PLACEMENT["R11"]  = (AX + 38, BY + 34 + DY, 0)
PLACEMENT["R12"]  = (AX + 48, BY + 34 + DY, 0)
PLACEMENT["C22"]  = (AX + 58, BY + 34 + DY, 0)
PLACEMENT["U9"]   = (AX + 12, BY + 16 + DY, 0)
PLACEMENT["C23"]  = (AX + 2,  BY + 8  + DY, 0)
PLACEMENT["C24"]  = (AX + 2,  BY + 24 + DY, 0)
PLACEMENT["R13"]  = (AX + 2,  BY + 34 + DY, 0)
PLACEMENT["R14"]  = (AX + 12, BY + 34 + DY, 0)
PLACEMENT["R15"]  = (AX + 22, BY + 34 + DY, 0)

# --- CONNECTORS (edges) ---
PLACEMENT["J2"]   = (AX + 78, BY + 50, 0)     # Display 1×14 (4×37mm) — right edge
PLACEMENT["J7"]   = (AX + 72, BY + 102, 0)    # GPIO 2×10 (6×26mm) — right side
PLACEMENT["J8"]   = (AX + 62, BY + 130, 0)    # UART 1×4 — bottom-right

PLACEMENT["J3"]   = (AX + 4,  BY + 118, 0)    # 1-Wire JSTs (14mm spacing)
PLACEMENT["J4"]   = (AX + 18, BY + 118, 0)
PLACEMENT["J5"]   = (AX + 32, BY + 118, 0)
PLACEMENT["J6"]   = (AX + 46, BY + 118, 0)
PLACEMENT["R31"]  = (AX + 4,  BY + 110, 0)


# ================================================================
# EXTRACT BOUNDING BOXES FROM PCB
# ================================================================

def extract_bboxes(pcb_content):
    """Extract component bounding boxes from PCB footprints."""
    bboxes = {}

    # Split into footprint blocks
    fp_starts = [m.start() + 1 for m in re.finditer(r'\n\t\(footprint \"', pcb_content)]

    for si, start in enumerate(fp_starts):
        end = fp_starts[si + 1] if si + 1 < len(fp_starts) else len(pcb_content)
        block = pcb_content[start:end]

        ref_m = re.search(r'\(property "Reference" "([^"]+)"', block)
        if not ref_m:
            continue
        ref = ref_m.group(1)

        at_m = re.search(r'^\s*\(at ([\d.-]+) ([\d.-]+)( ([\d.-]+))?\)', block, re.MULTILINE)
        if not at_m:
            continue
        cx, cy = float(at_m.group(1)), float(at_m.group(2))
        rot = float(at_m.group(4)) if at_m.group(4) else 0

        # Collect all coordinate points
        pts = []
        for lm in re.finditer(r'\(fp_line\s*\(start ([\d.-]+) ([\d.-]+)\)\s*\(end ([\d.-]+) ([\d.-]+)\)', block):
            pts.extend([(float(lm.group(1)), float(lm.group(2))),
                        (float(lm.group(3)), float(lm.group(4)))])
        for rm in re.finditer(r'\(fp_rect\s*\(start ([\d.-]+) ([\d.-]+)\)\s*\(end ([\d.-]+) ([\d.-]+)\)', block):
            pts.extend([(float(rm.group(1)), float(rm.group(2))),
                        (float(rm.group(3)), float(rm.group(4)))])
        for pm in re.finditer(r'\(pad\s+\S+\s+\S+\s+\S+\s*\(at ([\d.-]+) ([\d.-]+)[^)]*\)\s*\(size ([\d.-]+) ([\d.-]+)\)', block):
            px, py = float(pm.group(1)), float(pm.group(2))
            sw, sh = float(pm.group(3)), float(pm.group(4))
            pts.extend([(px - sw/2, py - sh/2), (px + sw/2, py + sh/2)])

        if not pts:
            continue

        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        lx1, ly1, lx2, ly2 = min(xs), min(ys), max(xs), max(ys)

        # Apply rotation
        if rot != 0:
            rad = math.radians(-rot)
            corners = [(lx1, ly1), (lx2, ly1), (lx1, ly2), (lx2, ly2)]
            rc = [(x * math.cos(rad) - y * math.sin(rad),
                   x * math.sin(rad) + y * math.cos(rad)) for x, y in corners]
            lx1 = min(c[0] for c in rc)
            lx2 = max(c[0] for c in rc)
            ly1 = min(c[1] for c in rc)
            ly2 = max(c[1] for c in rc)

        # Store local bbox (relative to component center)
        bboxes[ref] = (lx1, ly1, lx2, ly2)

    return bboxes


def get_abs_bbox(ref, pos, local_bboxes):
    """Get absolute bounding box for a component."""
    x, y, rot = pos
    if ref not in local_bboxes:
        # Default small bbox for unknown components
        return (x - 1, y - 1, x + 1, y + 1)
    lx1, ly1, lx2, ly2 = local_bboxes[ref]
    return (x + lx1, y + ly1, x + lx2, y + ly2)


def boxes_overlap(b1, b2, margin=0.5):
    """Check if two bounding boxes overlap with margin."""
    return not (b1[2] + margin <= b2[0] or b2[2] + margin <= b1[0] or
                b1[3] + margin <= b2[1] or b2[3] + margin <= b1[1])


def resolve_overlaps(placement, local_bboxes, iterations=200):
    """Iteratively push overlapping components apart."""
    pos = {ref: list(p) for ref, p in placement.items()}  # mutable copies

    # Components that should NOT move (board-edge connectors)
    fixed = set()  # We'll let everything move for now

    for iteration in range(iterations):
        moved = False
        refs = list(pos.keys())

        for i in range(len(refs)):
            for j in range(i + 1, len(refs)):
                r1, r2 = refs[i], refs[j]
                b1 = get_abs_bbox(r1, pos[r1], local_bboxes)
                b2 = get_abs_bbox(r2, pos[r2], local_bboxes)

                if not boxes_overlap(b1, b2, margin=0.8):
                    continue

                # Calculate overlap amount and push direction
                ox = min(b1[2], b2[2]) - max(b1[0], b2[0])  # overlap in X
                oy = min(b1[3], b2[3]) - max(b1[1], b2[1])  # overlap in Y

                if ox <= 0 or oy <= 0:
                    continue

                # Push apart along the axis of least overlap
                push = 0.5  # push each component half the overlap + margin

                if ox < oy:
                    # Push in X
                    dx = (ox / 2 + 0.5)
                    if pos[r1][0] <= pos[r2][0]:
                        pos[r1][0] -= dx
                        pos[r2][0] += dx
                    else:
                        pos[r1][0] += dx
                        pos[r2][0] -= dx
                else:
                    # Push in Y
                    dy = (oy / 2 + 0.5)
                    if pos[r1][1] <= pos[r2][1]:
                        pos[r1][1] -= dy
                        pos[r2][1] += dy
                    else:
                        pos[r1][1] += dy
                        pos[r2][1] -= dy

                moved = True

        # Clamp to board boundaries
        for ref in refs:
            bbox = get_abs_bbox(ref, pos[ref], local_bboxes)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]

            if bbox[0] < BX:
                pos[ref][0] += (BX - bbox[0])
            if bbox[2] > BX + BW:
                pos[ref][0] -= (bbox[2] - (BX + BW))
            if bbox[1] < BY:
                pos[ref][1] += (BY - bbox[1])
            if bbox[3] > BY + BH:
                pos[ref][1] -= (bbox[3] - (BY + BH))

        if not moved:
            print(f"  Resolved all overlaps after {iteration + 1} iterations")
            break

    return {ref: tuple(p) for ref, p in pos.items()}


# ================================================================
# WRITE POSITIONS TO PCB
# ================================================================

def update_pcb(pcb_path, placement):
    with open(pcb_path, "r") as f:
        content = f.read()

    updated = 0
    for ref, (x, y, rot) in placement.items():
        ref_pattern = rf'(\(property "Reference" "{re.escape(ref)}")'
        ref_matches = list(re.finditer(ref_pattern, content))
        if not ref_matches:
            continue

        for ref_match in ref_matches:
            pos = ref_match.start()
            fp_start = content.rfind("\t(footprint ", 0, pos)
            if fp_start == -1:
                continue

            at_pattern = r'\(at ([-\d.]+) ([-\d.]+)( [-\d.]+)?\)'
            search_region = content[fp_start:pos]
            at_match = re.search(at_pattern, search_region)
            if at_match:
                x_r = round(x, 2)
                y_r = round(y, 2)
                new_at = f"(at {x_r} {y_r} {int(rot)})" if rot != 0 else f"(at {x_r} {y_r})"
                abs_start = fp_start + at_match.start()
                abs_end = fp_start + at_match.end()
                content = content[:abs_start] + new_at + content[abs_end:]
                updated += 1
                break

    # Update board outline
    content = re.sub(r'\t\(gr_line \(start [^)]+\) \(end [^)]+\).*?\(layer "Edge\.Cuts"\).*?\)\n', '', content)
    content = re.sub(r'\t\(gr_rect \(start [^)]+\) \(end [^)]+\).*?\(layer "Edge\.Cuts"\).*?\)\n', '', content)
    content = re.sub(r'\t\(gr_line \(start [^)]+\) \(end [^)]+\).*?\(layer "Dwgs\.User"\).*?\)\n', '', content)

    x1, y1 = BX, BY
    x2, y2 = BX + BW, BY + BH
    hv_x = HV_BOUNDARY

    outline = f"""
\t(gr_line (start {x1} {y1}) (end {x2} {y1})
\t\t(stroke (width 0.1) (type default)) (layer "Edge.Cuts") (uuid "b0a00001-0000-0000-0000-000000000001"))
\t(gr_line (start {x2} {y1}) (end {x2} {y2})
\t\t(stroke (width 0.1) (type default)) (layer "Edge.Cuts") (uuid "b0a00002-0000-0000-0000-000000000002"))
\t(gr_line (start {x2} {y2}) (end {x1} {y2})
\t\t(stroke (width 0.1) (type default)) (layer "Edge.Cuts") (uuid "b0a00003-0000-0000-0000-000000000003"))
\t(gr_line (start {x1} {y2}) (end {x1} {y1})
\t\t(stroke (width 0.1) (type default)) (layer "Edge.Cuts") (uuid "b0a00004-0000-0000-0000-000000000004"))
\t(gr_line (start {hv_x} {y1}) (end {hv_x} {y2})
\t\t(stroke (width 0.3) (type dash)) (layer "Dwgs.User") (uuid "b0a00005-0000-0000-0000-000000000005"))
"""

    last_paren = content.rfind(")")
    content = content[:last_paren] + outline + content[last_paren:]

    with open(pcb_path, "w") as f:
        f.write(content)

    return updated, content


# ================================================================
# MAIN
# ================================================================

if __name__ == "__main__":
    # Step 1: Write initial placement
    print("Step 1: Writing initial placement...")
    with open(PCB_FILE, "r") as f:
        pcb = f.read()

    updated, pcb = update_pcb(PCB_FILE, PLACEMENT)
    print(f"  Placed {updated} components")

    # Step 2: Read back and extract bounding boxes
    print("Step 2: Extracting bounding boxes...")
    with open(PCB_FILE, "r") as f:
        pcb = f.read()
    local_bboxes = extract_bboxes(pcb)
    print(f"  Found {len(local_bboxes)} footprint bboxes")

    # Show largest
    for ref in sorted(local_bboxes, key=lambda r: (local_bboxes[r][2]-local_bboxes[r][0])*(local_bboxes[r][3]-local_bboxes[r][1]), reverse=True)[:10]:
        b = local_bboxes[ref]
        print(f"    {ref:6s} {b[2]-b[0]:.0f}x{b[3]-b[1]:.0f}mm")

    # Step 3: Count initial overlaps
    refs = list(PLACEMENT.keys())
    overlaps_before = 0
    for i in range(len(refs)):
        for j in range(i + 1, len(refs)):
            b1 = get_abs_bbox(refs[i], PLACEMENT[refs[i]], local_bboxes)
            b2 = get_abs_bbox(refs[j], PLACEMENT[refs[j]], local_bboxes)
            if boxes_overlap(b1, b2):
                overlaps_before += 1
    print(f"\nStep 3: Initial overlaps: {overlaps_before}")

    # Step 4: Resolve overlaps
    print("Step 4: Resolving overlaps...")
    resolved = resolve_overlaps(PLACEMENT, local_bboxes, iterations=500)

    # Step 5: Write resolved placement
    print("Step 5: Writing resolved placement...")
    # Re-read original PCB (before our initial write mangled it)
    updated, _ = update_pcb(PCB_FILE, resolved)
    print(f"  Updated {updated} components")

    # Step 6: Verify
    with open(PCB_FILE, "r") as f:
        pcb = f.read()
    local_bboxes = extract_bboxes(pcb)

    overlaps_after = 0
    overlap_pairs = []
    for i in range(len(refs)):
        for j in range(i + 1, len(refs)):
            b1 = get_abs_bbox(refs[i], resolved[refs[i]], local_bboxes)
            b2 = get_abs_bbox(refs[j], resolved[refs[j]], local_bboxes)
            if boxes_overlap(b1, b2):
                overlaps_after += 1
                overlap_pairs.append((refs[i], refs[j]))

    print(f"\nResult: {overlaps_before} → {overlaps_after} overlaps")
    if overlap_pairs:
        for a, b in overlap_pairs[:20]:
            print(f"  {a} <-> {b}")

    # Check board bounds
    out = 0
    for ref in refs:
        b = get_abs_bbox(ref, resolved[ref], local_bboxes)
        if b[0] < BX or b[2] > BX + BW or b[1] < BY or b[3] > BY + BH:
            print(f"  OUT: {ref} ({b[0]:.0f},{b[1]:.0f})-({b[2]:.0f},{b[3]:.0f})")
            out += 1

    print(f"Board: {BW}x{BH}mm, edges ({BX},{BY})-({BX+BW},{BY+BH})")
    print(f"Components outside board: {out}")
