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
    (113,73),(122,71),(132,69),(143,72),(151,73),(166,77),(175,82),
    (181,89),(192,96),(197,108),(204,116),(204,128),(211,139),
    (207,150),(213,161),(208,174),(212,184),(205,198),(201,211),
    (192,217),(191,231),(179,238),(168,244),(159,245),(145,251),
    (133,249),(123,252),(110,248),(99,243),(87,242),(76,233),
    (71,223),(59,215),(54,203),(53,189),(47,179),(50,168),
    (46,154),(51,143),(50,130),(57,118),(58,109),(67,99),
    (73,88),(85,83),(93,78),(105,77)
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
nucleus = ('M97 145 C102 138 110 140 117 135 C125 131 124 125 135 123 '
           'C144 120 158 124 163 134 C170 140 175 150 174 162 '
           'C177 175 169 181 168 189 C161 197 159 196 151 200 '
           'C143 203 140 213 128 212 C116 214 102 210 95 201 '
           'C85 193 83 182 87 174 C85 162 90 153 97 145Z')

FOLD_SHAPES = [
    ('M-.93 -.41 C-.95 -.83 -.46 -1.08 -.07 -.99 '
     'C.31 -1.13 .91 -.67 .95 -.18 C1.10 .22 .80 .84 .29 .96 '
     'C-.23 1.11 -.86 .75 -.99 .25 C-1.10 -.06 -.95 -.21 -.93 -.41Z'),
    ('M-.98 -.20 C-1.10 -.58 -.58 -1.03 -.22 -.91 '
     'C.16 -1.21 .78 -.73 .84 -.32 C1.19 .03 .90 .55 .35 .89 '
     'C-.14 1.16 -.51 .72 -.91 .47 C-1.09 .29 -1.12 .01 -.98 -.20Z'),
    ('M-.93 -.51 C-.67 -.88 -.52 -.77 -.20 -1.00 '
     'C.35 -1.10 .60 -.79 .84 -.49 C1.19 -.08 .94 .29 .73 .56 '
     'C.51 1.01 -.16 1.09 -.49 .76 C-1.01 .66 -1.15 -.10 -.93 -.51Z'),
    ('M-1 -.29 C-.93 -.90 -.43 -.81 -.15 -.98 '
     'C.17 -1.09 .41 -.84 .62 -.69 C1.12 -.49 1.10 .31 .75 .65 '
     'C.51 1.03 -.22 1.02 -.58 .67 C-.95 .50 -1.16 .11 -1 -.29Z'),
]


def fold(rng, cx, cy, rx, ry, angle, color, opacity):
    """One of four rounded, uneven fold contours; no repeated hard highlight."""
    d = rng.choice(FOLD_SHAPES)
    angle += rng.uniform(-27,27)
    return (f'<g transform="translate({cx:.2f} {cy:.2f}) rotate({angle:.1f}) '
            f'scale({rx:.2f} {ry:.2f})" opacity="{opacity:.2f}">'
            f'<path d="{d}" fill="url(#foldShade)" '
            'transform="translate(.19 .27)"/>'
            f'<path d="{d}" fill="url(#{color})"/>'
            '</g>')


