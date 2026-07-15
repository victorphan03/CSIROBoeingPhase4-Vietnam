# Hướng dẫn Chuyển đổi dữ liệu vệ tinh sang Microsoft Planetary Computer STAC

Tài liệu này ghi chú lại các bước chuẩn hóa và các đoạn code mẫu để chuyển đổi việc tải dữ liệu vệ tinh (Sentinel-1, Sentinel-2) từ kho lưu trữ đóng (như AWS S3 yêu cầu xác thực) sang nền tảng mở **Microsoft Planetary Computer STAC API**. Bạn có thể dùng tài liệu này làm context (ngữ cảnh) gửi cho các AI khác để chúng hiểu cách thực hiện tương tự.

---

## 1. Mục đích
- Bỏ qua các lỗi liên quan đến xác thực đám mây (VD: `RasterioIOError: AWS_SECRET_ACCESS_KEY not defined`).
- Tải dữ liệu miễn phí, trực tiếp từ kho dữ liệu mở của Microsoft Planetary Computer.
- Đảm bảo đầu ra (output) của dữ liệu STAC giống hệt với định dạng của ảnh TIF gốc tải bằng `rioxarray` để không làm hỏng các luồng xử lý Machine Learning ở phía sau.

## 2. Các thư viện bắt buộc (Dependencies)
Đảm bảo môi trường Python có cài đặt các thư viện sau:
```python
import pystac_client
import planetary_computer
import odc.stac
import xarray as xr
import rioxarray
```

## 3. Các bước thực hiện chi tiết

### Bước 1: Kết nối đến STAC API và truy vấn dữ liệu
Thay vì dùng `rioxarray.open_rasterio("s3://...")`, chúng ta khởi tạo STAC Client và tìm kiếm dữ liệu theo tọa độ (`bbox`) và thời gian (`datetime`).

```python
# 1. Kết nối STAC Client có kèm chữ ký xác thực (sign_inplace) của Microsoft
catalog = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace,
)

# 2. Định nghĩa toạ độ và thời gian
bbox = [105.5, 9.2, 106.4, 10.0] # [min_lon, min_lat, max_lon, max_lat]
datetime = "2022-09-01/2023-10-01"

# 3. Tìm kiếm Items
# Thay "sentinel-1-rtc" bằng "sentinel-2-l2a" nếu tải ảnh quang học
search = catalog.search(
    collections=["sentinel-1-rtc"],
    bbox=bbox,
    datetime=datetime,
)
items = list(search.items())
```

### Bước 2: Tải dữ liệu xuống xarray bằng `odc.stac`
Thay vì tải thủ công từng link URL, `odc.stac.load` sẽ tự động tải, cắt ảnh theo `bbox`, đổi hệ tọa độ (reproject) và ghép lại thành một khối dữ liệu không gian - thời gian (DataCube).

```python
# Tải dữ liệu thành xarray Dataset
ds_s1 = odc.stac.load(
    items,
    bands=["vv", "vh"],           # Tên các band cần tải
    bbox=bbox,
    crs="EPSG:32648",             # Ép về hệ toạ độ đích (VD: UTM Zone 48N cho VN)
    resolution=10,                # Độ phân giải (10 mét)
    chunks={"x": 2048, "y": 2048, "time": 1} # Dùng Dask chunking để tránh tràn RAM
)
```

### Bước 3: Nén trục thời gian (Temporal Compositing)
Dữ liệu từ STAC sẽ có 3 chiều: `(time, y, x)`. Do ảnh TIF gốc cũ thường là ảnh đã được nén (ví dụ trung bình của 1 năm), ta cần dùng phép tính trung vị (`median`) hoặc trung bình (`mean`) để triệt tiêu trục `time`, biến dữ liệu thành dạng 2D `(y, x)`.

```python
# Tính giá trị trung vị theo thời gian
ds_median = ds_s1.median(dim="time").compute()

# Tách riêng các DataArray
vv = ds_median["vv"]
vh = ds_median["vh"]
```

### Bước 4: Khôi phục cấu trúc DataArray gốc (Mimic rioxarray)
Hàm `rioxarray.open_rasterio` gốc luôn trả về dữ liệu có trục `band` (kích thước = 1). Để code Machine Learning bên dưới không bị lỗi "out of bounds" hay "missing dimension", ta phải thêm trục `band` giả và gán lại thông tin `crs`.

```python
# Thêm chiều 'band' để giống hệt rioxarray
vv = vv.expand_dims(dim="band")
vh = vh.expand_dims(dim="band")

# Phục hồi metadata về toạ độ
vv = vv.rio.write_crs("EPSG:32648")
vh = vh.rio.write_crs("EPSG:32648")
```

### Bước 5: Quét và sửa các đoạn code "Hardcode" kích thước
Do lưới tọa độ của STAC tự sinh (dựa trên bounding box) có thể lệch vài pixel so với lưới của file TIF đã cắt tay trên S3 (VD: S3 là `8874 x 9902`, STAC là `8870 x 9900`), **phải tìm và xóa bỏ toàn bộ các con số fix cứng trong mảng**.

*Code cũ sai lầm:*
```python
tmp = np.ones((8874, 9902))
final_label = final_label.reshape(8874, 9902)
```

*Code chuẩn hóa:*
```python
# Lấy linh động theo shape thực tế của xarray
tmp = np.ones((ds_vhvv.shape[1], ds_vhvv.shape[2]))
final_label = final_label.reshape(ds_vhvv.shape[1], ds_vhvv.shape[2])
```

## 4. Tổng kết
Chỉ cần cung cấp tài liệu này cho bất kỳ AI nào, yêu cầu: *"Hãy refactor (viết lại) hàm load file TIF của tôi theo đúng 5 bước trong tài liệu Microsoft Planetary Computer này"*, AI đó sẽ có đủ toàn bộ tư duy và code mẫu để hoàn thành công việc một cách mượt mà nhất.
