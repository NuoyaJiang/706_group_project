import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Tuberculosis Threat Visualization",
    page_icon="🦠",
)

home_url = "https://706groupprojectlmn.streamlit.app/TB_Drug_Resistance"

st.write("# Welcome to Group NLM!")

# st.sidebar.success("Select a demo above.")

st.markdown(
    f"""
    Tuberculosis (TB) is an infectious disease caused by the bacterial pathogen _Mycobacterium tuberculosis_, which mainly affects the lungs of the patients. Annually, more than 1 million patients die of TB worldwide, making TB the second leading cause of death from a single infectious agent, following COVID-19 [[1](https://www.who.int/teams/global-tuberculosis-programme/tb-reports/global-tuberculosis-report-2023)].
    In this project, we visualize [its rising trend in drug resistance]({home_url}/TB_Drug_Resistance), [the burden caused by drug resistance]({home_url}/TB_Burden), and [socioeconomic factors that may help us hamper the trend]({home_url}/TB_Correlation).
"""
)