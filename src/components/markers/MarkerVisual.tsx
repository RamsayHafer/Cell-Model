import { useId } from 'react';
import type { MarkerPalette, MarkerVisualSpec, VisualFamily } from './types';

type Paint = { light: string; mid: string; dark: string; glow: string; shaft: string; bead: string };
const palette: Record<MarkerPalette, Omit<Paint, 'shaft' | 'bead'>> = {
  blue: { light:'#9fdfff', mid:'#349ace', dark:'#175b94', glow:'#74c9f1' },
  coral: { light:'#ffafa3', mid:'#ec5241', dark:'#922b2d', glow:'#fa7869' },
  purple: { light:'#d9b3f6', mid:'#8746c3', dark:'#512985', glow:'#b08ade' },
  green: { light:'#b2f4c3', mid:'#49bf72', dark:'#247447', glow:'#71d792' },
  gold: { light:'#ffdd72', mid:'#e49309', dark:'#754009', glow:'#ffb820' },
  cyan: { light:'#82f4ff', mid:'#00afd7', dark:'#035578', glow:'#24cde9' },
};

const isSurfaceFamily = (family: VisualFamily) =>
  family === 'membrane-receptor' || family === 'branched-receptor' || family === 'forked-receptor';

function Pearl({ x, y, r, paint }: { x:number; y:number; r:number; paint:Paint }) {
  return <g>
    <circle cx={x+.45} cy={y+.85} r={r+.35} fill={paint.dark} fillOpacity=".9"/>
    <circle cx={x} cy={y} r={r-.3} fill={paint.bead}/>
    <path d={`M ${x-r*.72} ${y+r*.46} Q ${x} ${y+r*1.06} ${x+r*.72} ${y+r*.46}`}
      fill="none" stroke={paint.dark} strokeOpacity=".48" strokeWidth="1.15" strokeLinecap="round"/>
    <ellipse cx={x-r*.35} cy={y-r*.45} rx={r*.35} ry={r*.22} fill="#fff" fillOpacity=".95"/>
    {r > 5 && <circle cx={x+r*.36} cy={y-r*.36} r={r*.1} fill="#fff" fillOpacity=".78"/>}
  </g>;
}

function SoftTerminal({ x, y, rx, ry, angle=0, id }: { x:number; y:number; rx:number; ry:number; angle?:number; id:string }) {
  return <g transform={`rotate(${angle} ${x} ${y})`}>
    <ellipse cx={x+.7} cy={y+1.5} rx={rx+.3} ry={ry+.4} fill="#3f3767" fillOpacity=".13"/>
    <ellipse cx={x} cy={y} rx={rx} ry={ry} fill={`url(#reference-bead-${id})`}/>
    <ellipse cx={x-rx*.28} cy={y-ry*.44} rx={rx*.36} ry={ry*.19} fill="#fff" fillOpacity=".43"/>
  </g>;
}

