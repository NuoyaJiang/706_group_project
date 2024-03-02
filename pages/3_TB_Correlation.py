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

expenditure = pd.read_csv("data/TB_expenditure_utilisation_2024-02-21.csv")

subset = expenditure[["exp_cpp_dstb", "exp_cpp_mdr", "exp_fld", "exp_sld",
                        "exp_lab", "exp_mdrmgt","exp_orsrvy","exp_oth",
                        "exp_patsup","exp_prog","exp_staff"]]

# corr_mat = np.corrcoef(subset)

# import seaborn as sns
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.matshow(subset.corr(), ax=ax)
st.write(fig)