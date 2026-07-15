import nbformat
nb_path = '/home/x79/CSIROBoeingPhase4-Vietnam/NDVI_train_sen1_sen2.ipynb'
nb = nbformat.read(nb_path, as_version=4)

for cell in nb.cells:
    if cell.cell_type == 'code':
        # Remove the global compute
        if 'average_ndvi = average_ndvi.compute()' in cell.source:
            cell.source = cell.source.replace('average_ndvi = average_ndvi.compute()', '# average_ndvi = average_ndvi.compute()')
        
        # Optimize plotting to just compute a small subset if needed
        if 'plt.imshow(average_ndvi.isel(time=5))' in cell.source:
            cell.source = cell.source.replace('plt.imshow(average_ndvi.isel(time=5))', 'plt.imshow(average_ndvi.isel(time=5)[::10, ::10].compute())')
            
        # Optimize the extraction loop using vectorized indexing
        if 'for idx, point in train.iterrows():' in cell.source:
            optimized_code = """
import xarray as xr

# Vectorized point extraction (much faster than loop)
x_coords = xr.DataArray(train.geometry.x.values, dims="point")
y_coords = xr.DataArray(train.geometry.y.values, dims="point")

print("Extracting NDVI data...")
ndvi_points = filled_ds.sel(x=x_coords, y=y_coords, method='nearest').compute()
print("Extracting VH data...")
vh_points = dsvh.sel(x=x_coords, y=y_coords, method='nearest').compute()
print("Extracting VV data...")
vv_points = dsvv.sel(x=x_coords, y=y_coords, method='nearest').compute()

loaded_datasets = {}
for idx, point in train.iterrows():
    key = f"point_{idx + 1}"
    try:
        ndvi_data = ndvi_points.isel(point=idx).values
        vh_data = vh_points.isel(point=idx).values
        vv_data = vv_points.isel(point=idx).values
        
        loaded_datasets[key] = {
            "data": np.concatenate((ndvi_data, vh_data, vv_data)),
            "label": point.HT_code
        }
    except Exception as e:
        print(e)
"""
            cell.source = optimized_code

nbformat.write(nb, nb_path)
print("Notebook optimized for faster extraction!")
