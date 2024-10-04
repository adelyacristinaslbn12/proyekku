import warnings
import pandas as pd
import streamlit as st
import plotly.express as px
from babel.numbers import format_currency

# Configuration
warnings.filterwarnings("ignore")
st.set_page_config(page_title="Bicycle Rental", page_icon=":bar_chart:", layout="wide")

# Title and styling
st.title(":bar_chart: Sample Bicycle Rental EDA")
st.markdown("<style>h1{font-size: 2rem;}</style>", unsafe_allow_html=True)

# Load data
url = "https://raw.githubusercontent.com/adelyacristinaslbn12/proyekku/main/dashboard/main_data.csv"
df = pd.read_csv(url, encoding="ISO-8859-1")

# Print column names to debug
print("Available columns:", df.columns.tolist())

# Data preprocessing
df["dteday"] = pd.to_datetime(df["dteday"])
startDate = pd.to_datetime(df["dteday"]).min()
endDate = pd.to_datetime(df["dteday"]).max()

# Date range selection
col1, col2 = st.columns(2)
with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))
with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

# Filter data based on date range
df = df[(df["dteday"] >= date1) & (df["dteday"] <= date2)].copy()

# Sidebar filters
st.sidebar.header("Choose your filter : ")

# Weather situation mapping and filter
weathersit_label = {
    1: 'clear',
    2: 'mist',
    3: 'light rain/snow',
    4: 'working day',
    5: 'non-working day'
}
df['weathersit_x'] = df['weathersit_x'].map(weathersit_label)
weathersit = st.sidebar.multiselect("Pick weather", df["weathersit_x"].unique())
df2 = df[df["weathersit_x"].isin(weathersit)] if weathersit else df.copy()

# Working Day Analysis
# Assuming the column is named 'workingday_x' instead of 'workingday'
df['workingday_label'] = df['workingday_x'].map({0: 'Non-working Day', 1: 'Working Day'})

# Create tabs for different visualizations
tab1, tab2 = st.tabs(["Weather Analysis", "Working Day Analysis"])

with tab1:
    col1, col2 = st.columns(2)
    
    # Bar Chart
    with col1:
        st.subheader("Total Bicycle Users by Weather")
        fig = px.bar(df2, x="weathersit_x", y="cnt_x", 
                    labels={"weathersit_x": "Weather", "cnt_x": "Total"})
        st.plotly_chart(fig, use_container_width=True)
    
    # Pie Chart
    with col2:
        st.subheader("Percentage of Users by Weather")
        fig = px.pie(df2, values="cnt_x", names="weathersit_x", 
                    labels={"weathersit_x": "Weather", "cnt_x": "Total"})
        fig.update_traces(textposition="inside")
        fig.update_layout(margin=dict(t=50))
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    
    # Working Day vs Non-working Day Bar Chart
    with col1:
        st.subheader("Total Bicycle Users by Day Type")
        working_day_data = df.groupby('workingday_label')['cnt_x'].sum().reset_index()
        fig = px.bar(working_day_data, x="workingday_label", y="cnt_x",
                     labels={"workingday_label": "Day Type", "cnt_x": "Total Users"},
                     color="workingday_label")
        st.plotly_chart(fig, use_container_width=True)
    
    # Average Users per Hour by Day Type
    with col2:
        st.subheader("Average Users by Hour and Day Type")
        hourly_avg = df.groupby(['hr', 'workingday_label'])['cnt_x'].mean().reset_index()
        fig = px.line(hourly_avg, x="hr", y="cnt_x", color="workingday_label",
                      labels={"hr": "Hour of Day", "cnt_x": "Average Users", 
                             "workingday_label": "Day Type"})
        st.plotly_chart(fig, use_container_width=True)

# Time series analysis
st.subheader("Monthly Trend")
linechart_df2 = df2.groupby(df2["dteday"].dt.strftime("%b : %Y"))["cnt_x"].sum().reset_index()
linechart_df2["dteday"] = pd.to_datetime(linechart_df2["dteday"], format="%b : %Y")
linechart_df2 = linechart_df2.sort_values(by="dteday")
fig = px.line(linechart_df2, x="dteday", y="cnt_x", 
              labels={"dteday": "Date", "cnt_x": "Total Users"})
st.plotly_chart(fig, use_container_width=True)

# Download original Dataset
st.subheader("Download Original Dataset")
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download Data", data=csv, file_name="Bicycle_Dataset.csv", mime="text/csv")