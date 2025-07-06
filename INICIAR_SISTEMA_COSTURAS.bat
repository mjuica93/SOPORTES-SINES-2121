@echo off
title Sistema Integrado SINES - Soportes e Isometricos
color 0A

echo ====================================================
echo       SISTEMA INTEGRADO SINES - VERSION 2.0
echo        Soportes, Isometricos y Relaciones
echo ====================================================
echo.

:: Verificar si existe Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no se encuentra en el PATH
    echo Por favor instala Python desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Verificar archivos necesarios
echo [INFO] Verificando archivos necesarios...

if not exist "support_data.json" (
    echo [ADVERTENCIA] No se encuentra support_data.json
    echo Ejecutando extraccion de datos de soportes...
    python extract_support_data_final.py
)

if not exist "support_pdf_mapping.json" (
    echo [ADVERTENCIA] No se encuentra support_pdf_mapping.json
    echo Creando mapeo de PDFs de soportes...
    python create_support_mapping.py
)

if not exist "isometric_data.json" (
    echo [ADVERTENCIA] No se encuentra isometric_data.json
    echo Analizando estructura de isometricos...
    python analyze_isometric_structure.py
)

if not exist "support_isometric_relation.json" (
    echo [ADVERTENCIA] No se encuentra support_isometric_relation.json
    echo Creando relaciones soportes-isometricos...
    python -c "from analyze_isometric_structure import analyze_isometric_structure; analyze_isometric_structure()"
)

echo [INFO] Todos los archivos necesarios estan disponibles.
echo.

:: Iniciar servidor web
echo [INFO] Iniciando servidor web en puerto 8080...
echo [INFO] El sistema estara disponible en: http://localhost:8080
echo.
echo [IMPORTANTE] Para detener el servidor, presiona Ctrl+C
echo.

:: Abrir navegador automaticamente
timeout /t 3 /nobreak >nul
start http://localhost:8080/index_isometricos_con_costuras.html

:: Iniciar servidor Python
python -m http.server 8080

pause 