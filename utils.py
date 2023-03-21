import os
import numpy as np
import xarray as xr
import pandas as pd
from xclim import ensembles
from xclim.ensembles import create_ensemble
from geopy.geocoders import Nominatim

def get_coords(city:str):
    '''
    get lat, lon from city
    see: https://geopy.readthedocs.io/en/stable/#nominatim
    '''
    geolocator = Nominatim(user_agent='http')
    location = geolocator.geocode(city)
    latitude, longitude = location.latitude, location.longitude
    print("Location, (lat, lon): ",location, (latitude, longitude))
    return (latitude, longitude)

def load_mf_dataset(path, models:list):
    '''
    load xr files into a dict of a multi-file dataset per model
    '''
    model_files = {}
    for model in models.split(","):
        model_filenames=[]
        for filename in os.listdir(path):
            if model in filename:
                model_filenames.append(filename)
        model_files[model] = model_filenames

    os.chdir(path)
    data = {}
    for model, files in model_files.items():
        print(model, len(files))
        data[model] = xr.open_mfdataset(files, engine='netcdf4', chunks={'time': 120})
    return data

def multimodel_ensemble(data):
    ''' given a dict of models i.e. model_name[data]=dataset, create an xclim ensemble
    '''
    ensemble = create_ensemble([model for model in data.values()]).load()
    ensemble.close()
    return ensemble