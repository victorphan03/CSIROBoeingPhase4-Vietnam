import nbformat
import os

nb_path = '/home/x79/CSIROBoeingPhase4-Vietnam/NDVI_train_sen1_sen2.ipynb'
nb = nbformat.read(nb_path, as_version=4)

# We want to wrap intermediate cells between data loading and cache loading.
# If cache exists, these cells should do nothing.

for cell in nb.cells:
    if cell.cell_type == 'code':
        # Cell: data_layer_names
        if "data_layer_names = [x for x in data.data_vars if x != 'scl']" in cell.source:
            cell.source = """if 'cache_file' in globals() and os.path.exists(cache_file):
    print("Cache found! Skipping layer names extraction.")
    data_layer_names = []
else:
    data_layer_names = [x for x in data.data_vars if x != 'scl']"""

        # Cell: result = data[data_layer_names].where(...)
        if "result = data[data_layer_names].where(good_pixel_mask)" in cell.source:
            cell.source = """if 'cache_file' in globals() and os.path.exists(cache_file):
    print("Cache found! Skipping mask application.")
    result = None
else:
    from dask.distributed import progress
    # Apply good pixel mask to blue, green, red and nir.
    result = data[data_layer_names].where(good_pixel_mask)"""

        # Cell: wait(result)
        if "wait(result)" in cell.source and "persist()" in cell.source:
            cell.source = """if 'cache_file' in globals() and os.path.exists(cache_file):
    print("Cache found! Skipping Dask wait.")
else:
    print("Using persist() - data is being computed in background")
    from distributed import wait
    wait(result)  # Wait for computation without progress bar
    print("Computation completed successfully!")"""

        # Cell: ds1 = calculate_indices(result, ...)
        if "ds1 = calculate_indices(result" in cell.source:
            cell.source = """if 'cache_file' in globals() and os.path.exists(cache_file):
    print("Cache found! Skipping index calculation.")
    ndvi = None
    average_ndvi = None
else:
    ds1 = calculate_indices(result, index='NDVI', satellite_mission='s2')
    ndvi = ds1["NDVI"]
    average_ndvi = ndvi.resample(time='1M').mean()  ## tính mean cho từng tháng -> time = 12"""

        # Cell: wait(average_ndvi)
        if "NDVI computation completed successfully" in cell.source:
            cell.source = """if 'cache_file' in globals() and os.path.exists(cache_file):
    print("Cache found! Skipping NDVI wait.")
else:
    print("Using persist() - NDVI data is being computed in background")
    from distributed import wait
    # wait(average_ndvi)  # Wait for computation without progress bar
    print("NDVI computation completed successfully!")"""

        # Cell: average_ndvi = average_ndvi.compute()
        if "average_ndvi = average_ndvi.compute()" in cell.source:
            cell.source = """if 'cache_file' in globals() and os.path.exists(cache_file):
    print("Cache found! Skipping NDVI compute.")
else:
    average_ndvi = average_ndvi.compute()"""

        # Cell: filled_ds = average_ndvi.interpolate_na(...)
        if "filled_ds = average_ndvi.interpolate_na(" in cell.source:
            cell.source = """if 'cache_file' in globals() and os.path.exists(cache_file):
    print("Cache found! Skipping interpolation.")
    filled_ds = None
else:
    # Fill in missing values
    filled_ds = average_ndvi.interpolate_na(dim='time')"""

        # Cell: filled_ds = average_ndvi.bfill(dim='time')
        if "filled_ds = average_ndvi.bfill(dim='time')" in cell.source:
            cell.source = """if 'cache_file' in globals() and os.path.exists(cache_file):
    print("Cache found! Skipping bfill/ffill.")
    filled_ds = None
else:
    filled_ds = average_ndvi.bfill(dim='time')
    filled_ds = filled_ds.ffill(dim='time')"""

        # Cell: dsvh = ...
        if "dsvh =" in cell.source and "dsvv =" in cell.source:
            cell.source = """if 'cache_file' in globals() and os.path.exists(cache_file):
    print("Cache found! Skipping Sentinel-1 loading.")
    dsvh = None
    dsvv = None
else:
    import rioxarray
    # Load Sentinel-1 data
    dsvh = rioxarray.open_rasterio("vh-0922_0923-full_ST.tif")
    dsvv = rioxarray.open_rasterio("vv-0922_0923-full_ST.tif")"""

nbformat.write(nb, nb_path)
print("Bypassed all intermediate cells successfully!")
