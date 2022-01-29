import streamlit as st
import data_clean
import os
import plotly.express as px
import numpy as np
import pandas as pd
import subprocess

LEFT_WIDTH = 1
CENTER_WIDTH = 4


def CleanData(strName):
  txt_filepath = os.path.join("UncleanedData",strName + ".txt")
  csv_filepath = os.path.join("CleanedData",strName + ".csv") 


def UpdateData(strName, cached = True):

  cleaned_df = pd.read_csv( os.path.join("CleanedData",strName + ".csv")  )
  cleaned_df["Date"] = pd.to_datetime(cleaned_df["Date"])

  ##do r process here
  Made_Predictions = True
  if Made_Predictions:
  #  path2script = "wsPrediction.r"
  #  x = subprocess.check_output( ['Rscript', path2script, csv_filepath])
  ##Update interpolated so it is strings
    #"Original Data", "Interpolated Data", "Predicted Values"
  ###append predicted values
    predicted_df = pd.read_csv( os.path.join("PredictedData", strName + "_for.csv") )
    predicted_df["Date"] = pd.to_datetime(predicted_df["Date"])
    combined_data = cleaned_df.append(predicted_df)
    combined_data["Any Interpolated"][ pd.isna(combined_data["Any Interpolated"]) ] = "Predicted Data"
  else:
    combined_data = cleaned_df

  return combined_data
  # CreateVisuals(cleaned_df)


def SetupPage():
  topbar = st.columns([LEFT_WIDTH, CENTER_WIDTH])
  # title columns widths can be different if we want?

  with topbar[0]:
    st.image("BakerBuoysLogo.png")

  with topbar[1]:
    st.title("Cognite Challenge")

  intro_row = st.columns([LEFT_WIDTH, CENTER_WIDTH])
  with intro_row[1]:
    # Add introductory information
    st.header("Introduction")
    st.write(
        "For our project, we began by cleaning the data from the three weather"
        " stations. In this process, we removed columns which did not have"
        " enough data and interpolated missing values from the columns that"
        " we decided to use. Our interpolation method was simple. For missing"
        " values, we simply took the average of the most recent value and the"
        " next value in the column.\n\n"
        "We then created this dashboard, which includes two plots: a polar"
        " plot of wind speed and direction data at every time point, and a plot"
        " that averages these data by day. These plots include historical data"
        " and the predicted data for the next three days.")

    # I feel like we need to greatly shorten this blurb or move it to the center
    st.header("Plots")
    st.write(
        "Below you can customize what data you want us to analyze."
        " There are three options of Weather Stations: KIKT, KAPT, "
        " and KMIS. Additionally, you can choose to update to the most recent "
        " data available at each of the sources ('Newest Data'), or to"
        " restore the data as it exsisted on the day of the datathon: Jan 28,"
        " 2022. ('Cached Data')")
    option = st.selectbox("Weather Station", ("KMIS", "KIKT", "KAPT"))
    if option == "KAPT":
      option = "KBQX"

    cleaned_df = UpdateData(option)

  CreateVisuals(cleaned_df)


def CreateVisuals(cleaned_df):
  # Create 1 helper function for each visual
  # this function will call of those and impose the proper formatting

  # Time series plot
  data_plots_first_row = st.columns([LEFT_WIDTH, CENTER_WIDTH])
  with data_plots_first_row[1]:
    # here goes first visual *tune series?
    st.plotly_chart(FullInfoPolar(cleaned_df))


    st.plotly_chart(DailyAveragePolar(cleaned_df))


