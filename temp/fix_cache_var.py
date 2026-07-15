import nbformat

nb_path = '/home/x79/CSIROBoeingPhase4-Vietnam/NDVI_train_sen1_sen2.ipynb'
nb = nbformat.read(nb_path, as_version=4)

for cell in nb.cells:
    if cell.cell_type == 'code' and "cache_file = 'data_cache.npz'" in cell.source:
        cell.source = cell.source.replace("cache_file = 'data_cache.npz'", "# cache_file is set globally in Cell 11")
        print("Fixed cache_file hardcoding!")

nbformat.write(nb, nb_path)
