from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import pandas as pd
import plotly
import requests
import streamlit as st

THEME_COLORS = {
  "dark-gray": "#1a1e24",
  "medium-gray": "#353d4a",
  "light-gray": "#d1d5db",
  "red": "#fca399",
  "green": "#80cbc4",
  "blue": "#4F8FC3",
}


load_dotenv()

# ------ FUNCTIONS ------
@st.cache_data
def get_data(url: str) -> pd.DataFrame:
    """Fetches data from a given URL and returns it as a DataFrame."""
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['data']
        df = pd.DataFrame(data)
        
        # ffill all columns
        df = df.ffill(axis=0)        
        
        df['date'] = pd.to_datetime(df['date'])
        return df
    else:
        st.error(f"Error fetching data: {response.status_code}")
        return pd.DataFrame()

# ------ FUNCTIONS ------
def metric_by_timeframe(df:pd.DataFrame, max_date:datetime, min_date:datetime, column_name:str="weight_body_mass") -> pd.DataFrame:  
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' does not exist in the DataFrame. Available columns are: {df.columns.tolist()}")
    if column_name != 'date':
        columns = ['date', column_name]
    
    df = df[columns]
    # order descending by date
    df = df.sort_values('date', ascending=False)
    
    df = df[(df['date'] >= min_date) & (df['date'] <= max_date)]
    return df

def get_metric_calculation(df:pd.DataFrame, column_name:str, max_date: datetime, min_date: datetime, function="difference") -> pd.DataFrame:
    """
    Get the metric calculation for a given column name(s) over a specified number of days.
    """
    # remove dups in column_names
    df = metric_by_timeframe(df, max_date = max_date, min_date= min_date, column_name=column_name)
    if df.empty:
        return None
    
    valid_functions = ["difference", "average", "max", "min"]
    if function not in valid_functions:
        raise ValueError(f"Invalid function. Choose from {valid_functions}.")

    if function == "difference":
        # calculate difference between max and min values for each column
        return round(df[column_name].iloc[0] - df[column_name].iloc[-1],2)
    if function == "average":
        return round(df[column_name].mean(),2)

# ------ SET PAGE CONFIGURATION ------
st.set_page_config(
    page_title="Health Dashboard",
    page_icon="./static/icon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------ APPLY THEME AND CONFIGS ------
with open('./static/styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

if "goal_weight" not in st.session_state:
        st.session_state.goal_weight = 0

weight_data = get_data('http://localhost:8005/body_composition')
activity_data = get_data('http://localhost:8005/exercise')
nutrition_data = get_data('http://localhost:8005/nutrition')
CICO_data = get_data('http://localhost:8005/CICO')

# ------ CONTENT ------
st.header('Personal Health and Activity Insights Dashboard')
st.markdown("""
**Summary:**

This application provides a comprehensive view of your personal health, activity, and nutrition data, transforming raw measurements into actionable insights. By seamlessly integrating data from external sources (like Apple Health), this dashboard empowers you to track trends, identify patterns, and make informed decisions about your well-being.

**Key Visualizations & Insights:**

* **Cardiovascular Health:**
    * **Heart Rate Trends:** Visualize your resting and active heart rates over time to monitor cardiovascular fitness and identify potential anomalies.
        * _Why:_ Track improvements in heart health through exercise and identify periods of stress or overexertion.
* **Physical Activity:**
    * **Daily Step Count & Activity Levels:** Chart your daily steps, distance traveled, and flights of stairs climbed to assess activity levels and progress towards fitness goals.
        * _Why:_ Monitor your daily movement, identify active periods, and ensure you're meeting your activity targets.
* **Weight Management & Body Composition:**
    * **Weight & BMI Tracking:** Chart your weight and Body Mass Index (BMI) over time to track progress towards weight management goals.
        * _Why:_ Visualize changes in body composition and identify trends related to diet and exercise.
* **Nutrition Analysis:**
    * **Calorie & Macronutrient Breakdown:** Analyze your daily calorie intake and macronutrient distribution (proteins, carbohydrates, fats) to ensure a balanced diet.
        * _Why:_ Gain insights into your dietary habits, identify areas for improvement, and optimize your nutrition for health and fitness.
* **Trend Analysis and Time-Series Visualization:**
    * All data is presented in time series charts, allowing for clear identification of trends and patterns over days, weeks, and months.
        * _Why:_ Time series data is important to see the progression of health and fitness over time.

**Data Integration:**

* Seamlessly integrates with external applications that export health data, such as those that sync with Apple Health.
* This allows for a centralized location to view all of your health metrics.

**Empowering Informed Decisions:**

This dashboard is designed to empower you with the knowledge needed to make informed decisions about your health and well-being. By visualizing your data, you can gain a deeper understanding of your body and take proactive steps towards a healthier lifestyle.

            """)