function SurfaceReceptor({ family, variant, paint, id }: { family:VisualFamily; variant?:string; paint:Paint; id:string }) {
  const branched = family === 'branched-receptor';
  const forked = family === 'forked-receptor';
  // Variants alter the silhouette within a family; the marker name is never consulted.
  const longArms = forked && variant === 'hooked';
  const left = longArms ? 'M40 69 V45 C33 40 24 34 19 25' : 'M40 70 V45 C33 38 26 33 22 24';
  const right = longArms ? 'M40 45 C48 38 55 34 58 22' : 'M40 45 C48 37 55 32 58 23';
  return <g>
    <path d={`${left} ${right}`} fill="none" stroke={paint.dark} strokeOpacity=".32" strokeWidth={branched?15:14} strokeLinecap="round" strokeLinejoin="round"/>
    <path d={`${left} ${right}`} fill="none" stroke={paint.shaft} strokeWidth={branched?11:10} strokeLinecap="round" strokeLinejoin="round"/>
    {branched && <><path d="M40 45 V29" fill="none" stroke={paint.dark} strokeOpacity=".32" strokeWidth="14" strokeLinecap="round"/>
      <path d="M40 45 V29" fill="none" stroke={paint.shaft} strokeWidth="10" strokeLinecap="round"/></>}
    <path d="M36.5 62V47 M29 34L24 28 M48 34L54 27" fill="none" stroke="#fff" strokeWidth="1.7" strokeOpacity=".39" strokeLinecap="round"/>
    <SoftTerminal x={longArms?18:21} y={22} rx={branched?7:6} ry={branched?9:8} angle={-23} id={id}/>
    <SoftTerminal x={59} y={longArms?21:21} rx={branched?7:6} ry={branched?9:8} angle={19} id={id}/>
    {branched ? <SoftTerminal x={40} y={29} rx={8} ry={9} id={id}/> :
      <SoftTerminal x={40} y={38} rx={forked?6:5} ry={forked?7:6} id={id}/>}
    {family === 'membrane-receptor' && <circle cx="40" cy="27" r="3" fill={paint.mid}/>}
  </g>;
}

// The reference variants use the same paint and result-state pipeline as every
// other family. Curved shafts and asymmetric terminals provide a higher-detail
// treatment without embedding pixels or making marker names choose artwork.
function ReferenceTreatment({ variant, paint, id }: { variant:string; paint:Paint; id:string }) {
  if (variant === 'reference-ki67') return <g>
    <ellipse cx="40" cy="39" rx="29" ry="26" fill={paint.glow} fillOpacity=".21" filter={`url(#bloom-${id})`}/>
    <path d="M26 43Q34 35 40 31Q47 38 54 43M40 31Q40 43 43 52" fill="none" stroke={paint.dark} strokeWidth="4.5" strokeOpacity=".75" strokeLinecap="round"/>
    <path d="M26 43Q34 35 40 31Q47 38 54 43M40 31Q40 43 43 52" fill="none" stroke={paint.shaft} strokeWidth="2.9" strokeLinecap="round"/>
    {[[24,43,6,7,-24],[40,27,6,7,16],[56,43,5,6,28],[43,54,5,6,-14]].map(([x,y,rx,ry,angle],i)=><SoftTerminal key={i} x={x} y={y} rx={rx} ry={ry} angle={angle} id={id}/>)}
  </g>;

  const cd30 = variant === 'reference-cd30';
  const cd7 = variant === 'reference-cd7';
  const contour = cd30
    ? 'M28 76C32 67 36 55 40 47C38 39 31 34 28 25M40 47C44 37 49 29 51 18M40 47C49 46 58 43 63 34M40 47C36 43 34 40 32 36'
    : cd7
      ? 'M74 42C62 43 51 45 42 43C33 43 27 37 22 28M42 43C32 44 22 48 17 58M42 43C35 50 33 57 31 63'
      : 'M46 76C43 64 39 52 37 44C29 42 22 36 18 27M37 44C44 38 49 27 51 20';
  const terminals: [number,number,number,number,number][] = cd30
    ? [[27,23,7,9,-18],[51,17,7,9,16],[63,33,8,7,30],[32,35,7,8,-35],[43,45,8,7,14]]
    : cd7 ? [[20,25,7,10,-35],[16,59,9,7,-35],[30,63,8,7,18]]
      : [[18,26,7,11,-28],[51,19,7,11,21]];
  return <g>
    <ellipse cx="40" cy="42" rx="27" ry="30" fill={paint.glow} fillOpacity=".21" filter={`url(#bloom-${id})`}/>
    <path d={contour} fill="none" stroke={paint.dark} strokeOpacity=".31" strokeWidth={cd30?15:14} strokeLinecap="round" strokeLinejoin="round"/>
    <path d={contour} fill="none" stroke={paint.shaft} strokeWidth={cd30?12:11} strokeLinecap="round" strokeLinejoin="round"/>
    <path d={cd30 ? 'M31 69Q36 58 39 51M41 42Q45 32 49 23M46 44L56 39'
      : cd7 ? 'M68 41Q55 42 44 41M36 42Q29 39 25 33'
        : 'M43 69Q39 55 36 46M33 41Q25 37 21 31'}
      fill="none" stroke="#fff" strokeOpacity=".36" strokeWidth="1.7" strokeLinecap="round"/>
    {terminals.map(([x,y,rx,ry,angle],i)=><SoftTerminal key={i} x={x} y={y} rx={rx} ry={ry} angle={angle} id={id}/>)}
  </g>;
}

