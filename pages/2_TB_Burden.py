import streamlit as st
import time
import numpy as np
import pandas as pd
import pickle

@st.cache
def load_data():
    df = pd.read_pickle("data/mtb_cleaned_data.pkl")
    return df

df = load_data()


#1. slider to choose year
st.write("## Visualize the temporal trend of TB burden across different countries")
year_min = df["year"].min()
year_max = df["year"].max()
year_slider = st.slider('A) Slide the bar to choose year range of viewing:',year_min, year_max, (2020, 2021))

subset = df[(df["year"] >= year_slider[0]) & (df["year"] <= year_slider[1])]