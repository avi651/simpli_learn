import joblib
import pandas as pd

from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# ==========================================================
# 1. Load Dataset
# ==========================================================

df = pd.read_csv("iris.csv")

print("Dataset Loaded Successfully")
print(df.head())

# ==========================================================
# 2. Features & Target
# ==========================================================

X = df.drop(columns=["species"])
y = df["species"]

# ==========================================================
# 3. Train/Test Split
# ==========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

# ==========================================================
# 4. Train Model
# ==========================================================

model = DecisionTreeClassifier(
    random_state=42
)

model.fit(X_train, y_train)

# ==========================================================
# 5. Evaluate Model
# ==========================================================

y_pred = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    y_pred,
)

print(f"\nAccuracy: {accuracy:.2%}")

# ==========================================================
# 6. Save Model
# ==========================================================

MODEL_FILE = "dtc_model.joblib"

joblib.dump(
    model,
    MODEL_FILE,
)

print(f"\nModel saved successfully: {MODEL_FILE}")