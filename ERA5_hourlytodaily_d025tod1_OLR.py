import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import metpy.calc as mpcalc
import numpy as np
import xarray as xr
import pandas as pd


import glob
# Create an empty list to store daily data for all years
daily_data_list = []

for year in range(1959, 2015):
    # List all NetCDF files for the current year
    files = glob.glob(f'/g/data/rt52/era5/single-levels/reanalysis/mtnlwrf/{year}/*.nc')

    # Read all NetCDF files into a single xarray Dataset object
    ds = xr.open_mfdataset(files)

    # Resample the data to daily frequency and take the mean
    daily_ds = ds.resample(time='1D').mean()

    # Append the daily data for the current year to the list
    daily_data_list.append(daily_ds)

# Concatenate the daily data for all years into a single xarray Dataset object
daily_data_all_years = xr.concat(daily_data_list, dim='time')

# Save the daily data for all years to a new NetCDF file
daily_data_all_years.to_netcdf('/g/data/w40/dy9345/MJO/ERA5_OLR_1959-2014.nc')

#convert 0.25° resolution to 1°
# Open the netCDF file
ds = xr.open_dataset('/g/data/w40/dy9345/MJO/ERA5_OLR_1959-2014.nc')

# Coarsen the data using a 4x4 window (for 1° resolution)
ds_coarsened = ds.coarsen(longitude=4, latitude=4,boundary='trim').mean()

# Update the resolution metadata
ds_coarsened.attrs['resolution'] = 1.0

# Save the output to a new netCDF file
ds_coarsened.to_netcdf('/g/data/w40/dy9345/MJO/ERA5_OLR_1959-2014_1deg.nc')
