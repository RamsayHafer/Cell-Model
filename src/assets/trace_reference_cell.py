"""Rebuild the supplied cell as native SVG color paths.

The reference image is used offline to sample its painterly texture. Saturated
receptors are removed before tracing because React renders those separately.
The shipped SVG contains paths only: no embedded raster or runtime dependency.
"""
from collections import defaultdict
from pathlib import Path
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy.ndimage import binary_dilation, distance_transform_edt, gaussian_filter

ROOT = Path(__file__).parent
if len(sys.argv) != 2:
    raise SystemExit('Usage: python trace_reference_cell.py /path/to/supplied-reference.png')
source = np.asarray(Image.open(sys.argv[1]).convert('RGB'), dtype=np.uint8)
height, width, _ = source.shape
yy, xx = np.mgrid[:height, :width]

# Remove baked-in saturated receptor pixels while keeping the cell's folds.
# The small halo around each silhouette is filled from the nearest cell color.
red = (source[:,:,0].astype(int) - source[:,:,1].astype(int) > 39)
blue = (source[:,:,2].astype(int) - source[:,:,0].astype(int) > 24) & (source[:,:,0] < 190)
violet = ((source[:,:,0].astype(int) + source[:,:,2].astype(int))/2 - source[:,:,1] > 21) & (source[:,:,0] < 180)
green = (source[:,:,1].astype(int) - source[:,:,0].astype(int) > 12) & (source[:,:,1] < 196)
remove = (
    (blue & (xx>64)&(xx<95)&(yy>52)&(yy<103)) |
    (red & (xx>155)&(xx<203)&(yy>49)&(yy<109)) |
    (violet & (xx>15)&(xx<65)&(yy>157)&(yy<199)) |
    (green & (xx>138)&(xx<176)&(yy>188)&(yy<224))
)
remove = binary_dilation(remove, iterations=2)
_, nearest = distance_transform_edt(remove, return_indices=True)
clean = source[nearest[0], nearest[1]].copy()
smoothed = gaussian_filter(clean.astype(float), sigma=(1.25,1.25,0))
clean[remove] = np.uint8(np.clip(smoothed[remove], 0, 255))

# A feathered silhouette prevents source paper/labels from becoming a square
# background. A loose polygon preserves the irregular perimeter in the pixels.
edge = [(117,68),(130,70),(145,70),(163,75),(183,86),(201,105),
        (208,126),(213,148),(213,171),(208,193),(202,216),(188,239),
        (169,248),(147,252),(124,252),(103,246),(83,240),(66,226),
        (56,205),(49,182),(47,158),(49,132),(55,112),(67,94),(84,81)]
mask = Image.new('L', (width,height),0)
ImageDraw.Draw(mask).polygon(edge,fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(1.6))
alpha = np.asarray(mask).astype(float)/255
paper = np.array([255,252,250],dtype=float)
color_distance = np.linalg.norm(clean.astype(float)-paper,axis=2)
alpha *= np.clip((color_distance-2.5)/13,0,1)
level = np.uint8(np.clip(np.round(alpha*4),0,4))

# Median-cut color layers preserve the reference's irregular spatial texture.
# Runs of same-color pixels become compact SVG paths instead of rectangles.
poster = Image.fromarray(clean).quantize(colors=192, method=Image.Quantize.MEDIANCUT,
                                          dither=Image.Dither.NONE)
ids = np.asarray(poster)
colors = poster.getpalette()
paths: dict[tuple[int,int],list[str]] = defaultdict(list)
for y in range(height):
    x=0
    while x<width:
        a = int(level[y,x])
        if not a:
            x+=1
            continue
        c = int(ids[y,x])
        end=x+1
        while end<width and level[y,end]==a and ids[y,end]==c:
            end+=1
        paths[(c,a)].append(f'M{x} {y}h{end-x}v1H{x}z')
        x=end

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
       'preserveAspectRatio="none" aria-hidden="true">',
       '<!-- Color paths traced from the user-supplied 244 × 259 reference. -->',
       '<defs><filter id="traceSoft" x="-2%" y="-2%" width="104%" height="104%"><feGaussianBlur stdDeviation=".32"/></filter></defs>',
       '<g filter="url(#traceSoft)">']
for (c,a), segments in sorted(paths.items()):
    rgb=colors[c*3:c*3+3]
    svg.append(f'<path fill="#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}" '
               f'opacity="{a/4:.2f}" d="{"".join(segments)}"/>')
svg.extend(['</g>','</svg>'])
(ROOT/'cell-reference.svg').write_text('\n'.join(svg)+'\n')
print(f'Wrote native SVG, {len(paths)} color/alpha layers, '
      f'{sum(map(len,paths.values()))} painted runs')
