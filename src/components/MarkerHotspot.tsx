import type { CSSProperties } from 'react';
import type { Marker } from '../markers';

export function MarkerHotspot({ marker, selected, muted, onSelect, onHover }: { marker: Marker; selected: boolean; muted: boolean; onSelect: () => void; onHover?: (value: boolean) => void }) {
  return <button type="button" aria-label={`${marker.name}: ${marker.status}`} aria-pressed={selected} onClick={onSelect} onMouseEnter={() => onHover?.(true)} onMouseLeave={() => onHover?.(false)} onFocus={() => onHover?.(true)} onBlur={() => onHover?.(false)}
    className={`marker-label marker-label--${marker.palette} ${selected ? 'is-active' : ''} ${muted ? 'is-muted' : ''}`}
    style={{ '--x': `${marker.labelX}%`, '--y': `${marker.labelY}%` } as CSSProperties}>
    <span>{marker.name}{marker.exampleOnly && marker.status === 'inside cell' &&
      <small className="marker-label__subtitle">(inside cell)</small>}</span>
  </button>;
}
