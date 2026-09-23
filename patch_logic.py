import sys
import base64

file_path = r'c:\Users\hp\Desktop\StockSense AI\files\app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# I want to append new Logic Helpers right before the Streamlit Page Logic starts
# Let's target the SESSION STATE section as an anchor
anchor = "# ════════════════════════════════════════════\n#  SESSION STATE"

new_logic = '''
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
Est. Unit Price:  ${supplier_data.get('cost', 0.0):.2f}
==================================================
TOTAL ESTIMATED COST: ${(quantity * supplier_data.get('cost', 0.0)):,.2f}
==================================================
AUTHORIZED BY: StockSense Enterprise AI Copilot"""
    return po_text.encode('utf-8')

'''

text = text.replace(anchor, new_logic + anchor)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Enterprise Logic Layer (Supplier, P&L, PO Generator) safely injected via V3 Patch.")
