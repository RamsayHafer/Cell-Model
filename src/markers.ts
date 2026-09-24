import type { MarkerVisualSpec } from './components/markers/types';

// Visual metadata is independent of placement, selection, text and evidence.
export type Marker = MarkerVisualSpec & {
  id: string;
  name: string;
  status: string;
  exampleOnly?: boolean;
  x: number; y: number; // Percent of 440 × 440 illustration viewBox.
  labelX: number; labelY: number;
  normal: string;
  reason: string;
  quote: string;
};

export const sampleMarkers: Marker[] = [
  { id:'cd4', name:'CD4', canonicalName:'CD4', status:'Positive', palette:'blue', cellularLocation:'membrane', visualFamily:'membrane-receptor', resultState:'present', orientation:-20, x:34, y:24, labelX:19, labelY:16,
    normal:'CD4 is a surface protein found on helper T cells, which help coordinate immune responses.',
    reason:'Doctors may use CD4 staining to help describe which immune cells are present in a tissue sample.',
    quote:'“The cells in your sample were CD4-positive.”' },
  { id:'cd30', name:'CD30', canonicalName:'CD30', status:'Present', palette:'coral', cellularLocation:'membrane', visualFamily:'branched-receptor', visualVariant:'reference-cd30', resultState:'present', size:1.2, orientation:16, x:71, y:25, labelX:83, labelY:16,
    normal:'CD30 is a signaling protein found on some activated immune cells. It helps regulate how immune cells respond and communicate.',
    reason:'Some lymphomas express CD30, so testing for it can help describe the cells and may inform treatment discussions.',
    quote:'“Your biopsy showed CD30-positive cells.”' },
  { id:'cd7', name:'CD7', canonicalName:'CD7', status:'Loss', palette:'purple', cellularLocation:'membrane', visualFamily:'forked-receptor', visualVariant:'reference-cd7', resultState:'lost', orientation:-90, x:19, y:58, labelX:11, labelY:54,
    normal:'CD7 is a surface protein commonly found on T cells.',
    reason:'A change in CD7 staining is one detail pathologists consider alongside the rest of the biopsy.',
    quote:'“The report notes loss of CD7 expression.”' },
  { id:'ki67', name:'Ki-67', canonicalName:'Ki-67', status:'Discussed', palette:'green', cellularLocation:'nuclear', visualFamily:'proliferation-pattern', resultState:'mentioned', x:54, y:51, labelX:86, labelY:80,
    normal:'Ki-67 is a protein associated with cells that are actively dividing.',
    reason:'Doctors may discuss the Ki-67 result as one way to describe how active the sampled cells appear.',
    quote:'“We also talked about the Ki-67 result.”' },
];

// These show spatial behaviors, not a co-expression pattern or patient findings.
export const markerStudyMarkers: Marker[] = [
  { ...sampleMarkers[1], id:'study-cd30', status:'Illustrated receptor', exampleOnly:true,
    x:72, y:25, labelX:83, labelY:14, size:1.3, orientation:18,
    quote:'A surface receptor illustration; no patient result is represented.' },
  { id:'study-cd7', name:'CD7', canonicalName:'CD7', status:'Illustrated receptor', palette:'purple', cellularLocation:'membrane', visualFamily:'forked-receptor', visualVariant:'reference-cd7', resultState:'present', exampleOnly:true,
    x:22, y:60, labelX:11, labelY:46, size:1.46, orientation:-90,
    normal:'CD7 is a cell-surface protein found on many T cells.',
    reason:'The graphic demonstrates a different surface receptor silhouette from CD30.',
    quote:'A surface receptor illustration; no patient result is represented.' },
  { id:'study-bcl2', name:'BCL2', canonicalName:'BCL2', status:'Illustrated location', palette:'gold', cellularLocation:'cytoplasmic', visualFamily:'cytoplasmic-protein', resultState:'present', exampleOnly:true,
    x:37, y:69, labelX:15, labelY:84, size:1.28,
    normal:'BCL2 is a protein associated with cell survival and is found at mitochondria inside the cell.',
    reason:'This warm amber protein cluster demonstrates an intracellular location; it is not a surface receptor.',
    quote:'An intracellular location example; no patient result is represented.' },
  { id:'study-p53', name:'p53', canonicalName:'p53', status:'Illustrated location', palette:'cyan', cellularLocation:'nuclear', visualFamily:'nuclear-protein', resultState:'present', exampleOnly:true,
    x:54, y:51, labelX:84, labelY:77, size:1.16,
    normal:'p53 is a protein involved in a cell’s response to damage and is commonly found in the nucleus.',
    reason:'This compact blue cluster demonstrates a nuclear marker, distinct from a membrane receptor.',
    quote:'A nuclear location example; no patient result is represented.' },
];

// A dedicated visual reference scene, never a patient result. These positions
// follow the supplied 244 × 259 illustration; the visit scene retains its
// clinical states and the four-location study remains available separately.
export const referenceStudyMarkers: Marker[] = [
  { ...sampleMarkers[0], id:'reference-cd4', status:'Illustrated receptor', exampleOnly:true,
    visualVariant:'reference-cd4', size:1.03, orientation:-21, x:30, y:26, labelX:19, labelY:12 },
  { ...sampleMarkers[1], id:'reference-cd30', status:'Illustrated receptor', exampleOnly:true,
    size:1.18, orientation:24, x:72, y:26, labelX:83, labelY:9 },
  { ...sampleMarkers[2], id:'reference-cd7', status:'Illustrated receptor', exampleOnly:true,
    resultState:'present', size:1.26, orientation:-79, x:19, y:60, labelX:7, labelY:47 },
  { ...sampleMarkers[3], id:'reference-ki67', status:'Illustrated pattern', exampleOnly:true,
    resultState:'present', visualVariant:'reference-ki67', size:1.12,
    x:67, y:71, labelX:91, labelY:87 },
];
