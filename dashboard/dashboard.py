import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

st.set_page_config(page_title="Bicycle Rental", page_icon=":bar_chart:", layout="wide")
st.title(":bar_chart: Sample Bicycle Rental EDA")
st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True)
url = "https://raw.githubusercontent.com/muhammadalvarokhikman/dashboard/main/dashboard/main_data.csv"
df = pd.read_csv(url, encoding="ISO-8859-1")



