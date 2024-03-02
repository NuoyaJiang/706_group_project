import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Tuberculosis Threat Visualization",
    page_icon="🦠",
)

home_url = "https://706groupprojectlmn.streamlit.app"
target = "_self"

st.write("# Welcome to Group NLM!")

st.sidebar.header("Home")

st.markdown(
    """
    Tuberculosis (TB) is an infectious disease caused by the bacterial pathogen _Mycobacterium tuberculosis_, which mainly affects the lungs of the patients. Annually, more than 1 million patients die of TB worldwide, making TB the second leading cause of death from a single infectious agent, following COVID-19 [[1](https://www.who.int/teams/global-tuberculosis-programme/tb-reports/global-tuberculosis-report-2023)].
    More distressingly, recent years have witnessed a rapid rise in _Mtb_'s ability to resist antibiotics, such as Rifampicin. This severely increased the difficulty to treat TB, posing a serious threat to human health [[2](https://onlinelibrary-wiley-com.ezp-prod1.hul.harvard.edu/doi/10.1111/resp.13304)].
"""
)

st.markdown(f"In this project, we visualize <a href={home_url+'/TB_Drug_Resistance'} target={target}>its rising trend in drug resistance</a>, <a href={home_url+'/TB_Burden'} target={target}>the burden caused by drug resistance</a>, and <a href={home_url+'/TB_Correlation'} target={target}>socioeconomic factors that may help us hamper the trend</a> with data from [WHO Global Tuberculosis Programme](https://www.who.int/teams/global-tuberculosis-programme/data). We hope our efforts could raise more awareness of the issue.", unsafe_allow_html=True)

st.image('images/tuberculosis.jpeg', caption='Spread of Tuberculosis')

st.markdown('Source: [Harvard Health](https://www.health.harvard.edu/a_to_z/tuberculosis-a-to-z)')

st.image('images/resisting-bacteria.png', caption='Drug Resistance')

st.markdown('Source: [It Ain\'t Magic](https://itaintmagic.riken.jp/hot-off-the-press/bacterial-drug-resistance-studied-by-robotic-e-coli-evolution/)')