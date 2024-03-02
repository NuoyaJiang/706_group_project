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
year_slider = st.slider('A) Slide the bar to choose year range of viewing:',year_min, year_max, (year_min, year_max))
subset = df[(df["year"] >= year_slider[0]) & (df["year"] <= year_slider[1])]

