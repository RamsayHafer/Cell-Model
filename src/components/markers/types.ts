export type CellularLocation = 'membrane' | 'nuclear' | 'cytoplasmic' | 'unknown';

export type VisualFamily =
  | 'membrane-receptor'
  | 'branched-receptor'
  | 'forked-receptor'
  | 'cytoplasmic-protein'
  | 'nuclear-protein'
  | 'transcription-factor'
  | 'proliferation-pattern'
  | 'dna-mutation'
  | 'gene-fusion'
  | 'copy-number'
  | 'chromosomal-loss'
  | 'generic';

export type MarkerPalette = 'blue' | 'coral' | 'purple' | 'green' | 'gold' | 'cyan';
export type MarkerResultState = 'present' | 'reduced' | 'absent' | 'lost' | 'pending' | 'mentioned' | 'numeric';

// This contract is independent of placement, tap targets, text, and evidence.
// A consuming app can pass its existing marker data through an adapter.
export type MarkerVisualSpec = {
  canonicalName: string;
  cellularLocation: CellularLocation;
  visualFamily: VisualFamily;
  visualVariant?: string;
  palette: MarkerPalette;
  resultState: MarkerResultState;
  // A numeric value alone has no biological direction. Set this only when
  // clinical logic outside the renderer has interpreted the number.
  numericInterpretation?: 'present' | 'reduced' | 'absent';
  size?: number;
  orientation?: number;
};
