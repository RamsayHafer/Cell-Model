"""Generate an editable, layered SVG cell study from the supplied reference.

The output contains native SVG paths, gradients, clips and filters. It does not
embed the reference raster. Run this file to regenerate cell-reference.svg.
"""
from __future__ import annotations

from math import cos, pi, sin
from pathlib import Path
from random import Random

R = Random(27)
PARTS: list[str] = []


def spline(points: list[tuple[float, float]]) -> str:
    """Closed Catmull-Rom curve expressed as editable cubic SVG segments."""
    out = [f"M {points[0][0]:.1f} {points[0][1]:.1f}"]
    n = len(points)
    for i in range(n):
        p0, p1, p2, p3 = [points[(i + k) % n] for k in (-1, 0, 1, 2)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        out.append(f"C {c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}")
    return " ".join(out) + " Z"


def contour(cx: float, cy: float, rx: float, ry: float, count: int, phase: float, wobble: float) -> str:
    points = []
    for i in range(count):
        t = 2 * pi * i / count + phase
        bulge = 1 + wobble * (.52 * sin(t * 7 + .7) + .33 * sin(t * 11 + 1.8)
                              + .23 * cos(t * 17 - .4))
        points.append((cx + rx * bulge * cos(t), cy + ry * bulge * sin(t)))
    return spline(points)


outer = contour(219, 222, 166, 178, 52, .08, .068)
inner = contour(219, 221, 148, 157, 45, .13, .049)
cyto = contour(218, 222, 131, 140, 37, .16, .038)
nucleus = (
    "M 129 245 C 127 224 135 204 150 188 C 166 170 176 150 198 146 "
    "C 211 141 229 143 241 149 C 262 149 268 165 282 178 "
    "C 299 197 305 219 302 242 C 300 263 290 281 276 296 "
    "C 258 319 226 329 198 322 C 177 322 157 312 145 296 "
    "C 132 283 126 264 129 245 Z"
)

PARTS.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 440" role="img"
  aria-label="Soft lavender ruffled immune cell, pale blue cytoplasm and irregular purple nucleus">
<defs>
  <radialGradient id="membrane" cx="37%" cy="26%" r="77%">
    <stop stop-color="#fffafd"/><stop offset=".31" stop-color="#f0eafa"/>
    <stop offset=".7" stop-color="#d5c8ed"/><stop offset="1" stop-color="#aaa0d7"/>
  </radialGradient>
  <radialGradient id="pearl" cx="31%" cy="23%" r="76%">
    <stop stop-color="#fff" stop-opacity=".94"/><stop offset=".29" stop-color="#f4f1ff" stop-opacity=".9"/>
    <stop offset=".7" stop-color="#d9cdec" stop-opacity=".85"/>
    <stop offset="1" stop-color="#ac9ed7" stop-opacity=".91"/>
  </radialGradient>
  <radialGradient id="blueBody" cx="33%" cy="23%" r="77%">
    <stop stop-color="#f9ffff"/><stop offset=".4" stop-color="#e1f3ff"/>
    <stop offset=".77" stop-color="#c5e1f4"/><stop offset="1" stop-color="#a8b8dc"/>
  </radialGradient>
  <radialGradient id="blueFold" cx="27%" cy="23%" r="76%">
    <stop stop-color="#fff" stop-opacity=".88"/><stop offset=".45" stop-color="#e7f6ff" stop-opacity=".66"/>
    <stop offset="1" stop-color="#a9c5ed" stop-opacity=".35"/>
  </radialGradient>
  <radialGradient id="nuclear" cx="33%" cy="22%" r="77%">
    <stop stop-color="#d9c6f6"/><stop offset=".38" stop-color="#b499df"/>
    <stop offset=".72" stop-color="#8466b7"/><stop offset="1" stop-color="#644b9a"/>
  </radialGradient>
  <radialGradient id="nuclearFold" cx="30%" cy="23%" r="75%">
    <stop stop-color="#d7c1ef" stop-opacity=".75"/>
    <stop offset=".52" stop-color="#a284d1" stop-opacity=".42"/>
    <stop offset="1" stop-color="#664a9a" stop-opacity=".3"/>
  </radialGradient>
  <filter id="cellShadow" x="-30%" y="-30%" width="160%" height="170%">
    <feGaussianBlur stdDeviation="11"/>
  </filter>
  <filter id="softEdge" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation=".9"/>
  </filter>
  <filter id="bloom" x="-35%" y="-35%" width="170%" height="170%">
    <feGaussianBlur stdDeviation="7"/>
  </filter>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency=".085" numOctaves="2" seed="9"/>
    <feColorMatrix type="saturate" values="0"/>
    <feComponentTransfer><feFuncA type="linear" slope=".045"/></feComponentTransfer>
  </filter>
  <clipPath id="cellClip"><path d="{outer}"/></clipPath>
  <clipPath id="cytoClip"><path d="{cyto}"/></clipPath>
  <clipPath id="nucleusClip"><path d="{nucleus}"/></clipPath>
</defs>
<ellipse cx="222" cy="379" rx="136" ry="28" fill="#7e74b2" fill-opacity=".17" filter="url(#cellShadow)"/>
<path d="{outer}" fill="url(#membrane)" stroke="#ece4ff" stroke-width="2"/>
<g clip-path="url(#cellClip)">
  <path d="{inner}" fill="#dcd3f2" fill-opacity=".85"/>
''')

# Overlapping irregular lavender lobes form a puffy perimeter, with their
# translucent light faces blending into the blue center.
for i in range(38):
    t = 2 * pi * i / 38 + .06
    radius = R.uniform(140, 159)
    x = 219 + radius * cos(t)
    y = 222 + radius * 1.06 * sin(t)
    rx = R.uniform(17, 26)
    ry = R.uniform(19, 29)
    shape = contour(x, y, rx, ry, 14, t, .13)
    PARTS.append(f'<path d="{shape}" fill="url(#pearl)" opacity="{R.uniform(.63,.91):.2f}" '
                 f'stroke="#fbf7ff" stroke-opacity=".47" stroke-width="1.1"/>')

PARTS.append(f'''<path d="{cyto}" fill="url(#blueBody)" fill-opacity=".92"
  stroke="#f8ffff" stroke-opacity=".72" stroke-width="2.4"/>
<g clip-path="url(#cytoClip)">
''')

# Broad feathered shapes replace a tiled-circle pattern. Different depths and
# sizes create the low-frequency, cloudlike translucency in the supplied cell.
for i in range(50):
    t = R.random() * 2 * pi
    dist = (R.random() ** .68) * 127
    x = 218 + cos(t) * dist
    y = 222 + sin(t) * dist * 1.06
    rx, ry = R.uniform(12, 34), R.uniform(12, 32)
    shape = contour(x, y, rx, ry, 13, t, .11)
    PARTS.append(f'<path d="{shape}" fill="url(#blueFold)" opacity="{R.uniform(.28,.64):.2f}" '
                 f'filter="url(#softEdge)"/>')

PARTS.append('''<ellipse cx="160" cy="140" rx="95" ry="69" fill="#fff" fill-opacity=".2" filter="url(#bloom)"/>
</g><path d="''' + cyto + '''" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="2"/>
<path d="''' + outer + '''" fill="url(#grain)" opacity=".55"/>
</g>
''')

# The asymmetrical nucleus has a soft indigo underpainting and multiple raised
# lobes. Everything remains individually editable in the generated SVG.
PARTS.append(f'''<path d="{nucleus}" fill="#69539e" fill-opacity=".3"
  transform="translate(2 5)" filter="url(#bloom)"/>
<path d="{nucleus}" fill="url(#nuclear)" stroke="#f0e4ff" stroke-opacity=".7" stroke-width="2"/>
<g clip-path="url(#nucleusClip)">
  <ellipse cx="192" cy="174" rx="83" ry="58" fill="#e9d8ff" fill-opacity=".18" filter="url(#bloom)"/>
''')
for i in range(22):
    t = R.random() * 2 * pi
    radius = R.uniform(12, 79)
    x = 216 + cos(t) * radius
    y = 233 + sin(t) * radius * .92
    rx, ry = R.uniform(14, 34), R.uniform(12, 28)
    shape = contour(x, y, rx, ry, 12, t, .1)
    PARTS.append(f'<path d="{shape}" fill="url(#nuclearFold)" opacity="{R.uniform(.28,.63):.2f}"/>')
PARTS.append(f'''<path d="{nucleus}" fill="url(#grain)" opacity=".6"/>
</g>
<path d="M145 200 C167 161 211 147 245 155" fill="none" stroke="#f9eaff"
  stroke-opacity=".17" stroke-width="3" stroke-linecap="round" filter="url(#softEdge)"/>
</svg>''')

target = Path(__file__).with_name('cell-reference.svg')
target.write_text('\n'.join(PARTS) + '\n')
print(f'Wrote {target}')
