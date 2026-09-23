import sys

file_path = r'c:\Users\hp\Desktop\StockSense AI\files\app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update logo to Cart
text = text.replace(
    "<div style='font-size:2.2rem'>💠</div>",
    "<div style='font-size:2.2rem'>🛒</div>"
)

# 2. Update Assistant Name to StockSense Copilot
text = text.replace('"🤖 Nexus AI Copilot"', '"🤖 StockSense Copilot"')
text = text.replace('<h1>🤖 Nexus AI Copilot</h1>', '<h1>🤖 StockSense Copilot</h1>')
text = text.replace("Hi! I'm Nexus AI.", "Hi! I'm StockSense Copilot.")
text = text.replace("Hi! I'm Nexus AI Copilot.", "Hi! I'm StockSense Copilot.")

# 3. Add products logic
target = 'def chatbot_response(query: str, df: pd.DataFrame) -> str:\n    """Rule-based inventory chatbot."""\n    q = query.lower().strip()\n    latest = df.sort_values("date").groupby(["product_id","product_name"]).last().reset_index()'

new_logic = target + '''

    if any(k in q for k in ["products", "product", "items", "what do i have", "things i have", "sell", "inventory list", "what are the"]):
        total_types = df["product_name"].nunique()
        cats = ", ".join(df["category"].dropna().unique())
        return (f"🛒 You currently sell **{total_types} unique products** across categories like: *{cats}*.\\n\\n"
                 "To see the full detailed list of every single product you have intuitively organized, navigate to your **Executive Dashboard** or **Business Summary** tab!")'''

text = text.replace(target, new_logic)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print('Chatbot updated with products catalog logic and new name.')
