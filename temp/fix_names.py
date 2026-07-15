import nbformat

nb_path = '/home/x79/CSIROBoeingPhase4-Vietnam/NDVI_train_sen1_sen2.ipynb'
nb = nbformat.read(nb_path, as_version=4)

for cell in nb.cells:
    if cell.cell_type == 'code':
        if "n_ndvi_months = 12" in cell.source and "feature_names = [" in cell.source:
            new_source = """
# Dynamic feature names based on actual number of features
n_features = len(feature_importances)
if n_features >= 2:
    feature_names = [f'NDVI_Step_{i+1}' for i in range(n_features - 2)] + ['VH (Sentinel-1)', 'VV (Sentinel-1)']
else:
    feature_names = [f'Feature_{i+1}' for i in range(n_features)]

# Tạo DataFrame và sắp xếp theo importance
importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': feature_importances
}).sort_values('Importance', ascending=False)

print("Feature Importance Ranking / Xếp hạng mức độ quan trọng của đặc trưng:")
print("="*70)
for idx, row in importance_df.iterrows():
    print(f"{row['Feature']:25s}: {row['Importance']:.4f} ({row['Importance']*100:.2f}%)")
print("="*70)
"""
            # Replace the whole block of code
            start_str = "# Tạo tên cho các features"
            end_str = "print(\"=\"*70)"
            
            if start_str in cell.source and end_str in cell.source:
                start_idx = cell.source.find(start_str)
                end_idx = cell.source.find(end_str) + len(end_str)
                cell.source = cell.source[:start_idx] + new_source.strip() + cell.source[end_idx:]

nbformat.write(nb, nb_path)
print("Fixed dynamic feature naming!")
