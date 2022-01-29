import streamlit as st


def SetupPage():
  cols = st.columns([1, 3, 1])

  with cols[1]:
    st.title("Cognite Challenge")

  cols = st.columns([1, 3, 1])
  with cols[1]:
    # Add introductory information
    st.header("Introduction")
    st.write("Lorem ipsum dolor amet.")

    # Time series plot
  with cols[2]:
    option = st.selectbox("Weather station", ("KIKT", "KAPT", "KMIS"))


if __name__ == "__main__":
  SetupPage()
