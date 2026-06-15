import joblib
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Iris Species Predictor", layout="centered")
st.title("Iris Species Prediction (Decision Tree)")
st.write(
    "Use the sliders below to predict iris species with the trained Decision Tree model."
)


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

col1, col2 = st.columns(2)
with col1:
    sepal_length = st.slider("Sepal Length", 4.0, 8.0, 5.8, 0.1)
    # Syntax: st.slider(label, min_value, max_value, default_value, step)
    sepal_width = st.slider("Sepal Width", 2.0, 4.5, 3.0, 0.1)
with col2:
    petal_length = st.slider("Petal Length", 1.0, 7.0, 4.3, 0.1)
    petal_width = st.slider("Petal Width", 0.1, 2.5, 1.3, 0.1)

if st.button("Predict Species"):
    input_df = pd.DataFrame(
        [[sepal_length, sepal_width, petal_length, petal_width]],
        columns=["sepal_length", "sepal_width", "petal_length", "petal_width"],
    )
    prediction = model.predict(input_df)[0]
    st.success(f"Predicted Species: {prediction}")
