@echo off
cd /d "C:\Users\robbd\Documents\Git\Technical Task – Mobile Full-Stack"
call venv\Scripts\activate.bat
python -m uvicorn app.main:app --reload --port 8000
pause
