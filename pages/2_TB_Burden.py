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
year_slider = st.slider('A) Slide the bar to choose year range of viewing:',year_min, year_max, (year_min, year_max))
subset = df[(df["year"] >= year_slider[0]) & (df["year"] <= year_slider[1])]

#2. selection for countries
countries_options = st.multiselect(
    "B) Choose countries to view:",
    df['country'].unique().tolist(),
    "Albania"
)
subset = subset[subset["country"].isin(countries_options)]



#1) view incidence rate only, with density of color going up with higher incidence rate [incidence > 100 per 100,000 population defined as high incidence*]
#2) view treatment success rate only
#3) view ratio of treatment success to incidence rate only
