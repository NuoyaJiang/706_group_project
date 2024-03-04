from vega_datasets import data
import streamlit as st
import time
import numpy as np
import pandas as pd
import altair as alt
from vega_datasets import data

st.set_page_config(
    page_title="TB Drug Burden",
    page_icon="🦠",
)

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

#2. selection for countries, variable calculations
countries = ["United States of America", "Australia", "United Kingdom of Great Britain and Northern Ireland", "India", "South Africa", "Russian Federation", "Costa Rica", "Brazil"]
countries_options = st.multiselect(
    "B) Choose countries to view:",
    df['country'].unique().tolist(),
    countries
)
subset = subset[subset["country"].isin(countries_options)]
#e_rr_pct_new #Estimated percentage of new TB cases with rifampicin resistant TB
#e_rr_pct_ret #Estimated percentage of previously treated TB cases with rifampicin resistant TB
    ### ('e_rr_pct_new' + 'e_rr_pct_ret') * 'e_inc_num' = TB resistant cases
subset['incidence_resistant'] = (subset['e_rr_pct_new'] + subset['e_rr_pct_ret']) * subset['e_inc_num']

#mdr_coh #Outcomes for MDR-TB cases: cohort size
#mdr_succ #Outcomes for MDR-TB cases: treatment success (Cured or treatment completed)
    ### 'mdr_succ' / 'mdr_coh' = treatment success rate for TB resistant patients
subset['success_rate_resistant'] = subset['mdr_succ'] / subset['mdr_coh']



#3. wolrd maps - all cases
source = alt.topo_feature(data.world_110m.url, 'countries')

df1 = subset.groupby(['country'])['c_new_tsr'].mean().reset_index() #e_inc_num#Estimated number of incident cases (all forms)
df2 = subset.groupby(['country'])['e_inc_num'].mean().reset_index() ##c_new_tsr ##Treatment success rate for all new cases (including relapse cases if rel_with_new_flg = 1), percent
df3 = subset.groupby(['country'])['incidence_resistant'].mean().reset_index()
df4 = subset.groupby(['country'])['success_rate_resistant'].mean().reset_index()

df_mean = df1.merge(df2, on = 'country').merge(df3, on='country').merge(df4, on='country')
df_mean = df_mean.merge(country_df[['country', 'country-code']], on='country')
#df3 = df3[~((df3['c_new_tsr'].isna())|(df3['e_inc_num'].isna()))]


width = 450
height  = 225
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
        from_=alt.LookupData(df_mean, "country-code", ['country',"c_new_tsr", "e_inc_num"]),
)

# fix the color schema so that it will not change upon user selection
rate_scale = alt.Scale(domain=[df_mean['c_new_tsr'].min(), df_mean['c_new_tsr'].max()], scheme='oranges')
#rate_color = alt.Color(field="c_new_tsr", type="quantitative", scale=rate_scale)

chart_treatmentrate = chart_base.mark_geoshape().encode(
      color=alt.Color('c_new_tsr:Q', scale=rate_scale, title="Treatment Success Rate (%)",
                      legend=alt.Legend(orient="bottom", direction="horizontal")),
      tooltip=['year:O', alt.Tooltip("c_new_tsr:Q", title="Treatment Success Rate")]
    ).transform_filter(
    selector
    ).properties(
    title=f'Average TB Treatment Success Rate Worldwide during {year_slider[0]} and {year_slider[1]}'
)

# fix the color schema so that it will not change upon user selection
population_scale = alt.Scale(domain=[df_mean['e_inc_num'].min(), df_mean['e_inc_num'].max()], scheme='yellowgreenblue')
chart_incidence = chart_base.mark_geoshape().encode(
      color=alt.Color('e_inc_num:Q', title= "cases per 100,000 population", scale = population_scale,
                      legend=alt.Legend(orient="bottom", direction="horizontal")),
      tooltip=['year:O', alt.Tooltip("e_inc_num:Q", title="cases per 100,000 population")]
    ).transform_filter(
    selector
).properties(
    title=f'Average Estimated TB Incidences Worldwide during {year_slider[0]} and {year_slider[1]}'
)

chart_treatmentrate = alt.vconcat(background + chart_treatmentrate).resolve_scale(color='independent')
chart_incidence = alt.vconcat(background + chart_incidence).resolve_scale(color='independent')





#3.5 wolrd maps - RESISTANT cases
source = alt.topo_feature(data.world_110m.url, 'countries')

df1 = subset.groupby(['country'])['c_new_tsr'].mean().reset_index() #e_inc_num#Estimated number of incident cases (all forms)
df2 = subset.groupby(['country'])['e_inc_num'].mean().reset_index() ##c_new_tsr ##Treatment success rate for all new cases (including relapse cases if rel_with_new_flg = 1), percent
df3 = subset.groupby(['country'])['incidence_resistant'].mean().reset_index()
df4 = subset.groupby(['country'])['success_rate_resistant'].mean().reset_index()

df_mean = df1.merge(df2, on = 'country').merge(df3, on='country').merge(df4, on='country')
df_mean = df_mean.merge(country_df[['country', 'country-code']], on='country')
#df3 = df3[~((df3['c_new_tsr'].isna())|(df3['e_inc_num'].isna()))]

    #base plot
chart_base = alt.Chart(source
    ).properties(
        width=width,
        height=height
    ).project(project
    ).add_selection(selector
    ).transform_lookup(
        lookup="id",
        from_=alt.LookupData(df_mean, "country-code", ['country',"incidence_resistant", "success_rate_resistant"]),
)

