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
treasury=treasury.resample('M', on='DATE')['interpolate'].agg(['first'])
treasury.reset_index(inplace=True)
treasury['DATE']=treasury['DATE'].apply(lambda x: x.strftime('%Y-%m'))

chunksize=100000
def f(x):
    if (x['TO_MATURITY']>=1) and (x['TO_MATURITY']<=360):
        return x['first'](x['TO_MATURITY'])
    else:
        return -999

print('start')
data=pd.read_stata('../working/analysis.dta')
data['TRADE_TIME'] = pd.to_datetime(data['TRADE_YEAR'].apply(lambda x: str(int(x))) + data['TRADE_MONTH'].apply(lambda x: str(int(x))),format='%Y%m')
data['TO_MATURITY'] = ((data['MATURITY_DATE'] - data['TRADE_TIME']) / np.timedelta64(1, 'M')).fillna(999).astype(int)
data['TRADE_TIME']=data['TRADE_TIME'].apply(lambda x: x.strftime('%Y-%m'))
data=data.merge(treasury,left_on='TRADE_TIME',right_on='DATE')
data['TS_YIELD']=data.apply(f,axis=1).astype('float')
data.drop(columns=['DATE','first'],inplace=True)
data.to_stata('../working/analysis_yield.dta')

# data=pd.read_stata('../working/analysis.dta',chunksize=chunksize)
# for chunk in data:
#     num=chunk.index[0]
#     chunk['TRADE_TIME'] = pd.to_datetime(chunk['TRADE_YEAR'].apply(lambda x: str(int(x))) + chunk['TRADE_MONTH'].apply(lambda x: str(int(x))),format='%Y%m')
#     chunk['TO_MATURITY'] = ((chunk['MATURITY_DATE'] - chunk['TRADE_TIME']) / np.timedelta64(1, 'M')).fillna(999).astype(int)
#     chunk['TRADE_TIME']=chunk['TRADE_TIME'].apply(lambda x: x.strftime('%Y-%m'))
#     chunk=chunk.merge(treasury,left_on='TRADE_TIME',right_on='DATE')
#     chunk['TS_YIELD']=chunk.apply(f,axis=1).astype('float')
#     chunk.drop(columns=['DATE','first'],inplace=True)
#     print(num)
#     chunk.to_stata('../working/analysis_yield' + str(num//chunksize) + '.dta')

# match dataset line by line
# chunksize=10000
# data=pd.read_stata('../working/analysis.dta',chunksize=chunksize)
# for chunk in data:
#     chunk['TRADE_TIME'] = pd.to_datetime(
#         chunk['TRADE_YEAR'].apply(lambda x: str(int(x))) + chunk['TRADE_MONTH'].apply(lambda x: str(int(x))),
#         format='%Y%m')
#     # difference between trade time
#     date = chunk[chunk['MATURITY_DATE'].isna() == False]
#     chunk['TO_MATURITY'] = ((chunk['MATURITY_DATE'] - chunk['TRADE_TIME']) / np.timedelta64(1, 'M')).fillna(999).astype(
#         int)
#     # loop to get match yield of treasury
#     chunk['TREASURY'] = 0
#     for idx in np.arange(chunk.index[0],chunk.index[0]+chunk.shape[0]):
#         if (idx / 100.0 == idx // 100):
#             print(idx)
#         if ((chunk.loc[idx, 'TO_MATURITY'] >= 1) and (chunk.loc[idx, 'TO_MATURITY'] <= 360)):
#             chunk.loc[idx, 'TREASURY'] = \
#             treasury.iloc[treasury.index.get_loc(chunk['TRADE_TIME'][idx], method='nearest')]['interpolate'](
#                 chunk.loc[idx, 'TO_MATURITY'])
#         else:
#             chunk.loc[idx, 'TREASURY'] = 999
#     chunk.to_stata('../working/analysis_yield'+str(chunk.index[0]//chunksize)+'.dta')

print('hehe')