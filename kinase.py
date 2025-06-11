import pandas as pd

# Input file path
input_path = r'C:\Users\Hp\Downloads\phosphositemapping - proteinlocation_0.55.csv'

df = pd.read_csv(input_path)

df = df.loc[:, ~df.columns.str.match(r'^\s*$')]
df.columns = df.columns.str.strip().str.replace('.', '_', regex=False)

print("✅ Available columns in file:")
print(df.columns.tolist())

if 'Protein_ID' in df.columns and 'Function' in df.columns:
    # Filter rows where 'Function' mentions 'kinase'
    kinase_df = df[df['Function'].str.contains('kinase', case=False, na=False)]

   
    kinase_ids = kinase_df['Protein_ID'].unique()

  
    print("\n✅ Proteins with kinase activity found:")
    for pid in kinase_ids:
        print(pid)

  
    output_path = input_path.replace('.csv', '_kinase_only.csv')
    kinase_df.to_csv(output_path, index=False)
    print(f"\n Kinase protein data saved to: {output_path}")
else:
    print("Error: The file does not contain 'Protein_ID' and/or 'Function' columns after cleaning.")
