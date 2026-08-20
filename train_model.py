import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report


# Load dataset
data = pd.read_csv("data/phishing_dataset.csv")

# Input and target
X = data["text"]
y = data["label"]


# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)


# Create ML pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        sublinear_tf=True
    )),
    ("classifier", LogisticRegression(
        max_iter=1000,
        random_state=42
    ))
])


# Train model
model.fit(X_train, y_train)


# Evaluate model
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\n" + "=" * 50)
print("PHISHGUARD AI - MODEL TRAINING")
print("=" * 50)

print(f"\nModel Accuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test, predictions))


# Save trained model
joblib.dump(model, "models/phishing_model.joblib")

print("\nModel saved successfully!")
print("Location: models/phishing_model.joblib")