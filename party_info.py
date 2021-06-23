import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
import datetime

#import race information data
df=pd.read_stata('../working/raceinfo.dta')
df=df[df['office']=='GOVERNOR']
df['rd_diff']=(df['repvote']-df['demvote'])/(df['repvote']+df['demvote'])
df['racedate']=pd.to_datetime(df['racedate'])
close_cutoff=0.05

structure=pd.read_stata('../working/party.dta')

# #generate a state*year*month dataset
# structure={}
# for state in df['state'].unique():
#     structure[state]={}
#     for year in np.arange(1991,2021):
#         structure[state][year]={}
#         for month in np.arange(1,13):
#             structure[state][year][month]=0
# structure=sorted([(k1,k2,k3,v3) for k1,v1 in structure.items() for k2,v2 in v1.items() for k3,v3 in v2.items()], key=lambda x: (x[0], x[1]))
# structure=pd.DataFrame(structure,columns=list(['state','year','month','vote']))
# structure['election']=0
#
# #indicators for parties in all states, all years and all months
# for state in df['state'].unique():
#     print(state)
#     state_race=df[df['state']==state]
#     state_race.reset_index(inplace=True)
#     #add one more line for convenience
#     state_race.loc[state_race.shape[0],'racedate']=datetime.datetime(2025,12,30) #anytime later than 2020
#     for year in np.arange(1991,2021,dtype=int):
#         for month in np.arange(1,13,dtype=int):
#             obs_time=datetime.datetime(year,month,28)
#             for i in np.arange(state_race.shape[0]-1):
#                 #locate to the correct interval
#                 if ((state_race.loc[i,'racedate']<obs_time) and (state_race.loc[i+1,'racedate']>=obs_time)):
#                     # if state_race.loc[i,'rd_diff']<0:
#                     #     structure.loc[(structure['state']==state) & (structure['year']==year) & (structure['month']==month),'party']=-1
#                     # elif state_race.loc[i,'rd_diff']>0:
#                     #     structure.loc[(structure['state']==state) & (structure['year']==year) & (structure['month']==month),'party']=1
#                     structure.loc[(structure['state']==state) & (structure['year']==year) & (structure['month']==month),'vote']=state_race.loc[i,'rd_diff']
#                 #point value for election and close election indicator
#                 if ((year==state_race.loc[i,'racedate'].year) and (month==state_race.loc[i,'racedate'].month)):
#                     structure.loc[(structure['state']==state) & (structure['year']==year) & (structure['month']==month),'election']=1
#                     # if (np.abs(state_race.loc[i,'rd_diff'])<close_cutoff):
#                     #     structure.loc[(structure['state']==state) & (structure['year']==year) & (structure['month']==month),'close']=1


#time to the next election
#time to the last election
structure['to_last']=structure['election']
structure['to_next']=structure['election']
election_index=structure.index[structure['election']==1]
for idx in np.arange(structure.shape[0]):
    print(idx)
    earlier=[it for it in election_index if ((it<idx) and(structure.loc[it,'state']==structure.loc[idx,'state']))]
    later=[it for it in election_index if ((it>idx) and(structure.loc[it,'state']==structure.loc[idx,'state']))]
    if len(earlier)==0:
        structure.loc[idx,'to_last']=-999
    else:
        structure.loc[idx,'to_last']=idx-max(earlier)+1
    if len(later)==0:
        structure.loc[idx,'to_next']=-999
    else:
        structure.loc[idx,'to_next']=min(later)-idx




structure.to_stata('../working/party.dta')



print('hehe')