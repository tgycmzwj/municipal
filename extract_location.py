import pandas as pd
import numpy as np
import re as regex
states={
    'AL':['ALABAMA',' ALA ',' ALA$'],
    'AK':['ALASKA'],
    'AR':[' ARK ',' ARK$','ARKANSAS'],
    'AZ':['ARIZ'],
    'CA':[' CALIF',' CALIF$','CALIFORNIA'],
    'CO':[' COLO ',' COLO$','COLORA'],
    'CT':[' CONN ','^CONN',' CONN$','CONNECTI'],
    'DC':['DISTRICT COL'],
    'DE':['DELAWARE'],
    'FL':[' FLA ',' FLA$','FLORIDA'],
    'GA':[' GA ',' GA$','GEORGIA'],
    #'GU':['GUAM'],
    'HI':['HAWAII'],
    'ID':['IDAHO'],
    'IL':[' ILL ',' ILL$','ILLINOIS'],
    'IN':[' IND ',' IND$','INDIANA'],
    'IA':['IOWA'],
    'KS':[' KANS ',' KANS$','KANSAS'],
    'KY':[' KY ',' KY$','KENTUCKY'],
    'LA':[' LA ',' LA$','LOUISIA'],
    'ME':[' ME ',' ME$','MAINE'],
    'MD':[' MD ',' MD$','MARYLAND'],
    'MA':[' MASS ',' MASS$','MASSAC'],
    'MI':[' MICH ',' MICH$','MICHIGAN'],
    'MN':[' MINN ',' MINN$','MINNESO'],
    'MS':[' MISS ',' MISS$','MISSISS'],
    'MO':[' MO ',' MO$','MISSOU'],
    'MT':['MONTANA',' MT ', ' MT$'],
    'NE':[' NEB ',' NEB$','NEBRA'],
    'NV':[' NEV ',' NEV$','NEVADA'],
    'NH':[' N H ',' N H$','NEW HAM'],
    'NJ':['N J','NEW JERS'],
    'NM':['N MEX','NEW MEX'],
    'NY':['N Y','NEW YORK'],
    'NC':[' N C ',' N C$','NORTH CAR'],
    'ND':[' N D ',' N D$','NORTH DAK'],
    'OH':['OHIO'],
    'OK':['OKLA'],
    'OR':[' ORE ',' ORE$','OREGON'],
    'PA':[' PA ',' PA$','PENNSY'],
    'PR':['PUERTO'],
    'RI':[' R I ',' R I$','RHODE'],
    'SC':[' S C ',' S C$','SOUTH CAR'],
    'SD':[' S D ',' S D$','SOUTH DAK'],
    'TN':['TENN'],
    'TX':[' TEX ',' TEX$','TEXAS'],
    'UT':['UTAH'],
    'VT':[' VT ',' VT$','VERMONT'],
    'VA':[' VA ',' VA$','^VIRGINIA'],
    'WA':[' WASH ',' WASH$','WASHINGTON'],
    'WV':['WEST VIR'],
    'WI':[' WIS ',' WIS$','WISCON'],
    'WY':['WYOM']
}
if __name__=='__main__':
    df = pd.read_stata('../working/id.dta')
    df['state']=''
    for state,abbs in states.items():
        print(state)
        for abb in abbs:
            print(abb)
            df.loc[df['SECURITY_DESCRIPTION'].apply(lambda x: bool(regex.match(abb,x))),'state']=state
    df.to_stata('../working/id_new.dta')
    print('hehe')