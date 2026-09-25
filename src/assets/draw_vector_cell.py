"""Author the Cell Lab cell as editable SVG shapes, without sampling pixels.

The arrays below describe intentional folds and organic contours in the
244 × 259 reference coordinate system. Receptors remain separate React SVGs.
"""

from math import cos, sin, pi
from pathlib import Path
from random import Random

ROOT = Path(__file__).parent


def contour(points):
    """Closed smooth path through hand-positioned membrane landmarks."""
    n = len(points)
    parts = [f'M{points[0][0]:.2f} {points[0][1]:.2f}']
    for i in range(n):
        previous, start, end, following = (
            points[(i - 1) % n], points[i], points[(i + 1) % n], points[(i + 2) % n]
        )
        c1 = (start[0] + (end[0] - previous[0]) / 6,
              start[1] + (end[1] - previous[1]) / 6)
        c2 = (end[0] - (following[0] - start[0]) / 6,
              end[1] - (following[1] - start[1]) / 6)
        parts.append(f'C{c1[0]:.2f} {c1[1]:.2f} {c2[0]:.2f} {c2[1]:.2f} {end[0]:.2f} {end[1]:.2f}')
    return ' '.join(parts) + 'Z'


outer = contour([
    (116,72),(124,73),(132,69),(142,72),(152,74),(163,78),(173,79),
    (183,88),(189,96),(199,105),(202,116),(207,126),(207,138),
    (213,148),(209,158),(213,169),(207,182),(206,195),(199,207),
    (198,219),(188,228),(181,237),(169,243),(155,249),(144,248),
    (132,253),(121,249),(109,249),(100,243),(86,242),(77,235),
    (68,226),(63,215),(55,207),(51,195),(50,181),(47,170),
    (49,157),(48,146),(51,136),(52,123),(57,113),(63,103),
    (71,94),(77,84),(87,81),(97,76),(108,77)
])
inner = contour([
    (117,90),(130,89),(142,89),(154,92),(164,96),(177,101),
    (184,112),(193,121),(195,135),(198,147),(196,160),(199,173),
    (195,185),(191,198),(184,210),(174,222),(162,228),(148,232),
    (133,236),(122,233),(108,232),(96,227),(86,220),(75,211),
    (68,199),(63,189),(60,177),(59,161),(62,149),(62,135),
    (68,125),(72,112),(83,105),(91,96),(105,93)
])
core = contour([
    (111,103),(127,99),(144,100),(157,103),(169,111),(178,119),
    (184,134),(187,148),(188,164),(185,182),(178,198),(166,212),
    (149,220),(131,225),(113,223),(96,218),(84,208),(75,196),
    (69,178),(69,163),(72,145),(79,131),(88,119),(99,109)
])
nucleus = ('M101 139 C106 133 111 128 122 126 C131 120 144 121 153 124 '
           'C161 127 167 134 171 146 C176 158 174 174 170 184 '
           'C166 199 155 206 142 211 C129 215 115 214 105 210 '
           'C93 205 87 196 85 185 C81 172 87 160 93 150 '
           'C96 145 98 142 101 139Z')

def petal(rng, cx, cy, rx, ry, angle, color, opacity):
    # Each fold has an independent irregular contour, broad colored underside,
    # and short interior glint. No pixel-color posterization or tiled pattern.
    d = ('M -1 -.94 C .34 -1.13 .82 -.72 .96 -.19 '
         'C 1.14 .22 .73 .81 .16 1.00 '
         'C -.31 1.10 -.89 .72 -1.02 .23 '
         'C -1.18 -.21 -.89 -.66 -1 -.94Z')
    angle += rng.uniform(-12,12)
    return (f'<g transform="translate({cx:.2f} {cy:.2f}) rotate({angle:.1f}) '
            f'scale({rx:.2f} {ry:.2f})" opacity="{opacity:.2f}">'
            f'<path d="{d}" fill="url(#{color})"/>'
            '<path d="M-.74 -.3 C-.55 -.80 -.13 -.85 .31 -.67" '
            'fill="none" stroke="#fff" stroke-opacity=".44" '
            'stroke-width=".13" stroke-linecap="round"/>'
            '</g>')


