from datetime import datetime, timedelta
from dotenv import load_dotenv
import pandas as pd
import plotly
import streamlit as st
import plotly.graph_objects as go

from Home import get_metric_calculation, weight_data, THEME_COLORS

# ------ SET PAGE CONFIGURATION ------
st.set_page_config(
    page_title="Body Composition",
    page_icon="./static/icon.png",
    layout="wide",  
    initial_sidebar_state="expanded"
)

def body_page():
    
    
    
    # ------ APPLY THEME AND CONFIGS ------
    with open('./static/styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    st.subheader("Body Metrics")
    # st.write(weight_data)

body_page()