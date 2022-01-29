import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import io



def SimpleInterpolateColumn(one_pandas_columns):
    
    this_col_interpolated = pd.Series( [False] * len(one_pandas_columns))
    for i in range(len(one_pandas_columns)):
        if pd.isna(one_pandas_columns.iloc[i]) or one_pandas_columns.iloc[i]>360 or one_pandas_columns.iloc[i]<0  :
            # We know [i-1] must be non null at the point, only have 
            # to worry about if [i+1] is non null, if it is null we go 
            # forward until we reach end of data or we find one that is 
            # non null

            next_non_null_idx = i+1
            while True:
                if next_non_null_idx >= len(one_pandas_columns):
                    #If there is no future, then just use the past
                    one_pandas_columns.iloc[i] = one_pandas_columns.iloc[i-1]
                    this_col_interpolated[i] = True
                    break
                elif not (pd.isna(one_pandas_columns.iloc[i]) or one_pandas_columns.iloc[i]>360 or one_pandas_columns.iloc[i]<0):
                    ##Then we have found the future
                    one_pandas_columns.iloc[i] = one_pandas_columns.iloc[next_non_null_idx] + one_pandas_columns.iloc[i-1]
                    this_col_interpolated[i] = True
                    break
                else:
                    next_non_null_idx+=1
    
    return one_pandas_columns, this_col_interpolated

def CleanWholeDataFrame(df):

    df = df.drop(labels = 0, axis = 0)

    ##These columns were 80+% nulls when we wrote the project
    drop_list = ['WVHT','DPD','GST','APD','MWD','PRES','WTMP','PTDY','TIDE']

    df.drop(drop_list, inplace=True, axis=1)
    df = df.rename(columns = lambda x: "YY" if x == "#YY" else x)

    df["Date"] = pd.to_datetime(df[ ["YY","MM","DD","hh","mm"] ].rename(columns = {
        "YY":"year", "MM":"month", "DD":"day", "hh": "hour", "mm":"minute"}))
    
    df["Any Interpolated"] = [False] * len(df)
    for col_name in df.columns:
        if col_name == "Date" or col_name == "Any Interpolated":
            continue
        df[col_name][ df[col_name] == "MM" ] = np.nan
        df[col_name] = df[col_name].astype("float32")
        df[col_name],this_col_interpolated = SimpleInterpolateColumn(df[col_name])
        if col_name == "WDIR" or col_name == "WSDP":
            df["Any Interpolated"] = df["Any Interpolated"] | this_col_interpolated

    df["Any Interpolated"] = df["Any Interpolated"].apply( lambda bool: "Interpolated Data" if bool else "Original Data")
    #print(df["Any Interpolated"])
    df = df.sort_values(by = "Date")
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
