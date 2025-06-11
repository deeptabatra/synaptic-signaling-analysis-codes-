import pandas as pd
import os
import requests

def fetch_sequence_only(protein_id):
    """Fetch amino acid sequence (not FASTA header) from UniProt"""
    url = f"https://rest.uniprot.org/uniprotkb/{protein_id}.fasta"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            fasta = response.text.split('\n')
            sequence = ''.join([line.strip() for line in fasta if not line.startswith('>')])
            return sequence
        else:
            return f"Error: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Request error: {e}"

input_path = r'C:\Users\Hp\Downloads\1_B_30m_PE.csv'
output_path = os.path.join(os.path.dirname(input_path), 'filtered_final.csv')

df = pd.read_csv(input_path, encoding='utf-8', engine='python')

print(f"Original data: {len(df)} rows")
print(f"Columns found: {list(df.columns)}")

df['PTM.Localising'] = pd.to_numeric(df['PTM.Localising'], errors='coerce')
df['PTM.Site.Confidence'] = pd.to_numeric(df['PTM.Site.Confidence'], errors='coerce')

filtered_df = df[df['PTM.Localising'] != 0]

print(f"After filtering (PTM.Localising != 0): {len(filtered_df)} rows")

if 'Protein.Ids' in filtered_df.columns:
    print("Expanding protein IDs...")
    filtered_df['Protein.Ids'] = filtered_df['Protein.Ids'].astype(str).str.split(';')
    filtered_df = filtered_df.explode('Protein.Ids').reset_index(drop=True)
    print(f"After expanding protein IDs: {len(filtered_df)} rows")
else:
    print("Column 'Protein.Ids' not found. Skipping explosion.")

filtered_df['Protein.Ids'] = filtered_df['Protein.Ids'].str.strip()

print("Fetching protein sequences from UniProt...")
print("This may take a while depending on the number of unique proteins...")

unique_proteins = filtered_df['Protein.Ids'].nunique()
print(f"Need to fetch sequences for {unique_proteins} unique proteins")

filtered_df['Protein_Sequence'] = filtered_df['Protein.Ids'].apply(fetch_sequence_only)

filtered_df.to_csv(output_path, index=False)

print(f"\nFinal filtered, exploded, and annotated data saved to: {output_path}")
print(f"Final dataset: {len(filtered_df)} rows")