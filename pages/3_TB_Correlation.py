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

corr_mat = data[["e_rr_pct_new", "e_rr_pct_ret", 'c_new_tsr', 'c_tsr_resist', 
               "exp_fld", "exp_sld", "exp_lab","exp_orsrvy","exp_oth", 
               "exp_patsup", "exp_staff"]].corr().iloc[4:,0:4]

columns = ['Percent of New Resistant Cases', 'Percent of Treated Resistant Cases', 
           'All New Case Treatment Success Rate', 'Resistant Case Treatment Success Rate']


corr_mat.columns = columns

indices = ['Expenditure for Drug-susceptible TB', 'Expenditure for Drug-resistant TB', 
            'Expenditure on Laboratory Infrastructure', 'Expenditure on Operational Research', 
            'Expenditure on All Other Budget Line Items',
            'Expenditure on Patient Support', 'Expenditure on National TB Programme staff ']

corr_mat.index = indices

corr_mat = corr_mat.reset_index()

corr_mat = pd.melt(corr_mat, id_vars="index", value_name="Corr", var_name="TB Burden")
corr_mat.columns = ['Expenditure', 'TB Burden', 'Corr']
corr_mat['Corr'] = corr_mat['Corr'].round(2)

corrplot = alt.Chart(corr_mat).mark_bar().encode(
    y=alt.Y("Expenditure:N", title=""),
    color=alt.Color("Corr:Q", title="Correlation").scale(scheme='turbo'),
    x=alt.X("TB Burden:N"),
    tooltip=["Corr:Q"],
).configure_axis(
        titleFontSize=14,
        labelLimit=0
)

st.altair_chart(corrplot, use_container_width=True)

x_option = st.selectbox('Select X dimension', indices)
y_option = st.selectbox('Select Y dimension', columns)

x_var = ["exp_fld", "exp_sld", "exp_lab","exp_orsrvy","exp_oth", 
               "exp_patsup", "exp_staff"][np.where(indices == x_option)]

y_var = ["e_rr_pct_new", "e_rr_pct_ret", 'c_new_tsr', 'c_tsr_resist'][np.where(columns == y_option)]

scatterplot = alt.Chart(data).mark_point().encode(
    y=alt.Y(y_var, title=y_option),
    x=alt.X(x_var, title=x_option),
).configure_axis(
        titleFontSize=14,
        labelLimit=0
)
st.altair_chart(scatterplot, use_container_width=True)

