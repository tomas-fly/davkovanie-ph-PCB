#!/usr/bin/env python3
"""Swap BNC footprints from Vertical to Horizontal in PCB file."""

import re

PCB = "ph-verzion-01.kicad_pcb"
HORIZ_FP = "/Users/ing.tomaslaso/Documents/kiCad/sym/kicad-footprints/Connector_Coaxial.pretty/BNC_TEConnectivity_1478035_Horizontal.kicad_mod"

with open(PCB, "r") as f:
    pcb = f.read()

with open(HORIZ_FP, "r") as f:
    horiz_template = f.read()

# Extract geometry elements from horizontal template (fp_line, fp_circle, pad blocks)
def extract_geometry(fp_text):
    """Extract fp_line, fp_circle, fp_rect, fp_text user, pad blocks from footprint."""
    lines = []
    # Match all fp_line blocks on F.Fab and F.SilkS layers
    for m in re.finditer(r'\t(fp_line\s*\(start[^)]+\)\s*\(end[^)]+\)\s*\(stroke[^)]+\)[^)]*\)\s*\(layer "[^"]+"\)\s*\(uuid "[^"]+"\)\s*\))', fp_text, re.DOTALL):
        lines.append(m.group(0))
    for m in re.finditer(r'\t(fp_circle\s*\(center[^)]+\)\s*\(end[^)]+\).*?\))', fp_text, re.DOTALL):
        lines.append(m.group(0))
    return lines

def extract_pads(fp_text):
    """Extract pad blocks."""
    pads = []
    for m in re.finditer(r'(\t\(pad\s+"?\d+"?\s+thru_hole\s+\w+.*?\n\t\))', fp_text, re.DOTALL):
        pads.append(m.group(1))
    return pads

# For each BNC reference (P1, P2), find and replace the footprint content
for ref in ["P1", "P2"]:
    # Find the footprint block for this reference
    ref_idx = pcb.find(f'"Reference" "{ref}"')
    ref_match = ref_idx >= 0
    if not ref_match:
        print(f"  {ref} not found in PCB!")
        continue

    # Find the footprint start
    fp_start = pcb.rfind('\t(footprint "', 0, ref_idx)

    # Find the matching end — count parentheses
    depth = 0
    fp_end = fp_start
    for i in range(fp_start, len(pcb)):
        if pcb[i] == '(':
            depth += 1
        elif pcb[i] == ')':
            depth -= 1
            if depth == 0:
                fp_end = i + 1
                break

    old_block = pcb[fp_start:fp_end]

    # Replace footprint name
    new_block = old_block.replace(
        'Connector_Coaxial:BNC_TEConnectivity_1478204_Vertical',
        'Connector_Coaxial:BNC_TEConnectivity_1478035_Horizontal'
    )

    # Replace geometry: remove old fp_line on F.Fab/F.SilkS/F.CrtYd, add new ones
    # Remove old geometry lines
    new_block = re.sub(r'\t\t\(fp_line\s*\(start[^)]+\)\s*\(end[^)]+\).*?\(layer "F\.(Fab|SilkS|CrtYd)".*?\)\n', '', new_block)

    # Remove old pads
    new_block = re.sub(r'\t\t\(pad\s+.*?\n\t\t\)', '', new_block, flags=re.DOTALL)

    # Read horizontal template geometry and pads
    with open(HORIZ_FP, "r") as f:
        tmpl = f.read()

    # Extract lines from template (indented with single tab in .kicad_mod, need double tab for PCB)
    geom_lines = []
    for m in re.finditer(r'(\t\(fp_line.*?\))\n', tmpl, re.DOTALL):
        geom_lines.append('\t' + m.group(1))  # add extra tab for PCB embedding
    for m in re.finditer(r'(\t\(fp_circle.*?\))\n', tmpl, re.DOTALL):
        geom_lines.append('\t' + m.group(1))

    # Extract pads
    pad_lines = []
    for m in re.finditer(r'(\t\(pad\s+.*?\))\n\t\(', tmpl, re.DOTALL):
        pad_lines.append('\t' + m.group(1))
    # Last pad might not have \n\t( after it
    pad_blocks = re.findall(r'(\t\(pad\s+"?\d+"?\s+thru_hole\s+\w+\s*\n(?:\t\t.*\n)*?\t\))', tmpl)

    # Simpler: just extract everything between properties and model
    geom_text = ""
    for m in re.finditer(r'\t(\(fp_line\b.*?\))\n', tmpl):
        geom_text += '\t\t' + m.group(1) + '\n'
    for m in re.finditer(r'\t(\(fp_circle\b.*?\))\n', tmpl):
        geom_text += '\t\t' + m.group(1) + '\n'
    for m in re.finditer(r'\t(\(fp_text\s+user\b.*?\))\n', tmpl):
        geom_text += '\t\t' + m.group(1) + '\n'

    # Extract pads more carefully
    pad_text = ""
    for m in re.finditer(r'\t(\(pad\s+"?\d+"?.*?\))\n', tmpl, re.DOTALL):
        pad_text += '\t\t' + m.group(1) + '\n'

    # Insert before closing paren of footprint
    # Find last ) in new_block
    insert_pos = new_block.rfind('\t)')
    if insert_pos == -1:
        insert_pos = new_block.rfind(')')

    new_block = new_block[:insert_pos] + geom_text + pad_text + new_block[insert_pos:]

    # Also update the 3D model reference
    new_block = new_block.replace(
        'BNC_TEConnectivity_1478204_Vertical.step',
        'BNC_TEConnectivity_1478035_Horizontal.step'
    )
    new_block = new_block.replace(
        'BNC_TEConnectivity_1478204_Vertical.wrl',
        'BNC_TEConnectivity_1478035_Horizontal.step'
    )

    pcb = pcb[:fp_start] + new_block + pcb[fp_end:]
    print(f"  Swapped {ref} to Horizontal BNC")

with open(PCB, "w") as f:
    f.write(pcb)
print("Done! BNC footprints swapped to Horizontal.")
