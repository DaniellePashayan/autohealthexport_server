from datetime import datetime, timedelta
from dotenv import load_dotenv
import pandas as pd
import plotly
import streamlit as st

from Home import get_metric_calculation, weight_data, THEME_COLORS

# ------ GRAPHS ------
def weight_loss_trend_graph(df:pd.DataFrame, column_name:str="weight_body_mass"):
    """
    Create a line graph for weight loss trend.
    """
    fig = plotly.graph_objects.Figure()
    fig.add_trace(plotly.graph_objects.Scatter(
        x=df['date'],
        y=df[column_name],
        mode='lines+markers',
        name='Weight Loss Trend',
        line=dict(color=THEME_COLORS["blue"], width=2),
        # no markers
        marker=dict(size=0.1, color=THEME_COLORS["blue"], line=dict(width=1, color=THEME_COLORS["blue"])),
    ))
    # add a trend line that does a rolling 14 days average
    df['rolling_avg'] = df[column_name].rolling(window=14).mean()
    fig.add_trace(plotly.graph_objects.Scatter(
        x=df['date'],
        y=df['rolling_avg'],
        mode='lines',
        name='14-Day Rolling Average',
        line=dict(color=THEME_COLORS["green"], width=1),
    ))
    
    fig.update_layout(
        title="Weight Loss Trend",
        xaxis_title="Date",
        yaxis_title="Weight (lbs)",
        template="plotly_white",
    )
    # hide the legend
    fig.update_layout(showlegend=False)
    return fig

# ------ PAGE ------
def weight_loss_page():
    
    # ------ SET PAGE CONFIGURATION ------
    st.set_page_config(
        page_title="Weight",
        page_icon="./static/icon.png",
        layout="wide",  
        initial_sidebar_state="expanded"
    )
    
    # ------ APPLY THEME AND CONFIGS ------
    with open('./static/styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    st.subheader("Weight Metrics")
    with st.container():
        columns = st.columns(3)
        with columns[0]:
            starting_weight = get_metric_calculation(weight_data.copy(), "weight_body_mass", max_date=weight_data["date"].min(), min_date=weight_data["date"].min(), function="average")
            st.metric(
                label="Starting Weight",
                value=str(starting_weight) + " lbs",    
            )
        with columns[1]:
            current_weight = get_metric_calculation(weight_data.copy(), "weight_body_mass", max_date=weight_data["date"].max(), min_date=weight_data["date"].max(), function="average")
            st.metric(
                label="Current Weight",
                value=str(current_weight) + " lbs",    
            )
        with columns[2]:
            goal_weight = st.number_input(label="Goal Weight",
                                    min_value=0,
                                    max_value=999,
                                    value=150,  # default value
                                    )
            # update goal weight in session state
            st.session_state.goal_weight = goal_weight

        columns = st.columns(4)
        with columns[0]:
            this_week_weight_lost = get_metric_calculation(weight_data.copy(), "weight_body_mass", max_date=weight_data["date"].max(), min_date=weight_data["date"].max() - pd.Timedelta(days=6), function="difference")
            st.metric(
                label="Weight Loss - 7 days",
                value=str(this_week_weight_lost),
                delta_color="inverse"
            )
        with columns[1]:
            this_month_weight_lost = get_metric_calculation(weight_data.copy(), "weight_body_mass", max_date=weight_data["date"].max(), min_date=weight_data["date"].max() - pd.Timedelta(days=29), function="difference")
            st.metric(
                label="Weight Loss - 30 days",
                value=str(this_month_weight_lost),
                delta_color="inverse"
            )
        with columns[2]:
            this_quarter_weight_lost = get_metric_calculation(weight_data.copy(), "weight_body_mass", max_date=weight_data["date"].max(), min_date=weight_data["date"].max() - pd.Timedelta(days=89), function="difference")
            st.metric(
                label="Weight Loss - 90 days",
                value=str(this_quarter_weight_lost),
                delta_color="inverse"
            )
        with columns[3]:
            total_weight_loss = get_metric_calculation(weight_data.copy(), "weight_body_mass", max_date=weight_data["date"].max(), min_date=weight_data["date"].max() - pd.Timedelta(days=999), function="difference")
            st.metric(
                label="Weight Loss - Total",
                value=str(total_weight_loss),
                delta_color="inverse"
            )

    st.subheader("Progress")
    with st.container():
        weight_loss_progress = ((1-(current_weight - goal_weight) / (starting_weight - goal_weight)) * 100 if starting_weight > goal_weight else 0)
        columns = st.columns([1, 7])
        with columns[0]:
            text = str(round(weight_loss_progress,1)) + "%"
            st.write(
                f'<p style="font-size: 20px; text-align: center;">{text}</p>', unsafe_allow_html=True)
        with columns[1]:
            st.progress(weight_loss_progress/100)
        
        st.plotly_chart(weight_loss_trend_graph(weight_data.copy(), column_name="weight_body_mass"), use_container_width=True)

weight_loss_page()