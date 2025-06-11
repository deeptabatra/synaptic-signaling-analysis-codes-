import pandas as pd
import os

input_path = r'C:\Users\Hp\Downloads\phosphositemapping - proteinlocation 0.75 (1).csv'
df = pd.read_csv(input_path)

direct_keywords = [
    'phosphorylation', 'phosphorylated', 'phosphatase', 'kinase',
    'phospho-', 'dephosphorylation', 'autophosphorylation'
]

context_keywords = [
    'synaptic vesicle exocytosis', 'synaptic transmission', 'signal transduction',
    'actin cytoskeleton', 'microtubule', 'transport', 'receptor trafficking',
    'nmda receptor', 'endocytosis', 'vesicle transport', 'dendritic spine',
    'synaptic plasticity'
]

def tag_phospho_target(function_text):
    if pd.isna(function_text):
        return False, ''
    text = function_text.lower()
    for kw in direct_keywords:
        if kw in text:
            return True, f"matched keyword: {kw}"
    for kw in context_keywords:
        if kw in text:
            return True, f"matched keyword: {kw}"
    return False, ''

results = df['Function'].apply(tag_phospho_target)
df['Is_Phospho_Target'] = results.apply(lambda x: x[0])
df['Phospho_Target_Reason'] = results.apply(lambda x: x[1])

output_path = os.path.join(os.path.dirname(input_path), 'phosphosite_with_phospho_targets.csv')
df.to_csv(output_path, index=False)

print(f"Updated file saved to: {output_path}")

