import nbformat
nb_path = '/home/x79/CSIROBoeingPhase4-Vietnam/NDVI_train_sen1_sen2.ipynb'
nb = nbformat.read(nb_path, as_version=4)

for cell in nb.cells:
    if cell.cell_type == 'code':
        if 'plt.imshow(filled_ds.isel(time=' in cell.source:
            # Comment out the offending imshow
            new_source = []
            for line in cell.source.split('\n'):
                if 'plt.imshow(filled_ds' in line:
                    new_source.append('# ' + line)
                else:
                    new_source.append(line)
            cell.source = '\n'.join(new_source)

nbformat.write(nb, nb_path)
print("Second plot commented out!")
