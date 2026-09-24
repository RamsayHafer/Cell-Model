import type { Marker } from '../markers';

export function MarkerDetailSheet({ marker, onClose }: { marker: Marker | undefined; onClose: () => void }) {
  if (!marker) return null;
  return <section className={`detail-sheet detail-sheet--${marker.palette}`} aria-label={`${marker.name} details`}>
    <div className="sheet-handle"/><div className="sheet-heading"><div><span className="sheet-eyebrow">MARKER DETAIL</span><h2>{marker.name} <span className="sheet-status">{marker.status}</span></h2></div>
      <button className="sheet-close" type="button" onClick={onClose} aria-label="Close marker details">×</button></div>
    <div className="sheet-scroll"><h3>What it normally does</h3><p>{marker.normal}</p><h3>Why doctors look at it</h3><p>{marker.reason}</p><div className="doctor-quote"><span>{marker.exampleOnly ? 'IN THIS DEMO' : 'WHAT YOUR DOCTOR SAID'}</span><p>{marker.quote}</p></div></div>
  </section>;
}