DEFS = '''<defs>
  <radialGradient id="body" cx="41%" cy="37%" r="77%">
    <stop stop-color="#f9f9ff"/><stop offset=".24" stop-color="#e6edfc"/>
    <stop offset=".58" stop-color="#d7e2f7"/><stop offset=".83" stop-color="#d4c9f2"/>
    <stop offset="1" stop-color="#bab2e2"/>
  </radialGradient>
  <radialGradient id="cortex" cx="43%" cy="34%" r="69%">
    <stop stop-color="#f2f4ff" stop-opacity=".81"/>
    <stop offset=".44" stop-color="#d5e5fa" stop-opacity=".69"/>
    <stop offset=".76" stop-color="#c2d3ef" stop-opacity=".44"/>
    <stop offset="1" stop-color="#c5bce9" stop-opacity=".15"/>
  </radialGradient>
  <radialGradient id="innerLight" cx="38%" cy="30%" r="77%">
    <stop stop-color="#e8edff" stop-opacity=".56"/>
    <stop offset=".57" stop-color="#cad7f3" stop-opacity=".42"/>
    <stop offset="1" stop-color="#b5bfea" stop-opacity=".12"/>
  </radialGradient>
  <radialGradient id="foldLav" cx="34%" cy="26%" r="78%">
    <stop stop-color="#fff" stop-opacity=".89"/>
    <stop offset=".28" stop-color="#f8f0ff" stop-opacity=".83"/>
    <stop offset=".62" stop-color="#d9c9f8" stop-opacity=".57"/>
    <stop offset="1" stop-color="#a99bd7" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="foldBlue" cx="30%" cy="24%" r="84%">
    <stop stop-color="#fff" stop-opacity=".88"/>
    <stop offset=".32" stop-color="#e8f1ff" stop-opacity=".81"/>
    <stop offset=".68" stop-color="#b7d1f1" stop-opacity=".56"/>
    <stop offset="1" stop-color="#899fdb" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="foldPink" cx="34%" cy="25%" r="82%">
    <stop stop-color="#fff9ff" stop-opacity=".86"/>
    <stop offset=".34" stop-color="#f3dff8" stop-opacity=".82"/>
    <stop offset=".70" stop-color="#dac0ed" stop-opacity=".53"/>
    <stop offset="1" stop-color="#bc99df" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="foldShade" cx="67%" cy="74%" r="68%">
    <stop stop-color="#8f83bd" stop-opacity=".40"/>
    <stop offset=".53" stop-color="#aaa0d7" stop-opacity=".22"/>
    <stop offset="1" stop-color="#c4bced" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="nucleus" cx="29%" cy="21%" r="84%">
    <stop stop-color="#c8b5e7"/><stop offset=".23" stop-color="#af9cda"/>
    <stop offset=".58" stop-color="#8c78c0"/>
    <stop offset=".89" stop-color="#7261af"/>
    <stop offset="1" stop-color="#665aa4"/>
  </radialGradient>
  <radialGradient id="nuclearMist">
    <stop stop-color="#f0dffb" stop-opacity=".94"/>
    <stop offset=".52" stop-color="#d4bfe9" stop-opacity=".50"/>
    <stop offset="1" stop-color="#ab99d8" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="nuclearLav">
    <stop stop-color="#d7bfef" stop-opacity=".76"/>
    <stop offset=".60" stop-color="#ab94d3" stop-opacity=".39"/>
    <stop offset="1" stop-color="#ab94d3" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="cloudBlue">
    <stop stop-color="#7caadf" stop-opacity=".42"/>
    <stop offset=".51" stop-color="#9ac9e7" stop-opacity=".19"/>
    <stop offset="1" stop-color="#b5ddf7" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="cloudLav">
    <stop stop-color="#a899d5" stop-opacity=".45"/>
    <stop offset=".58" stop-color="#c8b6e9" stop-opacity=".19"/>
    <stop offset="1" stop-color="#d5c9f4" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="cloudWhite">
    <stop stop-color="#fff" stop-opacity=".83"/>
    <stop offset=".45" stop-color="#f2f7ff" stop-opacity=".37"/>
    <stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="nuclearShade">
    <stop stop-color="#594995" stop-opacity=".59"/>
    <stop offset=".56" stop-color="#6a56a3" stop-opacity=".33"/>
    <stop offset="1" stop-color="#7562ae" stop-opacity="0"/>
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

    # Membrane is a set of irregular *clusters*, not an evenly spaced ring.
    # Each anchor describes a hand-chosen pocket of lobes. Soft alpha gradients
    # let neighboring folds merge without faceted or crystalline seams.
    anchors = [
        (-94,.97,5),(-86,.83,3),(-78,1.00,5),(-66,.85,4),(-55,.93,6),
        (-41,.88,3),(-32,1.00,5),(-21,.87,4),(-9,.93,6),(5,.82,3),
        (18,1.00,4),(31,.89,5),(47,.96,6),(63,.83,4),(77,.94,5),
        (89,1.00,4),(106,.85,6),(119,.95,4),(136,.99,6),
        (148,.82,3),(162,.94,6),(177,.91,4),(193,.99,5),
        (209,.81,4),(226,.92,5),(241,1.00,4),(258,.84,5),
    ]
    for index,(degrees,distance,count) in enumerate(anchors):
        t = degrees*pi/180
        anchor_x = 130+79*cos(t)*distance
        anchor_y = 161+89*sin(t)*distance
        for j in range(count):
            x = anchor_x+rng.uniform(-8.5,8.5)
            y = anchor_y+rng.uniform(-8.0,8.0)
            color = ('foldPink' if index in (2,3,4,7,8) and j%2 else
                     'foldBlue' if (index*3+j)%5 in (0,2) else 'foldLav')
            bits.append(fold(rng,x,y,rng.uniform(4.0,10.5),
                             rng.uniform(4.8,12.3),degrees+100,
                             color,rng.uniform(.49,.87)))

    bits.extend([
        f'<path d="{inner}" fill="url(#cortex)"/>',
        f'<path d="{core}" fill="url(#innerLight)"/>',
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
        bits.append(fold(rng,x+rng.uniform(-3.3,3.3),y+rng.uniform(-3.8,3.8),
                         sx*rng.uniform(.70,1.31),sy*rng.uniform(.74,1.35),
                         turn,'foldBlue' if i%4 else 'foldLav',
                         rng.uniform(.39,.72)))

    # A few broad, translucent whorls hint at connective folds. They do not
    # outline the concentric layers or repeat around the perimeter.
    creases = [
        ('M76 132 C89 112 100 118 112 105 C121 100 131 108 138 103',11),
        ('M169 122 C184 131 174 147 186 157',8),
        ('M73 195 C81 205 95 206 100 217',10),
        ('M159 209 C172 198 175 196 180 186',9),
        ('M62 164 C69 152 69 141 79 132',8),
    ]
    for i,(d,width) in enumerate(creases):
        bits.append(f'<path d="{d}" fill="none" stroke="{("#fff" if i%3 else "#e7dcff")}" '
                    f'stroke-width="{width}" stroke-opacity=".095" '
                    'stroke-linecap="round"/>')

    # Uneven fields of color and scattered pearly lights fill gaps between
    # lobes. Radial alpha gradients fade each field without a global blur.
    color_fields = [
        (78,119,15,12,'cloudLav'),(98,109,13,9,'cloudBlue'),
        (119,105,15,9,'cloudWhite'),(148,102,16,10,'cloudBlue'),
        (177,118,15,13,'cloudLav'),(188,139,12,16,'cloudWhite'),
        (179,162,15,14,'cloudBlue'),(188,181,15,16,'cloudLav'),
        (177,201,15,14,'cloudWhite'),(154,218,17,10,'cloudBlue'),
        (132,230,16,9,'cloudLav'),(103,222,14,13,'cloudWhite'),
        (79,202,12,15,'cloudBlue'),(70,178,13,13,'cloudWhite'),
        (78,153,13,13,'cloudBlue'),(91,134,16,11,'cloudWhite'),
        (107,122,11,10,'cloudBlue'),(144,120,14,11,'cloudLav'),
        (162,133,12,13,'cloudBlue'),(160,191,14,15,'cloudWhite'),
        (115,214,16,10,'cloudBlue'),(86,181,12,12,'cloudLav'),
        (186,110,10,14,'cloudWhite'),(103,238,13,10,'cloudLav'),
    ]
    for x,y,rx,ry,shade in color_fields:
        bits.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" '
                    f'fill="url(#{shade})"/>')

    # Boundary glow is a fine uneven contour, not a blur over the cell.
    bits.extend([
        f'<path d="{outer}" fill="none" stroke="#fff" stroke-width="1.1" '
        'stroke-opacity=".24"/>',
        '<path d="M66 149 C65 118 91 91 122 85 C148 79 174 94 188 112" '
        'fill="none" stroke="#fff" stroke-opacity=".13" stroke-width="1.45" '
        'stroke-linecap="round"/>',
        '<path d="M52 174 C52 210 88 244 129 246" fill="none" '
        'stroke="#f7f3ff" stroke-opacity=".16" stroke-width="1.4" '
        'stroke-linecap="round"/>',
        '</g>',
        # Soft nested edges give the nucleus an irregular, translucent
        # boundary without blurring the SVG silhouette.
        f'<path d="{nucleus}" fill="none" stroke="#9b8bc9" '
        'stroke-width="7" stroke-opacity=".12"/>',
        f'<path d="{nucleus}" fill="none" stroke="#c9bae5" '
        'stroke-width="4.2" stroke-opacity=".19"/>',
        f'<path d="{nucleus}" fill="url(#nucleus)" opacity=".85"/>',
        f'<g clip-path="url(#nucleusClip)">',
    ])

    # Layering low-contrast, fading fields gives the nucleus mottled texture.
    # None of these patches has a visible edge or glossy pearl highlight.
    nuclear_fields = [
        (112,142,19,13,'nuclearMist',.70),(141,135,18,11,'nuclearLav',.70),
        (155,144,13,12,'nuclearShade',.61),(104,155,12,15,'nuclearLav',.56),
        (126,153,17,11,'nuclearMist',.48),(145,153,13,9,'nuclearShade',.62),
        (162,159,11,14,'nuclearMist',.48),(99,173,12,17,'nuclearShade',.53),
        (116,169,16,13,'nuclearMist',.54),(139,172,13,14,'nuclearShade',.62),
        (156,178,14,13,'nuclearLav',.66),(109,189,17,15,'nuclearLav',.51),
        (126,185,18,15,'nuclearShade',.60),(147,188,14,9,'nuclearMist',.50),
        (130,201,17,11,'nuclearMist',.41),(161,194,9,10,'nuclearShade',.55),
        (95,190,11,11,'nuclearMist',.46),(122,134,13,8,'nuclearShade',.43),
        (164,171,7,10,'nuclearShade',.55),(146,205,10,8,'nuclearLav',.48),
        (115,203,10,8,'nuclearShade',.48),(136,146,12,6,'nuclearLav',.49),
        (105,146,8,9,'nuclearMist',.43),(150,132,10,6,'nuclearMist',.38),
    ]
    for i,(x,y,rx,ry,shade,opacity) in enumerate(nuclear_fields):
        bits.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" '
                    f'fill="url(#{shade})" opacity="{opacity:.2f}" '
                    f'transform="rotate({(i*47)%119-59} {x} {y})"/>')

    # Larger overlapping pigment islands loosen the radial gradients. Their
    # fills feather to transparency, so none reads as a discrete glossy bead.
    for d,shade,opacity in [
        ('M99 147 C109 136 120 141 125 133 C132 128 143 134 148 139 C141 151 129 148 123 156 C111 159 103 156 99 147Z','nuclearMist',.60),
        ('M131 144 C142 134 149 138 155 143 C166 143 170 158 160 162 C151 169 146 156 137 161 C128 161 124 153 131 144Z','nuclearShade',.55),
        ('M91 169 C101 157 110 166 120 161 C128 163 129 177 120 181 C108 179 103 193 95 186 C87 184 86 177 91 169Z','nuclearLav',.55),
        ('M109 180 C117 169 128 171 134 177 C144 175 153 181 150 189 C144 199 134 193 124 199 C111 197 105 189 109 180Z','nuclearShade',.54),
        ('M143 169 C150 161 159 166 165 171 C169 179 160 185 156 191 C143 194 137 188 137 178 C137 172 140 170 143 169Z','nuclearMist',.54),
        ('M98 190 C105 184 119 192 128 188 C139 185 142 200 133 206 C119 211 102 204 98 190Z','nuclearLav',.48),
    ]:
        bits.append(f'<path d="{d}" fill="url(#{shade})" opacity="{opacity:.2f}"/>')

    bits.extend([
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
