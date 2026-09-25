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
nucleus = ('M97 145 C102 138 109 136 116 134 C124 131 124 125 135 123 '
           'C145 121 155 125 161 132 C171 137 173 151 174 161 '
           'C175 172 170 181 168 189 C165 198 157 202 150 204 '
           'C143 204 139 211 130 212 C117 214 103 209 95 202 '
           'C88 195 84 183 86 173 C86 162 90 153 97 145Z')

def petal(rng, cx, cy, rx, ry, angle, color, opacity):
    # Each fold has an independent irregular contour, broad colored underside,
    # and short interior glint. No pixel-color posterization or tiled pattern.
    d = ('M -1 -.70 C -.73 -1.16 -.12 -1.16 .14 -.98 '
         'C .54 -1.11 1.05 -.54 .90 -.15 '
         'C 1.14 .27 .61 .96 .09 1.03 '
         'C -.52 1.14 -.58 .65 -1.01 .35 '
         'C -1.16 .01 -1.13 -.33 -1 -.70Z')
    angle += rng.uniform(-12,12)
    return (f'<g transform="translate({cx:.2f} {cy:.2f}) rotate({angle:.1f}) '
            f'scale({rx:.2f} {ry:.2f})" opacity="{opacity:.2f}">'
            f'<path d="{d}" fill="#8a82bf" opacity=".11" '
            'transform="translate(.11 .17)"/>'
            f'<path d="{d}" fill="url(#{color})"/>'
            '</g>')


