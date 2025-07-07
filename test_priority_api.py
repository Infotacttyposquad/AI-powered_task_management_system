import requests

response = requests.post(
    "http://127.0.0.1:5000/predict_priority",
    json={"features": [7, 5]}
)

print("Response from API:", response.json())