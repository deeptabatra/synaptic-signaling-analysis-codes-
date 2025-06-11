import pandas as pd

df = pd.read_csv(r"C:\Users\Hp\Downloads\input_path.csv")

df['Phospho_Site_Count'] = df.groupby('Protein_ID')['Site_Label'].transform('nunique')

df['Phospho_Density'] = df['Phospho_Site_Count'] / df['Protein_Length']

output_file_name = r"C:\Users\Hp\Downloads\phospho_density_outputt.csv"
df.to_csv(output_file_name, index=False)

print(f"Phosphorylation density saved to: {output_file_name}")

