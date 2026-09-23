import sys

file_path = r'c:\Users\hp\Desktop\StockSense AI\files\app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update logo
text = text.replace(
    "<div style='font-size:2.2rem'>📦</div>",
    "<div style='font-size:2.2rem'>💠</div>"
)

# 2. Update Assistant Name
text = text.replace('"🤖 AI Assistant"', '"🤖 Nexus AI Copilot"')
text = text.replace('<h1>🤖 E-Commerce AI Assistant</h1>', '<h1>🤖 Nexus AI Copilot</h1>')
text = text.replace("Hi! I'm your inventory AI Assistant.", "Hi! I'm Nexus AI.")

# 3. Update Chatbot Fallback and add bottom-seller logic
old_fallback = '''    return ("🤔 I didn't catch that. Try asking about:\\n"
            "**stockouts**, **overstock**, **best sellers**, **reorder suggestions**, "
            "**revenue**, **dead stock**, or **inventory health**.")'''

new_fallback = '''    if any(k in q for k in ["least", "worst", "lowest", "bad"]):
        bottom = df.groupby("product_name")["units_sold"].sum().nsmallest(3)
        lines = [f"{i+1}. {n} ({int(v)} units)" for i,(n,v) in enumerate(bottom.items())]
        return "📉 **Bottom 3 lowest-sellers:**\\n" + "\\n".join(lines)

    rev = (df['units_sold'] * df['price']).sum()
    h = inventory_health_score(df)
    return ("🤔 I'm analyzing that, but here is a quick snapshot of your inventory:\\n"
            f"• **Health Score:** {h['score']}/100\\n"
            f"• **Total Revenue:** ${rev:,.0f}\\n"
            "Try asking me specifically about *stockouts*, *best sellers*, *lowest sellers*, or *dead stock*.")'''

text = text.replace(old_fallback, new_fallback)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print('Chatbot AI logic, name, and logo successfully upgraded.')
