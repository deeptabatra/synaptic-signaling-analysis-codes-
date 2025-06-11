import pandas as pd
import requests

input_csv = r'C:\Users\Hp\Downloads\phospho_residue_only_with_uniprot_metadatta.csv'  
protein_column = 'Protein.Ids'  # <--- update this to the column name in your CSV containing protein IDs
output_path = 'protein_function_description.csv'

df = pd.read_csv(input_csv)

df[protein_column] = df[protein_column].astype(str).str.strip()

unique_proteins = df[protein_column].unique()

def fetch_function_description(protein_id):
    url = f"https://rest.uniprot.org/uniprotkb/{protein_id}.json"
    response = requests.get(url)
    if response.status_code != 200:
        return "NA"
    
    data = response.json()
    for comment in data.get("comments", []):
        if comment.get("commentType") == "FUNCTION":
            texts = comment.get("texts", [])
            if texts:
                return texts[0].get("value", "NA")
    return "NA"

results = []
for pid in unique_proteins:
    function = fetch_function_description(pid)
    results.append({'Protein_ID': pid, 'Function': function})

result_df = pd.DataFrame(results)


result_df.to_csv(output_path, index=False)
print(f"Done! Function descriptions saved to: {output_path}")
