import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# Correct column names
task_col = "Task Description"
priority_col = "Priority"  


# Load and clean data
df = pd.read_csv("task_dataset.csv")
df.columns = df.columns.str.strip() 
df = df.dropna(subset=[task_col, priority_col])

# Feature engineering
df["word_count"] = df[task_col].apply(lambda x: len(str(x).split()))
df["has_urgent_word"] = df[task_col].str.lower().str.contains(r"\burgent|asap|immediately\b").astype(int)
df["has_deadline_word"] = df[task_col].str.lower().str.contains(r"\bbefore|by|due\b").astype(int)
X = df[["word_count", "has_urgent_word", "has_deadline_word"]]

# Encode priority labels
le = LabelEncoder()
y = le.fit_transform(df[priority_col])
joblib.dump(le, "priority_label_encoder.joblib")

# Train model
X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
model = LogisticRegression(class_weight="balanced")
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "priority_model.joblib")
print(" Model training complete. Files saved: priority_model.joblib, priority_label_encoder.joblib")