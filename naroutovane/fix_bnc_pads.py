#!/usr/bin/env python3
"""Fix broken BNC pad blocks in PCB file."""

import re, uuid

PCB = "ph-verzion-01.kicad_pcb"

with open(PCB, "r") as f:
    pcb = f.read()

# The broken pad section looks like:
# (pad "1" thru_hole rect
# (at 0 0)
# (pad "2" thru_hole circle
# ...repeated...
# It needs to be replaced with properly formatted pad blocks

BROKEN_PADS = """\t\t\t(pad "1" thru_hole rect
\t\t\t(at 0 0)
\t\t\t(pad "2" thru_hole circle
\t\t\t(at -5.025 -5.025)
\t\t\t(pad "2" thru_hole circle
\t\t\t(at -5.025 5.025)
\t\t\t(pad "2" thru_hole circle
\t\t\t(at 5.025 -5.025)
\t\t\t(pad "2" thru_hole circle
\t\t\t(at 5.025 5.025)"""

# Also try with less tabs
BROKEN_PADS2 = """\t\t(pad "1" thru_hole rect
\t\t(at 0 0)
\t\t(pad "2" thru_hole circle
\t\t(at -5.025 -5.025)
\t\t(pad "2" thru_hole circle
\t\t(at -5.025 5.025)
\t\t(pad "2" thru_hole circle
\t\t(at 5.025 -5.025)
\t\t(pad "2" thru_hole circle
\t\t(at 5.025 5.025)"""

def make_good_pads():
    """Generate properly formatted pad blocks with unique UUIDs."""
    u1 = str(uuid.uuid4())
    u2 = str(uuid.uuid4())
    u3 = str(uuid.uuid4())
    u4 = str(uuid.uuid4())
    u5 = str(uuid.uuid4())
    return f"""\t\t(pad "1" thru_hole rect
\t\t\t(at 0 0)
\t\t\t(size 3.5 3.5)
\t\t\t(drill 1.1)
\t\t\t(layers "*.Cu" "*.Mask")
\t\t\t(remove_unused_layers no)
\t\t\t(uuid "{u1}")
\t\t)
\t\t(pad "2" thru_hole circle
\t\t\t(at -5.025 -5.025)
\t\t\t(size 4 4)
\t\t\t(drill 1.5)
\t\t\t(layers "*.Cu" "*.Mask")
\t\t\t(remove_unused_layers no)
\t\t\t(uuid "{u2}")
\t\t)
\t\t(pad "2" thru_hole circle
\t\t\t(at -5.025 5.025)
\t\t\t(size 4 4)
\t\t\t(drill 1.5)
\t\t\t(layers "*.Cu" "*.Mask")
\t\t\t(remove_unused_layers no)
\t\t\t(uuid "{u3}")
\t\t)
\t\t(pad "2" thru_hole circle
\t\t\t(at 5.025 -5.025)
\t\t\t(size 4 4)
\t\t\t(drill 1.5)
\t\t\t(layers "*.Cu" "*.Mask")
\t\t\t(remove_unused_layers no)
\t\t\t(uuid "{u4}")
\t\t)
\t\t(pad "2" thru_hole circle
\t\t\t(at 5.025 5.025)
\t\t\t(size 4 4)
\t\t\t(drill 1.5)
\t\t\t(layers "*.Cu" "*.Mask")
\t\t\t(remove_unused_layers no)
\t\t\t(uuid "{u5}")
\t\t)"""

# Also need to move pads BEFORE the model block
# Current order: ...geometry... (model ...) (pad broken...)
# Correct order: ...geometry... (pad correct...) (model ...)

# Strategy: find each BNC footprint block, fix it
for ref in ["P1", "P2"]:
    idx = pcb.find(f'"Reference" "{ref}"')
    if idx < 0:
        print(f"  {ref} not found!")
        continue

    fp_start = pcb.rfind('\t(footprint "', 0, idx)

    # Find end of footprint block
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

    block = pcb[fp_start:fp_end]

    # Remove broken pads (any line starting with (pad)
    lines = block.split('\n')
    clean_lines = [l for l in lines if not l.strip().startswith('(pad ')]

    # Find the model block position and insert pads before it
    clean_block = '\n'.join(clean_lines)

    # Find embedded_fonts or model position
    model_pos = clean_block.find('\t\t(embedded_fonts')
    if model_pos < 0:
        model_pos = clean_block.find('\t\t(model ')

    if model_pos > 0:
        good_pads = make_good_pads()
        clean_block = clean_block[:model_pos] + good_pads + '\n' + clean_block[model_pos:]

    # Also remove extra blank lines
    while '\n\n\n' in clean_block:
        clean_block = clean_block.replace('\n\n\n', '\n\n')

    pcb = pcb[:fp_start] + clean_block + pcb[fp_end:]
    print(f"  Fixed {ref} pads")

with open(PCB, "w") as f:
    f.write(pcb)
print("Done! BNC pads fixed.")
