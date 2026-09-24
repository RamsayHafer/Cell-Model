export type CellularLocation = 'surface' | 'cytoplasm' | 'nucleus';

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
export type MarkerResultState = 'present' | 'reduced' | 'absent' | 'lost' | 'pending' | 'mentioned';

// This contract is independent of placement, tap targets, text, and evidence.
// A consuming app can pass its existing marker data through an adapter.
export type MarkerVisualSpec = {
  canonicalName: string;
  cellularLocation: CellularLocation;
  visualFamily: VisualFamily;
  visualVariant?: string;
  palette: MarkerPalette;
  resultState: MarkerResultState;
  size?: number;
  orientation?: number;
};
