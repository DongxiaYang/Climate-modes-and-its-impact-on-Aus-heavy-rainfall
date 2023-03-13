
Input Data Source:

    
# Daily rainfall
downloa from      wget https://downloads.psl.noaa.gov/Datasets/20thC_ReanV3/Dailies/accumsMO/apcp.$i.nc

local:
    frain = xr.open_mfdataset('//Users/dongxiay/Documents/data/daily/*.nc', parallel=True)
Gadi: /g/data/ua8/LE_models/20CRv3/mean_daily/




# Daily nino34 data 
http://climexp.knmi.nl/data/inino34_daily.dat
    


# Daily MJO
    dt = pd.read_csv("http://passage.phys.ocean.dal.ca/~olivere/data/mjoindex_IHR_20CRV2c.dat")
    dt['date'] = pd.to_datetime(dt[["year", "month", "day"]])
    dt = dt.set_index('date')
    dt.loc[dt['amplitude'].lt(1) ,'phase'] = 0
    mjo=dt[['IHR1','IHR2']].loc['1980-12-01':'2016-02-28']
