import rioxarray
import os
os.environ["AWS_HTTPS"] = ""
os.environ["GDAL_HTTP_PROXY"] = ""
from easi_tools import unset_cachingproxy
vvpath = 's3://easi-asia-dc-data/staging/ctu/sentinel-1/vv-0922_0923-full_ST.tif'
with unset_cachingproxy():
    vv = rioxarray.open_rasterio(vvpath)
    print("Shape:", vv.shape)
    print("CRS:", vv.rio.crs)
    print("Resolution:", vv.rio.resolution())
    print("Bounds:", vv.rio.bounds())
