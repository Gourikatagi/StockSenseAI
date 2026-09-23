import re
import sys

file_path = r'c:\Users\hp\Desktop\StockSense AI\files\app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# I need to completely replace the cache_data block for load_sample_data
# Let's extract the target string block
start_sig = '@st.cache_data(show_spinner=False)\ndef load_sample_data():'
end_sig = 'def clean_data(df: pd.DataFrame)'

if start_sig not in text or end_sig not in text:
    print("Signatures not found!")
    sys.exit(1)

start_idx = text.find(start_sig)
end_idx = text.find(end_sig)

target_block = text[start_idx:end_idx]

new_block = '''@st.cache_data(show_spinner=False)
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


'''

text = text.replace(target_block, new_block)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Data Architecture successfully upgraded with Daily mapping, Holidays, Warehouses, and Suppliers!")
