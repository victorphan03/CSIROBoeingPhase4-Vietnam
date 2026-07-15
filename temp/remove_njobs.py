import nbformat

nb_path = '/home/x79/CSIROBoeingPhase4-Vietnam/NDVI_train_sen1_sen2.ipynb'
nb = nbformat.read(nb_path, as_version=4)

for cell in nb.cells:
    if cell.cell_type == 'code':
        if "GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy', n_jobs=-1)" in cell.source:
            cell.source = cell.source.replace("GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy', n_jobs=-1)", "GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy')")

nbformat.write(nb, nb_path)
print("Removed n_jobs=-1")
