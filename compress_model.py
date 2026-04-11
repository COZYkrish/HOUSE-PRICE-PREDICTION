import joblib
import os

model_path = 'house_price_model.pkl'

print(f"Original size: {os.path.getsize(model_path) / (1024 * 1024):.2f} MB")

# Load and re-dump with compression
model = joblib.load(model_path)
joblib.dump(model, model_path, compress=3)

print(f"Compressed size: {os.path.getsize(model_path) / (1024 * 1024):.2f} MB")
