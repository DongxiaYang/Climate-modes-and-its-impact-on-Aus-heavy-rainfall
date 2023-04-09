#!/usr/bin/python3
# needs large memories, access gadi by gadi_jupyter_4cpu.sh
#

import numpy as np
import pandas as pd
import xarray as xr
import time
from datetime import date
import os
import regionmask

import matplotlib.pyplot as plt



#--------------------------------------------------
# 1. get data
# 20CR 1942-2011 U/V wind
# Nino 3.4
# Oliver12 MJO
#--------------------------------------------------

#20CR 1942-2011 U/V wind-----------------------------
filelist=[]
for i in range(1950,2015,1):
    filelist.append(f'/g/data/ua8/LE_models/20CRv3/mean_daily/vwnd/vwnd.{i}.nc')
ds1=xr.open_mfdataset(filelist,combine='by_coords')
ds=ds1['vwnd'].loc[:,850,-45:20,100:160]

##Oliver MJO---------------------------------------
df=pd.read_csv("/g/data/w40/dy9345/MJO/MJO_ot12.csv")
df['time']=pd.to_datetime(df[['year','month','day']])
df=df.set_index('time').drop(columns=['year','month','day'])
df.loc[df['amplitude'].lt(1) ,'phase'] = 0

##----------------------------------------------------
##NINO3.4, monthly resample to daily, nino34>1 elnino, nino34<-1 lanina, else neatural
##----------------------------------------------------
nino=pd.read_csv("/g/data/w40/dy9345/MJO/nina34.anom.data",
                sep='  ', skiprows=3,skipfooter=4,names=np.arange(1,13))
nino=nino.reset_index()
nino_long = pd.melt(nino,id_vars='index')
nino_long = nino_long.rename(columns={'index':'year','variable':'month'})
nino_long['day'] = 1
nino_long['time'] = pd.to_datetime(nino_long[['year','month','day']])
nino_long = nino_long[['time','value']]
nino_long = nino_long.set_index('time').resample('1d').ffill()

nino_long.loc[nino_long['value']<(-1) ,'watch'] = -1
nino_long.loc[nino_long['value']>(1) ,'watch'] = 1
nino_long.loc[(nino_long['value']>(-1)) & (nino_long['value']<(1)),'watch']=0

df2=nino_long

##merge
dfmjo=df.loc[(df.index >= ds.time.min().values) & (df.index <= ds.time.max().values)][['amplitude','phase']]
dfenso=df2.loc[(df2.index >= ds.time.min().values) & (df2.index <= ds.time.max().values)]['watch']
data=xr.merge([ds,dfmjo.to_xarray(),dfenso.to_xarray()],join='inner').load()
data = data.sel(time=data.time.dt.month.isin([1, 2, 3, 4, 11, 12]))


##select Nov-Apr, ELNINO
U_nina = data['vwnd'].loc[data.watch== 1]
phasenina= data['phase'].loc[data.watch== 1]
Ucli=U_nina.mean('time')
Ucli=Ucli.rename('Vcli')

Uano=U_nina-Ucli
U_9 = Uano.groupby(phasenina).mean()
U_9=U_9.rename('Vano')

outf=xr.merge([U_9,Ucli],join='inner').load()
filename = "/g/data/w40/dy9345/MJO/"+'20cr_mean_Vano_elnino_1950_2014.nc'
outf.to_netcdf(filename, 'w')


##select Nov-Apr, LaNina
U_nina = data['vwnd'].loc[data.watch== -1]
phasenina= data['phase'].loc[data.watch== -1]
Ucli=U_nina.mean('time')
Ucli=Ucli.rename('Vcli')

Uano=U_nina-Ucli
U_9 = Uano.groupby(phasenina).mean()
U_9=U_9.rename('Vano')

outf=xr.merge([U_9,Ucli],join='inner').load()
filename = "/g/data/w40/dy9345/MJO/"+'20cr_mean_Vano_lanina_1950_2014.nc'
outf.to_netcdf(filename, 'w')