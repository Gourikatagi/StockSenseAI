import codecs

file_path = r'c:\Users\hp\Desktop\StockSense AI\files\app.py'
with codecs.open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Replace all $ with Rs.
text = text.replace('f"${total_rev:,.0f}"', 'f"Rs. {total_rev:,.0f}"')
text = text.replace('f"${pl[\'total_revenue\']:,.0f}"', 'f"Rs. {pl[\'total_revenue\']:,.0f}"')
text = text.replace('f"-${pl[\'lost_revenue\']:,.0f}"', 'f"-Rs. {pl[\'lost_revenue\']:,.0f}"')
text = text.replace('f"-${pl[\'holding_costs\']:,.0f}"', 'f"-Rs. {pl[\'holding_costs\']:,.0f}"')
text = text.replace('Unit Cost:** ${supplier', 'Unit Cost:** Rs. {supplier')

# Update the PO generator
text = text.replace('Est. Unit Price:  ${supplier_data.get(\'cost\', 0.0):.2f}', 'Est. Unit Price:  Rs. {supplier_data.get(\'cost\', 0.0):.2f}')
text = text.replace('TOTAL ESTIMATED COST: ${(quantity * supplier_data.get(\'cost\', 0.0)):,.2f}', 'TOTAL ESTIMATED COST: Rs. {(quantity * supplier_data.get(\'cost\', 0.0)):,.2f}')


# 2. Fix the chart complexity on Dashboard
# The area chart is plotted using pivot = df.groupby(["date","category"])["units_sold"].sum().unstack().fillna(0)
# We need to resample it to Monthly to smooth it out.
old_chart_code = '''    with st.container(border=True):
        st.markdown("<div class='section-title'>📈 Monthly Sales Trend (All Products)</div>",
                    unsafe_allow_html=True)
        pivot = df.groupby(["date","category"])["units_sold"].sum().unstack().fillna(0)
        fig = px.area(pivot, facet_col=None, color_discrete_sequence=px.colors.qualitative.Pastel)
        fig = plotly_dark_layout(fig, height=350)
        fig.update_layout(legend_title="category")
        st.plotly_chart(fig, use_container_width=True)'''

new_chart_code = '''    with st.container(border=True):
        st.markdown("<div class='section-title'>📈 Monthly Sales Trend (All Products)</div>",
                    unsafe_allow_html=True)
        # Resample daily to monthly to strictly fix dense spiky graph
        daily_cat = df.groupby(["date","category"])["units_sold"].sum().reset_index()
        monthly = daily_cat.set_index("date").groupby("category").resample("M")["units_sold"].sum().reset_index()
        pivot = monthly.pivot(index="date", columns="category", values="units_sold").fillna(0)
        
        # Smoothed Area graph
        fig = px.area(pivot, facet_col=None, color_discrete_sequence=px.colors.qualitative.Pastel)
        fig = plotly_dark_layout(fig, height=350)
        fig.update_layout(legend_title="category")
        st.plotly_chart(fig, use_container_width=True)'''

text = text.replace(old_chart_code, new_chart_code)


with codecs.open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Currency updated to Rs and graph smoothed cleanly.")
