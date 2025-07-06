@echo off
echo ============================================
echo   ACTUALIZADOR DEL SISTEMA DE SOPORTES
echo ============================================
echo.
echo Este script actualiza automaticamente el sistema
echo cuando se añaden nuevos archivos PDF.
echo.
echo Presiona cualquier tecla para continuar...
pause > nul

python actualizar_sistema.py

echo.
echo ============================================
echo Presiona cualquier tecla para salir...
pause > nul 