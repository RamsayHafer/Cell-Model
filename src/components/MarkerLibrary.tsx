import { markerCatalog } from '../markerCatalog';
import { MarkerVisual } from './markers/MarkerVisual';

export function MarkerLibrary() {
  return <section className="marker-library" aria-label="Illustrated marker library">
    <p className="marker-library__note">Artwork examples only. The colors and shapes do not represent a patient result or the molecular structure of a marker.</p>
    {markerCatalog.map(group=><section className="marker-library__group" key={group.title}>
      <h2>{group.title}</h2>
      <div className="marker-library__grid">{group.markers.map(marker=><div className="marker-library__card" key={marker.canonicalName}>
        <span className={`marker-library__name marker-library__name--${marker.palette}`}>{marker.canonicalName}</span>
        <span className="marker-library__illustration"><MarkerVisual {...marker}/></span>
      </div>)}</div>
    </section>)}
  </section>;
}
