import os
import joblib
import pandas as pd
import streamlit as st
from datetime import datetime

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(page_title="Iris Species Predictor", layout="centered")

st.title("🌸 Iris Species Prediction (Decision Tree)")
st.write(
    "Use the sliders below to predict iris species with the trained Decision Tree model."
)

LOG_FILE = "prediction_logs.csv"

# =====================================================
# MODEL LOADING
# =====================================================


@st.cache_resource
def load_model():
    return joblib.load("dtc_model.joblib")


try:
    model = load_model()
except FileNotFoundError:
    st.error(
        "dtc_model.joblib not found. Run the notebook cell that saves the model first."
    )
    st.stop()

# =====================================================
# INPUT SECTION
# =====================================================

col1, col2 = st.columns(2)

with col1:
    sepal_length = st.slider("Sepal Length", 4.0, 8.0, 5.8, 0.1)

    sepal_width = st.slider("Sepal Width", 2.0, 4.5, 3.0, 0.1)

with col2:
    petal_length = st.slider("Petal Length", 1.0, 7.0, 4.3, 0.1)

    petal_width = st.slider("Petal Width", 0.1, 2.5, 1.3, 0.1)

# =====================================================
# LOGGING FUNCTION
# =====================================================


def log_prediction(record):

    df = pd.DataFrame([record])

    if os.path.exists(LOG_FILE):
        df.to_csv(LOG_FILE, mode="a", header=False, index=False)
    else:
        df.to_csv(LOG_FILE, mode="w", header=True, index=False)


# =====================================================
# PREDICTION
# =====================================================

if st.button("Predict Species"):
    input_df = pd.DataFrame(
        [[sepal_length, sepal_width, petal_length, petal_width]],
        columns=["sepal_length", "sepal_width", "petal_length", "petal_width"],
    )

    prediction = model.predict(input_df)[0]

    st.success(f"Predicted Species: {prediction}")

    # -----------------------------------
    # Logging
    # -----------------------------------

    log_record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sepal_length": sepal_length,
        "sepal_width": sepal_width,
        "petal_length": petal_length,
        "petal_width": petal_width,
        "prediction": prediction,
    }

    log_prediction(log_record)

    st.info("Prediction logged successfully.")

# =====================================================
# VIEW LOGS
# =====================================================

st.markdown("---")
st.subheader("Prediction History")

if os.path.exists(LOG_FILE):
    logs_df = pd.read_csv(LOG_FILE)

    st.dataframe(
        logs_df,
        use_container_width=True,  # Make the dataframe take the full width of the container
    )

    # ===================================
    # CSV DOWNLOAD
    # ===================================

    csv = logs_df.to_csv(index=False)

    st.download_button(
        label="📥 Download Prediction Logs",
        data=csv,
        file_name="prediction_logs.csv",
        mime="text/csv",  # Set the MIME type to text/csv for better compatibility
    )

else:
    st.warning("No prediction logs available yet.")
