import streamlit as st
import joblib
import pandas as pd

# Load the trained model and scaler
def load_model_and_scaler(): # Removed @st.cache_resource for Colab execution
    try:
        model = joblib.load('final_model.joblib')
        scaler = joblib.load('scaler_for_api.joblib')
        return model, scaler
    except FileNotFoundError as e:
        # In a Colab environment, st.error and st.stop do not halt execution.
        # Re-raising the error to provide a clear traceback if files are genuinely missing.
        raise FileNotFoundError(f"Model or scaler files not found: {e}. Please ensure 'final_model.joblib' and 'scaler_for_api.joblib' are in the correct directory.") from e

model, scaler = load_model_and_scaler()