function ProteinCluster({ family, variant, paint }: { family:VisualFamily; variant?:string; paint:Paint }) {
  const nuclear = family === 'nuclear-protein';
  const compact = variant === 'compact';
  const nodes = nuclear
    ? [[27,28,7],[42,22,6],[54,34,8],[44,49,7],[27,51,6],[22,41,5]]
    : compact ? [[28,27,8],[48,25,7],[24,47,7],[47,48,9],[37,38,6]]
      : [[25,28,8],[48,26,8],[24,51,7],[49,50,8],[39,40,7]];
  return <g>
    <ellipse cx="39" cy="39" rx={nuclear?18:17} ry={nuclear?17:15} fill={paint.dark} fillOpacity={nuclear?'.22':'.28'}/>
    <path d={nuclear?'M27 28L42 22L54 34L44 49L27 51L22 41Z M27 28L44 49':'M28 27L48 25L47 48L24 47L28 27 M28 27L39 40'}
      fill="none" stroke={paint.dark} strokeWidth="5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d={nuclear?'M27 28L42 22L54 34L44 49L27 51L22 41Z':'M28 27L48 25L47 48L24 47'}
      fill="none" stroke={paint.shaft} strokeWidth="2.5" strokeLinecap="round"/>
    {nodes.map(([x,y,r],i)=><Pearl key={i} x={x} y={y} r={r} paint={paint}/>)}
  </g>;
}

