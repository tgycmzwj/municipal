from municipal.extract_location import states
import pandas as pd
import numpy as np
import re as regex
import os

for state in list(states.keys()):
    print(state)
    df1=pd.read_stata('../working/city_'+state+'.dta')
    df2=pd.read_stata('../working/id_'+state+'.dta')
    df2['county']=''
    #matching
    counties=[]
    for index in np.arange(df1.shape[0]):
        #cities
        cur_city=df1.loc[index,'city_ascii']
        cur_county=df1.loc[index,'county_name']
        city_match=df2['SECURITY_DESCRIPTION'].apply(lambda x: bool(regex.match(cur_city,x)))
        df2.loc[city_match, 'county'] = cur_county
        print('Num of match for city '+cur_city+' is '+str(city_match.sum()))
        #counties
        if (cur_county not in counties):
            counties.append(cur_county)
            county_match=df2['SECURITY_DESCRIPTION'].apply(lambda x: bool(regex.match(cur_county, x)))
            df2.loc[county_match, 'county'] = cur_county
            print('Num of match for county ' + cur_county + ' is ' + str(county_match.sum()))
    if state=='MA':
        df2['MATURITY_DATE']=pd.to_datetime(df2['MATURITY_DATE'],errors = 'coerce')
    df2.to_stata('../working/id_county_'+state+'.dta')

os.system('say "your program has finished"')
print('hehe')