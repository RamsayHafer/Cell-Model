import React from 'react';
import { createRoot } from 'react-dom/client';
import { useState } from 'react';
import { CellVisualization } from './components/CellVisualization';
import type { CellMode } from './components/CellArtwork';
import { sampleMarkers, markerStudyMarkers, referenceStudyMarkers } from './markers';
import './styles.css';

function App() {
  const referencePreview = new URLSearchParams(window.location.search).has('reference');
  const [mode, setMode] = useState<CellMode>('a');
  const [showMarkers, setShowMarkers] = useState(true);
  const [markerSet, setMarkerSet] = useState<'visit' | 'locations' | 'reference'>(referencePreview ? 'reference' : 'visit');
  return <main className={`app-shell ${markerSet === 'reference' ? 'reference-scene' : ''}`}><header className="topbar"><div className="brand-icon" aria-hidden="true">✳</div><span>VISIT EXPLAINED <span className="brand-divider">/</span> CELL LAB</span></header>
    <nav className="prototype-switch" aria-label="Select prototype"><button type="button" aria-current={mode === 'a' ? 'page' : undefined} onClick={() => setMode('a')}>A <span>Interactive SVG</span></button><button type="button" aria-current={mode === 'b' ? 'page' : undefined} onClick={() => setMode('b')}>B <span>Illustration + Overlay</span></button></nav>
    <div className="intro"><span className="eyebrow">{markerSet === 'visit' ? 'YOUR BIOPSY, VISUALIZED' : 'BIOMARKER VISUAL STUDY'}</span><h1>{'Your T cell (simplified)'}</h1><p>{markerSet === 'visit' ? 'Tap a marker to explore what your doctor discussed.' : 'Four illustrated markers; no patient results.'}</p></div>
    <CellVisualization key={markerSet} mode={mode} markers={markerSet === 'visit' ? sampleMarkers : markerSet === 'reference' ? referenceStudyMarkers : markerStudyMarkers} showMarkers={showMarkers} referenceStudy={markerSet === 'reference'}/>
    <div className="marker-set" role="group" aria-label="Marker examples"><button type="button" aria-pressed={markerSet === 'visit'} onClick={() => setMarkerSet('visit')}>Visit markers</button><button type="button" aria-pressed={markerSet === 'locations'} onClick={() => setMarkerSet('locations')}>Marker study</button><button type="button" aria-pressed={markerSet === 'reference'} onClick={() => setMarkerSet('reference')}>Reference study</button></div>
    <label className="quiet-toggle"><input type="checkbox" checked={!showMarkers} onChange={event => setShowMarkers(!event.target.checked)}/><span className="toggle-track"/><span>View cell without markers</span></label>
  </main>;
}

createRoot(document.getElementById('root')!).render(<React.StrictMode><App/></React.StrictMode>);
