import pandas as pd

file_path = r"C:\Users\Hp\Downloads\1_D_I_30m.mzML.xlsx - Sheet1.csv"
df = pd.read_csv(file_path)

df.columns = df.columns.str.strip()
print("Columns:", df.columns.tolist())  # Optional debug line

df['is_phospho'] = df['Modified.Sequence'].str.contains('UniMod:21', na=False)
df['is_unmod'] = df['Modified.Sequence'] == df['Stripped.Sequence']

# Prepare results
results = []

# Group by Protein.Ids and Stripped.Sequence
for (protein, peptide), group in df.groupby(['Protein.Ids', 'Stripped.Sequence']):
    phospho_intensity = group[group['is_phospho']]['Precursor.Quantity'].sum()
    unmod_intensity = group[group['is_unmod']]['Precursor.Quantity'].sum()
    total = phospho_intensity + unmod_intensity
    if total > 0:
        occupancy = phospho_intensity / total * 100
        results.append({
            'Protein.Ids': protein,
            'Peptide': peptide,
            'Phospho_Intensity': phospho_intensity,
            'Unmod_Intensity': unmod_intensity,
            'Occupancy_percent': occupancy
        })

occupancy_df = pd.DataFrame(results)
occupancy_df.to_csv('phosphosite_occupanccy_results.csv', index=False)
print(occupancy_df)
