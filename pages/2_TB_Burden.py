import streamlit as st
import time
import numpy as np
import pandas as pd
import altair as alt

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



#Treatment successful rate, incidence rate
#e_inc_num#Estimated number of incident cases (all forms)
#c_new_tsr ##Treatment success rate for all new cases (including relapse cases if rel_with_new_flg = 1), percent


#3. wolrd maps
from vega_datasets import data
source = alt.topo_feature(data.world_110m.url, 'countries')


df1 = subset.groupby(['country'])['c_new_tsr'].mean().reset_index()
df2 = subset.groupby(['country'])['e_inc_num'].mean().reset_index()
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
selector = alt.selection_single(
    fields=['country']
)
    #base plot
chart_base = alt.Chart(source
    ).properties(
        width=width,
        height=height
    ).project(project
    ).add_selection(selector
    ).transform_lookup(
        lookup="id",
        from_=alt.LookupData(df1, "country-code", ['c_new_str']),
)

# fix the color schema so that it will not change upon user selection
rate_scale = alt.Scale(domain=[df1['c_new_str'].min(), df1['c_new_str'].max()], scheme='oranges')
rate_color = alt.Color(field="c_new_str", type="quantitative", scale=rate_scale)

chart_treatmentrate = chart_base.mark_geoshape().encode(
      color=alt.Color('c_new_str:Q', scale=alt.Scale(scheme='oranges')),
      tooltip=['country:N', 'c_new_str:Q']
    ).transform_filter(
    selector
    ).properties(
    title=f'Average TB Treatment Success Rate Worldwide during {year_min} and {year_max}'
)

# fix the color schema so that it will not change upon user selection
population_scale = alt.Scale(domain=[df2['e_inc_num'].min(), df2['e_inc_num'].max()], scheme='yellowgreenblue')
chart_incidence = chart_base.mark_geoshape().encode(
    ######################
    # P3.2 map visualization showing the mortality rate
    # add your code here
      color='e_inc_num:Q',
     ######################
    # P3.3 tooltip
    # add your code here
      tooltip=['country:N', 'e_inc_num:Q']
    ).transform_filter(
    selector
).properties(
    title=f'Average Estimated number of incident cases (all forms) Worldwide during {year_min} and {year_max}'
)

chart2 = alt.vconcat(background + chart_treatmentrate, background + chart_incidence
).resolve_scale(
    color='independent'
)

st.altair_chart(chart2, use_container_width=True)
