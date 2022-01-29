import streamlit as st


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


if __name__ == "__main__":
  SetupPage()
