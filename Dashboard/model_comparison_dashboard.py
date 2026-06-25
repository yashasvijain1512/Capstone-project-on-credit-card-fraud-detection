import streamlit as st

from Dashboard.model_comparison_page import render_model_comparison_page


st.set_page_config(page_title="Fraud Model Comparison Dashboard", layout="wide")
render_model_comparison_page(show_title=True)
