# import os
# from flask import Flask, request, render_template_string
# import joblib
# import pandas as pd
# from datetime import datetime

# app = Flask(__name__)

# # Load the trained model, LabelEncoder, and feature names
# model = joblib.load("model.pkl")
# le = joblib.load("label_encoder.pkl")
# feature_names = joblib.load("feature_names.pkl")

# # Read index.html content
# with open("index.html", "r") as file:
#     index_html = file.read()

# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         date = request.form["date"]
#         junction = request.form["junction"]
        
#         try:
#             # Convert junction to numeric
#             if isinstance(junction, str) and junction.startswith("Junction "):
#                 junction = int(junction.split(" ")[1])
            
#             # Ensure the junction is valid
#             if junction not in le.transform(le.classes_):
#                 available_junctions = ', '.join([f"Junction {i}" for i in range(len(le.classes_))])
#                 return f"Unknown junction: {junction}. Available junctions are: {available_junctions}"

#             # Parse the date
#             date = pd.to_datetime(date)

#             # Create features from the date
#             features = {
#                 "Year": date.year,
#                 "Month": date.month,
#                 "Day": date.day,
#                 "Hour": date.hour,
#                 "DayOfWeek": date.dayofweek,
#                 "Junction": junction
#             }

#             # Convert to DataFrame
#             features_df = pd.DataFrame([features])

#             # Reorder columns to match the training data
#             features_df = features_df[feature_names]

#             # Predict traffic level
#             prediction = model.predict(features_df)

#             result = "High" if prediction[0] == 1 else "Low"
#             return render_template_string(index_html, prediction=result)

#         except Exception as e:
#             return str(e)

#     return render_template_string(index_html, prediction=None)

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=port, debug=True)
import os
from flask import Flask, request, render_template_string
import joblib
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Load the trained model, LabelEncoder, and feature names
model = joblib.load("model.pkl")
le = joblib.load("label_encoder.pkl")
feature_names = joblib.load("feature_names.pkl")

# Read index.html content
with open("index.html", "r") as file:
    index_html = file.read()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        date = request.form["date"]
        junction = request.form["junction"]
        
        try:
            # Ensure the junction is valid and convert to integer
            junction = int(junction)
            if junction not in le.transform(le.classes_):
                available_junctions = ', '.join([f"Junction {i}" for i in range(len(le.classes_))])
                return f"Unknown junction: {junction}. Available junctions are: {available_junctions}"

            # Parse the date
            date = pd.to_datetime(date)

            # Create features from the date
            features = {
                "Year": date.year,
                "Month": date.month,
                "Day": date.day,
                "Hour": date.hour,
                "DayOfWeek": date.dayofweek,
                "Junction": junction
            }

            # Convert to DataFrame
            features_df = pd.DataFrame([features])

            # Reorder columns to match the training data
            features_df = features_df[feature_names]

            # Predict traffic level
            prediction = model.predict(features_df)

            result = "High" if prediction[0] == 1 else "Low"
            return render_template_string(index_html, prediction=result)

        except Exception as e:
            return str(e)

    return render_template_string(index_html, prediction=None)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
