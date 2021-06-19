import pandas as pd
import numpy as np
import datetime
import os
from scipy import interpolate


def remove_dup_columns(frame):
    keep_names = set()
    keep_icols = list()
    for icol, name in enumerate(frame.columns):
        if name not in keep_names:
            keep_names.add(name)
            keep_icols.append(icol)
    return frame.iloc[:, keep_icols]


#treasury year data
treasury={}
files=[file for file in os.listdir('../raw/treasury') if file.endswith('.csv')]
for file in files:
    treasury[file]=pd.read_csv('../raw/treasury/'+file)
    treasury[file]['DATE']=pd.to_datetime(treasury[file]['DATE'])
    treasury[file]=treasury[file][treasury[file]['DATE']>datetime.datetime(2004,12,31)]
    treasury[file].reset_index(inplace=True)
treasury=pd.concat(treasury,axis=1)
treasury=treasury.droplevel(0,axis=1)
treasury=remove_dup_columns(treasury)
treasury=treasury[['DATE','DGS1MO','DGS3MO','DGS6MO','DGS1','DGS2','DGS3','DGS5','DGS7','DGS10','DGS20','DGS30']]
#interpolate
x=np.array([1,3,6,12,24,36,60,84,120,240,360])
treasury['interpolate']=''
treasury=treasury[treasury['DGS1MO']!='.']
treasury.reset_index(inplace=True)
del treasury['index']
# for var in treasury.columns[1:]:
#     treasury.loc[treasury[var]=='.',var]=100
for idx in np.arange(treasury.shape[0]):
    treasury.loc[idx,'interpolate']=interpolate.interp1d(x,treasury.loc[idx,:][1:-1],kind='quadratic')
treasury.index=treasury['DATE']



data=pd.read_stata('../working/analysis.dta')
data['TRADE_TIME']=pd.to_datetime(data['TRADE_YEAR'].apply(lambda x: str(int(x))) +data['TRADE_MONTH'].apply(lambda x: str(int(x))) , format='%Y%m')
#difference between trade time
date=data[data['MATURITY_DATE'].isna()==False]
data['TO_MATURITY']=((data['MATURITY_DATE']-data['TRADE_TIME'])/np.timedelta64(1,'M')).fillna(999).astype(int)
#loop to get match yield of treasury
data['TREASURY']=0
for idx in np.arange(data.shape[0]):
    if (idx/100.0==idx//100):
        print(idx)
    if ((data.loc[idx,'TO_MATURITY']>=1) and (data.loc[idx,'TO_MATURITY']<=360)):
        data.loc[idx,'TREASURY']=treasury.iloc[treasury.index.get_loc(data['TRADE_TIME'][idx],method='nearest')]['interpolate'](data.loc[idx,'TO_MATURITY'])
    else:
        data.loc[idx,'TREASURY']=999

data.to_stata('../working/analysis_yield.dta')
print('hehe')