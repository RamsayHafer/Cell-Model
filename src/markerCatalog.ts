import type { MarkerVisualSpec } from './components/markers/types';

export type MarkerCatalogGroup = { title:string; markers:MarkerVisualSpec[] };

// Illustrative artwork from the supplied reference sheet. These are visual
// examples, never patient findings or a claim about molecular shape.
const membrane = (canonicalName:string, visualVariant:string, palette:MarkerVisualSpec['palette'], visualFamily:MarkerVisualSpec['visualFamily']='membrane-receptor'):MarkerVisualSpec =>
  ({ canonicalName, cellularLocation:'membrane', visualFamily, visualVariant, palette, resultState:'present' });
const inside = (canonicalName:string, visualVariant:string, palette:MarkerVisualSpec['palette'], cellularLocation:MarkerVisualSpec['cellularLocation']='cytoplasmic'):MarkerVisualSpec =>
  ({ canonicalName, cellularLocation, visualFamily:cellularLocation==='nuclear'?'proliferation-pattern':'cytoplasmic-protein', visualVariant, palette, resultState:'present' });

export const markerCatalog:MarkerCatalogGroup[] = [
  { title:'T-cell markers', markers:[
    membrane('CD3','sheet-triple','blue'), membrane('CD4','sheet-fork','blue','forked-receptor'),
    membrane('CD5','sheet-triad','green','branched-receptor'), membrane('CD7','sheet-quad','purple','forked-receptor'),
    membrane('CD8','sheet-twin','indigo','forked-receptor'),
  ]},
  { title:'B-cell markers', markers:[
    membrane('CD19','sheet-triad','pink','branched-receptor'), membrane('CD20','sheet-loops','purple'),
    membrane('CD79a','sheet-y','pink','forked-receptor'),
  ]},
  { title:'Activation / lymphoma markers', markers:[
    membrane('CD25','sheet-four','orange','branched-receptor'), membrane('CD30','sheet-cluster','coral','branched-receptor'),
    membrane('CD45','sheet-wave','gold'),
  ]},
  { title:'Cytotoxic / NK markers', markers:[
    membrane('CD56','sheet-many','green','branched-receptor'), inside('TIA-1','sheet-granules','blue'),
    inside('Granzyme B','sheet-spray','cyan'),
  ]},
  { title:'Intracellular / proliferation / checkpoint', markers:[
    inside('Ki-67','sheet-dots','green','nuclear'), membrane('PD-1','sheet-fork','purple','forked-receptor'),
    membrane('PD-L1','sheet-curve','pink'), inside('ALK','sheet-bands','indigo'),
  ]},
];
