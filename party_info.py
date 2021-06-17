import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
import datetime

#import race information data
df=pd.read_stata('../working/raceinfo.dta')
df=df[df['office']=='GOVERNOR']
df['rd_diff']=(df['repvote']-df['demvote'])/(df['repvote']+df['demvote'])
df['racedate']=pd.to_datetime(df['racedate'])
#generate a state*year*month dataset
structure={}
for state in df['state'].unique():
    structure[state]={}
    for year in np.arange(1995,2021):
        structure[state][year]={}
        for month in np.arange(1,13):
            structure[state][year][month]=0
structure=sorted([(k1,k2,k3,v3) for k1,v1 in structure.items() for k2,v2 in v1.items() for k3,v3 in v2.items()], key=lambda x: (x[0], x[1]))
structure=pd.DataFrame(structure,columns=list(['state','year','month','party']))

for state in df['state'].unique():
    print(state)
    state_race=df[df['state']==state]
    state_race.reset_index(inplace=True)
    #add one more line for convenience
    state_race.loc[state_race.shape[0],'racedate']=datetime.datetime(2025,12,30) #anytime later than 2020
    for year in np.arange(1995,2021,dtype=int):
        for month in np.arange(1,13,dtype=int):
            obs_time=datetime.datetime(year,month,28)
            for i in np.arange(state_race.shape[0]-1):
                #locate to the correct interval
                if ((state_race.loc[i,'racedate']<obs_time) and (state_race.loc[i+1,'racedate']>=obs_time)):
                    if state_race.loc[i,'rd_diff']<0:
                        structure.loc[(structure['state']==state) & (structure['year']==year) & (structure['month']==month),'party']=-1
                    elif state_race.loc[i,'rd_diff']>0:
                        structure.loc[(structure['state']==state) & (structure['year']==year) & (structure['month']==month),'party']=1
structure.to_stata('../working/party.dta')






print('hehe')