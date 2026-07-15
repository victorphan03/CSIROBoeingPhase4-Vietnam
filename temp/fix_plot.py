import nbformat
nb_path = '/home/x79/CSIROBoeingPhase4-Vietnam/NDVI_train_sen1_sen2.ipynb'
nb = nbformat.read(nb_path, as_version=4)

for cell in nb.cells:
    if cell.cell_type == 'code':
        # Fix time index and limit spatial extent for the plot
        if 'isel(time=0)[::10, ::10].compute()' in cell.source:
            cell.source = cell.source.replace('isel(time=0)[::10, ::10].compute()', 'isel(time=0)[1000:1100, 1000:1100].compute()')

nbformat.write(nb, nb_path)
print("Plot optimized!")
