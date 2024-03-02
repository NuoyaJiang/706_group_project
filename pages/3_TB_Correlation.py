import altair as alt
import pandas as pd
# import numpy as np
import streamlit as st

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

# corr_mat = np.corrcoef(subset)

import seaborn as sns
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
sns.heatmap(subset.corr().iloc[4:,0:4], ax=ax)
st.write(fig)