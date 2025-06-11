import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

input_file = r"C:\Users\Hp\Downloads\phospho_density_outputt.csv"
df = pd.read_csv(input_file)

df['Phospho_Site_Count'] = df.groupby('Protein_ID')['Site_Label'].transform('nunique')

df['Phospho_Density'] = df['Phospho_Site_Count'] / df['Protein_Length']

df = df.dropna(subset=['Phospho_Density'])

df_unique_proteins = df[['Protein_ID', 'Protein_Length', 'Phospho_Site_Count', 'Phospho_Density']].drop_duplicates(subset='Protein_ID')

sns.set_style("whitegrid")

n_top = 20
top_density_proteins = df_unique_proteins.sort_values(by='Phospho_Density', ascending=False).head(n_top)

plt.figure(figsize=(12, 7))
sns.barplot(x='Phospho_Density', y='Protein_ID', data=top_density_proteins, palette='viridis')
plt.title(f'Top {n_top} Proteins by Phosphorylation Density', fontsize=16)
plt.xlabel('Phospho_Density (Sites per Amino Acid)', fontsize=12)
plt.ylabel('Protein ID', fontsize=12)
plt.tight_layout()
plt.savefig(f'top_{n_top}_phospho_density_proteins.png', dpi=300)
plt.close()

print(f"Plot saved as 'top_{n_top}_phospho_density_proteins.png'")
