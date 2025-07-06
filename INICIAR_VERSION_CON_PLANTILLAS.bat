@echo off
title Sistema de Soportes SINES - Version con Variables de Plantilla
echo ========================================================
echo    SISTEMA DE SOPORTES SINES - VERSION CON PLANTILLAS
echo ========================================================
echo.
echo Esta version incluye:
echo   * Variables de plantilla extraidas del Excel (A, B, C, D, E, R, X, Y, EL, N., SH.)
echo   * Titulos descriptivos para cada variable
echo   * Valores con unidades (mm, grados C)
echo   * Seccion especifica "Variables de Plantilla"
echo   * Facilita la interpretacion de los PDFs tecnicos
echo.
echo Iniciando servidor web local...
echo.
echo URL: http://localhost:8000/index_enhanced_with_templates.html
echo.
echo Para detener el servidor, presiona Ctrl+C
echo ========================================================
echo.

start "" "http://localhost:8000/index_enhanced_with_templates.html"
python server.py
pause 