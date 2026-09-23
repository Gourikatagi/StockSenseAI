# ============================================================
#  StockSense AI – Smart Inventory Demand Forecasting System
#  Full working app — Streamlit + Scikit-learn + Plotly
# ============================================================

import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import datetime
import random

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score
try:
    import xgboost as xgb
except ImportError:
    xgb = None
from sklearn.metrics import root_mean_squared_error
from sklearn.model_selection import train_test_split

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="StockSense AI",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL CSS  (dark glassmorphism theme)
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;700&display=swap');

/* ── Root vars ── */
:root {
    --bg:        #050810;
    --surface:   #0f1423;
    --card:      rgba(20, 25, 40, 0.6);
    --border:    rgba(140, 160, 255, 0.15);
    --accent:    #3b82f6;
    --accent-glow: rgba(59, 130, 246, 0.4);
    --accent2:   #8b5cf6;
    --green:     #10b981;
    --red:       #ef4444;
    --yellow:    #f59e0b;
    --text:      #f3f4f6;
    --muted:     #9ca3af;
}

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: radial-gradient(circle at top right, #10162a 0%, #050810 100%) !important;
    background-attachment: fixed !important;
    color: var(--text) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(10, 15, 25, 0.8) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── Main area ── */
.main .block-container { padding: 1.5rem 2rem 3rem 2rem; }

/* ── Headings ── */
h1,h2,h3 { font-family:'Outfit', sans-serif; font-weight:700; letter-spacing: -0.02em; }
h1 { font-size:2.5rem; background:linear-gradient(135deg, #60a5fa, #c084fc);
     -webkit-background-clip:text; -webkit-text-fill-color:transparent; 
     text-shadow: 0 4px 20px rgba(96, 165, 250, 0.2); margin-bottom: 0.5rem; }

/* ── KPI cards ── */
.kpi-card {
    background: linear-gradient(145deg, rgba(30, 40, 60, 0.5), rgba(15, 20, 35, 0.5));
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 1.5rem 1.5rem;
    backdrop-filter: blur(16px);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.kpi-card:hover { 
    transform: translateY(-5px) scale(1.02); 
    box-shadow: 0 12px 40px rgba(96, 165, 250, 0.15); 
    border-color: rgba(140, 160, 255, 0.3);
}
.kpi-label { font-size:0.85rem; text-transform:uppercase; letter-spacing:0.08em; color:var(--muted); margin-bottom:0.4rem; font-weight: 600; }
.kpi-value { font-size:2.2rem; font-weight:700; font-family:'Outfit', sans-serif; line-height: 1.1; }
.kpi-sub   { font-size:0.8rem; color:var(--muted); margin-top:0.4rem; font-weight: 500; }
.kpi-green { color:var(--green); text-shadow: 0 0 10px rgba(16, 185, 129, 0.3); }
.kpi-red   { color:var(--red); text-shadow: 0 0 10px rgba(239, 68, 68, 0.3); }
.kpi-blue  { color:var(--accent); text-shadow: 0 0 10px var(--accent-glow); }
.kpi-yellow{ color:var(--yellow); text-shadow: 0 0 10px rgba(245, 158, 11, 0.3); }

/* ── Section cards ── */
.section-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 1.75rem;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(16px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    transition: transform 0.3s ease;
}
.section-card:hover { border-color: rgba(140, 160, 255, 0.25); }
.section-title { font-family:'Outfit', sans-serif; font-size:1.15rem; font-weight:600; color:var(--accent); margin-bottom:1.2rem; }

/* ── Badges ── */
.badge { display:inline-block; border-radius:999px; padding:0.25rem 0.8rem; font-size:0.75rem; font-weight:600; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
.badge-green  { background:rgba(16,185,129,0.15); color:var(--green); border:1px solid rgba(16,185,129,0.4); }
.badge-red    { background:rgba(239,68,68,0.15); color:var(--red);   border:1px solid rgba(239,68,68,0.4); }
.badge-yellow { background:rgba(245,158,11,0.15);  color:var(--yellow);border:1px solid rgba(245,158,11,0.4); }
.badge-blue   { background:rgba(59,130,246,0.15);  color:var(--accent);border:1px solid rgba(59,130,246,0.4); }

/* ── Alert boxes ── */
.alert-red    { background:linear-gradient(90deg, rgba(239,68,68,0.1), transparent); border-left:4px solid var(--red); border-radius:10px; padding:1rem; margin:0.5rem 0; font-size:0.9rem; }
.alert-yellow { background:linear-gradient(90deg, rgba(245,158,11,0.1), transparent);  border-left:4px solid var(--yellow); border-radius:10px; padding:1rem; margin:0.5rem 0; font-size:0.9rem; }
.alert-green  { background:linear-gradient(90deg, rgba(16,185,129,0.1), transparent);  border-left:4px solid var(--green); border-radius:10px; padding:1rem; margin:0.5rem 0; font-size:0.9rem; }

/* ── Insight box ── */
.insight-box { background:linear-gradient(135deg,rgba(59,130,246,0.1),rgba(139,92,246,0.1)); border:1px solid rgba(59,130,246,0.3); border-radius:14px; padding:1.1rem 1.4rem; margin:0.6rem 0; font-size:0.9rem; box-shadow: 0 4px 15px rgba(59,130,246,0.05); }

/* ── Chat bubble ── */
.chat-user { background:linear-gradient(135deg, rgba(59,130,246,0.2), rgba(59,130,246,0.1)); border-radius:16px 16px 4px 16px; padding:0.8rem 1.2rem; margin:0.5rem 0; font-size:0.9rem; text-align:right; border: 1px solid rgba(59,130,246,0.2); }
.chat-bot  { background:rgba(255,255,255,0.08); border-radius:16px 16px 16px 4px; padding:0.8rem 1.2rem; margin:0.5rem 0; font-size:0.9rem; border: 1px solid rgba(255,255,255,0.05); }

/* ── Score ring placeholder ── */
.score-ring { display:flex; align-items:center; justify-content:center; width:120px; height:120px; border-radius:50%; background:conic-gradient(var(--accent) var(--pct), rgba(255,255,255,0.05) 0); font-size:1.8rem; font-weight:700; font-family:'Outfit',sans-serif; box-shadow: inset 0 0 20px rgba(0,0,0,0.5); }

/* ── Streamlit overrides ── */
.stSelectbox>div>div, .stMultiSelect>div>div { background: rgba(15,20,35,0.8) !important; border-color:var(--border) !important; border-radius: 10px !important; }
.stTextInput>div>div>input { background: rgba(15,20,35,0.8) !important; border-color:var(--border) !important; color:var(--text) !important; border-radius: 10px !important; }
div[data-testid="stMetricValue"] { color:var(--accent) !important; font-family: 'Outfit', sans-serif !important; }
.stTabs [data-baseweb="tab-list"] { background:transparent !important; gap:.5rem; }
.stTabs [data-baseweb="tab"] { background: rgba(255,255,255,0.05) !important; border-radius:10px !important; border:1px solid var(--border) !important; color:var(--muted) !important; transition: all 0.3s ease !important; }
.stTabs [aria-selected="true"] { background:rgba(59,130,246,0.2) !important; color:var(--text) !important; border-color: rgba(59,130,246,0.5) !important; }
hr { border-color:var(--border) !important; opacity: 0.5; }
.stButton>button { border-radius: 10px !important; transition: all 0.3s ease !important; }
.stButton>button:hover { transform: translateY(-2px) !important; box-shadow: 0 4px 15px rgba(59,130,246,0.3) !important; border-color: var(--accent) !important; color: var(--accent) !important; }

/* ── Pro Sidebar Navigation (Hiding Radios) ── */
section[data-testid="stSidebar"] div[role="radiogroup"] > label {
    padding: 0.6rem 1rem !important;
    border-radius: 12px !important;
    margin-bottom: 0.4rem !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
    background: transparent !important;
    width: 100% !important;
}
section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
    background: rgba(255, 255, 255, 0.05) !important;
    transform: translateX(4px);
}
section[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child {
    display: none !important; /* Hides the native radio circle */
}
section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {
    background: linear-gradient(90deg, rgba(59,130,246,0.25) 0%, rgba(59,130,246,0.05) 100%) !important;
    border-left: 4px solid var(--accent) !important;
    border-radius: 4px 12px 12px 4px !important;
}
section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) p {
    font-weight: 700 !important;
    color: var(--accent) !important;
}

/* ── Pro File Uploader ── */
section[data-testid="stSidebar"] [data-testid="stFileUploadDropzone"] {
    background: rgba(15, 20, 35, 0.4) !important;
    border: 1px dashed rgba(140, 160, 255, 0.3) !important;
    border-radius: 16px !important;
    padding: 1rem !important;
    transition: all 0.2s ease !important;
}
section[data-testid="stSidebar"] [data-testid="stFileUploadDropzone"]:hover {
    background: rgba(59, 130, 246, 0.1) !important;
    border-color: rgba(59, 130, 246, 0.6) !important;
}
/* ── Pro native containers layout (st.container) ── */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(15, 20, 35, 0.7) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 1.5rem 1rem !important;
    margin-bottom: 1.5rem !important;
}
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════
#  HELPERS / UTILITIES
# ════════════════════════════════════════════

def plotly_dark_layout(fig, height=380):
    """Apply a consistent dark transparent layout to every Plotly chart."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#e2e8f0", size=12),
        height=height,
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.1)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.1)"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
    )
    return fig


@st.cache_data(show_spinner=False)
def load_sample_data():
    """Generate mock enterprise daily data for 2025 with warehouses/suppliers."""
    try:
        df = pd.read_csv("sample_inventory.csv", parse_dates=["date"])
        if "warehouse" in df.columns: # Verify it is new
            return df
    except FileNotFoundError:
        pass

    products = [
        ("P001","Wireless Earbuds","Electronics",29.99),
        ("P002","Running Shoes","Footwear",89.99),
        ("P003","Protein Powder","Health",49.99),
        ("P004","Coffee Maker","Kitchen",129.99),
        ("P005","Yoga Mat","Sports",34.99),
        ("P006","Notebook Set","Stationery",12.99),
        ("P007","Bluetooth Speaker","Electronics",59.99),
        ("P008","Water Bottle","Sports",19.99),
        ("P009","Face Cream","Beauty",24.99),
        ("P010","LED Desk Lamp","Home",44.99),
    ]
    warehouses = ["WH-New York", "WH-Los Angeles", "WH-Chicago"]
    suppliers = [
        ("PrimeLogistics", 2, 95), 
        ("FastTrack Global", 4, 88), 
        ("ValueSupply Co", 8, 70)
    ]
    
    rows = []
    rng = np.random.default_rng(42)
    start_date = datetime.date(2025, 1, 1)
    
    for day in range(365):
        date = start_date + datetime.timedelta(days=day)
        
        # Holiday Spikes
        is_black_friday = (date.month == 11 and 20 <= date.day <= 30)
        is_christmas = (date.month == 12 and 15 <= date.day <= 25)
        is_diwali = (date.month == 10 and 15 <= date.day <= 25) # Approx
        
        spike_multiplier = 1.0
        if is_black_friday: spike_multiplier = 3.5
        elif is_christmas: spike_multiplier = 2.8
        elif is_diwali: spike_multiplier = 2.5
        
        for pid, name, cat, price in products:
            for wh in warehouses:
                base = {"Electronics":15,"Footwear":12,"Health":20,"Kitchen":8,
                        "Sports":15,"Stationery":25,"Beauty":18,"Home":10}.get(cat, 10)
                
                # Assign a primary supplier pseudo-randomly based on product
                supplier_idx = (int(pid[-1]) + len(wh)) % 3
                sup_name, lead, rel = suppliers[supplier_idx]
                unit_cost = price * rng.uniform(0.3, 0.6) # Cost is 30-60% of price
                
                seasonal = 1 + 0.3 * np.sin((date.month - 3) * np.pi / 6)
                weekend_boost = 1.3 if date.weekday() >= 5 else 1.0
                
                sold = int(max(0, rng.normal(base * seasonal * weekend_boost * spike_multiplier, base*0.2)))
                # Stock gradually depletes and spikes up
                stock = max(0, int(150 + 50*np.sin(day/10) + rng.integers(-20, 20)))
                
                # Inject lost sales tracking implicitly because if stock=0 we lost sales
                rows.append([date, pid, name, cat, wh, sup_name, lead, rel, sold, stock, price, unit_cost])

    df = pd.DataFrame(rows, columns=[
        "date","product_id","product_name","category",
        "warehouse","supplier","lead_time_days","supplier_reliability",
        "units_sold","current_stock","price","unit_cost"
    ])
    return df


def clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, list]:
    """Clean data and return (cleaned_df, list_of_steps)."""
    steps = []
    orig_rows = len(df)
    df = df.copy()

    # Ensure date column
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Drop full-duplicate rows
    dups = df.duplicated().sum()
    if dups:
        df = df.drop_duplicates()
        steps.append(f"✅ Removed {dups} duplicate rows")

    # Fill numeric NaN with median
    num_cols = df.select_dtypes(include=np.number).columns
    filled = 0
    for c in num_cols:
        n = df[c].isna().sum()
        if n:
            df[c] = df[c].fillna(df[c].median())
            filled += n
    if filled:
        steps.append(f"✅ Imputed {filled} missing numeric values with column medians")

    # Fill string NaN with 'Unknown'
    str_cols = df.select_dtypes(include="object").columns
    for c in str_cols:
        n = df[c].isna().sum()
        if n:
            df[c] = df[c].fillna("Unknown")
            steps.append(f"✅ Filled {n} missing text values in '{c}' with 'Unknown'")

    # Clip negatives in units_sold / current_stock
    for col in ["units_sold", "current_stock"]:
        if col in df.columns:
            neg = (df[col] < 0).sum()
            if neg:
                df[col] = df[col].clip(lower=0)
                steps.append(f"✅ Clipped {neg} negative values in '{col}' to 0")

    if not steps:
        steps.append("✅ Data is already clean — no issues found")

    final_rows = len(df)
    if orig_rows != final_rows:
        steps.append(f"ℹ️ Dataset size: {orig_rows} → {final_rows} rows")

    # Add time features
    if "date" in df.columns:
        df["month"]      = df["date"].dt.month
        df["quarter"]    = df["date"].dt.quarter
        df["year"]       = df["date"].dt.year
        df["month_name"] = df["date"].dt.strftime("%b")

    return df, steps


def build_features(df: pd.DataFrame, product_id: str) -> pd.DataFrame:
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
    return pf


def train_models(df: pd.DataFrame, product_id: str):
    """Train XGBoost, RF, LR. Return predictions, metrics, and best model."""
    pf = build_features(df, product_id)
    if len(pf) < 35:
        return None

    features = ["day_of_week", "month", "lag1", "lag7", "lag30", "ma7", "ma30"]
    X = pf[features]
    y = pf["units_sold"]

    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, shuffle=False)

    models = {
        "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
        "Linear Regression": LinearRegression()
    }
    if xgb is not None:
        models["XGBoost"] = xgb.XGBRegressor(
            n_estimators=100, learning_rate=0.1, random_state=42
        )
    
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

def abc_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Return product-level ABC classification."""
    summary = (df.groupby(["product_id","product_name"])
                 .agg(total_revenue=("units_sold", lambda x: (x * df.loc[x.index,"price"]).sum()),
                      total_sold=("units_sold","sum"))
                 .reset_index()
                 .sort_values("total_revenue", ascending=False))
    summary["cum_pct"] = summary["total_revenue"].cumsum() / summary["total_revenue"].sum() * 100
    summary["ABC"] = summary["cum_pct"].apply(
        lambda x: "A – High Value" if x <= 70
        else ("B – Medium Value" if x <= 90 else "C – Low Value"))
    return summary


def inventory_health_score(df: pd.DataFrame) -> dict:
    """Compute 0-100 health score and sub-scores."""
    latest = df.sort_values("date").groupby("product_id").last().reset_index()

    # Stockout risk: products with stock < 30-day avg demand
    avg_demand = df.groupby("product_id")["units_sold"].mean()
    merged = latest.set_index("product_id").join(avg_demand.rename("avg_demand"))
    merged["days_cover"] = merged["current_stock"] / merged["avg_demand"].replace(0, 1)

    stockout_risk = (merged["days_cover"] < 1).sum() / len(merged) * 100
    overstock_pct = (merged["days_cover"] > 6).sum()  / len(merged) * 100
    dead_stock_pct= (merged["days_cover"] > 12).sum() / len(merged) * 100

    fill_score    = max(0, 100 - stockout_risk * 2)
    overstock_pen = overstock_pct * 0.5
    dead_pen      = dead_stock_pct * 1.0
    health        = max(0, min(100, fill_score - overstock_pen - dead_pen))

    return {
        "score": round(health),
        "stockout_risk_pct": round(stockout_risk, 1),
        "overstock_pct":     round(overstock_pct, 1),
        "dead_stock_pct":    round(dead_stock_pct, 1),
        "days_cover":        merged["days_cover"].round(1),
        "merged":            merged.reset_index(),
    }


def chatbot_response(query: str, df: pd.DataFrame) -> str:
    """Rule-based inventory chatbot."""
    q = query.lower().strip()
    latest = df.sort_values("date").groupby(["product_id","product_name"]).last().reset_index()

    if any(k in q for k in ["products", "product", "items", "what do i have", "things i have", "sell", "inventory list", "what are the"]):
        total_types = df["product_name"].nunique()
        cats = ", ".join(df["category"].dropna().unique())
        return (f"🛒 You currently sell **{total_types} unique products** across categories like: *{cats}*.\n\n"
                 "To see the full detailed list of every single product you have intuitively organized, navigate to your **Executive Dashboard** or **Business Summary** tab!")

    if any(k in q for k in ["stockout","out of stock","low stock","running low"]):
        avg_d = df.groupby("product_id")["units_sold"].mean()
        merged = latest.set_index("product_id").join(avg_d.rename("avg"))
        risky = merged[merged["current_stock"] < merged["avg"]]["product_name"].tolist()
        if risky:
            return (f"⚠️ **{len(risky)} products** are at stockout risk: "
                    + ", ".join(risky[:5])
                    + (f" (+{len(risky)-5} more)" if len(risky) > 5 else "")
                    + ". Consider reordering immediately.")
        return "✅ No immediate stockout risks detected — inventory looks healthy!"

    if any(k in q for k in ["overstock","excess","too much"]):
        avg_d = df.groupby("product_id")["units_sold"].mean()
        merged = latest.set_index("product_id").join(avg_d.rename("avg"))
        over = merged[merged["current_stock"] > merged["avg"] * 6]["product_name"].tolist()
        if over:
            return (f"📦 **{len(over)} products** are overstocked: "
                    + ", ".join(over[:5])
                    + ". Consider promotions or redistribution.")
        return "✅ No major overstock issues detected."

    if any(k in q for k in ["best seller","top product","most sold","bestseller"]):
        top = df.groupby("product_name")["units_sold"].sum().nlargest(3)
        lines = [f"{i+1}. {n} ({int(v)} units)" for i,(n,v) in enumerate(top.items())]
        return "🏆 **Top 3 best-sellers:**\n" + "\n".join(lines)

    if any(k in q for k in ["revenue","profit","earnings","sales value"]):
        df2 = df.copy()
        df2["revenue"] = df2["units_sold"] * df2["price"]
        top = df2.groupby("product_name")["revenue"].sum().nlargest(3)
        lines = [f"{i+1}. {n} (¥{v:,.0f})" for i,(n,v) in enumerate(top.items())]
        return "💰 **Top 3 revenue generators:**\n" + "\n".join(lines)

    if any(k in q for k in ["reorder","purchase","buy more","order"]):
        avg_d = df.groupby("product_id")["units_sold"].mean()
        merged = latest.set_index("product_id").join(avg_d.rename("avg"))
        merged["reorder_qty"] = ((merged["avg"] * 3) - merged["current_stock"]).clip(lower=0).round()
        need = merged[merged["reorder_qty"] > 0][["product_name","reorder_qty"]]
        if need.empty:
            return "✅ All products have sufficient stock — no reorders needed right now."
        lines = [f"• {row['product_name']}: reorder **{int(row['reorder_qty'])} units**"
                 for _, row in need.iterrows()]
        return "🛒 **Suggested reorders:**\n" + "\n".join(lines[:6])

    if any(k in q for k in ["category","segment","type"]):
        cat_sales = df.groupby("category")["units_sold"].sum().sort_values(ascending=False)
        lines = [f"{c}: {int(v)} units" for c, v in cat_sales.items()]
        return "📊 **Sales by category:**\n" + "\n".join(lines)

    if any(k in q for k in ["dead stock","dead","not selling","slow"]):
        avg_d = df.groupby("product_id")["units_sold"].mean()
        merged = latest.set_index("product_id").join(avg_d.rename("avg"))
        dead = merged[(merged["current_stock"] > 0) & (merged["avg"] < 5)]["product_name"].tolist()
        if dead:
            return ("🪦 **Possible dead/slow-moving stock:** "
                    + ", ".join(dead)
                    + ". Consider clearance pricing.")
        return "✅ No dead-stock issues found."

    if any(k in q for k in ["health","score","status"]):
        h = inventory_health_score(df)
        return (f"🏥 **Inventory Health Score: {h['score']}/100**\n"
                f"• Stockout risk: {h['stockout_risk_pct']}% of products\n"
                f"• Overstock: {h['overstock_pct']}% of products\n"
                f"• Dead stock: {h['dead_stock_pct']}% of products")

    if any(k in q for k in ["hello","hi","hey","help","what can","what do"]):
        return ("👋 Hi! I'm **StockSense AI** — your inventory assistant.\n\n"
                "Try asking me:\n"
                "• *Which products are at stockout risk?*\n"
                "• *Show me best sellers*\n"
                "• *What should I reorder?*\n"
                "• *Any overstock issues?*\n"
                "• *What's the inventory health score?*")

    if any(k in q for k in ["least", "worst", "lowest", "bad"]):
        bottom = df.groupby("product_name")["units_sold"].sum().nsmallest(3)
        lines = [f"{i+1}. {n} ({int(v)} units)" for i,(n,v) in enumerate(bottom.items())]
        return "📉 **Bottom 3 lowest-sellers:**\n" + "\n".join(lines)

    rev = (df['units_sold'] * df['price']).sum()
    h = inventory_health_score(df)
    return ("🤔 I'm analyzing that, but here is a quick snapshot of your inventory:\n"
            f"• **Health Score:** {h['score']}/100\n"
            f"• **Total Revenue:** ${rev:,.0f}\n"
            "Try asking me specifically about *stockouts*, *best sellers*, *lowest sellers*, or *dead stock*.")



# ════════════════════════════════════════════
#  V3 ENTERPRISE LOGIC LAYER
# ════════════════════════════════════════════

def recommend_best_supplier(df: pd.DataFrame, product_name: str) -> dict:
    """Evaluate all known suppliers for this product and recommend the mathematically best one."""
    sub = df[df["product_name"] == product_name].copy()
    if sub.empty or "supplier" not in sub.columns:
        return {}
    
    # Get latest unique supplier metrics
    sups = sub.drop_duplicates(subset=["supplier"])[["supplier", "lead_time_days", "supplier_reliability", "unit_cost"]]
    
    best_score = -float("inf")
    best_sup = {}
    
    for _, row in sups.iterrows():
        # Score Logic: Reliability is good (+), Cost is bad (-), Lead time is bad (-)
        # Normalize arbitrarily for scoring
        score = (row["supplier_reliability"] * 2.0) - (row["lead_time_days"] * 5.0) - (row["unit_cost"] * 0.5)
        if score > best_score:
            best_score = score
            best_sup = {
                "name": row["supplier"],
                "cost": row["unit_cost"],
                "lead": row["lead_time_days"],
                "reliability": row["supplier_reliability"],
                "score": round(score, 1)
            }
    return best_sup


def compute_profit_loss(df: pd.DataFrame) -> dict:
    """Calculate lost revenue due to stockouts and holding costs due to overstock."""
    if "unit_cost" not in df.columns:
        return {}
        
    latest = df.sort_values("date").groupby(["warehouse", "product_id"]).last().reset_index()
    avg_d = df.groupby(["warehouse", "product_id"])["units_sold"].mean().reset_index(name="avg_demand")
    merged = pd.merge(latest, avg_d, on=["warehouse", "product_id"])
    
    # Financial math
    # Overstock: Anything over 30 days of average demand incurs a 1.2% daily holding cost on inventory value
    merged["excess_stock"] = (merged["current_stock"] - (merged["avg_demand"] * 30)).clip(lower=0)
    merged["holding_cost_penalty"] = merged["excess_stock"] * merged["unit_cost"] * 0.012
    
    # Stockouts: If current stock is 0, we lose avg_demand * price
    merged["stockout_loss"] = np.where(merged["current_stock"] == 0, merged["avg_demand"] * merged["price"], 0)
    
    total_loss = merged["stockout_loss"].sum()
    total_holding = merged["holding_cost_penalty"].sum()
    total_revenue = (df["units_sold"] * df["price"]).sum()
    
    return {
        "lost_revenue": total_loss,
        "holding_costs": total_holding,
        "total_revenue": total_revenue,
        "efficiency": max(0, 100 - ((total_loss + total_holding) / (total_revenue + 1e-9) * 100))
    }


def generate_po_pdf(product: str, quantity: int, supplier_data: dict) -> bytes:
    """Generate a raw HTML-based TXT/Fake-PDF Purchase Order (Streamlit compatible download)."""
    # Simply generate a rigorous text string that acts as the PO
    date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    po_text = f"""==================================================
                 OFFICIAL PURCHASE ORDER
==================================================
PO No:      PO-{np.random.randint(10000, 99999)}
Date:       {date_str}

SUPPLIER DETAILS
--------------------------------------------------
Vendor Name:      {supplier_data.get('name', 'N/A')}
Reliability:      {supplier_data.get('reliability', 'N/A')}%
Estimated Lead:   {supplier_data.get('lead', 'N/A')} Days

LINE ITEMS
--------------------------------------------------
Product:          {product}
Quantity:         {int(quantity)} Units
Est. Unit Price:  Rs. {supplier_data.get('cost', 0.0):.2f}
==================================================
TOTAL ESTIMATED COST: Rs. {(quantity * supplier_data.get('cost', 0.0)):,.2f}
==================================================
AUTHORIZED BY: StockSense Enterprise AI Copilot"""
    return po_text.encode('utf-8')

# ════════════════════════════════════════════
#  SESSION STATE
# ════════════════════════════════════════════
if "df_clean" not in st.session_state:
    st.session_state.df_clean = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "active_page" not in st.session_state:
    st.session_state.active_page = "🏠 Dashboard"


# ════════════════════════════════════════════
#  SIDEBAR
# ════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:1rem 0 .5rem'>
        <div style='font-size:2.2rem'>🛒</div>
        <div style='font-family:"Space Grotesk",sans-serif;font-size:1.25rem;
                    font-weight:700;background:linear-gradient(135deg,#4f9cf9,#a78bfa);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;'>
            StockSense AI
        </div>
        <div style='font-size:.72rem;color:#64748b;margin-top:.15rem;'>
            Smart Inventory Intelligence
        </div>
    </div>
    <hr style='margin:.5rem 0 1rem'/>
    """, unsafe_allow_html=True)

    pages = [
        "🌐 Executive Dashboard",
        "🔮 AI Demand Forecasting",
        "⚡ Real-Time Stock Alerts",
        "📊 ABC Segmentation",
        "🧠 AI Optimization Engine",
        "🤖 StockSense Copilot",
        "💼 Executive Business Summary",
    ]
    page = st.radio("Navigation", pages, key="nav",
                    label_visibility="collapsed")
    st.session_state.active_page = page

    st.markdown("<hr style='margin:1rem 0'/>", unsafe_allow_html=True)

    # ── Data upload ──────────────────────────────────────────────────────
    st.markdown("<div style='font-size:.8rem;color:#64748b;text-transform:uppercase;"
                "letter-spacing:.05em;margin-bottom:.5rem;'>Data Source</div>",
                unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload CSV", type=["csv"],
                                label_visibility="collapsed")
    use_sample = st.button("🎲 Use Sample Dataset", use_container_width=True)

    if uploaded is not None:
        raw = pd.read_csv(uploaded, parse_dates=["date"])
        cleaned, steps = clean_data(raw)
        st.session_state.df_clean = cleaned
        st.session_state.clean_steps = steps
        st.success(f"✅ Loaded {len(cleaned)} rows")
    elif use_sample:
        raw = load_sample_data()
        cleaned, steps = clean_data(raw)
        st.session_state.df_clean = cleaned
        st.session_state.clean_steps = steps
        st.success(f"✅ Sample data loaded ({len(cleaned)} rows)")

    if st.session_state.df_clean is not None:
        df = st.session_state.df_clean
        st.markdown(f"""
        <div style='margin-top:1.5rem; padding: 0.8rem; border-radius: 12px; 
                    background: rgba(59, 130, 246, 0.05); border: 1px solid rgba(59, 130, 246, 0.2);
                    font-size:.8rem; color:#9ca3af;'>
            <div style='margin-bottom: 0.3rem'>📅 <strong>{df['date'].min().strftime('%b %Y')} → {df['date'].max().strftime('%b %Y')}</strong></div>
            <div>🏷️ {df['product_id'].nunique()} products &nbsp;·&nbsp; {len(df)} records</div>
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════
#  NO DATA STATE
# ════════════════════════════════════════════
if st.session_state.df_clean is None:
    if page == "🏠 Dashboard":
        html_content = """
        <div style='text-align:center;padding:4rem 0;'>
            <div style='font-size:4rem;'>📦</div>
            <h1>Welcome to StockSense AI</h1>
            <p style='color:#9ca3af;max-width:480px;margin:.75rem auto;'>
            Upload your inventory CSV or click <strong>Use Sample Dataset</strong>
            in the sidebar to get started with real AI-powered demand forecasting.
            </p>
        </div>
        <div style='display:flex; justify-content:center; gap:2rem; max-width:800px; margin:0 auto; flex-wrap:wrap;'>
        """
        for icon, title, desc in [
            ("🔮", "Demand Forecasting", "ML-powered predictions for the next 3 months"),
            ("🔔", "Smart Alerts", "Auto low-stock & overstock warnings"),
            ("🤖", "AI Chatbot", "Ask anything about your inventory"),
        ]:
            html_content += f"""
            <div class='kpi-card' style='text-align:center; flex:1; min-width:200px; max-width:250px;'>
                <div style='font-size:2rem;'>{icon}</div>
                <div style='font-weight:600;margin:.5rem 0 .25rem;'>{title}</div>
                <div style='font-size:.8rem;color:#9ca3af;'>{desc}</div>
            </div>
            """
        html_content += "</div>"
        st.markdown(html_content, unsafe_allow_html=True)
    else:
        st.markdown(f"<h1>{page.split(' ', 1)[1] if ' ' in page else page}</h1>", unsafe_allow_html=True)
        st.warning("⚠️ **No Data Available.** Please upload an inventory CSV or click **Use Sample Dataset** in the sidebar to access this feature.")
    
    st.stop()


# ════════════════════════════════════════════
#  SHARED DATAFRAME
# ════════════════════════════════════════════
df = st.session_state.df_clean
products = sorted(df["product_id"].unique())
product_names = dict(df[["product_id","product_name"]].drop_duplicates().values)


# ════════════════════════════════════════════
#  PAGE: DASHBOARD
# ════════════════════════════════════════════
if page == "🌐 Executive Dashboard":
    st.markdown("<h1>🌐 E-Commerce Executive Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#9ca3af;margin-top:-.5rem;'>Real-time inventory intelligence powered by open-source AI</p>",
                unsafe_allow_html=True)

    # ── KPIs ─────────────────────────────────────────────────────────────
    df["revenue"] = df["units_sold"] * df["price"]
    total_rev   = df["revenue"].sum()
    total_units = df["units_sold"].sum()
    n_products  = df["product_id"].nunique()
    avg_stock   = df.groupby("product_id")["current_stock"].last().mean()
    health      = inventory_health_score(df)

    # stockout & overstock count from latest snapshot
    latest = df.sort_values("date").groupby("product_id").last().reset_index()
    avg_d  = df.groupby("product_id")["units_sold"].mean()
    merged_l = latest.set_index("product_id").join(avg_d.rename("avg_d"))
    n_stockout  = (merged_l["current_stock"] < merged_l["avg_d"]).sum()
    n_overstock = (merged_l["current_stock"] > merged_l["avg_d"] * 6).sum()

    col1, col2, col3, col4, col5 = st.columns(5)
    kpis = [
        (col1, "💰 Total Revenue",   f"Rs. {total_rev:,.0f}",   "All-time",        "kpi-blue"),
        (col2, "📦 Units Sold",      f"{total_units:,}",      "All-time",        "kpi-green"),
        (col3, "🏥 Health Score",    f"{health['score']}/100","Inventory health","kpi-green" if health['score']>=70 else "kpi-red"),
        (col4, "⚠️ Stockout Risk",   str(n_stockout),         "Products at risk", "kpi-red"),
        (col5, "📈 Overstock Items", str(n_overstock),        "Excess inventory","kpi-yellow"),
    ]
    for col, label, value, sub, cls in kpis:
        with col:
            st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-label'>{label}</div>
                <div class='kpi-value {cls}'>{value}</div>
                <div class='kpi-sub'>{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Row 2: Sales trend + Category pie ────────────────────────────────
    c1, c2 = st.columns([2, 1])

    with c1:
        with st.container(border=True):
            st.markdown("<div class='section-title'>📈 Monthly Sales Trend (All Products)</div>",
                        unsafe_allow_html=True)
            monthly = df.groupby(["date","category"])["units_sold"].sum().reset_index()
            fig = px.area(monthly, x="date", y="units_sold", color="category",
                          color_discrete_sequence=px.colors.qualitative.Vivid)
            fig = plotly_dark_layout(fig)
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        with st.container(border=True):
            st.markdown("<div class='section-title'>🏷️ Revenue by Category</div>",
                        unsafe_allow_html=True)
            cat_rev = df.groupby("category")["revenue"].sum().reset_index()
            fig2 = px.pie(cat_rev, names="category", values="revenue",
                          hole=0.55,
                          color_discrete_sequence=px.colors.qualitative.Pastel)
            fig2 = plotly_dark_layout(fig2, height=380)
            st.plotly_chart(fig2, use_container_width=True)

    # ── Row 3: Top 10 products + stock heatmap ────────────────────────────
    c3, c4 = st.columns(2)

    with c3:
        with st.container(border=True):
            st.markdown("<div class='section-title'>🏆 Top 10 Products by Units Sold</div>",
                        unsafe_allow_html=True)
            top10 = (df.groupby("product_name")["units_sold"].sum()
                       .nlargest(10).reset_index()
                       .sort_values("units_sold"))
            fig3 = px.bar(top10, x="units_sold", y="product_name", orientation="h",
                          color="units_sold",
                          color_continuous_scale=["#4f9cf9","#a78bfa"])
            fig3.update_coloraxes(showscale=False)
            fig3 = plotly_dark_layout(fig3, height=360)
            st.plotly_chart(fig3, use_container_width=True)

    with c4:
        with st.container(border=True):
            st.markdown("<div class='section-title'>🌡️ Seasonal Demand Heatmap</div>",
                        unsafe_allow_html=True)
            pivot = df.pivot_table(index="product_name", columns="month_name",
                                   values="units_sold", aggfunc="sum")
            month_order = ["Jan","Feb","Mar","Apr","May","Jun",
                           "Jul","Aug","Sep","Oct","Nov","Dec"]
            pivot = pivot.reindex(columns=[m for m in month_order if m in pivot.columns])
            fig4 = go.Figure(go.Heatmap(
                z=pivot.values, x=pivot.columns.tolist(), y=pivot.index.tolist(),
                colorscale="Viridis", showscale=True))
            fig4 = plotly_dark_layout(fig4, height=360)
            st.plotly_chart(fig4, use_container_width=True)

    # ── Data cleaning log ────────────────────────────────────────────────
    if hasattr(st.session_state, "clean_steps"):
        with st.expander("🧹 Data Cleaning Log"):
            for s in st.session_state.clean_steps:
                st.markdown(f"<div class='alert-green'>{s}</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════
#  PAGE: FORECASTING
# ════════════════════════════════════════════

elif page == "💸 Profit & Loss Analyzer":
    st.markdown("<h1 style='background: -webkit-linear-gradient(45deg, #10b981, #f59e0b); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>💸 Profit & Loss Analyzer</h1>", unsafe_allow_html=True)
    st.write("Financial intelligence identifying warehouse holding costs and stockout losses.")
    
    pl = compute_profit_loss(df)
    if not pl:
        st.warning("Cost data (unit_cost) missing.")
    else:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Generated Revenue", f"Rs. {pl['total_revenue']:,.0f}")
        c2.metric("Stockout Lost Revenue", f"-Rs. {pl['lost_revenue']:,.0f}", delta_color="inverse")
        c3.metric("Overstock Penalty Fees", f"-Rs. {pl['holding_costs']:,.0f}", delta_color="inverse")
        c4.metric("Supply Chain Efficiency", f"{pl['efficiency']:.1f}%")
        
        with st.container(border=True):
            st.markdown("### 🏛️ Inter-Warehouse Transfers & Financial Optimization")
            wh_dist = df.groupby(["warehouse", "category"])["current_stock"].sum().reset_index()
            import plotly.express as px
            fig = px.bar(wh_dist, x="warehouse", y="current_stock", color="category", barmode="overlay",
                         title="Live Global Warehouse Inventory Levels")
            st.plotly_chart(plotly_dark_layout(fig), use_container_width=True)
            
            st.info("💡 **Optimization Insight:** Transfer dead stock between underperforming warehouses to eliminate overstock holding costs.")

elif page == "🔮 AI Demand Forecasting":
    st.markdown("<h1 style='background: -webkit-linear-gradient(45deg, #f59e0b, #ef4444); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>🔮 AI Demand Forecasting</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#9ca3af;margin-top:-.5rem;'>Demand prediction utilizing massive parallel **XGBoost Regressors** and **Random Forests**.</p>", unsafe_allow_html=True)

    selected_pid = st.selectbox(
        "Select Product",
        products,
        format_func=lambda x: f"{x} – {product_names.get(x,x)}"
    )

    result = train_models(df, selected_pid)

    if result is None:
        st.warning("⚠️ Not enough historical data to test models (requires ≥ 35 days).")
        st.stop()

    pf = result["pf"]
    future = result["future"]

    st.markdown("<br/>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🏆 Advanced AI Engine", result["best_model"])
    c2.metric("Accuracy %", f"{result['acc']:.1f}%")
    c3.metric("RMSE Deviation", f"{result['rmse']:.1f} units", delta_color="inverse")
    c4.metric("7-Day Forecast", f"{int(result['agg_7'])} units")
    
    c_1, c_2 = st.columns(2)
    c_1.metric("30-Day Forecast", f"{int(result['agg_30'])} units")
    c_2.metric("90-Day Forecast", f"{int(result['agg_90'])} units")

    st.markdown("<br/>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("<div class='section-title'>📈 90-Day Demand Projection Matrix</div>", unsafe_allow_html=True)
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=pf["date"], y=pf["units_sold"],
                                 name="Historical Daily Sales", line=dict(color="#4f9cf9", width=2)))
        
        fig.add_trace(go.Scatter(x=future["date"], y=future["predicted_demand"],
                                 name=f"{result['best_model']} Future Forecast", 
                                 line=dict(color="#f43f5e", width=2, dash="dash")))

        fig = plotly_dark_layout(fig, height=380)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("<br/>", unsafe_allow_html=True)
        supplier = recommend_best_supplier(df, product_names.get(selected_pid, selected_pid))
        if supplier:
            with st.container(border=True):
                st.markdown(f"### 🚚 Recommended Procurement Logistics")
                st.success(f"**Best Rated Supplier:** {supplier['name']} \n\n**Expected Delivery:** {supplier['lead']} Days \n\n**Unit Cost:** Rs. {supplier['cost']:.2f}")
                po = generate_po_pdf(product_names.get(selected_pid, selected_pid), result['agg_30'], supplier)
                st.download_button("🧾 Auto-Generate Downloadable PDF/TXT Purchase Order", data=po, file_name=f"PO_{selected_pid}.txt")

elif page == "⚡ Real-Time Stock Alerts":
    st.toast("⚡ Scanning Multi-Warehouse Networks for Stockouts...", icon="📡")
    st.markdown("<h1>🚨 Stock Optimization Alerts</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#9ca3af;margin-top:-.5rem;'>Inventory optimization logic monitoring optimal stock levels and detecting losses</p>",
                unsafe_allow_html=True)

    latest = df.sort_values("date").groupby(["product_id","product_name","category","price"]).last().reset_index()
    avg_d  = df.groupby("product_id")["units_sold"].mean().rename("avg_demand")
    merged = latest.set_index("product_id").join(avg_d).reset_index()
    merged["days_cover"]    = (merged["current_stock"] / merged["avg_demand"].replace(0,1)).round(1)
    merged["reorder_qty"]   = ((merged["avg_demand"] * 3) - merged["current_stock"]).clip(lower=0).round().astype(int)
    merged["revenue_risk"]  = (merged["avg_demand"] * merged["price"]).round(2)

    stockout  = merged[merged["days_cover"] < 1].sort_values("days_cover")
    overstock = merged[merged["days_cover"] > 6].sort_values("days_cover", ascending=False)
    dead      = merged[(merged["days_cover"] > 12) & (merged["current_stock"] > 0)]

    # Summary cards
    a1, a2, a3 = st.columns(3)
    for col, icon, label, count, cls in [
        (a1, "🚨", "Stockout Risk",  len(stockout),  "kpi-red"),
        (a2, "📦", "Overstock Alert",len(overstock), "kpi-yellow"),
        (a3, "🪦", "Dead Stock",     len(dead),       "kpi-muted"),
    ]:
        with col:
            st.markdown(f"""<div class='kpi-card'>
                <div class='kpi-label'>{icon} {label}</div>
                <div class='kpi-value {cls}'>{count} products</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Stockout table ───────────────────────────────────────────────────
    with st.container(border=True):
        st.markdown("<div class='section-title'>🚨 Stockout Risk Products</div>", unsafe_allow_html=True)
        if stockout.empty:
            st.markdown("<div class='alert-green'>✅ No stockout risks detected.</div>",
                        unsafe_allow_html=True)
        else:
            for _, row in stockout.iterrows():
                st.markdown(f"""
                <div class='alert-red'>
                    <strong>{row['product_name']}</strong> ({row['category']}) &nbsp;
                    <span class='badge badge-red'>⚡ CRITICAL</span><br/>
                    Stock: <strong>{int(row['current_stock'])} units</strong> &nbsp;·&nbsp;
                    Avg demand: <strong>{row['avg_demand']:.1f}/month</strong> &nbsp;·&nbsp;
                    Days cover: <strong>{row['days_cover']} days</strong><br/>
                    🛒 Reorder suggestion: <strong>{row['reorder_qty']} units</strong> &nbsp;|&nbsp;
                    💸 Revenue at risk: <strong>${row['revenue_risk']:,.2f}/month</strong>
                </div>""", unsafe_allow_html=True)

    # ── Overstock table ──────────────────────────────────────────────────
    with st.container(border=True):
        st.markdown("<div class='section-title'>📦 Overstock Alert</div>", unsafe_allow_html=True)
        if overstock.empty:
            st.markdown("<div class='alert-green'>✅ No overstock detected.</div>",
                        unsafe_allow_html=True)
        else:
            for _, row in overstock.iterrows():
                excess = max(0, int(row["current_stock"] - row["avg_demand"] * 3))
                holding_cost = round(excess * row["price"] * 0.02, 2)
                st.markdown(f"""
                <div class='alert-yellow'>
                    <strong>{row['product_name']}</strong> ({row['category']}) &nbsp;
                    <span class='badge badge-yellow'>📦 OVERSTOCK</span><br/>
                    Stock: <strong>{int(row['current_stock'])} units</strong> &nbsp;·&nbsp;
                    Days cover: <strong>{row['days_cover']} months</strong><br/>
                    Excess ~<strong>{excess} units</strong> &nbsp;|&nbsp;
                    Est. holding cost: <strong>${holding_cost}/month</strong>
                </div>""", unsafe_allow_html=True)

    # ── Dead stock ───────────────────────────────────────────────────────
    with st.container(border=True):
        st.markdown("<div class='section-title'>🪦 Dead Stock / Slow Movers</div>", unsafe_allow_html=True)
        if dead.empty:
            st.markdown("<div class='alert-green'>✅ No dead stock detected.</div>",
                        unsafe_allow_html=True)
        else:
            for _, row in dead.iterrows():
                st.markdown(f"""
                <div style='background:rgba(100,116,139,.08);border-left:3px solid #64748b;
                            border-radius:8px;padding:.75rem 1rem;margin:.4rem 0;font-size:.85rem;'>
                    <strong>{row['product_name']}</strong> &nbsp;
                    <span class='badge badge-blue'>🐢 SLOW MOVER</span><br/>
                    Stock: {int(row['current_stock'])} units &nbsp;·&nbsp;
                    Avg demand: {row['avg_demand']:.1f}/month
                </div>""", unsafe_allow_html=True)

    # ── Risk chart ───────────────────────────────────────────────────────
    with st.container(border=True):
        st.markdown("<div class='section-title'>📊 Stock Coverage Chart (Days)</div>",
                    unsafe_allow_html=True)
        merged_sorted = merged.sort_values("days_cover")
        colors = merged_sorted["days_cover"].apply(
            lambda x: "#f87171" if x < 1 else ("#fbbf24" if x < 3 else "#34d399"))
        fig = go.Figure(go.Bar(
            x=merged_sorted["product_name"], y=merged_sorted["days_cover"],
            marker_color=colors.tolist(),
            text=merged_sorted["days_cover"].apply(lambda x: f"{x:.1f}m"),
            textposition="outside"))
        fig.add_hline(y=1, line_dash="dash", line_color="#f87171",
                      annotation_text="Stockout threshold", annotation_position="top right")
        fig.add_hline(y=6, line_dash="dash", line_color="#fbbf24",
                      annotation_text="Overstock threshold", annotation_position="top right")
        fig = plotly_dark_layout(fig, height=380)
        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(fig, use_container_width=True)


# ════════════════════════════════════════════
#  PAGE: ABC ANALYSIS
# ════════════════════════════════════════════
elif page == "📊 ABC Segmentation":
    st.markdown("<h1>📊 ABC Inventory Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b;margin-top:-.5rem;'>Pareto-based product classification for smarter procurement</p>",
                unsafe_allow_html=True)

    abc = abc_analysis(df)

    # ABC KPIs
    for cls in ["A – High Value", "B – Medium Value", "C – Low Value"]:
        sub = abc[abc["ABC"] == cls]
        count = len(sub)
        rev   = sub["total_revenue"].sum()
        pct   = sub["total_revenue"].sum() / abc["total_revenue"].sum() * 100

    a1, a2, a3 = st.columns(3)
    for col, cls, icon, badge in [
        (a1, "A – High Value",   "🥇", "badge-green"),
        (a2, "B – Medium Value", "🥈", "badge-yellow"),
        (a3, "C – Low Value",    "🥉", "badge-blue"),
    ]:
        sub = abc[abc["ABC"] == cls]
        with col:
            pct = sub["total_revenue"].sum() / abc["total_revenue"].sum() * 100
            st.markdown(f"""<div class='kpi-card'>
                <div class='kpi-label'>{icon} Class {cls[0]}</div>
                <div class='kpi-value kpi-blue'>{len(sub)} products</div>
                <div class='kpi-sub'>{pct:.1f}% of revenue</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    c1, c2 = st.columns([3, 2])

    with c1:
        with st.container(border=True):
            st.markdown("<div class='section-title'>📊 Revenue Contribution by Product</div>",
                        unsafe_allow_html=True)
            color_map = {
                "A – High Value":   "#34d399",
                "B – Medium Value": "#fbbf24",
                "C – Low Value":    "#4f9cf9",
            }
            fig = px.bar(abc.sort_values("total_revenue", ascending=False),
                         x="product_name", y="total_revenue", color="ABC",
                         color_discrete_map=color_map,
                         text="ABC")
            fig = plotly_dark_layout(fig, height=380)
            fig.update_layout(xaxis_tickangle=-35)
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        with st.container(border=True):
            st.markdown("<div class='section-title'>📈 Pareto Curve</div>",
                        unsafe_allow_html=True)
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(
                x=abc["product_name"], y=abc["total_revenue"],
                name="Revenue", marker_color="#4f9cf9"))
            fig2.add_trace(go.Scatter(
                x=abc["product_name"], y=abc["cum_pct"],
                name="Cumulative %", yaxis="y2",
                line=dict(color="#a78bfa", width=2)))
            fig2.update_layout(
                yaxis2=dict(overlaying="y", side="right", range=[0, 110],
                            gridcolor="rgba(0,0,0,0)", color="#e2e8f0"))
            fig2 = plotly_dark_layout(fig2, height=380)
            fig2.update_layout(xaxis_tickangle=-35)
            st.plotly_chart(fig2, use_container_width=True)

    # ABC Table
    with st.container(border=True):
        st.markdown("<div class='section-title'>📋 Full ABC Classification Table</div>",
                    unsafe_allow_html=True)
        display_abc = abc[["product_id","product_name","total_sold","total_revenue","cum_pct","ABC"]].copy()
        display_abc["total_revenue"] = display_abc["total_revenue"].round(2)
        display_abc["cum_pct"]       = display_abc["cum_pct"].round(1)
        display_abc.columns = ["ID","Product","Units Sold","Revenue ($)","Cumulative %","Class"]
        st.dataframe(display_abc, use_container_width=True, hide_index=True)

    # Fast vs Slow movers
    with st.container(border=True):
        st.markdown("<div class='section-title'>⚡ Fast vs Slow Movers</div>",
                    unsafe_allow_html=True)
        speed = df.groupby("product_name")["units_sold"].mean().reset_index()
        speed.columns = ["Product","Avg Monthly Sales"]
        median_s = speed["Avg Monthly Sales"].median()
        speed["Category"] = speed["Avg Monthly Sales"].apply(
            lambda x: "⚡ Fast Mover" if x >= median_s else "🐢 Slow Mover")

        fig3 = px.bar(speed.sort_values("Avg Monthly Sales", ascending=False),
                      x="Product", y="Avg Monthly Sales", color="Category",
                      color_discrete_map={"⚡ Fast Mover":"#34d399","🐢 Slow Mover":"#64748b"})
        fig3 = plotly_dark_layout(fig3, height=320)
        fig3.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(fig3, use_container_width=True)


# ════════════════════════════════════════════
#  PAGE: WHAT-IF SIMULATOR
# ════════════════════════════════════════════
elif page == "🧠 AI Optimization Engine":
    st.markdown("<h1>🧠 Inventory Optimization Engine</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#9ca3af;margin-top:-.5rem;'>Simulate demand shocks and optimize stock thresholds dynamically</p>",
                unsafe_allow_html=True)

    selected_pid = st.selectbox(
        "Select Product",
        products,
        format_func=lambda x: f"{x} – {product_names.get(x,x)}"
    )

    result = train_models(df, selected_pid)
    if result is None:
        st.warning("Not enough data for this product.")
        st.stop()

    current_stock = int(df[df["product_id"]==selected_pid]["current_stock"].iloc[-1])
    base_forecast  = result["future"]["predicted_demand"].tolist()

    st.markdown("<br/>", unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3)
    with s1:
        demand_delta = st.slider("📈 Demand Change (%)", -50, 100, 0, 5,
                                 help="Simulate a demand spike or drop")
    with s2:
        supplier_delay = st.slider("🚚 Supplier Delay (weeks)", 0, 12, 0,
                                   help="Extra weeks before restock arrives")
    with s3:
        price_change = st.slider("💰 Price Change (%)", -30, 50, 0, 5,
                                 help="Estimate revenue impact of repricing")

    adj_forecast = [max(0, round(v * (1 + demand_delta/100))) for v in base_forecast]
    total_demand_3m = sum(adj_forecast)
    gap = total_demand_3m - current_stock
    delay_consumption = round(
        df[df["product_id"]==selected_pid]["units_sold"].mean() / 4.3 * supplier_delay)
    effective_gap = gap + delay_consumption

    base_price = float(df[df["product_id"]==selected_pid]["price"].iloc[-1])
    new_price   = base_price * (1 + price_change / 100)
    base_rev    = sum(base_forecast) * base_price
    new_rev     = sum(adj_forecast)  * new_price
    rev_delta   = new_rev - base_rev

    # Result KPIs
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-label'>📦 Current Stock</div>
            <div class='kpi-value kpi-blue'>{current_stock:,}</div>
            <div class='kpi-sub'>units available</div>
        </div>""", unsafe_allow_html=True)
    with r2:
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-label'>📈 Adj 3-Month Demand</div>
            <div class='kpi-value {'kpi-red' if total_demand_3m > current_stock else 'kpi-green'}'>{total_demand_3m:,}</div>
            <div class='kpi-sub'>units needed</div>
        </div>""", unsafe_allow_html=True)
    with r3:
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-label'>⚠️ Stock Gap (incl delay)</div>
            <div class='kpi-value {'kpi-red' if effective_gap > 0 else 'kpi-green'}'>{'+' if effective_gap>0 else ''}{effective_gap:,}</div>
            <div class='kpi-sub'>{'units shortage' if effective_gap>0 else 'surplus units'}</div>
        </div>""", unsafe_allow_html=True)
    with r4:
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-label'>💰 Revenue Impact</div>
            <div class='kpi-value {'kpi-green' if rev_delta>=0 else 'kpi-red'}'>{'+' if rev_delta>=0 else ''}${rev_delta:,.0f}</div>
            <div class='kpi-sub'>vs baseline</div>
        </div>""", unsafe_allow_html=True)

    # Scenario recommendation
    st.markdown("<br/>", unsafe_allow_html=True)
    if effective_gap > 0:
        st.markdown(f"""
        <div class='alert-red'>
            🚨 <strong>Action Required:</strong> Under this scenario,
            you will face a shortage of <strong>{effective_gap} units</strong>.
            Immediately place a purchase order for at least
            <strong>{effective_gap + round(df[df['product_id']==selected_pid]['units_sold'].mean())} units</strong>
            (includes 1-month safety buffer).
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='alert-green'>
            ✅ <strong>You're safe:</strong> Current stock covers projected demand
            (surplus of {abs(effective_gap)} units). Consider deferring next reorder.
        </div>""", unsafe_allow_html=True)

    # Comparison chart
    st.markdown("<br/>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<div class='section-title'>📊 Base vs Scenario Demand Comparison</div>",
                    unsafe_allow_html=True)
        months = [str(r["date"]) for _, r in result["future"].iterrows()]
        fig = go.Figure()
        fig.add_trace(go.Bar(x=months, y=base_forecast,  name="Base Forecast", marker_color="#4f9cf9"))
        fig.add_trace(go.Bar(x=months, y=adj_forecast,   name="Scenario",      marker_color="#a78bfa"))
        fig.add_hline(y=current_stock, line_dash="dot", line_color="#34d399",
                      annotation_text=f"Current stock: {current_stock}", annotation_position="top left")
        fig = plotly_dark_layout(fig, height=360)
        fig.update_layout(barmode="overlay")
        st.plotly_chart(fig, use_container_width=True)


# ════════════════════════════════════════════
#  PAGE: AI CHATBOT
# ════════════════════════════════════════════
elif page == "🤖 StockSense Copilot":
    st.markdown("<h1 style='background: -webkit-linear-gradient(45deg, #6366f1, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>🤖 StockSense Copilot</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#9ca3af;margin-top:-.5rem;'>Ask anything about your inventory optimization queries in plain English</p>",
                unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history natively
    st.markdown("<br>", unsafe_allow_html=True)
    for role, msg in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(msg)

    if not st.session_state.chat_history:
        st.info("👋 Hi! I'm StockSense Copilot. Ask me about stockouts, forecasts, best sellers, or reorder suggestions.")

    # Native Chat Input
    if prompt := st.chat_input("Ask a question about your inventory... e.g. Which products need reordering?"):
        st.session_state.chat_history.append(("user", prompt))
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing inventory data..."):
                response = chatbot_response(prompt, df)
                st.markdown(response)
        st.session_state.chat_history.append(("assistant", response))

    if st.button("🗑️ Clear Chat", use_container_width=False):
        st.session_state.chat_history = []
        st.rerun()


# ════════════════════════════════════════════
#  PAGE: EXECUTIVE SUMMARY
# ════════════════════════════════════════════
elif page == "💼 Executive Business Summary":
    st.markdown("<h1 style='background: -webkit-linear-gradient(45deg, #34d399, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>📑 Executive Business Summary</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#9ca3af;margin-top:-.5rem;'>Comprehensive time-series reports to reduce losses and improve profitability</p>",
                unsafe_allow_html=True)

    df["revenue"] = df["units_sold"] * df["price"]
    total_rev     = df["revenue"].sum()
    total_units   = df["units_sold"].sum()
    health        = inventory_health_score(df)
    abc           = abc_analysis(df)

    latest = df.sort_values("date").groupby("product_id").last().reset_index()
    avg_d  = df.groupby("product_id")["units_sold"].mean()
    merged = latest.set_index("product_id").join(avg_d.rename("avg_d"))
    n_stockout  = (merged["current_stock"] < merged["avg_d"]).sum()
    n_overstock = (merged["current_stock"] > merged["avg_d"] * 6).sum()

    # Health score gauge
    score = health["score"]
    score_color = "#34d399" if score >= 70 else ("#fbbf24" if score >= 40 else "#f87171")
    gauge_deg   = int(score * 1.8)

    st.markdown(f"""
    <div style='background:linear-gradient(135deg,rgba(79,156,249,.1),rgba(167,139,250,.1));
                border:1px solid rgba(79,156,249,.2);border-radius:20px;padding:2rem;
                margin-bottom:1.5rem;'>
        <div style='display:flex;align-items:center;gap:2rem;flex-wrap:wrap;'>
            <div style='flex:1;min-width:220px;'>
                <div style='font-family:"Space Grotesk",sans-serif;font-size:1.5rem;
                            font-weight:700;margin-bottom:.5rem;'>Inventory Health Score</div>
                <div style='font-size:4rem;font-weight:800;color:{score_color};
                            font-family:"Space Grotesk",sans-serif;'>{score}<span style='font-size:1.5rem;'>/100</span></div>
                <div style='font-size:.85rem;color:#64748b;margin-top:.25rem;'>
                    {"🟢 Excellent" if score>=70 else ("🟡 Moderate" if score>=40 else "🔴 Critical")} health status
                </div>
            </div>
            <div style='flex:2;display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;'>
                <div style='text-align:center;'>
                    <div style='font-size:1.75rem;font-weight:700;color:#4f9cf9;'>${total_rev:,.0f}</div>
                    <div style='font-size:.75rem;color:#64748b;'>Total Revenue</div>
                </div>
                <div style='text-align:center;'>
                    <div style='font-size:1.75rem;font-weight:700;color:#f87171;'>{n_stockout}</div>
                    <div style='font-size:.75rem;color:#64748b;'>Stockout Risks</div>
                </div>
                <div style='text-align:center;'>
                    <div style='font-size:1.75rem;font-weight:700;color:#fbbf24;'>{n_overstock}</div>
                    <div style='font-size:.75rem;color:#64748b;'>Overstock Items</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # AI Insights panel
    with st.container(border=True):
        st.markdown("<div class='section-title'>🧠 AI-Generated Business Insights</div>",
                    unsafe_allow_html=True)

        top_product = df.groupby("product_name")["units_sold"].sum().idxmax()
        top_cat     = df.groupby("category")["revenue"].sum().idxmax()
        q4_rev      = df[df["quarter"]==4]["revenue"].sum() if "quarter" in df.columns else 0
        q1_rev      = df[df["quarter"]==1]["revenue"].sum() if "quarter" in df.columns else 1
        seasonal_ratio = q4_rev / max(q1_rev, 1)

        insights = [
            (f"🏆 <strong>{top_product}</strong> is your top-selling product — "
             "prioritise replenishment and consider bundling promotions to boost average order value."),
            (f"📊 <strong>{top_cat}</strong> contributes the highest category revenue. "
             "Consider expanding SKU range within this category to capitalise on demand."),
            (f"{'📈 Strong Q4 seasonality detected (' + str(round(seasonal_ratio,1)) + 'x Q1 volume). Pre-stock high-velocity items by October to avoid holiday stockouts.' if seasonal_ratio > 1.3 else '📊 Demand is relatively stable year-round — maintain consistent safety-stock levels.'}"),
            (f"⚠️ {n_stockout} products are below safety stock. Lost-sales opportunity: "
             f"<strong>${(merged[merged['current_stock'] < merged['avg_d']]['avg_d'] * merged[merged['current_stock'] < merged['avg_d']]['price']).sum():,.0f}/month</strong>."),
            ("🤖 Class A products drive 70%+ of revenue. Allocate 80% of procurement budget "
             "to Class A items and automate reorder triggers at 1.5× monthly demand threshold."),
            ("💡 Implement dynamic reorder points: set reorder level = average demand × (lead time + safety days) "
             "for each SKU to eliminate both stockouts and overstock simultaneously."),
        ]

        for insight in insights:
            st.markdown(f"<div class='insight-box'>{insight}</div>", unsafe_allow_html=True)

    # Charts row
    ec1, ec2 = st.columns(2)
    with ec1:
        with st.container(border=True):
            st.markdown("<div class='section-title'>📈 Revenue Trend</div>", unsafe_allow_html=True)
            rev_monthly = df.groupby("date")["revenue"].sum().reset_index()
            fig = px.line(rev_monthly, x="date", y="revenue",
                          color_discrete_sequence=["#4f9cf9"])
            fig.update_traces(fill="tozeroy", fillcolor="rgba(79,156,249,0.1)")
            fig = plotly_dark_layout(fig, height=280)
            st.plotly_chart(fig, use_container_width=True)

    with ec2:
        with st.container(border=True):
            st.markdown("<div class='section-title'>🏷️ ABC Distribution</div>", unsafe_allow_html=True)
            abc_counts = abc["ABC"].value_counts().reset_index()
            abc_counts.columns = ["Class","Count"]
            fig2 = px.pie(abc_counts, names="Class", values="Count", hole=0.6,
                          color_discrete_sequence=["#34d399","#fbbf24","#4f9cf9"])
            fig2 = plotly_dark_layout(fig2, height=280)
            st.plotly_chart(fig2, use_container_width=True)

    # Download full report
    report_parts = [
        "STOCKSENSE AI – EXECUTIVE INVENTORY REPORT",
        "=" * 50,
        f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        f"HEALTH SCORE    : {score}/100",
        f"TOTAL REVENUE   : ${total_rev:,.2f}",
        f"TOTAL UNITS SOLD: {total_units:,}",
        f"STOCKOUT RISKS  : {n_stockout} products",
        f"OVERSTOCK ITEMS : {n_overstock} products",
        "",
        "ABC CLASSIFICATION:",
    ]
    for cls in ["A – High Value","B – Medium Value","C – Low Value"]:
        sub = abc[abc["ABC"]==cls]
        report_parts.append(f"  Class {cls[0]}: {len(sub)} products "
                            f"({sub['total_revenue'].sum()/abc['total_revenue'].sum()*100:.1f}% revenue)")

    report_parts += ["", "TOP 5 PRODUCTS BY REVENUE:"]
    top5 = df.groupby("product_name")["revenue"].sum().nlargest(5)
    for i, (n, v) in enumerate(top5.items(), 1):
        report_parts.append(f"  {i}. {n}: ${v:,.2f}")

    report_txt = "\n".join(report_parts)
    st.download_button("⬇️ Download Executive Report (TXT)", report_txt,
                       file_name="stocksense_report.txt", mime="text/plain")

    clean_csv = df.to_csv(index=False).encode()
    st.download_button("⬇️ Download Cleaned Dataset (CSV)", clean_csv,
                       file_name="cleaned_inventory.csv", mime="text/csv")
