@echo off
title English Accelerator - Pareja
cd /d "%~dp0"
echo ========================================================
echo   Iniciando English Accelerator para Anderson y su Novia
echo ========================================================
echo.
call .\venv\Scripts\activate.bat
streamlit run app.py
pause
