import streamlit as st
import joblib
import os
st.write("Current working directory:", os.getcwd())

# Load the trained model and encoders
model = joblib.load("models/status_classifier_rf.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")
label_encoder = joblib.load("models/status_label_encoder.pkl")

# Streamlit page setup
st.set_page_config(page_title="AI Task Management", layout="centered")

# Apply custom CSS for cleaner visuals
st.markdown("""
    <style>
        .main {
            background-color: #f4f4f9;
        }
        .stTextArea label {
            font-weight: bold;
        }
        .stButton > button {
            background-color: #4CAF50;
            color: white;
        }
        .stButton > button:hover {
            background-color: #45a049;
        }
        .predicted-box {
            background-color: #e8f0fe;
            padding: 10px;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# App Header
st.title("🤖 AI-Powered Task Management System")
st.markdown("Use this tool to **predict the priority** of tasks using machine learning. Just enter a description and click predict!")

# Input Section
st.subheader("📌 Task Description")
task_description = st.text_area("", height=140, placeholder="E.g. Resolve critical server downtime immediately...")

# Predict Button
if st.button("🔍 Predict Priority"):
    if not task_description.strip():
        st.warning("⚠️ Please enter a valid task description.")
    else:
        # Preprocess and predict
        cleaned_text = task_description.lower()
        vectorized_input = vectorizer.transform([cleaned_text])
        prediction = model.predict(vectorized_input)[0]
        predicted_priority = label_encoder.inverse_transform([prediction])[0]

        # Display the prediction result
        st.markdown("### 🧠 Predicted Task Priority:")
        st.markdown(f"<div class='predicted-box'>{predicted_priority}</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("✨ Developed with Streamlit · Scikit-learn · ❤️")
