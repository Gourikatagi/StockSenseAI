import sys
import codecs
import re

file_path = r'c:\Users\hp\Desktop\StockSense AI\files\app.py'
with codecs.open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Fix MetricMixin TypeError
text = text.replace('variant_color="inverse"', 'delta_color="inverse"')
text = text.replace("variant_color='inverse'", 'delta_color="inverse"')

# 2. Add Sidebar Stock Alerts
# Locate the section where dashboard or sidebar is loaded to inject global alerts.
# A good place is right before `# ════════════════════════════════════════════\n#  PAGE: DASHBOARD`
anchor_sidebar = '# ════════════════════════════════════════════\n#  PAGE: DASHBOARD'
alerts_code = '''
# ── Global Sidebar Alerts ──────────────────────────────────────────
with st.sidebar:
    # Compute fast alert metrics
    if st.session_state.df_clean is not None:
        _d = st.session_state.df_clean
        _latest = _d.sort_values("date").groupby("product_id").last().reset_index()
        _avg = _d.groupby("product_id")["units_sold"].mean().rename("avg_d")
        _m = _latest.set_index("product_id").join(_avg).reset_index()
        
        _stockouts = _m[_m["current_stock"] < _m["avg_d"]]
        _overstocks = _m[_m["current_stock"] > _m["avg_d"] * 6]
        
        if not _stockouts.empty:
            st.error(f"🚨 {len(_stockouts)} products at Stockout Risk! Check Alerts Tab.")
        if not _overstocks.empty:
            st.warning(f"📦 {len(_overstocks)} products in Critical Overstock. Check Alerts.")

'''
if 'Global Sidebar Alerts' not in text:
    text = text.replace(anchor_sidebar, alerts_code + anchor_sidebar)

# 3. Graph Clarity in Optimization Engine
# Replace go.Bar with smoothed Area/Scatter charts
old_bar_1 = 'fig2.add_trace(go.Bar(x=sim_df["date"], y=sim_df["forecast"], name="Base Forecast", marker_color="#4f9cf9"))'
new_line_1 = 'fig2.add_trace(go.Scatter(x=sim_df["date"], y=sim_df["forecast"], name="Base Forecast", mode="lines", fill="tozeroy", line=dict(color="#4f9cf9", width=2)))'
text = text.replace(old_bar_1, new_line_1)

old_bar_2 = 'fig2.add_trace(go.Bar(x=sim_df["date"], y=sim_df["scenario_demand"], name="Scenario", marker_color="#a78bfa"))'
new_line_2 = 'fig2.add_trace(go.Scatter(x=sim_df["date"], y=sim_df["scenario_demand"], name="Scenario", mode="lines", fill="tozeroy", line=dict(color="#a78bfa", width=2)))'
text = text.replace(old_bar_2, new_line_2)

# Make the layout overlay instead of group (though they are lines now, but just in case)
text = text.replace('barmode="group"', 'barmode="overlay"')

# 4. Icon fix for Executive Summary and Optimization Engine
# I'll update the title strings to make them more professional 
text = text.replace('📑 Executive Summary', '💼 Executive Business Summary')
text = text.replace('<h1>📑 Executive Summary</h1>', '<h1>💼 Executive Business Summary</h1>')

# Ensure the UI headers all look perfect
text = text.replace('<h1>⚡ Stock Optimization Alerts</h1>', '<h1>🚨 Stock Optimization Alerts</h1>')


with codecs.open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Bugfixes successfully applied: delta_color resolved, Sidebar Alerts Added, Graph Smoothed.")
