import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r"C:\Users\Hp\Downloads\phospho_density_outputt.csv")

plt.figure(figsize=(8, 6))
sns.histplot(df['Phospho_Density'].dropna(), bins=30, kde=True, color='skyblue')
plt.title("Distribution of Phosphorylation Density")
plt.xlabel("Phosphorylation Density")
plt.ylabel("Frequency")
plt.tight_layout()

plt.savefig("phospho_density_histogram.png")  # <- Save the figure
print("Plot saved as 'phospho_density_histogram.png'")