DEFS = '''<defs>
  <radialGradient id="body" cx="41%" cy="37%" r="77%">
    <stop stop-color="#f4f9ff"/><stop offset=".24" stop-color="#d7edff"/>
    <stop offset=".58" stop-color="#cfddfa"/><stop offset=".83" stop-color="#c8c4f1"/>
    <stop offset="1" stop-color="#a9a9da"/>
  </radialGradient>
  <radialGradient id="cortex" cx="43%" cy="34%" r="69%">
    <stop stop-color="#f4f9ff" stop-opacity=".9"/>
    <stop offset=".44" stop-color="#c9e9fb" stop-opacity=".82"/>
    <stop offset=".76" stop-color="#a7cbea" stop-opacity=".63"/>
    <stop offset="1" stop-color="#b2b1e4" stop-opacity=".47"/>
  </radialGradient>
  <radialGradient id="innerLight" cx="38%" cy="30%" r="77%">
    <stop stop-color="#d5f3ff" stop-opacity=".67"/>
    <stop offset=".57" stop-color="#c1def4" stop-opacity=".55"/>
    <stop offset="1" stop-color="#a8bfe5" stop-opacity=".30"/>
  </radialGradient>
  <radialGradient id="foldLav" cx="34%" cy="26%" r="78%">
    <stop stop-color="#fff" stop-opacity=".92"/>
    <stop offset=".29" stop-color="#f3eaff" stop-opacity=".90"/>
    <stop offset=".70" stop-color="#d5c9f6" stop-opacity=".74"/>
    <stop offset="1" stop-color="#9c94d3" stop-opacity=".18"/>
  </radialGradient>
  <radialGradient id="foldBlue" cx="30%" cy="24%" r="84%">
    <stop stop-color="#fff" stop-opacity=".92"/>
    <stop offset=".32" stop-color="#e4f7ff" stop-opacity=".93"/>
    <stop offset=".75" stop-color="#b5d5f1" stop-opacity=".80"/>
    <stop offset="1" stop-color="#8ba8d8" stop-opacity=".16"/>
  </radialGradient>
  <radialGradient id="foldPink" cx="34%" cy="25%" r="82%">
    <stop stop-color="#fff9ff" stop-opacity=".96"/>
    <stop offset=".34" stop-color="#f3dff8" stop-opacity=".8"/>
    <stop offset=".75" stop-color="#dac0ed" stop-opacity=".62"/>
    <stop offset="1" stop-color="#bc99df" stop-opacity=".11"/>
  </radialGradient>
  <radialGradient id="nucleus" cx="29%" cy="21%" r="84%">
    <stop stop-color="#d1bbee"/><stop offset=".23" stop-color="#a18cd1"/>
    <stop offset=".58" stop-color="#7768b4"/>
    <stop offset=".89" stop-color="#5e519e"/>
    <stop offset="1" stop-color="#4d4b8c"/>
  </radialGradient>
  <linearGradient id="nucleusSheen" x1="0" y1="0" x2=".86" y2="1">
    <stop stop-color="#f8f1ff" stop-opacity=".76"/>
    <stop offset=".47" stop-color="#e3d2f9" stop-opacity=".23"/>
    <stop offset="1" stop-color="#5f4a9a" stop-opacity=".22"/>
  </linearGradient>
  <radialGradient id="nuclearPearl" cx="25%" cy="20%" r="78%">
    <stop stop-color="#f3e6ff" stop-opacity=".73"/>
    <stop offset=".39" stop-color="#d6c2f3" stop-opacity=".43"/>
    <stop offset="1" stop-color="#705ba8" stop-opacity=".04"/>
  </radialGradient>
  <radialGradient id="mint" cx="46%" cy="37%" r="66%">
    <stop stop-color="#d9fff3" stop-opacity=".64"/>
    <stop offset=".78" stop-color="#b8efdf" stop-opacity=".36"/>
    <stop offset="1" stop-color="#a8e3d8" stop-opacity="0"/>
  </radialGradient>
  <filter id="contact" x="-35%" y="-30%" width="170%" height="185%">
    <feGaussianBlur stdDeviation="3.1"/>
  </filter>
  <filter id="aura" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="6"/>
  </filter>
  <clipPath id="silhouette"><path d="''' + outer + '''"/></clipPath>
  <clipPath id="nucleusClip"><path d="''' + nucleus + '''"/></clipPath>
</defs>'''


