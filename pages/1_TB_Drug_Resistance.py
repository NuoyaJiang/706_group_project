import streamlit as st
import time
import numpy as np
import altair as alt
import pandas as pd
from vega_datasets import data

st.markdown("# Drug Resistance")
st.sidebar.header("Drug Resistance")
st.write(
    """This page illustrates TB Worldwide Drug Resistance from 2018 to 2022"""
)

@st.cache
def load_data():
    df = pd.read_pickle("data/mtb_cleaned_data.pkl")
    return df

df = load_data()
year_min = df["year"].min()
year_max = df["year"].max()
year = st.slider('Select a year', min_value=int(df['Year'].min()), max_value=int(df['Year'].max()), value=2012, step=1)

