"""Trace the reference accents into SVG paths for existing visual variants.

Run `python trace_reference_markers.py /path/to/reference.png` to regenerate
the optional JSX fragments. The reference bitmap is never bundled in the app.
"""
from collections import defaultdict
from pathlib import Path
import sys

import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation, label

root = Path(__file__).parent
if len(sys.argv)!=2:
    raise SystemExit('Usage: python trace_reference_markers.py /path/to/supplied-reference.png')
reference = Path(sys.argv[1])
source = np.asarray(Image.open(reference).convert('RGB'),dtype=np.uint8)
parts = {
    'reference-cd30':(153,48,202,109, 'coral'),
    'reference-cd7':(15,155,63,202, 'purple'),
    'reference-cd4':(64,51,97,105, 'blue'),
    'reference-ki67':(137,187,176,224, 'green'),
}

def segment(rgb, kind):
    r,g,b = [rgb[:,:,k].astype(int) for k in range(3)]
    if kind=='coral': base=(r-g>55)&(r-b>57)&(r>158)
    elif kind=='purple': base=(r-g>30)&(b-g>42)&(b>96)
    elif kind=='blue': base=(b-r>32)&(b-g>18)&(r<150)
    else: base=(g-r>24)&(g-b>8)&(g<185)
    if kind!='green':
        groups,n=label(base)
        if n:
            sizes=np.bincount(groups.ravel());sizes[0]=0
            base=groups==np.argmax(sizes)
    else: base=binary_dilation(base,iterations=1)
    return np.uint8(binary_dilation(base,iterations=1))

chunks=[]
for variant,(x0,y0,x1,y1,kind) in parts.items():
    rgb=source[y0:y1,x0:x1]
    height,width=rgb.shape[:2]
    mask=segment(rgb,kind)
    image=Image.fromarray(rgb).quantize(colors=64, method=Image.Quantize.MEDIANCUT,
                                         dither=Image.Dither.NONE)
    color_index=np.asarray(image)
    palette=image.getpalette()
    runs=defaultdict(list)
    for y in range(height):
        x=0
        while x<width:
            if not mask[y,x]:
                x+=1;continue
            c=int(color_index[y,x]);end=x+1
            while end<width and mask[y,end] and color_index[y,end]==c:end+=1
            runs[c].append(f'M{x} {y}h{end-x}v1H{x}z')
            x=end
    scale_x,scale_y=80/width,80/height
    chunks.append(f"  '{variant}': <g transform=\"scale({scale_x:.6f} {scale_y:.6f})\">")
    for c,paths in sorted(runs.items()):
        red,green,blue=palette[c*3:c*3+3]
        chunks.append(f'    <path fill="#{red:02x}{green:02x}{blue:02x}" d="{"".join(paths)}"/>')
    chunks.append('  </g>,')

out = '''// Auto-generated source-derived shapes. Existing MarkerVisual owns result
// states, size, orientation, selection and marker-name independence.
import type { ReactElement } from 'react';
export const referenceTraces: Record<string,ReactElement> = {
'''+'\n'.join(chunks)+'\n};\n'
destination=root.parent/'components'/'markers'/'referenceTraces.tsx'
destination.write_text(out)
print(f'Wrote {destination}, {len(out)} characters')