function Pattern({ family, paint }: { family:VisualFamily; paint:Paint }) {
  switch (family) {
    case 'transcription-factor':
      return <g><path d="M19 55Q40 44 61 55 M25 49V58 M34 46V57 M46 46V57 M55 49V58" fill="none" stroke={paint.dark} strokeWidth="2.5" strokeLinecap="round"/>
        <path d="M29 41L38 29L51 39" fill="none" stroke={paint.shaft} strokeWidth="5" strokeLinecap="round"/>
        <Pearl x={37} y={27} r={7} paint={paint}/><Pearl x={50} y={38} r={7} paint={paint}/></g>;
    case 'proliferation-pattern':
      return <g><circle cx="40" cy="40" r="22" fill={paint.glow} fillOpacity=".13" stroke={paint.mid} strokeOpacity=".72" strokeWidth="2"/>
        {[[40,18],[58,27],[62,43],[50,59],[32,60],[19,44],[24,27]].map(([x,y],i)=><Pearl key={i} x={x} y={y} r={3.7} paint={paint}/>)}
        <circle cx="40" cy="40" r="5" fill="none" stroke={paint.dark} strokeOpacity=".55" strokeWidth="2"/></g>;
    case 'dna-mutation':
      return <g><path d="M28 15C60 29 20 50 53 65 M52 15C20 29 60 50 27 65" fill="none" stroke={paint.shaft} strokeWidth="4" strokeLinecap="round"/>
        {[22,31,40,49,58].map((y,i)=><path key={i} d={`M ${i%2?31:35} ${y} H ${i%2?49:45}`} stroke={paint.dark} strokeWidth="2"/>)}
        <Pearl x={41} y={40} r={6} paint={paint}/></g>;
    case 'gene-fusion':
      return <g><path d="M15 24L34 38L42 48L63 61 M16 59L35 44L43 34L63 20" fill="none" stroke={paint.dark} strokeWidth="6" strokeLinecap="round"/>
        <path d="M15 24L34 38L42 48L63 61 M16 59L35 44L43 34L63 20" fill="none" stroke={paint.shaft} strokeWidth="3.5" strokeLinecap="round"/>
        <Pearl x={39} y={41} r={8} paint={paint}/></g>;
    case 'copy-number':
      return <g>{[24,34,44,54].map((x,i)=><g key={i}><rect x={x-3} y={22-i*2} width="8" height={35+i*3} rx="4" fill={paint.shaft} stroke={paint.dark} strokeWidth="1.2"/>
        <path d={`M${x-1} ${27-i*2}V${48+i*2}`} stroke="#fff" strokeOpacity=".62" strokeWidth="1.2"/></g>)}</g>;
    case 'chromosomal-loss':
      return <g><path d="M24 20L34 36L23 59 M54 20L46 34 M52 50L57 59" fill="none" stroke={paint.shaft} strokeWidth="6" strokeLinecap="round"/>
        <path d="M44 41L56 41" stroke={paint.dark} strokeWidth="3" strokeDasharray="3 4"/><circle cx="50" cy="42" r="11" fill="none" stroke={paint.dark} strokeDasharray="3 3" strokeWidth="1.7"/></g>;
    default:
      return <g><circle cx="40" cy="40" r="16" fill={paint.glow} fillOpacity=".2" stroke={paint.dark} strokeOpacity=".6" strokeWidth="2"/>
        {[0,1,2,3,4].map(i=><Pearl key={i} x={40+23*Math.cos(i*2*Math.PI/5)} y={40+23*Math.sin(i*2*Math.PI/5)} r={4.5} paint={paint}/>)}</g>;
  }
}

export type MarkerVisualProps = MarkerVisualSpec & {
  selected?: boolean;
  hovered?: boolean;
  decorative?: boolean;
};

