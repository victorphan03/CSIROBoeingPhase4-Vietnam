import nbformat
nb_path = '/home/x79/CSIROBoeingPhase4-Vietnam/NDVI_train_sen1_sen2.ipynb'
nb = nbformat.read(nb_path, as_version=4)

for cell in nb.cells:
    if cell.cell_type == 'code':
        # Remove persist()
        if '.persist()' in cell.source:
            cell.source = cell.source.replace('.persist()', '')
            
        # Remove wait()
        if 'wait(average_ndvi)' in cell.source:
            cell.source = cell.source.replace('wait(average_ndvi)', '# wait(average_ndvi)')
            
        # Fix time index out of bounds
        if 'isel(time=5)' in cell.source:
            cell.source = cell.source.replace('isel(time=5)', 'isel(time=0)')

nbformat.write(nb, nb_path)
print("Notebook final fixes applied!")
