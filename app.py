import streamlit as st
import pandas as pd
import joblib

# Load the trained model
model = joblib.load("Exercise Recommendation.pkl")

# Mappings
gender_mapping = {'Male': 0, 'Female': 1}
workout_mapping = {
    1: 'Strength',
    2: 'Cardio',
    3: 'Yoga',
    4: 'HIIT'
}

# Streamlit UI
st.title("🏋 GainWave - AI Exercise Recommendation")

st.markdown("Enter your personal data to get a recommended workout plan.")

# Form inputs
with st.form("recommendation_form"):
    age = st.number_input("Age", 10, 100, value=25)
    gender = st.selectbox("Gender", ["Male", "Female"])
    weight = st.number_input("Weight (kg)", 30.0, 200.0, value=70.0)
    height = st.number_input("Height (m)", 1.0, 2.5, value=1.7)
    max_bpm = st.number_input("Max BPM", 80, 220, value=180)
    avg_bpm = st.number_input("Average BPM", 60, 200, value=120)
    resting_bpm = st.number_input("Resting BPM", 40, 120, value=70)
    duration = st.number_input("Session Duration (hours)", 0.1, 5.0, value=1.0)
    calories = st.number_input("Calories Burned", 100, 3000, value=500)
    fat_pct = st.number_input("Fat Percentage", 5.0, 50.0, value=20.0)
    water = st.number_input("Water Intake (liters)", 0.5, 10.0, value=2.5)
    frequency = st.number_input("Workout Frequency (days/week)", 1, 7, value=3)
    experience = st.number_input("Experience Level (1-5)", 1, 5, value=2)
    bmi = st.number_input("BMI", 10.0, 50.0, value=22.5)

    submitted = st.form_submit_button("Get Recommendation")

    if submitted:
        input_data = pd.DataFrame([{
            "Age": age,
            "Gender": gender_mapping[gender],
            "Weight (kg)": weight,
            "Height (m)": height,
            "Max_BPM": max_bpm,
            "Avg_BPM": avg_bpm,
            "Resting_BPM": resting_bpm,
            "Session_Duration (hours)": duration,
            "Calories_Burned": calories,
            "Fat_Percentage": fat_pct,
            "Water_Intake (liters)": water,
            "Workout_Frequency (days/week)": frequency,
            "Experience_Level": experience,
            "BMI": bmi
        }])

        try:
            prediction = model.predict(input_data)
            recommendation = workout_mapping.get(int(prediction[0]), "Unknown")
            st.success(f"✅ Recommended Workout: *{recommendation}*")
        except Exception as e:
            st.error(f"Prediction failed: {e}")