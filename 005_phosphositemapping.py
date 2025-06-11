import pandas as pd
import requests

input_path = r'C:\Users\Hp\Downloads\1DHPG30min phosophosite.csv'
df = pd.read_csv(input_path)

df.columns = df.columns.str.strip()

df['PTM.Localising'] = pd.to_numeric(df['PTM.Localising'], errors='coerce')
df['PTM.Site.Confidence'] = pd.to_numeric(df['PTM.Site.Confidence'], errors='coerce')

filtered_df = df[(df['PTM.Localising'] != 0) & (df['PTM.Site.Confidence'] >= 0.55)]

def get_protein_site(row):
    protein_seq = str(row['Protein_Sequence'])
    peptide = str(row['Stripped.Sequence'])
    ptm_loc = row['PTM.Localising']
    peptide_start = protein_seq.find(peptide)
    if peptide_start == -1 or pd.isna(ptm_loc):
        return None
    return peptide_start + ptm_loc

filtered_df['Protein_Site'] = filtered_df.apply(get_protein_site, axis=1)
filtered_df['Site_Label'] = filtered_df['Phospho_Residue'] + filtered_df['Protein_Site'].astype(str)

phosphosite_df = filtered_df[['Phospho_Residue', 'Protein_Site', 'Site_Label', 'Protein_ID']].dropna().drop_duplicates()

unique_ids = phosphosite_df['Protein_ID'].unique()

def fetch_uniprot_data(protein_id):
    url = f"https://rest.uniprot.org/uniprotkb/{protein_id}.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        length = data.get("sequence", {}).get("length", None)
        organism = data.get("organism", {}).get("scientificName", None)
        try:
            protein_name = data['proteinDescription']['recommendedName']['fullName']['value']
        except KeyError:
            protein_name = None
        return pd.Series([length, organism, protein_name])
    else:
        return pd.Series([None, None, None])

metadata_df = pd.DataFrame(unique_ids, columns=['Protein_ID'])
metadata_df[['Protein_Length', 'Scientific_Name', 'Protein_Name']] = metadata_df['Protein_ID'].apply(fetch_uniprot_data)

final_df = phosphosite_df.merge(metadata_df, on='Protein_ID', how='left')

output_path = input_path.replace('.csv', '_with_uniprot_metadata.csv')
final_df.to_csv(output_path, index=False)

print(f"Formatted phosphosite data with UniProt metadata saved to:\n{output_path}")
