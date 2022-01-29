import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

kbqx_data = pd.read_csv('UncleanedData\KBQX.csv')
kikt_data = pd.read_csv('UncleanedData\KIKT.csv')
kmis_data = pd.read_csv('UncleanedData\KMIS.csv')

# kbqx_nan_count = kbqx_data.isnull().sum(axis = 0)
# kikt_nan_count = kikt_data.isnull().sum(axis = 0)
# kmis_nan_count = kmis_data.isnull().sum(axis = 0)

drop_list = ['WVHT','DPD','GST','APD','MWD','PRES','WTMP','PTDY','TIDE']

kbqx_data.drop(drop_list, inplace=True, axis=1)
kikt_data.drop(drop_list, inplace=True, axis=1)
kmis_data.drop(drop_list, inplace=True, axis=1)
        
# kbqx_nan_count = kbqx_data.isnull().sum(axis = 0)
# kikt_nan_count = kikt_data.isnull().sum(axis = 0)
# kmis_nan_count = kmis_data.isnull().sum(axis = 0) 

for col in kbqx_data.columns:
    if col == 'Date':
        break
    for i in range(len(kbqx_data)):
        if np.isnan(kbqx_data[col][i]):
            kbqx_data[col][i]= kbqx_data[col][i-1]
            
for col in kikt_data.columns:
    if col == 'Date':
        break
    for i in range(len(kikt_data)):
        if np.isnan(kikt_data[col][i]):
            kikt_data[col][i]= kikt_data[col][i-1]
            
for col in kmis_data.columns:
    if col == 'Date':
        break
    for i in range(len(kmis_data)):
        if np.isnan(kmis_data[col][i]):
            kmis_data[col][i]= kmis_data[col][i-1]
            
            
kbqx_nan_count = kbqx_data.isnull().sum(axis = 0)
kikt_nan_count = kikt_data.isnull().sum(axis = 0)
kmis_nan_count = kmis_data.isnull().sum(axis = 0) 

kbqx_data.to_csv('CleanData\KBQX.csv')
kikt_data.to_csv('CleanData\KIKT.csv')
kmis_data.to_csv('CleanData\KMIS.csv')
