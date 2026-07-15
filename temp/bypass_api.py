import nbformat
import os

nb_path = '/home/x79/CSIROBoeingPhase4-Vietnam/NDVI_train_sen1_sen2.ipynb'
nb = nbformat.read(nb_path, as_version=4)

# 1. Update Cell 11 (Specify the start and end times)
for cell in nb.cells:
    if cell.cell_type == 'code':
        if "items = list(search.items())" in cell.source and "TEST_MODE" in cell.source:
            cell.source = cell.source.replace(
                "search = catalog.search(\n    collections=[\"sentinel-2-l2a\"],\n    bbox=bbox,\n    datetime=datetime,\n)\nitems = list(search.items())\nprint(f\"Found {len(items)} STAC items\")",
                "if os.path.exists(cache_file):\n    print('Cache found! Skipping STAC search query.')\n    items = []\nelse:\n    search = catalog.search(\n        collections=[\"sentinel-2-l2a\"],\n        bbox=bbox,\n        datetime=datetime,\n    )\n    items = list(search.items())\n    print(f\"Found {len(items)} STAC items\")"
            )

# 2. Update Cell 17 (odc.stac.load)
for cell in nb.cells:
    if cell.cell_type == 'code':
        if "data = odc.stac.load(" in cell.source:
            # We want to skip loading if cache exists
            cell.source = """if 'cache_file' in globals() and os.path.exists(cache_file):
    print("Cache found! Skipping data loading and scaling.")
    data = None
else:
    # The replacement odc.stac.load function for this product
    data = odc.stac.load(
        items,
        **load_params
    )

    # Rename bands to match original code
    data = data.rename({'B02': 'blue', 'B03': 'green', 'B04': 'red', 'B08': 'nir', 'SCL': 'scl'})

    # Planetary computer Sentinel-2 data is already scaled, but might need offset depending on processing baseline. 
    # Usually odc.stac loads it as uint16. To match what datacube does (convert to float and apply scale/offset):
    # Planetary Computer Sentinel-2 L2A has scale=0.0001, offset=0
    data['blue'] = data['blue'].astype('float32') * 0.0001
    data['green'] = data['green'].astype('float32') * 0.0001
    data['red'] = data['red'].astype('float32') * 0.0001
    data['nir'] = data['nir'].astype('float32') * 0.0001

    display(data)
"""

# 3. Update Cell 19 (good_pixel_mask)
for cell in nb.cells:
    if cell.cell_type == 'code':
        if "good_pixel_mask = data[flag_name].isin(good_pixel_flags)" in cell.source:
            cell.source = """if 'cache_file' in globals() and os.path.exists(cache_file):
    print("Cache found! Skipping quality masking.")
    good_pixel_mask = None
else:
    # The "SCL" band contains quality flags and information.
    flag_name = 'scl'

    # Define good pixel flags for Sentinel-2 SCL manually since masking.describe_variable_flags was from datacube
    # 2: Dark area pixels, 4: Vegetation, 5: Not vegetated, 6: Water
    good_pixel_flags = [2, 4, 5, 6]

    # Create a "data quality" Mask layer
    # 1 = good data, 0 = "bad" data
    good_pixel_mask = data[flag_name].isin(good_pixel_flags)
"""

# 4. Update Cell 21 (display mask)
for cell in nb.cells:
    if cell.cell_type == 'code':
        if "display(good_pixel_mask)" in cell.source and "flag_name" not in cell.source:
            cell.source = """if 'cache_file' in globals() and os.path.exists(cache_file):
    print("Cache found! Skipping display mask.")
else:
    # Display the mask
    display(good_pixel_mask)
"""

nbformat.write(nb, nb_path)
print("Notebook optimized to skip API calls when cache exists!")
