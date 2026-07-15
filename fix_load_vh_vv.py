import nbformat

nb_path = '/home/x79/CSIROBoeingPhase4-Vietnam/load_VH_VV.ipynb'
nb = nbformat.read(nb_path, as_version=4)

for i, cell in enumerate(nb.cells):
    if cell.cell_type == 'code':
        # Replace Cell 2
        if "def load_ctu_s1_data():" in cell.source and "s3://" in cell.source:
            cell.source = """# Cấu hình tải dữ liệu Sentinel-1 từ Microsoft Planetary Computer STAC
import os
import pystac_client
import planetary_computer
import odc.stac
import xarray as xr
import rioxarray

TEST_MODE = True

if TEST_MODE:
    print("====================================================")
    print("--- CHẾ ĐỘ TEST (Chạy nhanh thử nghiệm code) ---")
    print("====================================================")
    min_date = '2022-09-01'
    max_date = '2022-10-01'
    cache_file_vv = 's1_vv_cache_test.nc'
    cache_file_vh = 's1_vh_cache_test.nc'
else:
    print("====================================================")
    print("--- CHẾ ĐỘ HUẤN LUYỆN CHÍNH THỨC (13 THÁNG) ---")
    print("====================================================")
    min_date = '2022-09-01'
    max_date = '2023-10-01'
    cache_file_vv = 's1_vv_cache_prod.nc'
    cache_file_vh = 's1_vh_cache_prod.nc'

def load_ctu_s1_data():
    if os.path.exists(cache_file_vv) and os.path.exists(cache_file_vh):
        print("Cache found! Loading VV and VH from disk...")
        vv = xr.open_dataarray(cache_file_vv).load()
        vh = xr.open_dataarray(cache_file_vh).load()
        return vv, vh
    
    print("Connecting to Planetary Computer STAC...")
    catalog = pystac_client.Client.open(
        "https://planetarycomputer.microsoft.com/api/stac/v1",
        modifier=planetary_computer.sign_inplace,
    )
    
    min_longitude, max_longitude = (105.5, 106.4)
    min_latitude, max_latitude = (9.2, 10.0)
    bbox = [min_longitude, min_latitude, max_longitude, max_latitude]
    datetime = f"{min_date}/{max_date}"
    
    print(f"Searching STAC for sentinel-1-rtc from {min_date} to {max_date}...")
    search = catalog.search(
        collections=["sentinel-1-rtc"],
        bbox=bbox,
        datetime=datetime,
    )
    items = list(search.items())
    print(f"Found {len(items)} STAC items")
    
    if len(items) == 0:
        raise ValueError("No STAC items found! STAC API might be down or parameters are wrong.")
    
    print("Loading data via odc.stac...")
    # Load vv and vh bands. Resolution 10m is standard for S1.
    ds_s1 = odc.stac.load(
        items,
        bands=["vv", "vh"],
        bbox=bbox,
        crs="EPSG:32648",  # Standard for Vietnam, matching what we used in S2
        resolution=10,
        chunks={"x": 2048, "y": 2048, "time": 1}
    )
    
    print("Calculating temporal median (compositing)...")
    ds_s1_median = ds_s1.median(dim="time").compute()
    
    # Extract DataArrays and add 'band' dimension to mimic rioxarray
    vv = ds_s1_median["vv"].expand_dims(dim="band")
    vh = ds_s1_median["vh"].expand_dims(dim="band")
    
    # Ensure they have spatial_ref coordinate like rioxarray
    vv = vv.rio.write_crs("EPSG:32648")
    vh = vh.rio.write_crs("EPSG:32648")
    
    print("Saving cache to disk...")
    vv.to_netcdf(cache_file_vv)
    vh.to_netcdf(cache_file_vh)
    
    return vv, vh

ds, dsvh = load_ctu_s1_data()
"""
            print("Updated Cell 2: Planetary Computer STAC")

        # Replace hardcoded 8874, 9902 in Cell 13
        if "tmp = -1 * np.ones((8874, 9902))" in cell.source:
            cell.source = cell.source.replace(
                "tmp = -1 * np.ones((8874, 9902))",
                "tmp = -1 * np.ones((ds_vhvv.shape[1], ds_vhvv.shape[2]))"
            )
            print("Fixed Cell 13: Removed hardcoded dimensions")

        # Replace hardcoded 8874, 9902 in Cell 17
        if "final_label = final_label.reshape(8874, 9902)" in cell.source:
            cell.source = cell.source.replace(
                "final_label = final_label.reshape(8874, 9902)",
                "final_label = final_label.reshape(ds_vhvv.shape[1], ds_vhvv.shape[2])"
            )
            print("Fixed Cell 17: Removed hardcoded dimensions")

nbformat.write(nb, nb_path)
