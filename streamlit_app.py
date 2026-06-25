import joblib
import pandas as pd
import streamlit as st


MODEL_PATH = "final_model.joblib"
SCALER_PATH = "scaler_for_api.joblib"

st.set_page_config(page_title="Credit Card Fraud Detection", layout="wide")


def get_default_feature_order():
    return ["Time"] + [f"V{i}" for i in range(1, 29)] + ["Amount"]


@st.cache_resource
def load_model_and_scaler():
    try:
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        return model, scaler
    except FileNotFoundError as exc:
        st.error(
            f"Missing file: {exc}. Keep {MODEL_PATH} and {SCALER_PATH} in the project root."
        )
        st.stop()
    except ModuleNotFoundError as exc:
        st.error(
            f"Dependency missing while loading model: {exc}. Install required packages (including xgboost)."
        )
        st.stop()


def get_expected_columns(model):
    if hasattr(model, "feature_names_in_"):
        return list(model.feature_names_in_)
    return get_default_feature_order()


def preprocess_input(input_df, expected_columns, scaler):
    processed_df = input_df.copy()

    for column in expected_columns:
        if column not in processed_df.columns:
            processed_df[column] = 0.0

    processed_df = processed_df[expected_columns]
    processed_df = processed_df.apply(pd.to_numeric, errors="coerce").fillna(0.0)

    if "Time" in processed_df.columns and "Amount" in processed_df.columns:
        processed_df[["Time", "Amount"]] = scaler.transform(processed_df[["Time", "Amount"]])

    return processed_df


model, scaler = load_model_and_scaler()
expected_columns = get_expected_columns(model)

st.title("Credit Card Fraud Detection")
st.caption("Model: final_model.joblib (Tuned XGBoost) | Preprocessing: scale Time and Amount")

st.sidebar.header("Transaction Input")
time_value = st.sidebar.number_input(
    "Time (seconds since first transaction)", min_value=0.0, value=10000.0, step=1.0
)
amount_value = st.sidebar.number_input("Amount", min_value=0.0, value=50.0, step=0.01)

v_inputs = {}
for i in range(1, 29):
    v_inputs[f"V{i}"] = st.sidebar.number_input(f"V{i}", value=0.0, step=0.01, format="%.6f")

raw_input = {"Time": time_value, **v_inputs, "Amount": amount_value}
input_df = pd.DataFrame([raw_input])

if st.button("Predict", type="primary"):
    try:
        model_input = preprocess_input(input_df, expected_columns, scaler)
        prediction = int(model.predict(model_input)[0])

        fraud_probability = None
        if hasattr(model, "predict_proba"):
            fraud_probability = float(model.predict_proba(model_input)[:, 1][0])

        st.subheader("Prediction")
        if prediction == 1:
            st.error("Fraudulent transaction detected")
        else:
            st.success("Legitimate transaction")

        if fraud_probability is not None:
            st.metric("Fraud Probability", f"{fraud_probability:.4f}")

        with st.expander("Processed features sent to model"):
            st.dataframe(model_input)
    except Exception as exc:
        st.error(f"Prediction failed: {exc}")

with st.expander("Model details"):
    st.write(f"Expected feature count: {len(expected_columns)}")
    st.write(expected_columns)

    
