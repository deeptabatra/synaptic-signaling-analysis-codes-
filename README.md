# synaptic-signaling-analysis-codes-
Python code for mass spectrometry-based synaptic signaling analysis- phosphosite mapping analysis
Phosphorylation Site Mapping
Phosphorylation site mapping constitutes a critical component of synaptic signaling analysis, focusing on the identification of post-translational modifications (PTMs), specifically phosphorylation sites, on peptide sequences.1
The process begins with the identification of PTM modifications on peptide sequences, and the confidence in these detections is assessed using three distinct thresholds: 0.75, 0.55, and no threshold.1 Following this, the specific phosphorylated residue (Serine (S), Threonine (T), or Tyrosine (Y)) and its precise location on the full protein sequence are determined. Identified proteins are then cross-referenced with UniProt, a comprehensive protein knowledgebase, to ascertain if they are known phosphorylation targets based on their annotated functions.
To quantitatively assess the extent of phosphorylation, "Phospho density" is calculated using the following formula :
PhosphoDensity=ProteinLengthPhosphoSiteCount​
This metric provides a measure of how densely a protein is phosphorylated, offering insights into the overall phosphorylation status of individual proteins.


Kinase Analysis
Kinase analysis aims to identify proteins exhibiting kinase activity and to characterize their potential roles in regulating synaptic signaling pathways.
Proteins showing kinase activity are identified based on the phosphorylation site mapping results, initially using 0.75 and 0.55 confidence thresholds. To ascertain the novelty of these findings, the PhosphoSitePlus server is utilized. This server helps determine if the identified phosphorylated residues and their specific locations are previously documented in public databases or represent novel findings.1 Furthermore, the InterPro Server is employed to perform motif prediction on identified kinase proteins. This step aids in understanding the conserved functional domains and potential binding sites within these proteins, providing structural and functional context.
