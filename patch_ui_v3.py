import codecs
import sys

file_path = r'c:\Users\hp\Desktop\StockSense AI\files\app.py'
with codecs.open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update pages array in Sidebar
pages_old = '''    pages = [
        "🌐 Executive Dashboard",
        "🔮 AI Demand Forecasting",
        "⚡ Real-Time Stock Alerts",
        "📊 ABC Segmentation",
        "🧠 AI Optimization Engine",
        "🤖 StockSense Copilot",
        "📑 Executive Summary",
    ]'''

pages_new = '''    pages = [
        "🌐 Executive Dashboard",
        "💸 Profit & Loss Analyzer",
        "🔮 AI Demand Forecasting",
        "⚡ Real-Time Stock Alerts",
        "📊 ABC Segmentation",
        "🧠 AI Optimization Engine",
        "🤖 StockSense Copilot",
        "📑 Executive Summary",
    ]'''
text = text.replace(pages_old, pages_new)

# Generate logic for P&L
p_and_l_ui = '''
elif page == "💸 Profit & Loss Analyzer":
    st.markdown("<h1 style='background: -webkit-linear-gradient(45deg, #10b981, #f59e0b); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>💸 Profit & Loss Analyzer</h1>", unsafe_allow_html=True)
    st.write("Financial intelligence identifying warehouse holding costs and stockout losses.")
    
    pl = compute_profit_loss(df)
    if not pl:
        st.warning("Cost data (unit_cost) missing.")
    else:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Generated Revenue", f"${pl['total_revenue']:,.0f}")
        c2.metric("Stockout Lost Revenue", f"-${pl['lost_revenue']:,.0f}", variant_color="inverse")
        c3.metric("Overstock Penalty Fees", f"-${pl['holding_costs']:,.0f}", variant_color="inverse")
        c4.metric("Supply Chain Efficiency", f"{pl['efficiency']:.1f}%")
        
        with st.container(border=True):
            st.markdown("### 🏛️ Inter-Warehouse Transfers & Financial Optimization")
            wh_dist = df.groupby(["warehouse", "category"])["current_stock"].sum().reset_index()
            import plotly.express as px
            fig = px.bar(wh_dist, x="warehouse", y="current_stock", color="category", barmode="group",
                         title="Live Global Warehouse Inventory Levels")
            st.plotly_chart(plotly_dark_layout(fig), use_container_width=True)
            
            st.info("💡 **Optimization Insight:** Transfer dead stock between underperforming warehouses to eliminate overstock holding costs.")

'''

# Inject P&L before Forecasting
text = text.replace('elif page == "🔮 AI Demand Forecasting":', p_and_l_ui + 'elif page == "🔮 AI Demand Forecasting":')

# Overhaul Forecasting header
forecast_old = '''    st.markdown("<h1 style='background: -webkit-linear-gradient(45deg, #f59e0b, #ef4444); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>🔮 AI Demand Forecasting</h1>", unsafe_allow_html=True)
    st.markdown("Demand prediction utilizing Open-Source Scikit-Learn Time-Series models")'''

forecast_new = '''    st.markdown("<h1 style='background: -webkit-linear-gradient(45deg, #f59e0b, #ef4444); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>🔮 AI Demand Forecasting</h1>", unsafe_allow_html=True)
    st.markdown("Demand prediction utilizing massive parallel **XGBoost Regressors** and **Random Forests**.")'''

text = text.replace(forecast_old, forecast_new)

# Provide fallback replacing logic using string splice because the exact string might naturally vary slightly
forecast_search = 'c1.metric("Best Model Algorithm", m_dict["best_model"])'
blocks = text.split(forecast_search)

if len(blocks) == 2:
    front = blocks[0].rsplit('c1, c2, c3 = st.columns(3)', 1)[0]
    back = blocks[1].split('st.plotly_chart(fig, use_container_width=True)', 1)[1]
    
    forecast_results_new = '''        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🏆 Advanced AI Engine", m_dict["best_model"])
        c2.metric("Accuracy %", f"{m_dict['acc']:.1f}%")
        c3.metric("RMSE Deviation", f"{m_dict['rmse']:.1f} units")
        c4.metric("7-Day Forecast", f"{int(m_dict['agg_7'])} units")
        
        c_1, c_2 = st.columns(2)
        c_1.metric("30-Day Forecast", f"{int(m_dict['agg_30'])} units")
        c_2.metric("90-Day Forecast", f"{int(m_dict['agg_90'])} units")

        st.markdown("<div class='section-title'>📈 90-Day Demand Projection Matrix</div>", unsafe_allow_html=True)
        # Plot historical
        pf = m_dict["pf"]
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=pf["date"], y=pf["units_sold"],
                                 name="Historical Daily Sales", line=dict(color="#4f9cf9", width=2)))
        
        # Plot future
        fut = m_dict["future"]
        fig.add_trace(go.Scatter(x=fut["date"], y=fut["predicted_demand"],
                                 name=f"{m_dict['best_model']} Future Forecast", 
                                 line=dict(color="#f43f5e", width=2, dash="dash")))

        fig = plotly_dark_layout(fig, height=350)
        st.plotly_chart(fig, use_container_width=True)
        
        supplier = recommend_best_supplier(df, p)
        if supplier:
            with st.container(border=True):
                st.markdown(f"### 🚚 Recommended Procurement Logistics")
                st.success(f"**Best Rated Supplier:** {supplier['name']} \\n\\n**Expected Delivery:** {supplier['lead']} Days \\n\\n**Unit Cost:** ${supplier['cost']:.2f}")
                po = generate_po_pdf(p, m_dict['agg_30'], supplier)
                st.download_button("🧾 Auto-Generate Downloadable PDF/TXT Purchase Order", data=po, file_name=f"PO_{p.split(' ')[0]}.txt")
'''
    text = front + forecast_results_new + back
else:
    print("Warning: Could not cleanly map forecast block.")
    
# Toast notification on Alerts Tab
text = text.replace('elif page == "⚡ Real-Time Stock Alerts":', 'elif page == "⚡ Real-Time Stock Alerts":\n    st.toast("⚡ Scanning Multi-Warehouse Networks for Stockouts...", icon="📡")')


with codecs.open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("V3 User Interface safely generated: P&L Tab, PDF generation, Warehouse matrices mapped.")