def FullInfoPolar(cleaned_df):
  # TODO: Verify if actually pointing right or if 90 degrees off
  dots = True
  if dots:
    fig = px.scatter_polar(
        cleaned_df,
        r="WSPD",
        theta="WDIR",
        width=150 * CENTER_WIDTH,
        height=150 * CENTER_WIDTH,
        animation_frame=cleaned_df["Date"].astype("str"),
        range_r=[0, np.max(cleaned_df["WSPD"])],
        title="Polar Plot Of Every Observed, Interpolated, and Predicted Wind Speed and Direction",
        color="Any Interpolated",
        labels={'Any Interpolated': 'Original, Interpolated, or Predicted'})
    return fig

  zeros_df = pd.DataFrame(
      data={
          "WSPD": [0] * len(cleaned_df),
          "Date": cleaned_df["Date"],
          "WDIR": [0] * len(cleaned_df)
      })
  plot_df = cleaned_df.append(zeros_df)
  fig = px.line_polar(
      plot_df,
      r="WSPD",
      theta="WDIR",
      width=150 * CENTER_WIDTH / 2,
      height=150 * CENTER_WIDTH,
      animation_frame=plot_df["Date"].astype("str"),
      range_r=[0, np.max(plot_df["WSPD"])],
      title="Polar Plot Of Every Observed, Interpolated, and Predicted Wind Speed and Direction",
      color="Any Interpolated",
      labels={'Any Interpolated': 'Original, Interpolated, or Predicted'})
  return fig


def DailyAveragePolar(cleaned_df):

  # For each day, convert all entries for that day to vectors
  # Average them and convert back to polar

  daily_average_df = findDailyAverage(cleaned_df)
  print(daily_average_df)

  fig = px.scatter_polar(daily_average_df,
                         r="WSPD",
                         theta="WDIR",
                         width=150 * CENTER_WIDTH,
                         height=150 * CENTER_WIDTH,
                         animation_frame=daily_average_df["Date"].astype("str"),
                         range_r=[0, np.max(daily_average_df["WSPD"])],
                         title="Polar Plot Of Average Wind Speeds and Directions for each Day",
                         color="Original or Predicted")
  return fig


def polar2cartesianx(r, theta_deg):
  theta_rad = 2 * np.pi * theta_deg / 360
  x = r * np.sin(
      theta_rad
  )  ##Usually these sin and cos should be flipped but our 0degrees is the y axis not the x
  return x


def polar2cartesiany(r, theta_deg):
  theta_rad = 2 * np.pi * theta_deg / 360
  y = r * np.cos(theta_rad)
  return y


def cartesian2polar(x, y):
  r = np.sqrt(x * x + y * y)
  # normally would be arccos but 0 dregrees is y axis

  theta_rad = np.arcsin(x / r)
  theta_deg = 360 * theta_rad / (2 * np.pi)
  return r, theta_deg


def findDailyAverage(df):

  #DateTime2Str = lambda datetime: str(datetime.month) + "/" + str(datetime.day) + "/" + str(datetime.year)
  set_of_days = set(df["Date"].dt.date)
  ##Use set to remove duplicates
  list_of_days = sorted(list(set_of_days))
  ##Sort to be properly ordered after setting

  list_of_avgr = []
  list_of_avgtheta = []
  for day in list_of_days:
    this_day_wind_speed = df["WSPD"][df["Date"].dt.date == day]
    this_day_wind_direction = df["WDIR"][df["Date"].dt.date == day]

    xlist = []
    ylist = []
    for idx in range(len(this_day_wind_direction)):
      xlist.append(
          polar2cartesianx(this_day_wind_speed.iloc[idx],
                           this_day_wind_direction.iloc[idx]))
      ylist.append(
          polar2cartesiany(this_day_wind_speed.iloc[idx],
                           this_day_wind_direction.iloc[idx]))

    avgx = np.average(xlist)
    avgy = np.average(ylist)
    avgr, avgtheta = cartesian2polar(avgx, avgy)
    list_of_avgr.append(avgr)
    list_of_avgtheta.append(avgtheta)

  if Made_Predictions:
    list_of_predicted_or_original_data = ["Orignal Data"] * (
        len(list_of_days) - 3) + ["Predicted Data"] * 3
  else:
    list_of_predicted_or_original_data = ["Orignal Data"] * (len(list_of_days))

  return pd.DataFrame(
      data={
          "WSPD": list_of_avgr,
          "WDIR": list_of_avgtheta,
          "Date": pd.to_datetime(list_of_days),
          "Original or Predicted": list_of_predicted_or_original_data
      })


###Uncomment this block of code if you want t recreate the cleaned .csv's
#for station_name in ("KIKT", "KBQX", "KMIS"):
#  CleanData(station_name)

#UpdateData("KBQX")


Made_Predictions = True
if __name__ == "__main__":
  SetupPage()
