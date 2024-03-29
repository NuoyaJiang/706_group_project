import altair as alt
import pandas as pd
import streamlit as st
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Financial Burden",
    page_icon="🦠",
)

st.sidebar.header("Financial Burden")

st.write("# Financial Burden")


st.write("### Correlation of Financial Expenditure and Resistance Percentage")

data = pd.read_pickle("data/mtb_cleaned_data_new.pkl")
subset = data[["e_rr_pct_new", "e_rr_pct_ret",
               "exp_cpp_dstb", "exp_cpp_mdr", "exp_lab","exp_orsrvy","exp_oth", 
               "exp_patsup", "exp_staff", 'exp_tpt']]

subset.columns = ['Percent of New Resistant Cases', 
                  'Percent of Returned Resistant Cases', 
                #   'All New Case Treatment Success Rate', 
                #   'Resistant Case Treatment Success Rate', 
                  'Average Cost of First-line Treatment', 
                  'Average Cost of Second-line Treatment',
                  'Expenditure on Laboratory Infrastructure', 
                  'Expenditure on Operational Research', 
                  'Expenditure on All Other Budget Line Items',
                  'Expenditure on Patient Support', 
                  'Expenditure on National TB Programme staff', 
                  'Expenditure for TB Prevention']

y_options = st.multiselect('Select Expenditure', options=subset.columns[2:], default=subset.columns[2:].tolist())
x_options = st.multiselect('Select Burden', options=subset.columns[0:2], default=subset.columns[0:2].tolist())

corr_mat = subset.corr().loc[x_options,y_options]

corr_mat = corr_mat.reset_index()

corr_mat = pd.melt(corr_mat, id_vars="index", value_name="Corr", var_name="TB Burden")
corr_mat.columns = ['Expenditure', 'TB Burden', 'Corr']
corr_mat['Corr'] = corr_mat['Corr'].round(2)

corrplot = alt.Chart(corr_mat).mark_bar().encode(
    x=alt.X("Expenditure:N", title=""),
    color=alt.Color("Corr:Q", title="Correlation").scale(scheme='blueorange'),
    y=alt.Y("TB Burden:N", title=""),
    tooltip=["Corr:Q"],
).configure_axis(
        titleFontSize=14,
        labelLimit=0
)

st.altair_chart(corrplot, use_container_width=True)

st.write("### Relationship of Financial Expenditure and Resistance Percentage")

x_option = st.selectbox('Select Burden', subset.columns[0:2], index=0)
y_option = st.selectbox('Select Expenditure', subset.columns[2:], index=6)

scatterplot = alt.Chart(subset).mark_point().encode(
    y=alt.Y(y_option, title=y_option, scale=alt.Scale(type='sqrt')),
    x=alt.X(x_option, title=x_option),
)

lineplot = scatterplot.transform_regression(x_option, y_option).mark_line()

chart = alt.layer(scatterplot, lineplot).configure_view(
    stroke='transparent'
).configure_axis(
        titleFontSize=14,
        labelLimit=0
)


st.altair_chart(chart, use_container_width=True)

st.write("### Difference in Cost in First- and Second-Line Treatment")

st.write("First-Line treatment is for normal patients, while Second-Line for resistant patients.")


# Bar
df_bar_f = pd.read_pickle("data/mtb_cleaned_data_new.pkl")
year_bar_f = st.slider('Select a year', min_value=int(df_bar_f['year'].min()), max_value=int(df_bar_f['year'].max()), value=2019, step=1)

countries_bar_f = ["United States of America", "Australia", "United Kingdom of Great Britain and Northern Ireland", "India", "South Africa", "Russian Federation", "Costa Rica", "Brazil"]
countries_options_bar_f = st.multiselect(
    "B) Choose countries to view:",
    df_bar_f['country'].unique().tolist(),
    countries_bar_f
)
bar_data_f = df_bar_f[df_bar_f["country"].isin(countries_options_bar_f)]
bar_data_f = bar_data_f[['country', 'year', "exp_cpp_dstb", "exp_cpp_mdr"]]
bar_data_f = bar_data_f.query('year == @year_bar_f')
bar_data_f.columns = ['country', 'year', 'First-Line', 'Second-Line']
bar_data_f = pd.melt(bar_data_f, id_vars=['country', 'year'], value_name="Treatment Cost", var_name="Type")

barplot = alt.Chart(bar_data_f).mark_bar().encode(
    x=alt.X('country:N'),
    y=alt.Y("Treatment Cost:Q"),
    color=alt.Color('Type:N'),
    tooltip=['Treatment Cost:Q']
)

st.altair_chart(barplot, use_container_width=True)