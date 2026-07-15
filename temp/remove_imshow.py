import nbformat
nb_path = '/home/x79/CSIROBoeingPhase4-Vietnam/NDVI_train_sen1_sen2.ipynb'
nb = nbformat.read(nb_path, as_version=4)

for cell in nb.cells:
    if cell.cell_type == 'code':
        new_source = []
        for line in cell.source.split('\n'):
            if 'plt.imshow' in line:
                new_source.append('# ' + line)
            else:
                new_source.append(line)
        cell.source = '\n'.join(new_source)

nbformat.write(nb, nb_path)
print("All imshow removed!")
