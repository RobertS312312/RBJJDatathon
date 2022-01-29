import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import io



def SimpleInterpolateColumn(one_pandas_columns):
    
    for i in range(len(one_pandas_columns)):
        if pd.isna(one_pandas_columns.iloc[i]):
            # We know [i-1] must be non null at the point, only have 
            # to worry about if [i+1] is non null, if it is null we go 
            # forward until we reach end of data or we find one that is 
            # non null

            next_non_null_idx = i+1
            while True:
                if next_non_null_idx < len(one_pandas_columns):
                    #If there is no future, then just use the past
                    one_pandas_columns.iloc[i] = one_pandas_columns.iloc[i-1]
                    break
                elif not pd.isna(one_pandas_columns[next_non_null_idx]):
                    ##Then we have found the future
                    one_pandas_columns.iloc[i] = one_pandas_columns.iloc[next_non_null_idx] + one_pandas_columns.iloc[i-1]
                    break
                else:
                    next_non_null_idx+=1
    
    return one_pandas_columns

def CleanWholeDataFrame(df):

    df = df.drop(labels = 0, axis = 0)

    ##These columns were 80+% nulls when we wrote the project
    drop_list = ['WVHT','DPD','GST','APD','MWD','PRES','WTMP','PTDY','TIDE']

    df.drop(drop_list, inplace=True, axis=1)

    for col_name in df.columns:
        df[col_name][ df[col_name] == "MM" ] = np.nan
        df[col_name] = df[col_name].astype("float32")

    for col in df.columns:
        if col == 'Date':
            break
    else:
        df[col] = SimpleInterpolateColumn(df[col])

    return df

def to_csv_string(filepath):

    f = open(filepath)
    csv_string = ""
    for line in f:
        csv_string += ",".join( line.split() )
        csv_string += "\n"
    
    return csv_string.strip()

def filepath2df(filepath):

    stream = io.StringIO(to_csv_string(filepath))
    df = pd.read_csv(stream, sep = ",")
    return df


#kbqx_data_old = pd.read_csv("UncleanedData\KBQX.csv")

#kbqx_data_new = pd.read_table("UncleanedData\KBQX.txt")


#kbqx_nan_count = kbqx_data.isnull().sum(axis = 0)
#kikt_nan_count = kikt_data.isnull().sum(axis = 0)
#kmis_nan_count = kmis_data.isnull().sum(axis = 0) 

#kbqx_data.to_csv('CleanData\KBQX.csv')
#kikt_data.to_csv('CleanData\KIKT.csv')
#kmis_data.to_csv('CleanData\KMIS.csv')