# fix the color schema so that it will not change upon user selection
rate_scale = alt.Scale(domain=[df_mean['incidence_resistant'].min(), df_mean['incidence_resistant'].max()], scheme='oranges')

chart_treatmentrate_resistant = chart_base.mark_geoshape().encode(
      color=alt.Color('incidence_resistant:Q', scale=rate_scale, title="Treatment Success Rate (%)",
                      legend=alt.Legend(orient="bottom", direction="horizontal")),
      tooltip=['year:O', alt.Tooltip("incidence_resistant:Q", title="Treatment Success Rate")]
    ).transform_filter(
    selector
    ).properties(
    title=f'Average TB Treatment Success Rate Worldwide during {year_slider[0]} and {year_slider[1]}'
)

# fix the color schema so that it will not change upon user selection
population_scale = alt.Scale(domain=[df_mean['success_rate_resistant'].min(), df_mean['success_rate_resistant'].max()], scheme='yellowgreenblue')
chart_incidence_resistant = chart_base.mark_geoshape().encode(
      color=alt.Color('success_rate_resistant:Q', title= "cases per 100,000 population", scale=population_scale,
                       legend=alt.Legend(orient="bottom", direction="horizontal")),
      tooltip=['year:O', alt.Tooltip("success_rate_resistant:Q", title="cases per 100,000 population")]
    ).transform_filter(
    selector
).properties(
    title=f'Average Estimated TB Incidences Worldwide during {year_slider[0]} and {year_slider[1]}'
)

chart_treatmentrate_resistant = alt.vconcat(background + chart_treatmentrate_resistant).resolve_scale(color='independent')
chart_incidence_resistant = alt.vconcat(background + chart_incidence_resistant).resolve_scale(color='independent')








#4. individual smaller plots, all & resistant
chart_trend_rate = alt.Chart(subset).mark_line(point=True).encode(
    x=alt.X('year:O'),
    y=alt.Y("c_new_tsr:Q", title= 'TB Treatment Success Rate (%)', scale=alt.Scale(type='log', domain=[subset['c_new_tsr'].min()-10, 100])),
    color=alt.Color('country:N'),
    tooltip=['year:O', alt.Tooltip("c_new_tsr:Q", title="TB Treatment Success Rate (%)")]
).transform_filter(
    selector
).properties(
    title=f'Yearly Trend of TB Treatment Success Rate Worldwide during {year_slider[0]} and {year_slider[1]}',
    width=width,
    height=height
)

chart_trend_incident = alt.Chart(subset).mark_line(point=True).encode(
    x=alt.X('year:O'),
    y=alt.Y("e_inc_num:Q", title= 'TB Incidences (per 100,000 population)', scale=alt.Scale(type='log')),
    color=alt.Color('country:N'),
    tooltip=['year:O', alt.Tooltip("e_inc_num:Q", title="cases per 100,000 population")]
).transform_filter(
    selector
).properties(
    title=f'Yearly Trend of TB Incidence Cases Worldwide during {year_slider[0]} and {year_slider[1]}',
    width=width,
    height=height
)


chart_trend_rate_resis = alt.Chart(subset).mark_line(point=True).encode(
    x=alt.X('year:O'),
    y=alt.Y("incidence_resistant:Q", title= 'TB Treatment Success Rate (%)', scale=alt.Scale(type='log')),#, domain=[subset['incidence_resistant'].min()-10, 100])),
    color=alt.Color('country:N'),
    tooltip=['year:O', alt.Tooltip("incidence_resistant:Q", title="TB Treatment Success Rate (%)")]
).transform_filter(
    selector
).properties(
    title=f'Yearly Trend of TB Treatment Success Rate Worldwide during {year_slider[0]} and {year_slider[1]}',
    width=width,
    height=height
)

chart_trend_incident_resis = alt.Chart(subset).mark_line(point=True).encode(
    x=alt.X('year:O'),
    y=alt.Y("success_rate_resistant:Q", title= 'TB Incidences (per 100,000 population)', scale=alt.Scale(type='log')),
    color=alt.Color('country:N'),
    tooltip=['year:O', alt.Tooltip("success_rate_resistant:Q", title="cases per 100,000 population")]
).transform_filter(
    selector
).properties(
    title=f'Yearly Trend of TB Incidence Cases Worldwide during {year_slider[0]} and {year_slider[1]}',
    width=width,
    height=height
)






#5. combine all plots
#chart_all = chart_maps & chart_trend_rate & chart_trend_incident
chart_top = alt.hconcat(chart_treatmentrate, chart_trend_rate).resolve_scale(color='independent')
chart_top_resis = alt.hconcat(chart_treatmentrate_resistant, chart_trend_rate_resis).resolve_scale(color='independent')
chart_bottom = alt.hconcat(chart_incidence, chart_trend_incident).resolve_scale(color='independent')
chart_bottom_resis = alt.hconcat(chart_incidence_resistant, chart_trend_incident_resis).resolve_scale(color='independent')
chart_all = chart_top & chart_top_resis
chart_all = chart_all & chart_bottom & chart_bottom_resis

st.altair_chart(chart_all, use_container_width=True)


countries_in_subset = df3["country"].unique()
if len(countries_in_subset) != len(countries):
    if len(countries_in_subset) == 0:
        st.write("No data avaiable for given subset.")
    else:
        missing = set(countries) - set(countries_in_subset)
        st.write("No data available for " + ", ".join(missing) + ".")
