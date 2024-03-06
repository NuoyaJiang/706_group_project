import altair as alt
import pandas as pd
import streamlit as st
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="TB Correlation",
    page_icon="🦠",
)

st.sidebar.header("TB Correlation")

st.write("# TB Correlation")

data = pd.read_pickle("data/mtb_cleaned_data_new.pkl")
subset = data[["e_rr_pct_new", "e_rr_pct_ret", 'c_new_tsr', 'c_tsr_resist', 
               "exp_cpp_dstb", "exp_cpp_mdr", "exp_lab","exp_orsrvy","exp_oth", 
               "exp_patsup", "exp_staff", 'exp_tpt']]

subset.columns = ['Percent of New Resistant Cases', 
                  'Percent of Treated Resistant Cases', 
                  'All New Case Treatment Success Rate', 
                  'Resistant Case Treatment Success Rate', 
                  'Average Cost of First-line Treatment', 
                  'Average Cost of Second-line Treatment',
                  'Expenditure on Laboratory Infrastructure', 
                  'Expenditure on Operational Research', 
                  'Expenditure on All Other Budget Line Items',
                  'Expenditure on Patient Support', 
                  'Expenditure on National TB Programme staff', 
                  'Expenditure for TB Prevention']

# subset.iloc[:, 4:] = subset.iloc[:, 4:].apply(np.sqrt)

x_options = st.multiselect('Select X dimension', options=subset.columns[6:], default=subset.columns[6:].tolist())
y_options = st.multiselect('Select Y dimension', options=subset.columns[0:6], default=subset.columns[0:6].tolist())

corr_mat = subset.corr().loc[x_options,y_options]

corr_mat = corr_mat.reset_index()

corr_mat = pd.melt(corr_mat, id_vars="index", value_name="Corr", var_name="TB Burden")
corr_mat.columns = ['Expenditure', 'TB Burden', 'Corr']
corr_mat['Corr'] = corr_mat['Corr'].round(2)

corrplot = alt.Chart(corr_mat).mark_bar().encode(
    x=alt.X("Expenditure:N", title=""),
    color=alt.Color("Corr:Q", title="Correlation").scale(scheme='blueorange'),
    y=alt.Y("TB Burden:N"),
    tooltip=["Corr:Q"],
).configure_axis(
        titleFontSize=14,
        labelLimit=0
)

st.altair_chart(corrplot, use_container_width=True)

x_option = st.selectbox('Select X dimension', subset.columns[6:], index=1)
y_option = st.selectbox('Select Y dimension', subset.columns[0:6], index=3)

scatterplot = alt.Chart(subset).mark_point().encode(
    y=alt.Y(y_option, title=y_option, scale=alt.Scale(type=f"{'symlog' if y_option in subset.columns[4:6] else 'linear'}")),
    x=alt.X(x_option, title=x_option, scale=alt.Scale(type='sqrt')),
)

lineplot = scatterplot.transform_regression(x_option, y_option).mark_line()

chart = alt.layer(scatterplot, lineplot).configure_view(
    stroke='transparent'
).configure_axis(
        titleFontSize=14,
        labelLimit=0
)




st.altair_chart(chart, use_container_width=True)

