# 📦 StockSense AI — Smart Inventory Demand Forecasting System
### Hackathon Edition · Streamlit + Scikit-learn + Plotly

---

## 🚀 HOW TO RUN IN ANTIGRAVITY (Step-by-Step)

### Step 1 — Upload files
Upload these 3 files to your Antigravity project root:
- `app.py`
- `requirements.txt`
- `sample_inventory.csv`

### Step 2 — Install dependencies
Open the Antigravity terminal and run:
```bash
pip install -r requirements.txt
```

### Step 3 — Launch the app
```bash
streamlit run app.py
```
Antigravity will give you a public URL — open it in your browser.

---

## 📁 PROJECT STRUCTURE
```
StockSenseAI/
├── app.py                  ← Complete single-file app
├── requirements.txt        ← Minimal dependencies
├── sample_inventory.csv    ← Auto-loaded demo data
└── README.md               ← This file
```

---

## 📦 FEATURES AT A GLANCE

| Feature | Description |
|---|---|
| 🏠 Dashboard | KPIs, revenue trends, heatmaps, top products |
| 📊 Forecasting | LR + RF model comparison, 3-month predictions |
| 🔔 Alerts | Stockout / overstock / dead-stock detection |
| 📦 ABC Analysis | Pareto classification + fast/slow movers |
| 🔬 What-If Simulator | Demand shocks, supplier delays, price changes |
| 🤖 AI Chatbot | Rule-based NLP inventory assistant |
| 📄 Executive Summary | AI insights panel + downloadable report |

---

## 🛠️ COMMON ERRORS & FIXES

**Error:** `ModuleNotFoundError: No module named 'plotly'`
**Fix:** Run `pip install plotly` in terminal

**Error:** `FileNotFoundError: sample_inventory.csv`
**Fix:** The app generates data inline automatically — or upload the CSV file

**Error:** `StreamlitAPIException` on rerun
**Fix:** Refresh the browser tab

**Error:** Slow first load
**Fix:** Normal — models train on first run (~3 sec). Subsequent loads are cached.

---

## 🎤 2-MINUTE JUDGE PITCH

"Every retailer loses 10-15% of revenue annually to stockouts and overstock.
StockSense AI solves this with a real-time ML dashboard that predicts demand
3 months ahead, auto-classifies inventory by value, and alerts warehouse
managers before problems occur.

We combine Random Forest forecasting with Pareto ABC analysis and a
what-if simulator — all in a SaaS-ready dashboard that any non-technical
operations manager can use from day one.

Market opportunity: $5B inventory management software market growing 10% YoY.
Our edge: AI-first, zero setup, runs on any browser."

---

## 🔭 FUTURE SCOPE

- 🔗 ERP integrations (SAP, Oracle, QuickBooks)
- 📱 Mobile PWA with push alerts
- 🌐 Multi-warehouse & multi-location support
- 🤖 LLM-powered chatbot (GPT/Claude API)
- 📧 Email/Slack automated alert system
- 🏭 Supplier lead-time API integrations
- 📊 Real-time IoT warehouse sensor feeds
- 🔐 Role-based access control (admin/buyer/analyst)
