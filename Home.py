import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Tuberculosis Threat Visualization",
    page_icon="👋",
)


st.write("# Welcome to Group NLM!")

# st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Tuberculosis (TB) is an infectious disease caused by the bacterial pathogen _Mycobacterium tuberculosis_, which mainly affects the lungs of the patients. Annually, more than 1 million patients die of TB worldwide, making Mtb the second leading cause of death as a single infectious agent, following SARS-CoV-2 [1](https://www.who.int/teams/global-tuberculosis-programme/tb-reports/global-tuberculosis-report-2023).
"""
)