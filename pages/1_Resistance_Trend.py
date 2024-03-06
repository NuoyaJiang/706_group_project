import streamlit as st
import time
import numpy as np
import altair as alt
import pandas as pd
from vega_datasets import data

st.set_page_config(
    page_title="Resistance Trend",
    page_icon="🦠",
)

st.markdown("# Resistance Trend")

st.sidebar.header("Resistance Trend")
st.write(
    """This page illustrates the Trend of TB Worldwide Drug Resistance from 2018 to 2021"""
)

@st.cache_data
def load_data():
    df = pd.read_pickle("data/mtb_cleaned_data_new.pkl")
    country_df = pd.read_csv('https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/country_codes.csv', dtype = {'conuntry-code': str})
    return df, country_df

df, country_df = load_data()
country_df['country'] = country_df['Country']
df = df.merge(country_df[['country', 'country-code']], on='country')

year_min = df["year"].min()
year_max = df["year"].max()
year = st.slider('Select a year', min_value=int(df['year'].min()), max_value=int(df['year'].max()), value=2019, step=1)

countries = ["United States of America", "Australia", "United Kingdom of Great Britain and Northern Ireland", "India", "South Africa", "Russian Federation", "Costa Rica", "Brazil", "China", "Canada"]
countries_options = st.multiselect(
    "B) Choose countries to view:",
    df['country'].unique().tolist(),
    countries
)

df1 = df[df['year']==year]
df1 = df1[df1["country"].isin(countries_options)]



df1 = df1.groupby(['country'])['e_rr_pct_ret'].mean().reset_index()
df1 = df1.merge(country_df[['country', 'country-code']], on='country')
df1.columns = ["country", "drug-resistance-percentage", "country-code"]
st.write(df1)
#df2 = df1.groupby(['country'])['e_rr_pct_new'].mean().reset_index()
#df3 = df1.merge(df2, on = 'country')

source = alt.topo_feature(data.world_110m.url, 'countries')

width = 600
height  = 300
project = 'equirectangular'

    # a gray map using as the visualization background
background = alt.Chart(source
).mark_geoshape(
    fill='#aaa',
    stroke='white'
).properties(
    width=width,
    height=height
).project(project)

    #*******create a selector to link map visualization w/ later visualizations
selector = alt.selection_point(
    fields=['country']
)
    #base plot
chart_base = alt.Chart(source
    ).properties(
        width=width,
        height=height
    ).project(project
    ).add_params(selector
    ).transform_lookup(
        lookup="id",
        from_=alt.LookupData(df1, "country-code", ['country',"drug-resistance-percentage"]),
)

rate_scale = alt.Scale(domain=[df1['drug-resistance-percentage'].min(), df1['drug-resistance-percentage'].max()], scheme='oranges')
rate_color = alt.Color(field="drug-resistance-percentage", type="quantitative", scale=rate_scale)

chart_resistance = chart_base.mark_geoshape().encode(
      color=alt.Color('drug-resistance-percentage:Q', scale=alt.Scale(scheme='oranges'), title="Percentage (%)"),
      tooltip=['year:T', alt.Tooltip("drug-resistance-percentage:Q", title="Percentage")]
    ).transform_filter(
    selector
    ).properties(
    title=f'Average TB Drug Resistance Percentage Worldwide in {year}'
)


chart_resistance = alt.vconcat(background + chart_resistance).resolve_scale(color='independent')
#st.altair_chart(chart_resistance, use_container_width=True)

df2 = df[df["country"].isin(countries_options)][["country", "year","e_rr_pct_ret", "country-code"]]
df2.columns = ["country", "year","drug-resistance-percentage", "country-code"]
#st.write(df2)

chart_trend_rate = alt.Chart(df2).mark_line(point=True).encode(
    x=alt.X('year:O'),
    y=alt.Y("drug-resistance-percentage:Q", title= 'Percentage (%)', scale=alt.Scale(type='linear', domain=[0, 100])),
    color=alt.Color('country:N', title="Country"),
    tooltip=['year:T', alt.Tooltip("drug-resistance-percentage:Q", title="Percentage (%)")]
).transform_filter(
    selector
).properties(
    title=f'Yearly Trend of Drug Resistance Percentage Worldwide in from 2018 to 2021',
    width=width,
    height=height
)

chart_all = alt.vconcat(chart_resistance, chart_trend_rate).resolve_scale(color='independent')
st.altair_chart(chart_all, use_container_width=True)



countries_in_subset = df1["country"].unique()
if len(countries_in_subset) != len(countries):
    if len(countries_in_subset) == 0:
        st.write("No data avaiable for given subset.")
    else:
        missing = set(countries) - set(countries_in_subset)
        st.write("No data available for " + ", ".join(missing) + ".")
