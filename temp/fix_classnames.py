import nbformat

nb_path = '/home/x79/CSIROBoeingPhase4-Vietnam/NDVI_train_sen1_sen2.ipynb'
nb = nbformat.read(nb_path, as_version=4)

for cell in nb.cells:
    if cell.cell_type == 'code':
        if "metrics_df = pd.DataFrame(" in cell.source:
            if "class_names = " not in cell.source:
                cell.source = "class_names = ['Lua tom', 'Lua', 'CHN', 'CLN', 'TS', 'Song', 'Dat xay dung', 'Rung']\n" + cell.source
        if "print(classification_report(y_val, y_pred, target_names=class_names))" in cell.source:
            if "class_names = " not in cell.source:
                cell.source = "class_names = ['Lua tom', 'Lua', 'CHN', 'CLN', 'TS', 'Song', 'Dat xay dung', 'Rung']\n" + cell.source
        if "xticklabels=class_names, yticklabels=class_names, ax=axes[0])" in cell.source:
            if "class_names = " not in cell.source:
                cell.source = "class_names = ['Lua tom', 'Lua', 'CHN', 'CLN', 'TS', 'Song', 'Dat xay dung', 'Rung']\n" + cell.source

nbformat.write(nb, nb_path)
print("Injected class_names")
