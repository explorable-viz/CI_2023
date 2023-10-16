# Climate Informatics 2023: 'A locally time-invariant metric for climate model ensemble predictions of extreme risk'

Code and data associated with the submission 'A locally time-invariant metric for climate model ensemble predictions of extreme risk'.

#### Data download

Data used to produce the results presented in tha paper are provided in the folder 'data'. These are time-series taken from one realisation per model for the CMIP6 members GFDL-ESM4, IPSL-CM6A-LR, MPI-ESM1-2-HR, MRI-ESM2-0, and UKESM1-0-LL, for nine cities Paris, Chicago, Sydney, Tokyo, Kolkata, Kinshasa, Shenzhen and Santo Domingo. The same time-series from an observational reanalysis data, W5E5, are also provided.

-- Notes:
I'm using Python 3.11.5

1. Some non-exhaustive dependencies I've had to install:
```
pip3 install esgf-pyclient
pip3 install geopy
pip3 install xclim
pip3 install netcdf4
```
2. Download one of the `nc` dataset files from [the reanalysis reference dataset W5E5 Data set](https://data.isimip.org/datasets/96369b63-4fbf-4b90-8b58-79e5f50a385a/). The smallest one is [this one](https://files.isimip.org/ISIMIP3a/SecondaryInputData/climate/atmosphere/obsclim/global/daily/historical/W5E5v2.0/tas_W5E5v2.0_19790101-19801231.nc).
3. `python3 data_download.py`

