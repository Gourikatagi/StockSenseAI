import sys, re

file_path = r'c:\Users\hp\Desktop\StockSense AI\files\app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add new imports
if 'import xgboost as xgb' not in text:
    import_block = "from sklearn.metrics import mean_absolute_error, r2_score\nimport xgboost as xgb\nfrom sklearn.metrics import root_mean_squared_error\n"
    text = text.replace('from sklearn.metrics import mean_absolute_error, r2_score\n', import_block)

# Replace build_features
build_features_old = '''def build_features(df: pd.DataFrame, product_id: str) -> pd.DataFrame:
    """Build ML feature set for one product."""
    pf = df[df["product_id"] == product_id].sort_values("date").copy()
    pf["lag1"]  = pf["units_sold"].shift(1)
    pf["lag2"]  = pf["units_sold"].shift(2)
    pf["lag3"]  = pf["units_sold"].shift(3)
    pf["ma3"]   = pf["units_sold"].rolling(3).mean()
    pf["ma6"]   = pf["units_sold"].rolling(6).mean()
    pf = pf.dropna()
    return pf'''

build_features_new = '''def build_features(df: pd.DataFrame, product_id: str) -> pd.DataFrame:
    """Build ML feature set for one product (Daily Data)."""
    # Group by date to handle multiple warehouse entries summing up for one product
    pf = df[df["product_id"] == product_id].groupby("date")["units_sold"].sum().reset_index()
    pf = pf.sort_values("date").copy()
    pf["day_of_week"] = pf["date"].dt.dayofweek
    pf["month"]       = pf["date"].dt.month
    pf["lag1"]  = pf["units_sold"].shift(1)
    pf["lag7"]  = pf["units_sold"].shift(7)
    pf["lag30"] = pf["units_sold"].shift(30)
    pf["ma7"]   = pf["units_sold"].rolling(7).mean()
    pf["ma30"]  = pf["units_sold"].rolling(30).mean()
    pf = pf.dropna()
    return pf'''

text = text.replace(build_features_old, build_features_new)

# Replace train_models
target_train_old = '''def train_models(df: pd.DataFrame, product_id: str):'''
end_train_idx = text.find('def abc_analysis', text.find(target_train_old))
train_block_old = text[text.find(target_train_old):end_train_idx]

train_block_new = '''def train_models(df: pd.DataFrame, product_id: str):
    """Train XGBoost, RF, LR. Return predictions, metrics, and best model."""
    pf = build_features(df, product_id)
    if len(pf) < 35:
        return None

    features = ["day_of_week", "month", "lag1", "lag7", "lag30", "ma7", "ma30"]
    X = pf[features]
    y = pf["units_sold"]

    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, shuffle=False)

    models = {
        "XGBoost": xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42),
        "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
        "Linear Regression": LinearRegression()
    }
    
    results = {}
    best_mae = float("inf")
    best_name = ""
    best_model = None
    
    for name, model in models.items():
        model.fit(X_tr, y_tr)
        preds = model.predict(X_te)
        mae = mean_absolute_error(y_te, preds)
        rmse = float(np.sqrt(np.mean((y_te - preds)**2)))
        r2 = max(0, r2_score(y_te, preds))
        acc = max(0, 100 - (mae / (y_te.mean()+1e-9) * 100))
        results[name] = {"mae": mae, "rmse": rmse, "r2": r2, "acc": acc, "model": model}
        if mae < best_mae:
            best_mae = mae
            best_name = name
            best_model = model

    # Multi-horizon forecast (7, 30, 90 days)
    future_preds = []
    current_features = pf.iloc[-1].copy()
    history = list(pf["units_sold"].values)
    
    last_date = pf["date"].iloc[-1]
    
    for step in range(1, 91): # 90 days
        pred_date = last_date + datetime.timedelta(days=step)
        
        row = {
            "day_of_week": pred_date.weekday(),
            "month": pred_date.month,
            "lag1": history[-1],
            "lag7": history[-7],
            "lag30": history[-30],
            "ma7": sum(history[-7:])/7,
            "ma30": sum(history[-30:])/30,
        }
        
        pred_val = float(best_model.predict(pd.DataFrame([row]))[0])
        pred_val = max(0, round(pred_val))
        history.append(pred_val)
        future_preds.append({"date": pred_date, "predicted_demand": pred_val})

    df_future = pd.DataFrame(future_preds)
    
    # 7, 30, 90 day aggregates
    agg_7 = df_future.iloc[:7]["predicted_demand"].sum()
    agg_30 = df_future.iloc[:30]["predicted_demand"].sum()
    agg_90 = df_future["predicted_demand"].sum()

    return {
        "pf": pf,
        "best_model": best_name,
        "results": results,
        "mae": results[best_name]["mae"],
        "rmse": results[best_name]["rmse"],
        "acc": results[best_name]["acc"],
        "r2": results[best_name]["r2"],
        "future": df_future,
        "agg_7": agg_7,
        "agg_30": agg_30,
        "agg_90": agg_90
    }

'''

text = text.replace(train_block_old, train_block_new)

# Additionally, let's fix the tab rendering for "Time-Series Forecasting" to display these new models.
# The Time-Series Forecast tab code needs to handle daily outputs and accuracy %.
# Wait, I'll write another script for UI changes later.

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Advanced XGBoost Models and 7/30/90 Day Horizon logic safely injected.")
