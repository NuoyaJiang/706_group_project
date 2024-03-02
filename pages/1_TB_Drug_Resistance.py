import streamlit as st
import time
import numpy as np
import altair as alt
import pandas as pd
from vega_datasets import data

st.markdown("# Drug Resistance")
st.sidebar.header("Drug Resistance")
st.write(
    """This page illustrates TB Worldwide Drug Resistance from 2018 to 2021"""
)

@st.cache_data
def load_data():
    df = pd.read_pickle("data/mtb_cleaned_data.pkl")
    country_df = pd.read_csv('https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/country_codes.csv', dtype = {'conuntry-code': str})
    return df, country_df

df, country_df = load_data()
country_df['country'] = country_df['Country']
df = df.merge(country_df[['country', 'country-code']], on='country')

year_min = df["year"].min()
year_max = df["year"].max()
year = st.slider('Select a year', min_value=int(df['year'].min()), max_value=int(df['year'].max()), value=2019, step=1)




df2 = df[df['year']==year]
df2 = df2.groupby(['country'])['e_rr_pct_ret'].mean().reset_index()

countries_options = st.multiselect(
    "B) Choose countries to view:",
    df['country'].unique().tolist(),
    "Albania"
)
subset = df2[df2["country"].isin(countries_options)]

source = alt.topo_feature(data.world_110m.url, 'countries')
width = 600
height  = 300
project = 'equirectangular'

background = alt.Chart(source
).mark_geoshape(
    fill='#aaa',
    stroke='white'
).properties(
    width=width,
    height=height
).project(project)

selector = alt.selection_single(
    fields=['country']
)

chart_base = alt.Chart(source
    ).properties(
        width=width,
        height=height
    ).project(project
    ).add_selection(selector
    ).transform_lookup(
        lookup="id",
        from_=alt.LookupData(subset, "country-code", ['e_rr_pct_ret']),
)

rate_scale = alt.Scale(domain=[subset['e_rr_pct_ret'].min(), subset['e_rr_pct_ret'].max()], scheme='oranges')
rate_color = alt.Color(field="e_rr_pct_ret", type="quantitative", scale=rate_scale)

chart_resistance = chart_base.mark_geoshape().encode(
      color=alt.Color('e_rr_pct_ret:Q', scale=alt.Scale(scheme='oranges')),
      tooltip=['country:N', 'e_rr_pct_ret:Q']
    ).transform_filter(
    selector
    ).properties(
    title=f'Average TB Drug Resistance Percentage Worldwide in year {year}'
)
st.altair_chart(chart_resistance, use_container_width=True)