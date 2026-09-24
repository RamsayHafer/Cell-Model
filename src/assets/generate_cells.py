"""Regenerate the two editable illustrated SVG cells (standard-library only)."""
from pathlib import Path
from math import pi, sin, cos
import random

out=Path(__file__).resolve().parent

def scallop(cx,cy,r,n,depth,phase=0):
    pts=[]
    for k in range(361):
        t=2*pi*k/360
        rad=r+depth*cos(n*t+phase)+2.1*sin(5*t+.55)+1.6*cos(11*t)
        pts.append((cx+rad*cos(t),cy+rad*sin(t)))
    return 'M '+' L '.join(f'{x:.1f},{y:.1f}' for x,y in pts)+' Z'

def bubble(x,y,r,opacity,gradient='bead'):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="url(#{gradient})" opacity="{opacity:.2f}"/>'
            f'<ellipse cx="{x-r*.30:.1f}" cy="{y-r*.36:.1f}" rx="{r*.30:.1f}" ry="{r*.17:.1f}" fill="#fff" opacity="{opacity*.15:.2f}"/>')

def make(mode):
    rich=mode=='b';rng=random.Random(22 if rich else 17)
    outline=scallop(220,221,150,24 if rich else 21,2.7 if rich else 2.1,.4)
    inner=scallop(220,220,132,22 if rich else 20,2.8 if rich else 1.6,.3)
    nucleus=scallop(225,224,66 if rich else 67,8,1.8 if rich else 1.2,1.6)
    parts=[f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 440 440" role="img" aria-label="Soft ruffled lavender immune cell with a sculpted purple nucleus">
<defs>
 <radialGradient id="shell" cx="37%" cy="23%" r="76%"><stop stop-color="#fff"/><stop offset=".32" stop-color="#e5e6ff"/><stop offset=".68" stop-color="#c1c2f2"/><stop offset=".90" stop-color="#a7a5df"/><stop offset="1" stop-color="#8e8ccf"/></radialGradient>
 <radialGradient id="cyto" cx="36%" cy="23%" r="79%"><stop stop-color="#eefaff"/><stop offset=".28" stop-color="#c8e8f9"/><stop offset=".65" stop-color="#aecff4"/><stop offset="1" stop-color="#8da7df"/></radialGradient>
 <radialGradient id="bead" cx="32%" cy="23%" r="78%"><stop stop-color="#ffffff" stop-opacity=".97"/><stop offset=".35" stop-color="#ecedff" stop-opacity=".91"/><stop offset=".70" stop-color="#c6caf6" stop-opacity=".94"/><stop offset="1" stop-color="#9896d7" stop-opacity=".96"/></radialGradient>
 <radialGradient id="blueBead" cx="32%" cy="23%" r="75%"><stop stop-color="#f9ffff"/><stop offset=".47" stop-color="#e4f2ff"/><stop offset="1" stop-color="#b1c9ed"/></radialGradient>
 <radialGradient id="core" cx="30%" cy="21%" r="81%"><stop stop-color="#dfc9f6"/><stop offset=".29" stop-color="#b99cde"/><stop offset=".68" stop-color="#876cbe"/><stop offset="1" stop-color="#69549e"/></radialGradient>
 <radialGradient id="coreBead" cx="27%" cy="22%" r="76%"><stop stop-color="#e1cbfb"/><stop offset=".45" stop-color="#ab8dd7"/><stop offset="1" stop-color="#775dab"/></radialGradient>
 <linearGradient id="rim" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#fff" stop-opacity=".9"/><stop offset=".43" stop-color="#fff" stop-opacity=".05"/><stop offset="1" stop-color="#8185bc" stop-opacity=".6"/></linearGradient>
 <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="15"/></filter>
 <filter id="soft"><feGaussianBlur stdDeviation="6"/></filter>
 <filter id="texture" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".07" numOctaves="2" seed="7"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncA type="linear" slope=".045"/></feComponentTransfer></filter>
 <clipPath id="cellClip"><path d="{outline}"/></clipPath>
 <clipPath id="innerClip"><path d="{inner}"/></clipPath>
 <clipPath id="nucleusClip"><path d="{nucleus}"/></clipPath>
</defs>

<path d="{outline}" fill="url(#shell)" stroke="#d1c9f0" stroke-width="2"/>
<g clip-path="url(#cellClip)">
 <ellipse cx="211" cy="279" rx="154" ry="125" fill="#8f8dcb" opacity=".17" filter="url(#soft)"/>
''']
    # Surface lobes feather the edge; gradients read as soft translucent, rounded folds.
    count=39 if rich else 24
    for i in range(count):
        t=2*pi*i/count+.15
        x=220+(139+rng.uniform(-3,3))*cos(t);y=221+(139+rng.uniform(-3,3))*sin(t)
        size=(18 if rich else 16)+rng.uniform(-3,5)
        parts.append(bubble(x,y,size,.86 if rich else .69))
    parts.append(f'<path d="{inner}" fill="url(#cyto)" opacity=".89" stroke="#eef0ff" stroke-opacity=".42" stroke-width="3"/>')
    # Folds at two depths, with an airy blue middle.
    for ring,count,rr,size in ((112,28 if rich else 19,12,19),(91,20 if rich else 13,7,17)):
        for i in range(count):
            t=2*pi*(i+.13)/count
            x=220+(ring+rr*cos(3*t))*cos(t);y=221+(ring+rr*sin(2*t))*sin(t)
            parts.append(bubble(x,y,size+rng.uniform(-4,4),.63 if rich else .48,'bead' if ring==112 else 'blueBead'))
    parts.append('<ellipse cx="193" cy="137" rx="88" ry="44" fill="#fff" opacity=".26" filter="url(#soft)"/>')
    parts.append(f'<path d="{nucleus}" fill="url(#core)" stroke="#aa8dce" stroke-opacity=".42" stroke-width="2"/>')
    parts.append(f'<g clip-path="url(#nucleusClip)">')
    parts.append('<ellipse cx="249" cy="260" rx="48" ry="29" fill="#5e4b9c" opacity=".20" filter="url(#soft)"/>')
    parts.append('<ellipse cx="198" cy="184" rx="47" ry="30" fill="#ead9fa" opacity=".31" filter="url(#soft)"/>')
    for i in range(19 if rich else 13):
        t=2*pi*rng.random()
        radial=rng.uniform(11,54)
        x=225+radial*cos(t);y=224+radial*sin(t)
        parts.append(bubble(x,y,rng.uniform(7,13),.22 if rich else .16,'coreBead'))
    parts.append('<ellipse cx="205" cy="183" rx="38" ry="19" fill="#f1ddff" opacity=".32" filter="url(#soft)"/>')
    parts.append('</g>')
    parts.append('<path d="M180 172 C195 146 232 139 256 153" fill="none" stroke="#f8eaff" opacity=".42" stroke-width="7" stroke-linecap="round" filter="url(#soft)"/>')
    parts.append('<path d="M107 202 C112 155 133 118 173 98" fill="none" stroke="#fff" opacity=".35" stroke-width="8" stroke-linecap="round" filter="url(#soft)"/>')
    parts.append('<rect width="440" height="440" filter="url(#texture)" opacity=".65"/>')
    parts.append('</g>')
    parts.append(f'<path d="{outline}" fill="none" stroke="url(#rim)" stroke-width="5" opacity=".8"/>')
    parts.append('</svg>')
    (out/f'cell-{mode}.svg').write_text('\n'.join(parts)+'\n')

if __name__=='__main__':
    make('a');make('b')