DEFS = '''<defs>
  <radialGradient id="body" cx="41%" cy="37%" r="77%">
    <stop stop-color="#f8faff"/><stop offset=".24" stop-color="#e1f0ff"/>
    <stop offset=".58" stop-color="#d7e4fc"/><stop offset=".83" stop-color="#d1c8f3"/>
    <stop offset="1" stop-color="#bab2e2"/>
  </radialGradient>
  <radialGradient id="cortex" cx="43%" cy="34%" r="69%">
    <stop stop-color="#f4f9ff" stop-opacity=".95"/>
    <stop offset=".44" stop-color="#cfebfc" stop-opacity=".83"/>
    <stop offset=".76" stop-color="#b8d8f0" stop-opacity=".57"/>
    <stop offset="1" stop-color="#bcb6e7" stop-opacity=".31"/>
  </radialGradient>
  <radialGradient id="innerLight" cx="38%" cy="30%" r="77%">
    <stop stop-color="#e4f4ff" stop-opacity=".76"/>
    <stop offset=".57" stop-color="#c5dff6" stop-opacity=".58"/>
    <stop offset="1" stop-color="#b0c1e9" stop-opacity=".24"/>
  </radialGradient>
  <radialGradient id="foldLav" cx="34%" cy="26%" r="78%">
    <stop stop-color="#fff" stop-opacity=".98"/>
    <stop offset=".30" stop-color="#f8f0ff" stop-opacity=".96"/>
    <stop offset=".68" stop-color="#d9c9f8" stop-opacity=".87"/>
    <stop offset="1" stop-color="#a99bd7" stop-opacity=".16"/>
  </radialGradient>
  <radialGradient id="foldBlue" cx="30%" cy="24%" r="84%">
    <stop stop-color="#fff" stop-opacity=".98"/>
    <stop offset=".31" stop-color="#eaf9ff" stop-opacity=".96"/>
    <stop offset=".73" stop-color="#b7d8f4" stop-opacity=".89"/>
    <stop offset="1" stop-color="#89a4d6" stop-opacity=".16"/>
  </radialGradient>
  <radialGradient id="foldPink" cx="34%" cy="25%" r="82%">
    <stop stop-color="#fff9ff" stop-opacity=".96"/>
    <stop offset=".34" stop-color="#f3dff8" stop-opacity=".8"/>
    <stop offset=".75" stop-color="#dac0ed" stop-opacity=".62"/>
    <stop offset="1" stop-color="#bc99df" stop-opacity=".11"/>
  </radialGradient>
  <radialGradient id="nucleus" cx="29%" cy="21%" r="84%">
    <stop stop-color="#e3d1f7"/><stop offset=".23" stop-color="#b8a1dc"/>
    <stop offset=".58" stop-color="#947fc8"/>
    <stop offset=".89" stop-color="#7567b3"/>
    <stop offset="1" stop-color="#645b9e"/>
  </radialGradient>
  <linearGradient id="nucleusSheen" x1="0" y1="0" x2=".86" y2="1">
    <stop stop-color="#f8f1ff" stop-opacity=".76"/>
    <stop offset=".47" stop-color="#e3d2f9" stop-opacity=".23"/>
    <stop offset="1" stop-color="#5f4a9a" stop-opacity=".22"/>
  </linearGradient>
  <radialGradient id="nuclearPearl" cx="25%" cy="20%" r="78%">
    <stop stop-color="#f6eaff" stop-opacity=".85"/>
    <stop offset=".39" stop-color="#dfcef9" stop-opacity=".56"/>
    <stop offset="1" stop-color="#7866b4" stop-opacity=".04"/>
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
    <stop stop-color="#504492" stop-opacity=".42"/>
    <stop offset=".56" stop-color="#61529b" stop-opacity=".20"/>
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

    # Two interlaced belts of translucent, uneven membrane folds. Their
    # overlaps form the luminous ruffled rim seen in the reference.
    for belt, number, distance, rx, ry in [(0,54,.91,9.0,10.6),(1,45,.74,10.2,12.0)]:
        for i in range(number):
            t = -pi/2 + 2*pi*(i + (.29 if belt else 0))/number
            t += rng.uniform(-.12,.12)
            radial = distance + rng.uniform(-.12,.10)
            x = 130 + 79*cos(t)*radial
            y = 161 + 88*sin(t)*radial
            x += rng.uniform(-3.9,3.9); y += rng.uniform(-4.6,4.6)
            color = ('foldPink' if i%11 in (0,1) and t < -.15 else
                     'foldLav' if (i+belt)%3 else 'foldBlue')
            bits.append(petal(rng,x,y,rx*rng.uniform(.60,1.40),
                              ry*rng.uniform(.63,1.44),t*180/pi+96,
                              color,rng.uniform(.45,.83)))

    bits.extend([
        f'<path d="{inner}" fill="url(#cortex)" stroke="#f7f1ff" '
        'stroke-opacity=".18" stroke-width=".9"/>',
        f'<path d="{core}" fill="url(#innerLight)"/>',
        '<path d="M66 149 C74 115 87 106 112 96 C137 89 162 103 179 118" '
        'fill="none" stroke="#fff" stroke-width="7.7" stroke-opacity=".19" stroke-linecap="round"/>',
        '<path d="M69 184 C73 216 106 233 133 231 C170 229 183 212 194 182" '
        'fill="none" stroke="#f6f2ff" stroke-width="9.4" stroke-opacity=".18" stroke-linecap="round"/>',
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
                          .56 if i%4 else .67))

    # Sweeping creases break up the individual folds. The second, offset stroke
    # supplies their darker underside while the wide white stroke stays soft.
    creases = [
        ('M73 130 C84 110 95 111 105 101 C119 92 127 109 139 104',8),
        ('M101 113 C116 107 127 114 137 105 C149 100 155 114 169 114',6),
        ('M163 120 C176 119 177 133 185 138 C191 148 183 157 190 163',8),
        ('M186 174 C176 181 181 193 169 199 C163 212 150 211 143 219',9),
        ('M134 226 C124 217 111 227 102 214 C91 211 82 208 78 196',8),
        ('M61 182 C73 175 65 162 76 153 C75 141 86 137 86 127',8),
        ('M82 163 C90 147 104 148 110 133 C122 122 132 133 139 121',6),
        ('M154 133 C172 139 166 147 179 155 C183 169 172 178 173 188',8),
        ('M72 199 C81 189 95 196 101 185 C107 173 119 175 126 166',6),
        ('M159 203 C144 198 146 209 133 208 C120 206 119 216 109 219',6),
        ('M104 98 C111 91 122 96 132 91 C139 86 146 94 154 94',7),
        ('M67 144 C78 134 74 124 84 116 C92 111 98 115 105 108',7),
    ]
    for i,(d,width) in enumerate(creases):
        bits.append(f'<path d="{d}" fill="none" stroke="#8f9dc8" '
                    f'stroke-width="{width+1}" stroke-opacity=".10" '
                    'stroke-linecap="round" transform="translate(.5 1.5)"/>')
        bits.append(f'<path d="{d}" fill="none" stroke="{("#fff" if i%3 else "#e7dcff")}" '
                    f'stroke-width="{width}" stroke-opacity=".21" '
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
        f'<path d="{outer}" fill="none" stroke="#fff" stroke-width="1.25" '
        'stroke-opacity=".34"/>',
        '<path d="M66 149 C65 118 91 91 122 85 C148 79 174 94 188 112" '
        'fill="none" stroke="#fff" stroke-opacity=".23" stroke-width="1.35" '
        'stroke-linecap="round"/>',
        '<path d="M52 174 C52 210 88 244 129 246" fill="none" '
        'stroke="#f7f3ff" stroke-opacity=".29" stroke-width="1.4" '
        'stroke-linecap="round"/>',
        '</g>',
        # Nucleus: one sculpted contour, translucent rim, organelle texture.
        f'<path d="{nucleus}" fill="#9684c8" opacity=".17" '
        'transform="translate(1.2 1.6)" filter="url(#contact)"/>',
        f'<path d="{nucleus}" fill="url(#nucleus)" stroke="#9c88c8" '
        'stroke-width="1.25" stroke-opacity=".46"/>',
        f'<g clip-path="url(#nucleusClip)">',
        '<path d="M84 176 C89 131 120 120 150 124 C171 125 185 145 177 170 '
        'C163 144 152 129 132 135 C108 142 105 157 93 179Z" '
        'fill="url(#nucleusSheen)" opacity=".64"/>',
        '<path d="M86 184 C96 202 121 216 142 211 C160 209 177 185 175 161 '
        'C166 181 153 192 138 190 C116 186 105 169 86 184Z" '
        'fill="#584e9a" opacity=".15"/>',
    ])

    for x,y,rx,ry in [(117,152,16,12),(151,150,13,11),(126,179,19,13),
                       (161,181,12,13),(108,191,14,14),(145,199,14,9)]:
        bits.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" '
                    'fill="url(#nuclearShade)"/>')

    for i,(x,y,rx,ry,alpha) in enumerate([
        (118,145,10,5,.52),(145,137,12,6,.48),(158,147,9,8,.39),
        (112,164,9,7,.50),(129,154,12,6,.37),(147,165,10,8,.45),
        (162,179,11,7,.41),(121,185,11,8,.38),(102,191,10,7,.39),
        (137,197,11,8,.32),(106,151,5,7,.38),(140,179,8,7,.44),
        (119,205,8,6,.30),(154,196,9,7,.35),(127,135,9,4,.49),
        (96,173,5,11,.27),(154,126,6,5,.35),(170,164,5,8,.32),
        (133,175,8,6,.31),(109,201,7,6,.29),(132,209,9,5,.23)
    ]):
        bits.append(f'<path d="M-.85 -.63 C-.42 -1.09 .06 -.83 .42 -.93 '
                    'C 1.08 -.62 1.12 .18 .64 .70 '
                    'C .11 1.03 -.48 .89 -.91 .45 C-1.12 .09 -1.12 -.27 -.85 -.63Z" '
                    f'fill="url(#nuclearPearl)" opacity="{min(1,alpha/.63):.2f}" '
                    f'transform="translate({x} {y}) rotate({(i*19)%87-43}) '
                    f'scale({rx} {ry})"/>')

    # Short interrupted color swirls give the nucleus depth without forming
    # long parallel bands across its surface.
    for d,w in [
        ('M106 142 C110 136 114 138 118 134',5),
        ('M139 133 C145 131 151 133 157 138',5),
        ('M101 165 C108 158 111 165 117 161',7),
        ('M131 160 C139 154 143 162 149 157',6),
        ('M154 176 C159 169 164 171 168 174',5),
        ('M97 189 C104 184 111 190 117 186',6),
        ('M121 198 C126 194 133 199 139 194',6),
        ('M143 183 C147 178 151 184 157 181',5),
    ]:
        bits.append(f'<path d="{d}" fill="none" stroke="#e8d5fb" '
                    f'stroke-width="{w}" stroke-opacity=".20" '
                    'stroke-linecap="round"/>')

    bits.extend([
        '<path d="M96 151 C100 136 117 128 131 125 C146 121 161 131 167 141" '
        'fill="none" stroke="#f3e4ff" stroke-opacity=".24" '
        'stroke-width="1.8" stroke-linecap="round"/>',
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
