# %%
import os
import numpy as np
import xarray as xr
import pandas as pd
import pyesgf as pyesgf
from pyesgf.search import SearchConnection
os.environ["ESGF_PYCLIENT_NO_FACETS_STAR_WARNING"] = "on"
from geopy.geocoders import Nominatim
from pyesgf.search import SearchConnection
from dask.diagnostics import ProgressBar
from utils import *

wd = os.getcwd()
print(wd)
# Make sure these directories exist
models_dir=os.path.join(wd, 'data/models')
reference_dir=os.path.join(wd, 'data/reference')
if not os.path.exists(models_dir):
  os.makedirs(models_dir)
if not os.path.exists(reference_dir):
  os.makedirs(reference_dir)

# %%
city = 'Nairobi'
latitude, longitude = get_coords(city)

# %%
# %%
# Download any of the reanalysis reference .nc datasets W5E5 from: https://data.isimip.org/datasets/96369b63-4fbf-4b90-8b58-79e5f50a385a/, and add it to the current working directory.
W5E5 = xr.open_mfdataset(os.path.join(wd, '*.nc'), engine = 'netcdf4').sel(lat=latitude, lon=longitude, method='nearest').convert_calendar("noleap")

# %%
project='CMIP6'
models = 'GFDL-ESM4,IPSL-CM6A-LR,MPI-ESM1-2-HR,MRI-ESM2-0'#,UKESM1-0-LL'
variable_id = 'tas'
table_id = 'day'
experiment_id='historical'
member_id='r1i1p1f1,r1i1p1f2' # f1 not available for UKESM1-0-LL

connection = SearchConnection('https://esgf-data.dkrz.de/esg-search', distrib=True)
query = connection.new_context(
    latest = True,
    project='CMIP6',
    source_id=models,
    experiment_id=experiment_id,
    variable_id=variable_id,
    table_id=table_id,
    member_id=member_id,
    data_node='esgf.ceda.ac.uk')

print("Number of search results:", query.hit_count)

results = query.search()
files=[]
for i, result in enumerate(results):
    print("Retrieving search results: ", result.dataset_id)
    #print(result.json)
    files.extend(list(map(lambda f : {'model': f.json['source_id'].pop(), 'dataset_id': result.dataset_id, 'filename': f.filename, 'url': f.opendap_url}, result.file_context().search())))

files = list(files)
files = pd.DataFrame.from_dict(files)
files.drop_duplicates('filename')

grouped_files = files.groupby('model', as_index=False).agg(list)
grouped_files

# %%
# load all files from url list for each model into xarray multi-file dataset

start_time = W5E5.time[0].values
end_time = W5E5.time[-1].values

data={}
for i,model in enumerate(grouped_files.model):
    print("Selecting location...")
    print("Loading dataset: ", model)

    data[model]=xr.open_mfdataset(grouped_files.iloc[i].url, chunks={'time': 120}).sel(
        lat=latitude, lon=longitude, method='nearest').convert_calendar(
        'noleap', align_on='year', missing='NaN').sel(
        time=slice(start_time,end_time)).interpolate_na(method='nearest')

# %%
os.chdir(wd)
for model, dataset in data.items():
    print("Saving ", model, "for selected city ", city)
    identifier = '_'.join([model, city])
    years, y_datasets = zip(*dataset.groupby("time.year"))
    fns=[identifier+f'_{y}.nc' for y in years]
    paths=[os.path.join(models_dir,fn) for fn in fns]
    with ProgressBar():
        xr.save_mfdataset(y_datasets[-2:], paths[-2:], mode="w") # saving only 2 years of data for demo
        ### For the purpsoe of inspecting the dataset as a pandas dataframe
        df = dataset.to_dataframe()
        print("Dataframe for (", model, ",", city, "):", df)


# %%
os.chdir(wd)
end_time = min([dataset.time[-1].values for dataset in data.values()])
reference = W5E5.sel(time=slice(start_time,end_time))
print("Saving reference for selected city ", city)
identifier = '_'.join(['W5E5', city])
years, y_datasets = zip(*reference.groupby("time.year"))
fns=[identifier+f'_{y}.nc' for y in years]
paths=[os.path.join(reference_dir,fn) for fn in fns]
with ProgressBar():
    xr.save_mfdataset(y_datasets[-2:], paths[-2:], mode="w")

# # %%
# ds = xr.open_dataset('/home/minh/Documents/CI_2023/data/models/GFDL-ESM4_Nairobi_1979.nc')
# df = ds.to_dataframe()
# print(df)


# %%



