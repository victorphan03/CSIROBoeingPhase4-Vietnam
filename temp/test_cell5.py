
import nbformat
nb = nbformat.read('NDVI_train_sen1_sen2.ipynb', as_version=4)
src = nb.cells[5].source.replace('%%time', '').replace('%matplotlib inline', '')
try:
    exec(src)
except Exception as e:
    import traceback
    traceback.print_exc()

