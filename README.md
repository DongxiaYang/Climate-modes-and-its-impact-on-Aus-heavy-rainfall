Aim:Using climate modes (ENSO/IOD/MJO) to simulate/predict the tropical Australian Rainfall variation based on RF/XGboost Machine Learning models
Input features:
Weekly/Monthly ENSO/IOD leading rainfall anomaly by 1-6 months, MJO leading rainfall anomaly by 1-6 weeks.
Input Data Source:
# Daily nino34 data 
http://climexp.knmi.nl/data/inino34_daily.dat
    
# weekly DMI data 
/Users/dongxiay/Documents/data/dmi.nc
download 
#!/bin/bash
for i in {1981..2020}
do
    wget https://downloads.psl.noaa.gov/Datasets/20thC_ReanV3/accumsMO/apcp.$i.nc
done

# Daily MJO
    dt = pd.read_csv("http://passage.phys.ocean.dal.ca/~olivere/data/mjoindex_IHR_20CRV2c.dat")
    dt['date'] = pd.to_datetime(dt[["year", "month", "day"]])
    dt = dt.set_index('date')
    dt.loc[dt['amplitude'].lt(1) ,'phase'] = 0
    mjo=dt[['IHR1','IHR2']].loc['1980-12-01':'2016-02-28']
    
# Daily railfall
downloa from      wget https://downloads.psl.noaa.gov/Datasets/20thC_ReanV3/Dailies/accumsMO/apcp.$i.nc
local:
    frain = xr.open_mfdataset('//Users/dongxiay/Documents/data/daily/*.nc', parallel=True)
Gadi: /g/data/ua8/LE_models/20CRv3/mean_daily/


Loss function: RMSE

How to tune hyperparameters?

1)skilearn gridsearch function  
2) self-define function


