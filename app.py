import streamlit as st
import pandas as pd

#page config
st.set_page_config(
    page_title = "Narsimha | Brute Force Detector",
    page_icon ="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

#Load CSS theme
def load_theme(theme_name):
    css_path = f"styles/{theme_name}.css"

    with open(css_path, "r")as css_file:
        css = css_file.read()

        st.markdown(
            f"<style>{css}</style>",
            unsafe_allow_html=True
        )
#Apply theme (Later to be added to buttons and stuff)
load_theme('oled-red')

##################
#DASHBOARD HEADER#
##################

st.title("Narsimha")
st.caption("BADS:Bruteforce Attack detection System")

#System status
col1, col2 = st.columns([5,1])

with col1:
    st.caption("Global Security Monitoring")

with col2:
    st.markdown(
        "<span style='color:#FF2424;'>ONLINE</span>",
        unsafe_allow_html=True
    )
st.divider()

##################
#SIDEBAR NAVIGATE#
##################

st.sidebar.title("NARSIMHA")
st.sidebar.caption("NAVIGATION")

page=st.sidebar.radio(
    "Navigate",
    [
        "Overview",
        "Attack Map",
        "Suspicious IPs",
        "Authentication Logs",
        "Reports"
    ]
)

st.sidebar.divider()

st.sidebar.caption("NARSIMHA v1.0")
st.sidebar.caption("Brute Force Detection System")

#Temporary Test code
st.header(page)