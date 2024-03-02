from vega_datasets import data
import streamlit as st
import time
import numpy as np
import pandas as pd
import altair as alt
from vega_datasets import data

@st.cache(allow_output_mutation=True)
def load_data():
    df = pd.read_pickle("data/mtb_cleaned_data.pkl")
    country_df = pd.read_csv('https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/country_codes.csv', dtype = {'conuntry-code': str})
    return df, country_df

df, country_df = load_data()
country_df['country'] = country_df['Country']
df = df.merge(country_df[['country', 'country-code']], on='country')

#1. slider to choose year
st.write("## Visualize the temporal trend of TB burden across different countries")
st.sidebar.header("TB Burden")
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
source = alt.topo_feature(data.world_110m.url, 'countries')
#world = alt.topo_feature('world_110m')

df1 = subset.groupby(['country'])['c_new_tsr'].mean().reset_index()
df2 = subset.groupby(['country'])['e_inc_num'].mean().reset_index()
df3 = df1.merge(df2, on = 'country')

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
        from_=alt.LookupData(df3, "country_code", ['country','c_new_tsr', 'e_inc_num']),
)

# fix the color schema so that it will not change upon user selection
rate_scale = alt.Scale(domain=[df3['c_new_tsr'].min(), df3['c_new_tsr'].max()], scheme='oranges')
rate_color = alt.Color(field="c_new_tsr", type="quantitative", scale=rate_scale)

chart_treatmentrate = chart_base.mark_geoshape().encode(
      color=alt.Color('c_new_tsr:Q', scale=alt.Scale(scheme='oranges')),
      tooltip=['country:N', 'c_new_tsr:Q']
    ).transform_filter(
    selector
    ).properties(
    title=f'Average TB Treatment Success Rate Worldwide during {year_min} and {year_max}'
)

# fix the color schema so that it will not change upon user selection
population_scale = alt.Scale(domain=[df3['e_inc_num'].min(), df3['e_inc_num'].max()], scheme='yellowgreenblue')
chart_incidence = chart_base.mark_geoshape().encode(
      color='e_inc_num:Q',
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
