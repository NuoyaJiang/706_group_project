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

subset = data[["e_rr_pct_new", "e_rr_pct_ret", 'c_new_tsr', 'c_tsr_resist', 
               "exp_cpp_dstb", "exp_cpp_mdr", "exp_fld", "exp_sld", 
               "exp_lab", "exp_mdrmgt","exp_orsrvy","exp_oth", 
               "exp_patsup","exp_prog","exp_staff"]]

corr_mat = subset.corr().iloc[4:,0:4].reset_index()
corr_mat = pd.melt(corr_mat, id_vars="index", value_name="Corr", var_name="TB Burden")
corr_mat.columns = ['Expenditure', 'TB Burden', 'Corr']

corrplot = alt.Chart(subset).mark_bar().encode(
    x=alt.X("Expenditure:O"),
    color=alt.Color("Corr:Q"),
    y=alt.Y("TB Burden:N"),
    tooltip=["Corr"],
)

st.altair_chart(corrplot, use_container_width=True)