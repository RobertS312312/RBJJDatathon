import streamlit as st
import data_clean
import os

def UpdateData(strName, cached = True):

  
  if cached:
    txt_filepath = os.path.join("UncleanedData",strName + ".txt")
    csv_filepath = os.path.join("CleanedData",strName + ".csv")
  else:
    txt_filepath = os.path.join("UncleanedData", "newest" + strName + ".txt")
    csv_filepath = os.path.join("CleanedData", "newest" + strName + ".csv")
  

  cleaned_df = data_clean.CleanWholeDataFrame(data_clean.filepath2df(txt_filepath))
  cleaned_df.to_csv(csv_filepath)
  ##do r process here
  CreateVisuals(cleaned_df)

def SetupPage():
  topbar = st.columns([1, 3, 1])

  with topbar[0]:
    st.image("BakerBuoysLogo.png")

  with topbar[1]:
    st.title("Cognite Challenge")

  intro_row = st.columns([1, 3, 1])
  with intro_row[1]:
    # Add introductory information
    st.header("Introduction")
    st.write("Lorem ipsum dolor amet.")

    # Time series plot
  data_plots = st.columns([1, 3, 1])
  with data_plots[2]:
    option = st.selectbox("Weather station", ("KIKT", "KAPT", "KMIS"))
    UpdateData(option)

def CreateVisuals(cleaned_df):
  ##Create 1 helper function for each visual 
  ##this function will call of those and impose the proper formatting
  pass

###Uncomment this block of code if you want t recreate the cleaned .csv's
#for station_name in ("KIKT", "KBQX", "KMIS"):
#  if station_name == "KBQX":
#    pass
#  UpdateData(station_name)


if __name__ == "__main__":
  SetupPage()
