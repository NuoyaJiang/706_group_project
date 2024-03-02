import altair as alt
import pandas as pd
import streamlit as st
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

corr_mat.columns = ['Percent of New Resistant Cases', 'Percent of Treated Resistant Cases', 
                    'All New Case Treatment Success Rate', 'Resistant Case Treatment Success Rate']


corr_mat.index = ['Expenditure for Drug-susceptible TB', 'Expenditure for Drug-resistant TB', 
                  'Expenditure on Laboratory Infrastructure', 'Expenditure on Operational Research', 
                  'Expenditure on All Other Budget Line Items',
                  'Expenditure on Patient Support', 'Expenditure on National TB Programme staff ']

corr_mat = corr_mat.reset_index()

corr_mat = pd.melt(corr_mat, id_vars="index", value_name="Corr", var_name="TB Burden")
corr_mat.columns = ['Expenditure', 'TB Burden', 'Corr']

corrplot = alt.Chart(corr_mat).mark_bar().encode(
    y=alt.Y("Expenditure:N", title=""),
    color=alt.Color("Corr:Q", title="Correlation").scale(scheme='plasma'),
    x=alt.X("TB Burden:N"),
    tooltip=["Corr:Q"],
).configure_axis(
        titleFontSize=14,
        labelLimit=0
)

st.altair_chart(corrplot, use_container_width=True)