export function MarkerVisual({ canonicalName, cellularLocation, visualFamily, visualVariant, palette: color, resultState, numericInterpretation, size=1, orientation=0, selected=false, hovered=false, decorative=true }: MarkerVisualProps) {
  const id = useId().replace(/:/g,'');
  const neutralNumeric = resultState === 'numeric' && !numericInterpretation;
  const { light, mid, dark, glow } = neutralNumeric
    ? { light:'#e6e8ed', mid:'#9298a5', dark:'#5e6675', glow:'#c6cbd5' }
    : palette[color];
  const paint: Paint = { light, mid, dark, glow, shaft:`url(#shaft-${id})`, bead:`url(#bead-${id})` };
  const family = cellularLocation === 'unknown' || neutralNumeric ? 'generic' : visualFamily;
  const referenceVariant = !neutralNumeric &&
    ((isSurfaceFamily(family) && ['reference-cd30','reference-cd7','reference-cd4'].includes(visualVariant ?? '')) ||
     (family === 'proliferation-pattern' && visualVariant === 'reference-ki67')) ? visualVariant : null;
  const effectiveState = resultState === 'numeric' ? numericInterpretation ?? 'mentioned' : resultState;
  const isSurface = isSurfaceFamily(family);
  const isProtein = family === 'cytoplasmic-protein' || family === 'nuclear-protein';
  const quiet = effectiveState === 'mentioned' || effectiveState === 'pending';
  const missing = effectiveState === 'absent' || effectiveState === 'lost';
  const opacity = missing ? .2 : effectiveState === 'reduced' ? .53 : quiet ? .48 : 1;
  // Transform only the painted geometry around its viewBox center. The caller
  // still owns positioning, selection, focus, and the interactive hit target.
  const visualSize = Number.isFinite(size) && size > 0 ? size : 1;
  const visualAngle = Number.isFinite(orientation) ? orientation : 0;
  return <svg className={`marker-visual marker-visual--${color}`} viewBox="0 0 80 80" style={{ overflow:'visible' }} aria-hidden={decorative}
    role={decorative?undefined:'img'} aria-label={decorative?undefined:`${canonicalName}: ${resultState} (${cellularLocation})`}
    data-family={family} data-location={cellularLocation} data-state={resultState} data-selected={selected} data-hovered={hovered}>
    <defs>
      <linearGradient id={`shaft-${id}`} x1="0" y1="0" x2=".82" y2="1"><stop stopColor={light}/><stop offset=".18" stopColor={mid}/><stop offset=".54" stopColor={mid}/><stop offset="1" stopColor={dark}/></linearGradient>
      <radialGradient id={`bead-${id}`} cx="27%" cy="18%" r="86%"><stop stopColor="#fff" stopOpacity=".86"/><stop offset=".12" stopColor={light}/><stop offset=".34" stopColor={mid}/><stop offset=".65" stopColor={mid}/><stop offset="1" stopColor={dark}/></radialGradient>
      <radialGradient id={`reference-bead-${id}`} cx="31%" cy="21%" r="94%"><stop stopColor="#fff" stopOpacity=".66"/><stop offset=".17" stopColor={light}/><stop offset=".68" stopColor={mid}/><stop offset="1" stopColor={dark} stopOpacity=".52"/></radialGradient>
      <filter id={`depth-${id}`} x="-35%" y="-35%" width="170%" height="180%">
        <feDropShadow dx="1" dy="2.2" stdDeviation="1.35" floodColor={dark} floodOpacity=".42"/>
      </filter>
      <filter id={`bloom-${id}`} x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="3.8"/></filter>
      <filter id={`contact-${id}`} x="-70%" y="-100%" width="240%" height="300%"><feGaussianBlur stdDeviation="1.7"/></filter>
      <filter id={`specular-${id}`} x="-35%" y="-80%" width="170%" height="260%"><feGaussianBlur stdDeviation=".72"/></filter>
    </defs>
    <g transform={`translate(40 40) rotate(${visualAngle}) scale(${visualSize}) translate(-40 -40)`}>
      <g opacity={opacity} filter={!quiet && !missing && !neutralNumeric && !referenceVariant ? `url(#depth-${id})` : undefined}>
        {neutralNumeric ? <g><circle cx="40" cy="40" r="20" fill={glow} fillOpacity=".18" stroke={dark} strokeOpacity=".7" strokeWidth="2"/>
          <text x="40" y="47" textAnchor="middle" fill={dark} fontSize="23" fontWeight="600">#</text></g> :
          referenceVariant ? <ReferenceTreatment variant={referenceVariant} paint={paint} id={id}/> :
          isSurface ? <SurfaceReceptor family={family} variant={visualVariant} paint={paint} id={id}/> :
            isProtein ? <ProteinCluster family={family} variant={visualVariant} paint={paint}/> :
              <Pattern family={family} paint={paint}/>}
      </g>
      {missing && <g><circle cx="40" cy="39" r="15" fill="#f7f1ff" fillOpacity=".7" stroke={dark} strokeOpacity=".85" strokeWidth="2" strokeDasharray="3 4"/>
        <path d="M34 39h12" stroke={dark} strokeWidth="3" strokeLinecap="round"/></g>}
      {effectiveState === 'pending' && <g><circle cx="55" cy="57" r="11" fill="#fff" fillOpacity=".9" stroke={dark} strokeWidth="1.8"/><path d="M55 51v6l4 2" stroke={dark} fill="none" strokeWidth="2" strokeLinecap="round"/></g>}
      {effectiveState === 'mentioned' && !neutralNumeric && <circle cx="40" cy="40" r="26" fill="none" stroke={dark} strokeOpacity=".4" strokeWidth="1.7" strokeDasharray="2 4"/>}
    </g>
  </svg>;
}
