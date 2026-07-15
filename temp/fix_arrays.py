import nbformat

nb_path = '/home/x79/CSIROBoeingPhase4-Vietnam/NDVI_train_sen1_sen2.ipynb'
nb = nbformat.read(nb_path, as_version=4)

for cell in nb.cells:
    if cell.cell_type == 'code':
        if "X_train, X_temp, y_train, y_temp= train_test_split(x_new, lb_new, test_size=0.4, random_state=42)" in cell.source:
            if "import numpy as np" not in cell.source:
                cell.source += """\n
import numpy as np
X_train = np.array(X_train, dtype=np.float32)
y_train = np.array(y_train, dtype=np.int32)
X_val = np.array(X_val, dtype=np.float32)
y_val = np.array(y_val, dtype=np.int32)
X_test = np.array(X_test, dtype=np.float32)
y_test = np.array(y_test, dtype=np.int32)
"""

nbformat.write(nb, nb_path)
print("Added explicit numpy array conversion!")
