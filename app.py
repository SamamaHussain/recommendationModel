from flask import Flask, request, jsonify
import joblib
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load the model (after fixing version mismatch)
model = joblib.load('Exercise Recommendation.pkl')

# EXPECTED_COLUMNS = ['Age', 'Gender', 'Weight (kg)', 'Height (m)', 'Max_BPM', 'Avg_BPM',
#        'Resting_BPM', 'Session_Duration (hours)', 'Calories_Burned',
#        'Fat_Percentage', 'Water_Intake (liters)',
#        'Workout_Frequency (days/week)', 'Experience_Level', 'BMI']

EXPECTED_COLUMNS = ['Age', 'Gender', 'Weight (kg)', 'Height (m)',
       'Session_Duration (hours)', 'Calories_Burned',
       'Fat_Percentage', 'Water_Intake (liters)',
       'Workout_Frequency (days/week)', 'Experience_Level', 'BMI']

gender_mapping = {
    0: 'Male',
    1: 'Female'
}

workout_mapping = {
    1: 'Strength',
    2: 'Cardio',
    3: 'Yoga',
    4: 'HIIT'
}

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        input_df = pd.DataFrame([data])
        input_df = input_df[EXPECTED_COLUMNS]

        prediction = model.predict(input_df)
        label = workout_mapping.get(int(prediction[0]), "Unknown")

        return jsonify({
            'recommendation': label,
            'status': 'success'
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
