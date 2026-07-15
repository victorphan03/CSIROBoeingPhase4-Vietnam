import nbformat
nb_path = '/home/x79/CSIROBoeingPhase4-Vietnam/NDVI_train_sen1_sen2.ipynb'
nb = nbformat.read(nb_path, as_version=4)

for cell in nb.cells:
    if cell.cell_type == 'code':
        if "vvpath = 'vv-0922_0923-full_ST.tif'" in cell.source:
            cell.source = cell.source.replace("vvpath = 'vv-0922_0923-full_ST.tif'", "vvpath = 'ThuanHoa/ThuanHoa_VV.tif'")
            cell.source = cell.source.replace("vhpath = 'vh-0922_0923-full_ST.tif'", "vhpath = 'ThuanHoa/ThuanHoa_VH.tif'")

nbformat.write(nb, nb_path)
print("Paths fixed!")
