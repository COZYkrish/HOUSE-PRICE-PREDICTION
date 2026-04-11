# 🏠 House Price Predictor — India

A beginner-friendly Machine Learning web app that predicts house prices
using **Linear Regression** and a **Flask** web interface.

---

## 📁 Project Structure

```
house_price_prediction/
├── train_model.py          ← Step 1: Train & save the ML model
├── app.py                  ← Step 2: Flask web server
├── house_price_model.pkl   ← Auto-generated after training
├── requirements.txt        ← Python dependencies
├── templates/
│   └── index.html          ← Frontend UI
└── static/
    ├── style.css           ← Styling
    └── script.js           ← JS logic (fetch API)
```

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train the Model
```bash
python train_model.py
```
> Update the `CSV_PATH` in `train_model.py` to point to your dataset.
> Default: `D:\Downloads D\House Price India.csv`

You'll see output like:
```
✅ Dataset loaded! Shape: (21613, 23)
✅ Model trained successfully!
   MAE  : 123,456.78
   RMSE : 234,567.89
   R²   : 0.6812 (68.12%)
✅ Model saved to house_price_model.pkl
```

### 3. Start the Web App
```bash
python app.py
```

### 4. Open in Browser
```
http://localhost:5000
```

---

## 🧠 How It Works

| Step | What Happens |
|------|-------------|
| 1 | Load CSV → Drop `id`, `Date` → Handle NaN |
| 2 | Split 80/20 train/test |
| 3 | Train `LinearRegression` from scikit-learn |
| 4 | Evaluate: MAE, RMSE, R² |
| 5 | Save model with `joblib` |
| 6 | Flask serves predictions via `/predict` API |
| 7 | HTML form → JS fetch → Result displayed |

---

## 📊 Features Used (20 total)

- Number of bedrooms / bathrooms / floors
- Living area, lot area, basement area
- Waterfront, views, condition, grade
- Built year, renovation year
- Postal code, latitude, longitude
- Renovated areas, schools nearby, airport distance

---

## ⚙️ Tech Stack

- **Python** — Core language
- **pandas** — Data loading and preprocessing
- **scikit-learn** — Linear Regression model
- **joblib** — Model saving/loading
- **Flask** — Web server / REST API
- **HTML + CSS + JS** — Frontend interface

---

*Built for learning purposes. No deep learning, no complex pipelines.*
