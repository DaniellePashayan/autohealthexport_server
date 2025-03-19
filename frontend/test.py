import requests
import pandas as pd
from dotenv import load_dotenv
import os
import streamlit as st
import plotly.express as px
import streamlit_shadcn_ui as ui
import numpy as np


## TODO: change to API endpoint
df = pd.read_csv('./health_metrics.csv')
df['weight_body_mass'].ffill(inplace=True)

## FUNCTIONS
def weight_over_time(df):
    """Plot weight over time."""
    weight = df[['date', 'weight_body_mass']].copy()
    # plot weight over time
    fig = px.line(weight, x='date', y='weight_body_mass', title='Weight Over Time')
    fig.update_traces(line=dict(color='blue', width=2))
    fig.update_layout(xaxis_title='Date', yaxis_title='Weight (lb)')
    # add trend line for weight
    z = np.polyfit(pd.to_datetime(weight['date']).astype(int) / 10**9, weight['weight_body_mass'], 1)
    p = np.poly1d(z)
    fig.add_trace(px.line(x=weight['date'], y=p(pd.to_datetime(weight['date']).astype(int) / 10**9), line_shape='spline').data[0])
    # made trendline green
    fig.data[-1].line.color = 'green'
    fig.data[-1].line.width = 2
    fig.data[-1].name = 'Trend Line'
    # make trendline dotted
    fig.data[-1].line.dash = 'dot'
    return fig

def calculate_weight_loss_week(df):
    """Calculate weight loss over the last 7 days."""
    df['date'] = pd.to_datetime(df['date'])
    last_week = df[df['date'] >= (df['date'].max() - pd.Timedelta(days=7))]
    if not last_week.empty:
        weight_loss = last_week['weight_body_mass'].iloc[0] - last_week['weight_body_mass'].iloc[-1]
        return weight_loss
    return 0

def calculate_weight_loss_month(df):
    """Calculate weight loss over the last month"""
    df['date'] = pd.to_datetime(df['date'])
    last_month = df[df['date'] >= (df['date'].max() - pd.Timedelta(days=30))]
    if not last_month.empty:
        weight_loss = last_month['weight_body_mass'].iloc[0] - last_month['weight_body_mass'].iloc[-1]
        return weight_loss
    return 0

def calculate_weight_loss_quarter(df):
    """Calculate weight loss over the last month"""
    df['date'] = pd.to_datetime(df['date'])
    last_month = df[df['date'] >= (df['date'].max() - pd.Timedelta(days=90))]
    if not last_month.empty:
        weight_loss = last_month['weight_body_mass'].iloc[0] - last_month['weight_body_mass'].iloc[-1]
        return weight_loss
    return 0

def calculate_total_weight_lost(df):
    """Calculate average weight loss over the last 7 days."""
    df['date'] = pd.to_datetime(df['date'])
    if not df.empty:
        weight_loss = df['weight_body_mass'].iloc[0] - df['weight_body_mass'].iloc[-1]
        return weight_loss
    return 0

def calculate_weight_lost_per_timeframe(df):
    # add a column that calculates the difference between the row date and the date of the row prior
    df['weight_lost_day'] = df['weight_body_mass'].diff()
    df['weight_lost_week'] = df['weight_body_mass'].diff(periods=7)
    df['weight_lost_month'] = df['weight_body_mass'].diff(periods=30)
    return df[['date', 'weight_body_mass', 'weight_lost_day', 'weight_lost_week', 'weight_lost_month']]


## PAGE
st.set_page_config(layout="wide")
st.title("Health Metrics Dashboard")

st.header("Weight Trends")
cols = st.columns(4)
with cols[0]:
    weight_loss = calculate_weight_loss_week(df)
    if weight_loss > 0:
        ui.card(
            title="Lost in 7 days",
            content=f"-{weight_loss:.2f} lb",
            key="weight_loss_week"  # Ensure unique key for the card
            ).render()
with cols[1]:
    weight_loss_month = calculate_weight_loss_month(df)
    if weight_loss_month > 0:
        ui.card(
            title="Lost in 30 days",
            content=f"-{weight_loss_month:.2f} lb",
            key="weight_loss_month"  # Ensure unique key for the card
            ).render()
with cols[2]:
    weight_loss_month = calculate_weight_loss_quarter(df)
    if weight_loss_month > 0:
        ui.card(
            title="Lost in 90 days",
            content=f"-{weight_loss_month:.2f} lb",
            key="weight_loss_quarter"  # Ensure unique key for the card
            ).render()
with cols[3]:
    avg_weight_loss = calculate_total_weight_lost(df)
    if avg_weight_loss > 0:
        ui.card(
            title="Total Weight Lost",
            content=f"-{avg_weight_loss:.2f} lb",
            key="total_weight_loss"  # Ensure unique key for the card
            ).render()

st.header("Predictions")
# add input box for goal weight
goal_weight = st.number_input("Goal Weight (lb)", min_value=0, value=150, step=1)
averages = calculate_weight_lost_per_timeframe(df)
cols = st.columns(3)
with cols[0]:
    weight_loss = calculate_weight_loss_week(df)
    if weight_loss > 0:
        ui.card(
            title="Commitment to Lose",
            content="-1.50 lb",
            key="weight_loss_week_goal"  # Ensure unique key for the card
            ).render()
with cols[1]:
    weight_loss_month = calculate_weight_loss_month(df)
    if weight_loss_month > 0:
        ui.card(
            title="Current Rate",
            content=f"-{weight_loss:.2f} lb",
            key="weight_loss_trend_week"  # Ensure unique key for the card
            ).render()
with cols[2]:
    avg_weight_loss = calculate_total_weight_lost(df)
    if avg_weight_loss > 0:
        ui.card(
            title="Overall Rate",
            content=f"{averages["weight_lost_week"].mean():.2f} lb",
            key="weight_loss_week_avg"  # Ensure unique key for the card
            ).render()


fig = weight_over_time(df)
st.plotly_chart(fig, use_container_width=True)