def draw(with_mint):
    rng = Random(41726)
    bits = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 244 259" '
            'preserveAspectRatio="xMidYMin slice" aria-hidden="true">',
            '<!-- Intentional vector reconstruction: smooth contours, independent folds, local light. -->',
            DEFS,
            '<ellipse cx="133" cy="164" rx="82" ry="86" fill="#bab5f1" opacity=".19" filter="url(#aura)"/>',
            f'<path d="{outer}" fill="#8a7fc2" opacity=".14" '
            'transform="translate(0 3)" filter="url(#contact)"/>',
            f'<path d="{outer}" fill="url(#body)" stroke="#ede3ff" '
            'stroke-width=".75" stroke-opacity=".35"/>',
            f'<g clip-path="url(#silhouette)">',
            '<path d="M54 146 C52 91 96 69 135 75 C193 76 216 123 208 159 '
            'C192 137 181 106 143 92 C102 77 78 106 54 146Z" '
            'fill="#fbf1ff" opacity=".31"/>',
            '<path d="M62 188 C88 221 143 258 183 228 C198 216 209 181 209 167 '
            'C194 195 173 226 127 221 C91 218 73 198 62 188Z" '
            'fill="#979ad5" opacity=".23"/>',
            '<path d="M187 86 C206 104 211 140 209 171 C199 164 202 129 181 111Z" '
            'fill="#edbfe7" opacity=".20"/>']

    # Two interlaced belts of translucent, uneven membrane folds. Their
    # overlaps form the luminous ruffled rim seen in the reference.
    for belt, number, distance, rx, ry in [(0,43,.89,7.2,9.4),(1,37,.73,8.2,10.3)]:
        for i in range(number):
            t = -pi/2 + 2*pi*(i + (.29 if belt else 0))/number
            t += rng.uniform(-.038,.038)
            radial = distance + rng.uniform(-.065,.065)
            x = 130 + 79*cos(t)*radial
            y = 161 + 88*sin(t)*radial
            x += rng.uniform(-2.2,2.2); y += rng.uniform(-2.1,2.1)
            color = ('foldPink' if i%11 in (0,1) and t < -.15 else
                     'foldLav' if (i+belt)%3 else 'foldBlue')
            bits.append(petal(rng,x,y,rx*rng.uniform(.76,1.34),
                              ry*rng.uniform(.72,1.27),t*180/pi+96,
                              color,rng.uniform(.40,.71)))

    bits.extend([
        f'<path d="{inner}" fill="url(#cortex)" stroke="#f7f1ff" '
        'stroke-opacity=".51" stroke-width="1.25"/>',
        f'<path d="{core}" fill="url(#innerLight)"/>',
        '<path d="M64 147 C74 115 88 101 115 93 C135 87 162 97 181 119" '
        'fill="none" stroke="#fff" stroke-width="5" stroke-opacity=".24" stroke-linecap="round"/>',
        '<path d="M73 184 C76 216 105 231 135 231 C166 232 188 207 195 182" '
        'fill="none" stroke="#f6f2ff" stroke-width="4.3" stroke-opacity=".29" stroke-linecap="round"/>',
    ])

    # Interior folds have independent geometry rather than a repeated tile.
    for i, (x,y,sx,sy,turn) in enumerate([
        (89,111,9,10,-28),(103,100,8,7,18),(120,94,9,7,-12),
        (143,96,9,8,22),(161,103,10,9,-31),(176,114,8,9,12),
        (187,134,7,10,40),(192,153,7,8,-5),(187,174,8,10,24),
        (182,195,9,9,-37),(170,211,8,8,15),(150,224,9,7,-12),
        (127,229,10,7,28),(105,224,9,9,-29),(88,214,9,10,33),
        (75,200,8,11,-19),(68,180,8,11,33),(67,160,8,10,-22),
        (75,139,9,11,22),(85,125,8,9,-16),(105,118,7,9,35),
        (127,111,7,9,-35),(148,112,9,9,10),(166,125,8,10,33),
        (174,149,8,10,-28),(172,182,9,9,14),(155,203,8,9,28),
        (110,204,8,8,-12),(90,187,7,11,35),(82,166,7,10,-20),
        (96,144,8,9,42),(114,129,7,9,18),(141,130,7,8,-38),
    ]):
        bits.append(petal(rng,x,y,sx,sy,turn,
                          'foldBlue' if i%3 else 'foldLav',
                          .39 if i%4 else .53))

    # Boundary glow is a fine uneven contour, not a blur over the cell.
    bits.extend([
        f'<path d="{outer}" fill="none" stroke="#fff" stroke-width="1.5" '
        'stroke-opacity=".31"/>',
        '<path d="M66 149 C65 118 91 91 122 85 C148 79 174 94 188 112" '
        'fill="none" stroke="#fff" stroke-opacity=".42" stroke-width="1.6" '
        'stroke-linecap="round"/>',
        '<path d="M52 174 C52 210 88 244 129 246" fill="none" '
        'stroke="#f7f3ff" stroke-opacity=".48" stroke-width="1.7" '
        'stroke-linecap="round"/>',
        '</g>',
        # Nucleus: one sculpted contour, translucent rim, organelle texture.
        f'<path d="{nucleus}" fill="#9684c8" opacity=".17" '
        'transform="translate(1.2 1.6)" filter="url(#contact)"/>',
        f'<path d="{nucleus}" fill="url(#nucleus)" stroke="#8a79bd" '
        'stroke-width="1.4" stroke-opacity=".58"/>',
        f'<g clip-path="url(#nucleusClip)">',
        '<path d="M84 176 C89 131 120 120 150 124 C171 125 185 145 177 170 '
        'C163 144 152 129 132 135 C108 142 105 157 93 179Z" '
        'fill="url(#nucleusSheen)" opacity=".68"/>',
        '<path d="M86 184 C96 202 121 216 142 211 C160 209 177 185 175 161 '
        'C166 181 153 192 138 190 C116 186 105 169 86 184Z" '
        'fill="#483f88" opacity=".24"/>',
    ])

    for i,(x,y,rx,ry,alpha) in enumerate([
        (118,145,10,5,.40),(145,137,12,6,.38),(158,147,9,8,.29),
        (112,164,9,7,.42),(129,154,12,6,.26),(147,165,10,8,.35),
        (162,179,11,7,.28),(121,185,11,8,.29),(102,191,10,7,.27),
        (137,197,11,8,.24),(106,151,5,7,.30),(140,179,8,7,.29),
        (119,205,8,6,.23),(154,196,9,7,.23),(127,135,9,4,.38)
    ]):
        bits.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" '
                    f'fill="url(#nuclearPearl)" opacity="{alpha/.55:.2f}" '
                    f'transform="rotate({(i*19)%61-30} {x} {y})"/>')

    bits.extend([
        '<path d="M96 151 C100 136 117 128 131 125 C146 121 161 131 167 141" '
        'fill="none" stroke="#f3e4ff" stroke-opacity=".38" '
        'stroke-width="2.4" stroke-linecap="round"/>',
        '<path d="M87 181 C87 197 101 210 119 212" fill="none" '
        'stroke="#bca7e4" stroke-opacity=".38" stroke-width="2.1" '
        'stroke-linecap="round"/>',
        '</g>',
    ])
    if with_mint:
        bits.append('<path d="M145 195 C153 187 168 184 178 188 C185 194 188 205 '
                    '183 215 C177 228 159 233 146 227 C135 220 135 205 145 195Z" '
                    'fill="url(#mint)"/>')
    bits.append('</svg>')
    return '\n'.join(bits) + '\n'


(ROOT/'cell-vector.svg').write_text(draw(True))
(ROOT/'cell-vector-clean.svg').write_text(draw(False))
print('Wrote intentional vector cell assets')
