import nbformat

nb_path = '/home/x79/CSIROBoeingPhase4-Vietnam/NDVI_train_sen1_sen2.ipynb'
nb = nbformat.read(nb_path, as_version=4)

# 1. Replace the extraction cell to add the IF condition
for cell in nb.cells:
    if cell.cell_type == 'code':
        if "ndvi_points = filled_ds.sel(x=x_coords, y=y_coords, method='nearest').compute()" in cell.source:
            # This is the extraction cell
            new_source = """import os
import numpy as np

cache_file = 'data_cache.npz'
if os.path.exists(cache_file):
    print("Cache found! Loading data from disk...")
    cache = np.load(cache_file)
    x_new = cache['x_new'].tolist()
    lb_new = cache['lb_new'].tolist()
    loaded_datasets = {} # Dummy to prevent errors later
else:
"""
            for line in cell.source.split('\n'):
                new_source += "    " + line + "\n"
            cell.source = new_source
            
        # 2. Modify the x_new appending cell to add saving logic
        if 'x_new.append(X[i]["data"])' in cell.source:
            new_source = """if not os.path.exists(cache_file):
    X = []
    x_new = []
    lb_new = []
    for k, v in loaded_datasets.items():
        X.append(v)
    for i in range(len(X)):
        if X[i] is not None:
            x_new.append(X[i]["data"])
            lb_new.append(numeric_labels[i])
            
    print("Saving extracted data to cache...")
    np.savez(cache_file, x_new=x_new, lb_new=lb_new)
else:
    print("Data loaded from cache successfully. Ready for training!")
"""
            cell.source = new_source

nbformat.write(nb, nb_path)
print("Caching logic injected!")
