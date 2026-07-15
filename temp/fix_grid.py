import nbformat
nb_path = '/home/x79/CSIROBoeingPhase4-Vietnam/NDVI_train_sen1_sen2.ipynb'
nb = nbformat.read(nb_path, as_version=4)

for cell in nb.cells:
    if cell.cell_type == 'code':
        if "'classifier__criterion'" in cell.source:
            cell.source = cell.source.replace("'classifier__criterion'", "'classifier__split_criterion'")

nbformat.write(nb, nb_path)
print("GridSearchCV param fixed!")
