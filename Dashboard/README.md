# Model Comparison Dashboard

This dashboard compares the three tuned models exported from the notebook workflow:
- Logistic Regression: Model_DIR/best_logistic_regression_rs_model.joblib
- Neural Network: Model_DIR/best_nn_model.joblib
- XGBoost: Model_DIR/best_xgboost_model.joblib

It reproduces the notebook-style comparison with:
- Precision, Recall, F1, PR-AUC, ROC-AUC
- False Positives / False Negatives
- Misclassification cost comparison
- Precision-Recall and ROC curves
- Confusion matrices for each model
- Threshold sensitivity chart (Precision/Recall/F1 vs threshold)
- Winner summary based on a selected ranking metric
- CSV export of comparison summary

## Run

From project root:

```bash
streamlit run Dashboard/model_comparison_dashboard.py
```

You can also use it inside the main app by selecting `Model Comparison` in `Dashboard Section`:

```bash
streamlit run streamlit_app.py
```

## Data input

You can use either:
- An uploaded CSV file with columns: Time, V1..V28, Amount, Class
- A local credit_card.csv in project root (enable sidebar checkbox)

The dashboard applies the same preprocessing approach used in the notebook:
- Scale Time and Amount using scaler_for_api.joblib
- Keep V1..V28 as provided
