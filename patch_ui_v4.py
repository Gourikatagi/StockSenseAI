import sys
import codecs

file_path = r'c:\Users\hp\Desktop\StockSense AI\files\app.py'
with codecs.open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

start_forecast = text.find('elif page == "🔮 AI Demand Forecasting":')
start_alerts = text.find('elif page == "⚡ Real-Time Stock Alerts":')

if start_forecast == -1 or start_alerts == -1:
    print("Cannot find anchor points.")
    sys.exit()

old_forecast_block = text[start_forecast:start_alerts]

new_forecast_block = '''elif page == "🔮 AI Demand Forecasting":
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
    c3.metric("RMSE Deviation", f"{result['rmse']:.1f} units", variant_color="inverse")
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
                st.success(f"**Best Rated Supplier:** {supplier['name']} \\n\\n**Expected Delivery:** {supplier['lead']} Days \\n\\n**Unit Cost:** ${supplier['cost']:.2f}")
                po = generate_po_pdf(product_names.get(selected_pid, selected_pid), result['agg_30'], supplier)
                st.download_button("🧾 Auto-Generate Downloadable PDF/TXT Purchase Order", data=po, file_name=f"PO_{selected_pid}.txt")

'''

text = text.replace(old_forecast_block, new_forecast_block)

with codecs.open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("UI successfully matched to backend XGBoost matrix!")
