import nbformat

nb_path = '/home/x79/CSIROBoeingPhase4-Vietnam/NDVI_train_sen1_sen2.ipynb'
nb = nbformat.read(nb_path, as_version=4)

# 1. Update Cell 11 (Specify the start and end times)
for cell in nb.cells:
    if cell.cell_type == 'code':
        if "min_date = '" in cell.source and "max_date = '" in cell.source and "catalog.search" in cell.source:
            new_source = """# MODE CONFIGURATION: TEST MODE OR PRODUCTION RUN
# CHẾ ĐỘ CHẠY: TEST (NHANH) HOẶC HUẤN LUYỆN CHÍNH THỨC
TEST_MODE = True  # Đổi thành False nếu muốn chạy chính thức (full thời gian, full tham số)

# Cấu hình thời gian và file cache dựa trên chế độ chạy
if TEST_MODE:
    print("====================================================")
    print("--- CHẾ ĐỘ TEST (Chạy nhanh thử nghiệm code) ---")
    print("====================================================")
    min_date = '2022-09-01'
    max_date = '2022-10-01'  # 1 tháng để chạy test siêu nhanh
    cache_file = 'data_cache_test.npz'
else:
    print("====================================================")
    print("--- CHẾ ĐỘ HUẤN LUYỆN CHÍNH THỨC ---")
    print("====================================================")
    min_date = '2022-09-01'
    max_date = '2023-10-01'  # Toàn bộ 13 tháng
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
print(f"Found {len(items)} STAC items")
"""
            cell.source = new_source

# 2. Update Cell 23 (Loading data from cache)
for cell in nb.cells:
    if cell.cell_type == 'code':
        if "cache_file = 'data_cache.npz'" in cell.source:
            cell.source = cell.source.replace(
                "cache_file = 'data_cache.npz'",
                "if 'cache_file' not in globals():\n    cache_file = 'data_cache.npz'"
            )

# 3. Update GridSearchCV cell (param_grid definition)
for cell in nb.cells:
    if cell.cell_type == 'code':
        if "param_grid = {" in cell.source and "GridSearchCV(pipeline, param_grid" in cell.source:
            new_param_grid = """# Thiết lập các tham số tối ưu hóa dựa theo chế độ chạy
if 'TEST_MODE' in globals() and TEST_MODE:
    # Chế độ TEST: Chỉ chạy 1 cấu hình để kiểm tra luồng code mất 2 giây
    print("GridSearchCV: Running in TEST_MODE (Fast run)...")
    param_grid = {
        'classifier__n_estimators': [100],
        'classifier__max_depth': [6],
        'classifier__split_criterion': ['gini'],
    }
else:
    # Chế độ PRODUCTION: Chạy đầy đủ 250 tổ hợp tham số (mất 5-10 phút trên GPU)
    print("GridSearchCV: Running in PRODUCTION_MODE (Full run)...")
    param_grid = {
        'classifier__n_estimators': [100, 300, 500, 700, 1000],
        'classifier__max_depth': [6, 8, 10, 15, 20],
        'classifier__split_criterion': ['gini', 'entropy'],
    }
"""
            # Replace the old param_grid dict
            start_str = "param_grid = {"
            end_str = "}"
            start_idx = cell.source.find(start_str)
            
            # Find the closing brace of param_grid
            # A simple search is fine because of format
            end_idx = cell.source.find(end_str, start_idx) + 1
            
            cell.source = cell.source[:start_idx] + new_param_grid.strip() + cell.source[end_idx:]

nbformat.write(nb, nb_path)
print("Notebook toggles successfully created!")
