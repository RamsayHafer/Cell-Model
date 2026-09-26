import type { CSSProperties } from 'react';
import traceCell from '../assets/cell-reference-clean.svg?raw';
import traceReference from '../assets/cell-reference.svg?raw';
import vectorCell from '../assets/cell-vector-clean.svg?raw';
import vectorReference from '../assets/cell-vector.svg?raw';
import cellB from '../assets/cell-b.svg?url';
import reference4x from '../assets/cell-reference-4x.webp?url';
import clean4x from '../assets/cell-reference-clean-4x.webp?url';
import type { Marker } from '../markers';
import { MarkerVisual } from './markers/MarkerVisual';

export type CellMode = 'a' | 'b';

// A stays inline SVG; B stays replaceable artwork. Marker illustrations use
// the same data-driven layer in both, independent of either base asset.
export function CellArtwork({ mode, markers, selectedId, hoveredId, referenceStudy=false }: { mode: CellMode; markers: Marker[]; selectedId: string | null; hoveredId?: string | null; referenceStudy?: boolean }) {
  const vectorPreview = new URLSearchParams(window.location.search).has('vector');
  const approvedTracePreview = new URLSearchParams(window.location.search).has('approved');
  const cellArt = vectorPreview
    ? referenceStudy ? vectorReference : vectorCell
    : referenceStudy ? traceReference : traceCell;
  return <div className={`cell-art cell-art--${mode}`}>
    {mode === 'a' ? vectorPreview || approvedTracePreview
      ? <div className="inline-art" aria-hidden="true" dangerouslySetInnerHTML={{ __html: cellArt }} />
      : <img className="art-image" src={referenceStudy ? reference4x : clean4x} width={1512} height={1512} alt="" aria-hidden="true" decoding="async" />
      : <img className="art-image" src={cellB} alt="Dimensional illustrated lavender immune cell" />}
    {markers.map(m => <span key={m.id}
      className={`receptor receptor--${m.palette} receptor--${m.cellularLocation} receptor--${m.visualFamily} ${selectedId === m.id ? 'is-active' : ''} ${hoveredId === m.id ? 'is-hovered' : ''} ${selectedId && selectedId !== m.id ? 'is-muted' : ''}`}
      style={{'--x': `${m.x}%`, '--y': `${m.y}%`} as CSSProperties} aria-hidden="true">
      <MarkerVisual {...m} selected={selectedId === m.id} hovered={hoveredId === m.id}/>
    </span>)}
  </div>;
}
