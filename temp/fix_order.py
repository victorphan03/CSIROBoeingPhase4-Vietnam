import nbformat

nb_path = '/home/x79/CSIROBoeingPhase4-Vietnam/NDVI_train_sen1_sen2.ipynb'
nb = nbformat.read(nb_path, as_version=4)

# Find cells
class_names_idx = -1
importance_idx = -1
vis_idx = -1

for i, cell in enumerate(nb.cells):
    if cell.cell_type == 'code':
        if "class_names = ['Lua tom', 'Lua'" in cell.source:
            class_names_idx = i
        if "importance_df = pd.DataFrame({" in cell.source:
            importance_idx = i
        if "precision_val, recall_val, f1_val, _ = precision_recall_fscore_support" in cell.source and vis_idx == -1:
            vis_idx = i

print(f"class_names: {class_names_idx}, importance: {importance_idx}, vis: {vis_idx}")

if importance_idx > vis_idx and vis_idx != -1:
    # Move importance cell before vis cell
    imp_cell = nb.cells.pop(importance_idx)
    nb.cells.insert(vis_idx, imp_cell)
    print("Moved importance_df cell up.")

if class_names_idx > vis_idx and vis_idx != -1:
    # Move class_names cell up
    # Re-find class_names_idx since array changed
    class_names_idx = -1
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code' and "class_names = ['Lua tom', 'Lua'" in cell.source:
            class_names_idx = i
            break
    if class_names_idx > vis_idx:
        cn_cell = nb.cells.pop(class_names_idx)
        nb.cells.insert(vis_idx, cn_cell)
        print("Moved class_names cell up.")

nbformat.write(nb, nb_path)
print("Notebook order fixed!")
