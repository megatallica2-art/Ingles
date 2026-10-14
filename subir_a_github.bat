@echo off
title Subir a GitHub - English Together
cd /d "%~dp0"
echo ========================================================
echo   Subiendo tu proyecto a GitHub:
echo   https://github.com/megatallica2-art/Ingles
echo ========================================================
echo.
echo Enviando archivos a GitHub...
git push -u origin main
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Si el repositorio en GitHub ya tenia un README o archivos previos:
    git push -u origin main --force
)
echo.
echo ========================================================
echo   Proceso finalizado. Revisa tu repositorio en GitHub!
echo ========================================================
pause
