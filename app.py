import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import pandas as pd

#page config
st.set_page_config(
    page_title = "Narsimha | Brute Force Detector",
    page_icon ="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load our CSS and JavaScript files
globe_css = Path("styles/globe.css").read_text(encoding="utf-8")
globe_js = Path("scripts/globe.js").read_text(encoding="utf-8")

# Load simulated attack data (Panda reads this and loads it)
mock_attacks = pd.read_csv("sample_data/mock_attacks.csv")

# Convert records into JSON for JavaScript (Panda makes it json)
attacks_json = mock_attacks.to_json(orient="records")
# Build the globe interface
globe_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        {globe_css}
    </style>
</head>

<body>

    <div id="globe-root">

        <!-- Interactive globe -->
        <div id="globeViz"></div>

        <!-- Top navigation -->
        <div id="topbar">
            <div id="brand">NARSIMHA</div>
            <div id="system-status">● SYSTEM ONLINE</div>
        </div>

        <!-- Attack information panel -->
        <div id="attack-panel" hidden>

            <button id="panel-close" onclick="
                document.getElementById('attack-panel').hidden = true;
            ">×</button>

            <div id="panel-title">
                THREAT INTELLIGENCE
            </div>

            <div class="attack-field">
                <div class="attack-label">IP ADDRESS</div>
                <div class="attack-value" id="attack-ip">--</div>
            </div>

            <div class="attack-field">
                <div class="attack-label">LOCATION</div>
                <div class="attack-value" id="attack-location">--</div>
            </div>

            <div class="attack-field">
                <div class="attack-label">FAILED ATTEMPTS</div>
                <div class="attack-value threat-value" id="attack-count">--</div>
            </div>

            <div class="attack-field">
                <div class="attack-label">TARGETED USERNAMES</div>
                <div class="attack-value" id="attack-users">--</div>
            </div>

            <div class="attack-field">
                <div class="attack-label">THREAT STATUS</div>
                <div class="attack-value threat-value" id="attack-status">--</div>
            </div>

        </div>

    </div>
    
    <!--loading  the country borders (i think)-->
    <script src="https://unpkg.com/globe.gl"></script>

    <!-- Load our globe logic -->
    <script>
        {globe_js}

        const container = document.getElementById("globeViz");
        const attacks = {attacks_json};

        console.log("Attacks data received:",attacks);
        console.log("Number of attacks:", attacks.length);

        
        initializeGlobe(container,attacks);
    </script>

</body>
</html>
"""

# Display the interface
components.html(
    globe_html,
    height=850,
    scrolling=False
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

#st.sidebar.title("NARSIMHA")
#st.sidebar.caption("NAVIGATION")

#page=st.sidebar.radio(
    #"Navigate",
    #[
        #"Overview",
        #"Attack Map",
        #"Suspicious IPs",
        #"Authentication Logs",
        #"Reports"
    #]
#)

st.sidebar.divider()

st.sidebar.caption("NARSIMHA v1.0")
st.sidebar.caption("Brute Force Detection System")

#Temporary Test code
#st.header(page)