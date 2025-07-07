from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# --- Load all models ---
try:
    type_model = joblib.load("task_type_model.joblib")
    vectorizer = joblib.load("task_vectorizer.joblib")
    priority_model = joblib.load("priority_model.joblib")
    priority_encoder = joblib.load("priority_label_encoder.joblib")
    print("✅ All models loaded successfully.")
except Exception as e:
    print(f"❌ Model loading error: {e}")

# --- Task Type Classification ---
@app.route("/classify_task", methods=["POST"])
def classify_task():
    try:
        data = request.get_json()
        task_text = data.get("task")
        if not task_text:
            return jsonify({"error": "Missing 'task' in input"}), 400

        vector = vectorizer.transform([task_text])
        prediction = type_model.predict(vector)[0]

        print("🧠 Predicted task type:", prediction)
        return jsonify({"task_type": prediction})
    except Exception as e:
        print(f"❌ Classification error: {e}")
        return jsonify({"error": f"Classification failed: {str(e)}"}), 500

# --- Priority Prediction (using word count only) ---
@app.route("/predict_priority", methods=["POST"])
def predict_priority():
    try:
        data = request.get_json()
        features = data.get("features")  # expects a list like: [word_count]
        if not features or not isinstance(features, list):
            return jsonify({"error": "Missing or invalid 'features'"}), 400

        raw_prediction = priority_model.predict([features])[0]
        priority_label = priority_encoder.inverse_transform([raw_prediction])[0]

        print("🚦 Predicted priority:", priority_label)
        return jsonify({"priority": priority_label})
    except Exception as e:
        print(f"❌ Priority prediction error: {e}")
        return jsonify({"error": f"Priority prediction failed: {str(e)}"}), 500

# --- Start the server ---
if __name__ == "__main__":
    app.run(port=5000)