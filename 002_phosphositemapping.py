import pandas as pd
import os
import numpy as np

input_path = r'C:\Users\Hp\Downloads\filtered_with_UniMod.csv'
output_path = os.path.join(os.path.dirname(input_path), 'phospho_residuee_only.csv')

df = pd.read_csv(input_path)


df['PTM.Localising_Original'] = df['PTM.Localising']

df['PTM.Localising'] = pd.to_numeric(df['PTM.Localising'], errors='coerce').apply(np.floor).astype('Int64')

def get_phosphorylated_residue(row):
    peptide = str(row['Stripped.Sequence']).strip()
    ptm_loc = row['PTM.Localising']
    
    if not peptide or pd.isna(ptm_loc):
        return None
    if ptm_loc <= 0 or ptm_loc > len(peptide):
        return None  # Invalid position

    # If the pointed residue is Proline (P), check previous residue
    if peptide[ptm_loc - 1] == 'P' and ptm_loc > 1:
        return peptide[ptm_loc - 2]
    else:
        return peptide[ptm_loc - 1]


df['Phospho_Residue'] = df.apply(get_phosphorylated_residue, axis=1)

df = df[df['Phospho_Residue'].isin(['S', 'T', 'Y'])]


df.to_csv(output_path, index=False)
print(f"Output saved to: {output_path}")
