import sys

file_path = r'c:\Users\hp\Desktop\StockSense AI\files\app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Navigation and Tab Strings
replaces = [
    ('"🏠 Executive Dashboard"', '"🌐 Executive Dashboard"'),
    ('"📈 Time-Series Forecasting"', '"🔮 AI Demand Forecasting"'),
    ('"🚨 Stock Optimization Alerts"', '"⚡ Real-Time Stock Alerts"'),
    ('"📦 ABC Analysis"', '"📊 ABC Segmentation"'),
    ('"⚙️ Optimization Engine"', '"🧠 AI Optimization Engine"'),
    ('"📄 Business Summary"', '"📑 Executive Summary"'),
    ('<h1>🏠', '<h1>🌐'),
    ('<h1>📈', '<h1>🔮'),
    ('<h1>🚨', '<h1>⚡'),
    ('<h1>📦', '<h1>📊'),
    ('<h1>⚙️', '<h1>🧠'),
    ('<h1>📄 Business & Optimization Summary</h1>', '<h1>📑 Executive Business Summary</h1>'),
    ('<h1>📄', '<h1>📑'),
    ('<h1>📄 Executive Summary</h1>', '<h1>📑 Executive Business Summary</h1>'),
]

for old, new in replaces:
    text = text.replace(old, new)

# 2. Add gradients to H1 to make it vastly more attractive (clean/professional)
grad_replaces = [
    ('<h1>🌐 Executive Dashboard</h1>', "<h1 style='background: -webkit-linear-gradient(45deg, #4f9cf9, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>🌐 Executive Dashboard</h1>"),
    ('<h1>🔮 AI Demand Forecasting</h1>', "<h1 style='background: -webkit-linear-gradient(45deg, #f59e0b, #ef4444); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>🔮 AI Demand Forecasting</h1>"),
    ('<h1>⚡ Real-Time Stock Alerts</h1>', "<h1 style='background: -webkit-linear-gradient(45deg, #ef4444, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>⚡ Real-Time Stock Alerts</h1>"),
    ('<h1>📊 ABC Segmentation</h1>', "<h1 style='background: -webkit-linear-gradient(45deg, #10b981, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>📊 ABC Segmentation</h1>"),
    ('<h1>🧠 AI Optimization Engine</h1>', "<h1 style='background: -webkit-linear-gradient(45deg, #8b5cf6, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>🧠 AI Optimization Engine</h1>"),
    ('<h1>🤖 StockSense Copilot</h1>', "<h1 style='background: -webkit-linear-gradient(45deg, #6366f1, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>🤖 StockSense Copilot</h1>"),
    ('<h1>📑 Executive Business Summary</h1>', "<h1 style='background: -webkit-linear-gradient(45deg, #34d399, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>📑 Executive Business Summary</h1>"),
]

for old, new in grad_replaces:
    text = text.replace(old, new)


with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)
print('Patched emojis and gradients successfully.')
