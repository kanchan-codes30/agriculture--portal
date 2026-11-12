import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# 📊 Load Dataset
data = pd.read_csv("crop_dataset.csv")

# 🧹 Features & Target
X = data.drop("crop", axis=1)
y = data["crop"]

# 🤖 Model Train
model = RandomForestClassifier()
model.fit(X, y)

# 💾 Save Model
joblib.dump(model, "model.pkl")

print("Model Ready ✔")