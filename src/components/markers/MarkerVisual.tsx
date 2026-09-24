import { useId } from 'react';
import type { MarkerPalette, MarkerVisualSpec, VisualFamily } from './types';

type Paint = { light: string; mid: string; dark: string; glow: string; shaft: string; bead: string };
const palette: Record<MarkerPalette, Omit<Paint, 'shaft' | 'bead'>> = {
  blue: { light:'#9fdfff', mid:'#349ace', dark:'#175b94', glow:'#74c9f1' },
  coral: { light:'#ffae78', mid:'#f04420', dark:'#812020', glow:'#ff6540' },
  purple: { light:'#d79aff', mid:'#8422cf', dark:'#40106f', glow:'#a64ae8' },
  green: { light:'#b2f4c3', mid:'#49bf72', dark:'#247447', glow:'#71d792' },
  gold: { light:'#ffdd72', mid:'#e49309', dark:'#754009', glow:'#ffb820' },
  cyan: { light:'#82f4ff', mid:'#00afd7', dark:'#035578', glow:'#24cde9' },
};

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

function SurfaceReceptor({ family, variant, paint }: { family:VisualFamily; variant?:string; paint:Paint }) {
  const branched = family === 'branched-receptor';
  const forked = family === 'forked-receptor';
  // Variants alter the silhouette within a family; the marker name is never consulted.
  const longArms = forked && variant === 'hooked';
  const left = longArms ? 'M40 69 V45 C33 40 24 34 19 25' : 'M40 70 V45 C33 38 26 33 22 24';
  const right = longArms ? 'M40 45 C48 38 55 34 58 22' : 'M40 45 C48 37 55 32 58 23';
  return <g>
    <path d={`${left} ${right}`} fill="none" stroke={paint.dark} strokeWidth={branched?15:14} strokeLinecap="round" strokeLinejoin="round"/>
    <path d={`${left} ${right}`} fill="none" stroke={paint.shaft} strokeWidth={branched?10:9} strokeLinecap="round" strokeLinejoin="round"/>
    {branched && <><path d="M40 45 V29" fill="none" stroke={paint.dark} strokeWidth="14" strokeLinecap="round"/>
      <path d="M40 45 V29" fill="none" stroke={paint.shaft} strokeWidth="9" strokeLinecap="round"/></>}
    <path d="M36.5 62V47 M29 34L24 28 M48 34L54 27" fill="none" stroke="#fff" strokeWidth="2.2" strokeOpacity=".76" strokeLinecap="round"/>
    <Pearl x={longArms?18:21} y={longArms?22:22} r={branched?9:7} paint={paint}/>
    <Pearl x={longArms?59:59} y={longArms?21:21} r={branched?9.5:7} paint={paint}/>
    {branched ? <Pearl x={40} y={29} r={9.5} paint={paint}/> :
      <Pearl x={40} y={38} r={forked?6:5} paint={paint}/>}
    {family === 'membrane-receptor' && <circle cx="40" cy="27" r="3" fill={paint.mid}/>}
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
  const effectiveState = resultState === 'numeric' ? numericInterpretation ?? 'mentioned' : resultState;
  const isSurface = family === 'membrane-receptor' || family === 'branched-receptor' || family === 'forked-receptor';
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
      <filter id={`depth-${id}`} x="-35%" y="-35%" width="170%" height="180%">
        <feDropShadow dx="1" dy="2.2" stdDeviation="1.35" floodColor={dark} floodOpacity=".42"/>
      </filter>
    </defs>
    <g transform={`translate(40 40) rotate(${visualAngle}) scale(${visualSize}) translate(-40 -40)`}>
      <g opacity={opacity} filter={!quiet && !missing && !neutralNumeric ? `url(#depth-${id})` : undefined}>
        {neutralNumeric ? <g><circle cx="40" cy="40" r="20" fill={glow} fillOpacity=".18" stroke={dark} strokeOpacity=".7" strokeWidth="2"/>
          <text x="40" y="47" textAnchor="middle" fill={dark} fontSize="23" fontWeight="600">#</text></g> :
          isSurface ? <SurfaceReceptor family={family} variant={visualVariant} paint={paint}/> :
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
