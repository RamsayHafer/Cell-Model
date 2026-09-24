import { useEffect, useState } from 'react';
import type { Marker } from '../markers';
import { CellArtwork, type CellMode } from './CellArtwork';
import { MarkerHotspot } from './MarkerHotspot';
import { MarkerDetailSheet } from './MarkerDetailSheet';

export function CellVisualization({ mode, markers, showMarkers = true }: { mode: CellMode; markers: Marker[]; showMarkers?: boolean }) {
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [hoveredId, setHoveredId] = useState<string | null>(null);
  useEffect(() => setSelectedId(null), [mode, showMarkers]);
  useEffect(() => { const close = (event: KeyboardEvent) => { if (event.key === 'Escape') setSelectedId(null); }; window.addEventListener('keydown', close); return () => window.removeEventListener('keydown', close); }, []);
  const visible = showMarkers ? markers : [];
  const selected = visible.find(marker => marker.id === selectedId);
  return <div className="cell-experience">
    <div className="cell-stage"><span className="stage-aura" aria-hidden="true"/><div className="cell-composition">
      <CellArtwork mode={mode} markers={visible} selectedId={selectedId} hoveredId={hoveredId}/>
      <svg className="marker-connectors" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
        {visible.filter(marker => marker.cellularLocation === 'nuclear' || marker.cellularLocation === 'cytoplasmic').map(marker => <path key={marker.id} className={`connector connector--${marker.palette} ${selectedId && selectedId !== marker.id ? 'is-muted' : ''}`}
          d={marker.exampleOnly && marker.status === 'inside cell'
            ? `M ${marker.x + 2} ${marker.y + 2} V ${marker.labelY - 7} Q ${marker.x + 2} ${marker.labelY - 3} ${marker.x + 6} ${marker.labelY - 3} H ${marker.labelX - 8}`
            : `M ${marker.x + 2} ${marker.y + 2} Q ${(marker.x + marker.labelX) / 2 + 5} ${marker.y + 13} ${marker.labelX - 5} ${marker.labelY - 3}`} />)}
      </svg>
      {visible.map(marker => <MarkerHotspot key={marker.id} marker={marker} selected={selectedId === marker.id} muted={!!selectedId && selectedId !== marker.id} onSelect={() => setSelectedId(marker.id)} onHover={active => setHoveredId(active ? marker.id : null)}/>)}
    </div></div>
    <div className="stage-caption">{showMarkers ? 'Tap a marker to explore' : 'A quiet moment to see the cell itself'}</div>
    <MarkerDetailSheet marker={selected} onClose={() => setSelectedId(null)}/>
  </div>;
}
