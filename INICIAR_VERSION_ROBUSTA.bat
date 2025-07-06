@echo off
title Sistema de Soportes SINES - Version Robusta
echo ================================================
echo    SISTEMA DE SOPORTES SINES - VERSION ROBUSTA
echo ================================================
echo.
echo Iniciando servidor web local...
echo.
echo URLs disponibles:
echo   Version Robusta: http://localhost:8000/index_enhanced_robust.html
echo   Version Normal:  http://localhost:8000/index_enhanced.html
echo   Version Basica:  http://localhost:8000/index.html
echo.
echo Para detener el servidor, presiona Ctrl+C
echo ================================================
echo.

start "" "http://localhost:8000/index_enhanced_robust.html"
python server.py
pause