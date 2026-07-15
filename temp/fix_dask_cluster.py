import nbformat
nb_path = '/home/x79/CSIROBoeingPhase4-Vietnam/NDVI_train_sen1_sen2.ipynb'
nb = nbformat.read(nb_path, as_version=4)

for cell in nb.cells:
    if cell.cell_type == 'code':
        if 'cluster = LocalCluster()' in cell.source:
            cell.source = cell.source.replace('cluster = LocalCluster()', "import os\nos.environ['GDAL_HTTP_MAX_RETRY'] = '5'\nos.environ['GDAL_HTTP_RETRY_DELAY'] = '3'\nos.environ['GDAL_HTTP_TIMEOUT'] = '60'\ncluster = LocalCluster(n_workers=4, threads_per_worker=4)")

nbformat.write(nb, nb_path)
print("Dask cluster optimized!")
