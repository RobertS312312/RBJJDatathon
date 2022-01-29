import streamlit as st
import data_clean
import os
import plotly.express as px
import numpy as np
import pandas as pd

def UpdateData(strName, cached = True):

  
  if cached:
    txt_filepath = os.path.join("UncleanedData",strName + ".txt")
    csv_filepath = os.path.join("CleanedData",strName + ".csv")
  else:
    ##TODO: Add in code to download new from the website and save in appropriate spot
    txt_filepath = os.path.join("UncleanedData", "newest" + strName + ".txt")
    csv_filepath = os.path.join("CleanedData", "newest" + strName + ".csv")
  

  cleaned_df = data_clean.CleanWholeDataFrame(data_clean.filepath2df(txt_filepath))
  cleaned_df.to_csv(csv_filepath)
  ##do r process here
  return cleaned_df
  #CreateVisuals(cleaned_df)

def SetupPage():
  topbar = st.columns([1, 3, 1])
    #title columns widths can be different if we want?

  with topbar[0]:
    st.image("BakerBuoysLogo.png")

  with topbar[1]:
    st.title("Cognite Challenge")

  intro_row = st.columns([left_width, center_width, right_width])
  with intro_row[1]:
    # Add introductory information
    st.header("Introduction")
    st.write("Lorem ipsum dolor amet.")

  with intro_row[2]:
    #I feel like we need to greatly shorten this blurb or move it to the center
    st.write("Below you can customize what data you want us to analyze."+
      " There are three options of Weather Stations: KIKT in ____, KAPT in ____, "+
      " and KMIS in ____. Additionally, you can choose to update to the most recent "
      " data available at each of the sources ('Newest Data'), or to restore the data " + 
      " as it exsisted on the day of the datathon: Jan 28, 2022. ('Cached Data')")
    option = st.selectbox("Weather Station", ("KIKT", "KAPT", "KMIS"))

    cleaned_df = UpdateData(option)
    if st.button("Cached Data"):
      print("Clicked Cached Data")
      cleaned_df = UpdateData(option)
      print("Updated Visuals?")

    if st.button("Newest Data"):
      print("Clicked Newest Data")
      cleaned_df = UpdateData(option,False)
      print("Updated Visuals?")

  CreateVisuals(cleaned_df)
  

def CreateVisuals(cleaned_df):
  ##Create 1 helper function for each visual 
  ##this function will call of those and impose the proper formatting

  # Time series plot
  data_plots_first_row = st.columns([left_width, center_width, right_width])
  with data_plots_first_row[1]:
    #here goes first visual *tune series?
    st.write("full information plotly interative")
    st.plotly_chart(FullInfoPolar(cleaned_df))
    
    st.write("Daily average plot")
    #st.plotly_chart(FullInfoPolar(cleaned_df))
  with data_plots_first_row[2]:
    #here goes download things?
    st.write("downloads")    

  data_plots_second_row = st.columns([left_width, center_width, right_width])

  with data_plots_second_row[1]:
    st.write("time Series")

def FullInfoPolar(cleaned_df):
  #TODO: Verify if actually pointing right or if 90 degrees of
  dots = True
  if dots:
    fig =  px.scatter_polar(cleaned_df, r = "WSPD", theta = "WDIR", width = 400*center_width/2, height = 400*center_width/2,
    animation_frame = cleaned_df["Date"].astype("str"), range_r = [0,np.max(cleaned_df["WSPD"])],
    title = "Test", color = "Any Interpolated")
    return fig


  zeros_df = pd.DataFrame( data = { "WSPD" : [0] * len(cleaned_df), "Date" : cleaned_df["Date"], "WDIR" : [0] * len(cleaned_df) } )
  plot_df = cleaned_df.append( zeros_df  )
  fig =  px.line_polar(plot_df, r = "WSPD", theta = "WDIR", width = 400*center_width/2, height = 400*center_width/2,
    animation_frame = plot_df["Date"].astype("str"), range_r = [0,np.max(plot_df["WSPD"])],
    title = "Test")
  return fig


def DailyAveragePolar(cleaned_df):
  ##TODO: actually do the daily averages
  pass



###Uncomment this block of code if you want t recreate the cleaned .csv's
for station_name in ("KIKT", "KBQX", "KMIS"):
  UpdateData(station_name)


if __name__ == "__main__":
  left_width = 1
  center_width = 3
  right_width = 2
  SetupPage()
