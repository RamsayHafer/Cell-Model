import type { CSSProperties } from 'react';
import cellA from '../assets/cell-reference.svg?raw';
import cellB from '../assets/cell-b.svg?url';
import type { Marker } from '../markers';
import { MarkerVisual } from './markers/MarkerVisual';

export type CellMode = 'a' | 'b';

// A stays inline SVG; B stays replaceable artwork. Marker illustrations use
// the same data-driven layer in both, independent of either base asset.
export function CellArtwork({ mode, markers, selectedId, hoveredId }: { mode: CellMode; markers: Marker[]; selectedId: string | null; hoveredId?: string | null }) {
  return <div className={`cell-art cell-art--${mode}`}>
    {mode === 'a' ? <div className="inline-art" aria-hidden="true" dangerouslySetInnerHTML={{ __html: cellA }} />
      : <img className="art-image" src={cellB} alt="Dimensional illustrated lavender immune cell" />}
    {markers.map(m => <span key={m.id}
      className={`receptor receptor--${m.palette} receptor--${m.cellularLocation} receptor--${m.visualFamily} ${selectedId === m.id ? 'is-active' : ''} ${hoveredId === m.id ? 'is-hovered' : ''} ${selectedId && selectedId !== m.id ? 'is-muted' : ''}`}
      style={{'--x': `${m.x}%`, '--y': `${m.y}%`} as CSSProperties} aria-hidden="true">
      <MarkerVisual {...m} selected={selectedId === m.id} hovered={hoveredId === m.id}/>
    </span>)}
  </div>;
}
