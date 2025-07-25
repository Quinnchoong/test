# -*- coding: utf-8 -*-
"""student_employability_app_final.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18-3dqWEVtZ9vWPIW7UxmFxQEr8itV66I
"""

# advanced_employability_app_final.py
# app.py — Final Streamlit App

import streamlit as st
import pandas as pd
import joblib
import numpy as np

# --- Load Model & Scaler ---
try:
    model = joblib.load('employability_predictor.pkl')
    scaler = joblib.load('scaler.pkl')
    st.success("✅ Model and Scaler loaded successfully!")
except FileNotFoundError:
    st.error("❌ Model or Scaler file not found. Please check the files.")
    st.stop()

# --- Feature Columns ---
feature_columns = [
    'GENDER', 'GENERAL_APPEARANCE', 'GENERAL_POINT_AVERAGE',
    'MANNER_OF_SPEAKING', 'PHYSICAL_CONDITION', 'MENTAL_ALERTNESS',
    'SELF-CONFIDENCE', 'ABILITY_TO_PRESENT_IDEAS', 'COMMUNICATION_SKILLS',
    'STUDENT_PERFORMANCE_RATING', 'NO_SKILLS', 'Year_of_Graduate'
]

# --- Title ---
st.title("🎓 Student Employability Prediction")
st.markdown("Predict whether a student is employable based on their attributes.")

# --- Single Prediction ---
st.header("🔍 Single Student Prediction")

col1, col2 = st.columns(2)
input_values = {}

with col1:
    input_values['GENDER'] = st.radio("Gender", [0,1], format_func=lambda x: "Female" if x==0 else "Male", index=1)
    input_values['GENERAL_APPEARANCE'] = st.slider("General Appearance (1-5)", 1,5,3)
    input_values['GENERAL_POINT_AVERAGE'] = st.number_input("GPA (0.0-4.0)", 0.0,4.0,3.0,0.01)
    input_values['MANNER_OF_SPEAKING'] = st.slider("Manner of Speaking (1-5)", 1,5,3)
    input_values['PHYSICAL_CONDITION'] = st.slider("Physical Condition (1-5)", 1,5,3)
    input_values['MENTAL_ALERTNESS'] = st.slider("Mental Alertness (1-5)", 1,5,3)

with col2:
    input_values['SELF-CONFIDENCE'] = st.slider("Self-Confidence (1-5)", 1,5,3)
    input_values['ABILITY_TO_PRESENT_IDEAS'] = st.slider("Ability to Present Ideas (1-5)", 1,5,3)
    input_values['COMMUNICATION_SKILLS'] = st.slider("Communication Skills (1-5)", 1,5,3)
    input_values['STUDENT_PERFORMANCE_RATING'] = st.slider("Student Performance Rating (1-5)", 1,5,3)
    input_values['NO_SKILLS'] = st.radio("Has No Skills?", [0,1], format_func=lambda x: "No" if x==0 else "Yes", index=0)
    input_values['Year_of_Graduate'] = st.number_input("Year of Graduation (2019-2025)", 2019,2025,2022)

input_df = pd.DataFrame([input_values])[feature_columns]
scaled_input = scaler.transform(input_df)

if st.button("🎯 Predict"):
    prediction = model.predict(scaled_input)
    proba = model.predict_proba(scaled_input)

    if prediction[0] == 1:
        st.success(f"🎉 Employable! (Probability: {proba[0][1]*100:.2f}%)")
    else:
        st.warning(f"⚠️ Less Employable. (Probability: {proba[0][0]*100:.2f}%)")

        st.markdown("### 📌 Suggested Improvements:")
        st.write("- Improve GPA and Technical Skills.")
        st.write("- Work on soft skills: Communication, Self-Confidence.")
        st.write("- Enhance presentation and mental alertness.")

# --- Batch Prediction ---
st.header("📁 Batch Prediction (CSV Upload)")
st.markdown("Upload a CSV file with the same columns as expected.")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    batch_df = pd.read_csv(uploaded_file)
    try:
        batch_scaled = scaler.transform(batch_df[feature_columns])
        batch_pred = model.predict(batch_scaled)
        batch_proba = model.predict_proba(batch_scaled)

        batch_df['Prediction'] = np.where(batch_pred==1, 'Employable', 'Less Employable')
        batch_df['Employable (%)'] = (batch_proba[:,1]*100).round(2)
        batch_df['Less Employable (%)'] = (batch_proba[:,0]*100).round(2)

        st.write("### 📋 Prediction Results:")
        st.dataframe(batch_df)

        csv = batch_df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download Results as CSV", data=csv, file_name="prediction_results.csv")

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")

# --- Footer ---
st.markdown("---")
st.caption("© 2025 CHOONG MUH IN | Employability Predictor | Powered by SVM")
