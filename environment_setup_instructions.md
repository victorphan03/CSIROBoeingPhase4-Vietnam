# Environment Setup Instructions

This document provides instructions for recreating the Python environment on another machine.

## Environment Details
- **Environment Name:** env_01
- **Python Version:** 3.10.18
- **Platform:** Linux x86_64
- **Export Date:** September 6, 2025

## Files Included
1. `environment.yml` - Complete conda environment specification
2. `requirements.txt` - Pip packages list
3. `environment_setup_instructions.md` - This instruction file

## Method 1: Complete Environment Recreation (Recommended)

### Step 1: Install Miniconda/Anaconda
If not already installed, download and install Miniconda:
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

### Step 2: Create Environment from YAML
```bash
# Navigate to the project directory
cd /path/to/CSIROBoeingPhase4-Vietnam

# Create environment from exported YAML
conda env create -f environment.yml

# Activate the environment
conda activate env_01
```

## Method 2: Manual Environment Creation

### Step 1: Create Base Environment
```bash
# Create new environment with Python 3.10
conda create -n env_01 python=3.10.18

# Activate environment
conda activate env_01
```

### Step 2: Install Core Scientific Packages
```bash
# Install from conda-forge (recommended for geospatial packages)
conda install -c conda-forge \
    numpy=1.26.4 \
    pandas=1.4.2 \
    scipy=1.15.3 \
    scikit-learn=1.1.1 \
    xarray=2025.6.1 \
    rioxarray=0.19.0 \
    rasterio=1.4.3 \
    gdal \
    geopandas \
    matplotlib \
    jupyter \
    ipykernel
```

### Step 3: Install Additional Packages
```bash
# Install remaining packages from requirements.txt
pip install -r requirements.txt
```

## Method 3: Key Packages Only (Minimal Setup)

For a minimal working environment with just the essential packages:

```bash
# Create environment
conda create -n env_01 python=3.10

# Activate
conda activate env_01

# Install core packages
conda install -c conda-forge \
    numpy \
    pandas \
    scipy \
    scikit-learn=1.1.1 \
    xarray \
    rioxarray \
    rasterio \
    gdal \
    geopandas \
    matplotlib \
    jupyter \
    boto3

# Install additional pip packages
pip install datacube easi-tools
```

## Verification

After setting up the environment, verify the installation:

```python
# Test imports
import numpy as np
import pandas as pd
import sklearn
import xarray as xr
import rioxarray
import rasterio
from osgeo import gdal
import geopandas as gpd

print("All imports successful!")
print(f"NumPy: {np.__version__}")
print(f"Pandas: {pd.__version__}")
print(f"Scikit-learn: {sklearn.__version__}")
print(f"Xarray: {xr.__version__}")
```

## Important Notes

1. **Platform Compatibility:** The exported environment is specific to Linux x86_64. For other platforms (Windows, macOS, ARM), some packages may need different versions.

2. **Critical Package Versions:**
   - `scikit-learn=1.1.1` (conda-forge) - Must use this specific version to avoid METRIC_MAPPING64 import errors
   - `numpy=1.26.4` - Compatible with the scikit-learn version
   - `rasterio`, `gdal`, `geopandas` - Use conda-forge channel for geospatial packages

3. **Channel Priority:** Always use `conda-forge` channel for geospatial and scientific packages to ensure compatibility.

4. **Jupyter Kernel:** After creating the environment, register it as a Jupyter kernel:
   ```bash
   conda activate env_01
   python -m ipykernel install --user --name env_01 --display-name "env_01 (Python 3.10)"
   ```

## Troubleshooting

### Common Issues:
1. **METRIC_MAPPING64 Error:** Ensure scikit-learn is installed from conda-forge, not pip
2. **GDAL Import Errors:** Use conda-forge for GDAL and related packages
3. **Version Conflicts:** Use the exact versions specified in environment.yml

### Environment Reset:
If issues persist, remove and recreate the environment:
```bash
conda env remove -n env_01
conda env create -f environment.yml
```

## Contact
If you encounter issues, refer to the original environment setup or contact the system administrator.
