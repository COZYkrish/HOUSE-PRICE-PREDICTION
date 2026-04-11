# ============================================================
# House Price Prediction - Flask Web App (Random Forest)
# ============================================================

import os
import joblib
import numpy as np
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

MODEL_PATH = "house_price_model.pkl"
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
    print("✅ Random Forest model loaded!")
else:
    model = None
    print("⚠️  Model not found. Run train_model.py first.")

# City → (Postal Code, Latitude, Longitude) mapping
CITY_MAP = {
    "Gurugram Sector 1":   (122001, 28.4595, 77.0266),
    "Gurugram Sector 5":   (122005, 28.4701, 77.0300),
    "Gurugram Sector 14":  (122014, 28.4680, 77.0200),
    "Gurugram Sector 23":  (122023, 28.4750, 77.0100),
    "Gurugram Sector 31":  (122031, 28.4500, 77.0350),
    "Gurugram Sector 40":  (122040, 28.4400, 77.0400),
    "Gurugram Sector 50":  (122050, 28.4300, 77.0450),
    "Gurugram Sector 57":  (122057, 28.4200, 77.0500),
    "Gurugram DLF Phase 1":(122002, 28.4725, 77.0935),
    "Gurugram DLF Phase 2":(122010, 28.4630, 77.0840),
    "Gurugram DLF Phase 3":(122010, 28.4600, 77.0900),
    "Gurugram DLF Phase 4":(122009, 28.4700, 77.0800),
    "Gurugram DLF Phase 5":(122009, 28.4680, 77.0860),
    "Gurugram Sohna Road": (122018, 28.4200, 77.0400),
    "Gurugram Golf Course":(122002, 28.4550, 77.1000),
    "Faridabad":           (121001, 28.4089, 77.3178),
    "Faridabad Sector 15": (121007, 28.4200, 77.3000),
    "Noida Sector 18":     (201301, 28.5672, 77.3210),
    "Noida Sector 62":     (201307, 28.6280, 77.3720),
    "Greater Noida":       (201308, 28.4744, 77.5040),
    "Delhi Dwarka":        (110075, 28.5921, 77.0460),
    "Delhi Rohini":        (110085, 28.7180, 77.1100),
    "Delhi Vasant Kunj":   (110070, 28.5200, 77.1580),
    "Delhi Saket":         (110017, 28.5245, 77.2066),
    "Delhi Lajpat Nagar":  (110024, 28.5677, 77.2433),
    "Manesar":             (122051, 28.3600, 76.9380),
    "Sohna":               (122103, 28.2458, 77.0700),
    "Rewari":              (123401, 28.1986, 76.6185),
    "Bhiwadi":             (301019, 28.2000, 76.8500),
    "Ballabhgarh":         (121004, 28.3400, 77.3200),
}

@app.route("/")
def home():
    cities = sorted(CITY_MAP.keys())
    return render_template("index.html", cities=cities)

@app.route("/city-info/<city_name>")
def city_info(city_name):
    if city_name in CITY_MAP:
        pc, lat, lon = CITY_MAP[city_name]
        return jsonify({"postal_code": pc, "latitude": lat, "longitude": lon})
    return jsonify({"error": "City not found"}), 404

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded. Run train_model.py first."}), 500
    try:
        data = request.get_json()
        features = [
            float(data["bedrooms"]),
            float(data["bathrooms"]),
            float(data["living_area"]),
            float(data["lot_area"]),
            float(data["floors"]),
            float(data["waterfront"]),
            float(data["views"]),
            float(data["condition"]),
            float(data["grade"]),
            float(data["area_excl_basement"]),
            float(data["basement_area"]),
            float(data["built_year"]),
            float(data["renovation_year"]),
            float(data["postal_code"]),
            float(data["latitude"]),
            float(data["longitude"]),
            float(data["living_area_renov"]),
            float(data["lot_area_renov"]),
            float(data["schools_nearby"]),
            float(data["airport_distance"]),
        ]
        arr = np.array(features).reshape(1, -1)
        price = model.predict(arr)[0]
        return jsonify({
            "predicted_price": round(float(price), 2),
            "formatted_price": f"₹ {round(float(price), 2):,.2f}"
        })
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
