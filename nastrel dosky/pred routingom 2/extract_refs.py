#!/usr/bin/env python3
"""Extract component reference designators and positions from a KiCad PCB file."""

import re
import sys

PCB_FILE = "/Users/ing.tomaslaso/Documents/kiCad/ph-verzion-01/ph-verzion-01.kicad_pcb"

def parse_pcb(filepath):
    with open(filepath, "r") as f:
        text = f.read()

    # Find all top-level footprint blocks with their content
    # We match (footprint "..." ... ) at the top indentation level
    components = []
    # Use a simple state-machine approach: find each footprint start,
    # then track parentheses to find its end
    idx = 0
    while True:
        match = re.search(r'\n\t\(footprint "([^"]+)"', text[idx:])
        if not match:
            break
        start = idx + match.start()
        fp_name = match.group(1)

        # Walk forward counting parens to find end of this block
        depth = 0
        i = idx + match.start() + 1  # skip the newline
        while i < len(text):
            if text[i] == '(':
                depth += 1
            elif text[i] == ')':
                depth -= 1
                if depth == 0:
                    break
            i += 1
        block = text[idx + match.start():i + 1]
        idx = i + 1

        # Extract (at X Y [angle])
        at_match = re.search(r'^\t\t\(at ([\d.\-]+) ([\d.\-]+)', block, re.MULTILINE)
        if not at_match:
            continue
        x, y = float(at_match.group(1)), float(at_match.group(2))

        # Extract (property "Reference" "XX" ...)
        ref_match = re.search(r'\(property "Reference" "([^"]+)"', block)
        ref = ref_match.group(1) if ref_match else "?"

        components.append((ref, fp_name, x, y))

    return components


def main():
    components = parse_pcb(PCB_FILE)
    components.sort(key=lambda c: (re.sub(r'\d+', '', c[0]), int(re.search(r'\d+', c[0]).group()) if re.search(r'\d+', c[0]) else 0))

    # Print table
    print(f"{'Ref':<8} {'X':>9} {'Y':>9}  {'Footprint'}")
    print("-" * 80)
    for ref, fp, x, y in components:
        print(f"{ref:<8} {x:>9.3f} {y:>9.3f}  {fp}")
    print(f"\nTotal: {len(components)} components")


if __name__ == "__main__":
    main()
