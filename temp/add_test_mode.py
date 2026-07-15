import nbformat
import os

nb_path = '/home/x79/CSIROBoeingPhase4-Vietnam/NDVI_train_sen1_sen2.ipynb'
nb = nbformat.read(nb_path, as_version=4)

# Find cell 11 (the one with min_date and max_date)
for idx, cell in enumerate(nb.cells):
    if cell.cell_type == 'code' and 'min_date' in cell.source and 'max_date' in cell.source and 'sentinel-2-l2a' in cell.source:
        cell.source = """# MODE CONFIGURATION: TEST MODE OR PRODUCTION RUN
# CHẾ ĐỘ CHẠY: TEST (NHANH) HOẶC HUẤN LUYỆN CHÍNH THỨC
TEST_MODE = True  # Đổi thành False nếu muốn chạy chính thức (full thời gian, full tham số)

if TEST_MODE:
    min_date = '2022-09-01'
    max_date = '2022-10-01'
    cache_file = 'data_cache_test.npz'
else:
    min_date = '2022-01-01'
    max_date = '2023-01-01'
    cache_file = 'data_cache_prod.npz'

# Specify a spatail region to search using latitude/longitude cooridinates
min_longitude, max_longitude = (105.5, 106.4)
min_latitude, max_latitude = (9.2, 10.0)

# Construct STAC search query
bbox = [min_longitude, min_latitude, max_longitude, max_latitude]
datetime = f"{min_date}/{max_date}"

search = catalog.search(
    collections=["sentinel-2-l2a"],
    bbox=bbox,
    datetime=datetime,
)
items = list(search.items())
print(f"Found {len(items)} STAC items")"""
        print("Updated Cell with TEST_MODE!")
        break

nbformat.write(nb, nb_path)
