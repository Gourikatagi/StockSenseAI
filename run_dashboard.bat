@echo off
echo ==============================================
echo   StockSense AI - Dashboard Initializer
echo ==============================================
echo.
echo Installing required components... (This might take a few minutes)
python -m pip install --only-binary :all: -r requirements.txt
echo.
echo Launching the Dashboard...
python -m streamlit run app.py
pause
