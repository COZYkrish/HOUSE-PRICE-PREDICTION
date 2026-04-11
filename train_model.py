# ============================================================
# House Price Prediction - Random Forest Model Training
# ============================================================

import pandas as pd
import numpy as np
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

print("=" * 60)
print("  House Price Prediction - Random Forest Model")
print("=" * 60)

# STEP 1: Load Dataset
CSV_PATH = r"D:\Downloads D\House Price India.csv"
print(f"\n📂 Loading dataset from: {CSV_PATH}")
df = pd.read_csv(CSV_PATH)
print(f"✅ Dataset loaded! Shape: {df.shape}")

# STEP 2: Preprocessing
print("\n🔧 Preprocessing...")
df = df.drop(columns=["id", "Date"])
df = df.dropna()
print(f"   Shape after cleaning: {df.shape}")

X = df.drop(columns=["Price"])
y = df["Price"]
print(f"   Features: {X.shape[1]} | Target: Price")

# STEP 3: Train/Test Split (80/20)
print("\n✂️  Splitting 80/20...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"   Train: {X_train.shape[0]} | Test: {X_test.shape[0]}")

# STEP 4: Linear Regression (Baseline)
print("\n📐 Training Linear Regression (baseline)...")
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
lr_pred = lr_model.predict(X_test)
lr_mae  = mean_absolute_error(y_test, lr_pred)
lr_rmse = np.sqrt(mean_squared_error(y_test, lr_pred))
lr_r2   = r2_score(y_test, lr_pred)
print(f"   MAE={lr_mae:,.0f}  RMSE={lr_rmse:,.0f}  R²={lr_r2:.4f}")

# STEP 5: Random Forest (Main Model)
print("\n🌳 Training Random Forest (100 trees)...")
rf_model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)
rf_mae  = mean_absolute_error(y_test, rf_pred)
rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))
rf_r2   = r2_score(y_test, rf_pred)
print(f"   MAE={rf_mae:,.0f}  RMSE={rf_rmse:,.0f}  R²={rf_r2:.4f}")

# STEP 6: Comparison
print("\n" + "=" * 55)
print(f"{'Metric':<15} {'Linear Reg':>18} {'Random Forest':>18}")
print("-" * 55)
print(f"{'MAE':<15} {lr_mae:>18,.2f} {rf_mae:>18,.2f}")
print(f"{'RMSE':<15} {lr_rmse:>18,.2f} {rf_rmse:>18,.2f}")
print(f"{'R²':<15} {lr_r2:>18.4f} {rf_r2:>18.4f}")
print("=" * 55)
print(f"🌳 RF improved R² by {((rf_r2-lr_r2)/max(abs(lr_r2),0.001))*100:.1f}%")

# STEP 7: Feature Importance
print("\n🔍 Top 10 Features (Random Forest):")
fi = pd.Series(rf_model.feature_importances_, index=X.columns).sort_values(ascending=False)
for i,(f,v) in enumerate(fi.head(10).items(),1):
    print(f"   {i:2}. {f:<42} {v:.4f}")

# STEP 8: Save Model
MODEL_FILE = "house_price_model.pkl"
joblib.dump(rf_model, MODEL_FILE)
print(f"\n💾 Model saved to '{MODEL_FILE}'")

# STEP 9: Sample Prediction
sample = X_test.iloc[[0]]
actual = y_test.iloc[0]
pred_rf = rf_model.predict(sample)[0]
pred_lr = lr_model.predict(sample)[0]
print(f"\n🏠 Sample Prediction:")
print(f"   Actual : ₹ {actual:,.2f}")
print(f"   RF     : ₹ {pred_rf:,.2f}  (err: ₹ {abs(actual-pred_rf):,.2f})")
print(f"   LR     : ₹ {pred_lr:,.2f}  (err: ₹ {abs(actual-pred_lr):,.2f})")
print("\n✅ Done! Run: python app.py → open http://localhost:5000\n")
