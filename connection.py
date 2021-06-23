import pandas as pd
import numpy as np
import datetime
import re

state_election=pd.read_stata('../working/party.dta')
race_info=pd.read_stata('../working/raceinfo.dta')
race_info['race_year']=race_info['racedate'].apply(lambda x: int(str(x)[:4]))
race_info['race_month']=race_info['racedate'].apply(lambda x: int(str(x)[4:6]))
df=pd.read_stata('../working/county_vote.dta')

#earlier vote
df['vote_1990']=0
for year in np.arange(1991,2020,dtype=int):
    df.loc[(df['vote_1990']==0) & (df['rd_diffG'+str(year)].isna()==False),'vote_1990']=df.loc[(df['vote_1990']==0) & (df['rd_diffG'+str(year)].isna()==False),'rd_diffG'+str(year)]
vote_1990=df[['state','county','vote_1990']]

#county vote data reshape to long
df=df[[x for x in df.columns if x.startswith('rd_diffP')==False and x.startswith('vote')==False]]
df=df.melt(id_vars=['state','county'])
df['variable']=df['variable'].apply(lambda x: int(x[-4:]))
df=df.sort_values(by=['state','county','variable']).reset_index().drop(columns=['index'])
df=df[df['value'].isna()==False]

# #construct a dataset at state*county*year*month level
# dataset={}
# for state in df['state'].unique():
#     dataset[state]={}
#     for county in df[df['state']==state]['county'].unique():
#         dataset[state][county]={}
#         for year in np.arange(1991,2021):
#             dataset[state][county][year]={}
#             for month in np.arange(1,13):
#                 dataset[state][county][year][month]=np.nan
# dataset=sorted([(k1,k2,k3,k4,v4) for k1,v1 in dataset.items() for k2,v2 in v1.items() for k3,v3 in v2.items() for k4,v4 in v3.items()], key=lambda x: (x[0], x[1]))
# dataset=pd.DataFrame(dataset,columns=list(['state','county','year','month','vote_last']))
# dataset=dataset.sort_values(by=['state','county','year','month'])
#
#
# for state in df['state'].unique():
#     print(state)
#     state_race=race_info[race_info['state']==state].reset_index()
#     state_race=state_race[state_race['office']=='GOVERNOR']
#     state_race.loc[state_race.shape[0],'racedate']=datetime.datetime(2025,12,30) #anytime later than 2020
#     for county in df[df['state']==state]['county'].unique():
#         print(county)
#         for i in np.arange(state_race.shape[0] - 1):
#             year=int(state_race.loc[i,'race_year'])
#             month=int(state_race.loc[i,'race_month'])
#             if (len(df.loc[(df['state']==state) & (df['county']==county) & (df['variable']==year),'value'])>0):
#                 dataset.loc[(dataset['state']==state) & (dataset['county']==county) & (dataset['year']==year) & (dataset['month']==month),'vote_last']=float(df.loc[(df['state']==state) & (df['county']==county) & (df['variable']==year),'value'])
# #dataset.to_stata('../working/party_county.dta')


dataset=pd.read_stata('../working/party_county.dta')

#fill missing values
filled=dataset.groupby(['state','county']).fillna(method='ffill')
dataset=dataset.merge(filled,left_index=True,right_index=True)
dataset.drop(columns=['year_y','month_y','vote_last_x'],inplace=True)
dataset.rename(columns={'year_x':'year','month_x':'month','vote_last_y':'vote_last'},inplace=True)

#earlier vote
dataset=dataset.merge(vote_1990,left_on=['state','county'],right_on=['state','county'],how='left')
dataset.drop(columns=['index_x','index_y'],inplace=True)

#indicator of election month
dataset=dataset.merge(state_election,left_on=['state','year','month'],right_on=['state','year','month'],how='left')
dataset.drop(columns=['level_0','index'],inplace=True)
dataset.rename(columns={'vote_last':'vote_last_county','vote_1990':'vote_1990_county','vote':'vote_last_state'},inplace=True)

#

dataset.to_stata('../working/party_county_all.dta')

print('hehe')