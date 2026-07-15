import nbformat

nb_path = '/home/x79/CSIROBoeingPhase4-Vietnam/NDVI_train_sen1_sen2.ipynb'
nb = nbformat.read(nb_path, as_version=4)

for cell in nb.cells:
    if cell.cell_type == 'code':
        if "wedges, texts, autotexts = axes[0].pie(importances" in cell.source:
            if "if sum(importances) > 0:" not in cell.source:
                new_source = cell.source.replace(
                    "wedges, texts, autotexts = axes[0].pie(importances",
                    "if sum(importances) > 0:\n    wedges, texts, autotexts = axes[0].pie(importances"
                )
                new_source = new_source.replace(
                    "colors=colors_pie, explode=explode, startangle=90,",
                    "    colors=colors_pie, explode=explode, startangle=90,"
                )
                new_source = new_source.replace(
                    "textprops={'fontsize': 11, 'weight': 'bold'})",
                    "    textprops={'fontsize': 11, 'weight': 'bold'})\nelse:\n    axes[0].text(0.5, 0.5, 'No Feature Names Matched', ha='center', va='center')"
                )
                cell.source = new_source

nbformat.write(nb, nb_path)
print("Fixed pie chart NaN issue!")
