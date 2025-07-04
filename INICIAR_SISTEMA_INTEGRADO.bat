@echo off
title Sistema Integrado SINES v3.0 - Completo con Instalaciones
color 0A

echo ========================================================
echo       SISTEMA INTEGRADO SINES - VERSION 3.0
echo   Soportes, Isometricos, Relaciones e Instalaciones
echo ========================================================
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

:: Mostrar funcionalidades disponibles
echo [FUNCIONALIDADES] Sistema integrado incluye:
echo   📋 Gestion de Soportes con PDFs
echo   📐 Visualizacion de Isometricos  
echo   🔗 Relaciones Soportes-Isometricos
echo   🔧 Control de Instalaciones
echo   📊 Trazabilidad Completa
echo   ⚡ Busqueda Paginada (12 resultados por pagina)
echo.

:: Mostrar estadisticas del sistema
echo [ESTADISTICAS] Mostrando resumen del sistema...
python -c "
import json
import os

try:
    # Cargar datos de soportes
    with open('support_data.json', 'r', encoding='utf-8') as f:
        supports = json.load(f)
    print(f'   🔧 Total de soportes: {len(supports):,}')
    
    # Cargar datos de isometricos
    if os.path.exists('isometric_data.json'):
        with open('isometric_data.json', 'r', encoding='utf-8') as f:
            isometrics = json.load(f)
        total_sheets = sum(len(line.get('sheets', [])) for line in isometrics.values())
        print(f'   📐 Lineas de isometricos: {len(isometrics):,}')
        print(f'   📄 Total hojas PDF: {total_sheets:,}')
    
    # Cargar relaciones
    if os.path.exists('support_isometric_relation.json'):
        with open('support_isometric_relation.json', 'r', encoding='utf-8') as f:
            relations = json.load(f)
        print(f'   🔗 Relaciones establecidas: {len(relations):,}')
        coverage = (len(relations) / len(supports)) * 100 if supports else 0
        print(f'   📊 Cobertura de relaciones: {coverage:.1f}%')
    
    print('   ✅ Sistema listo para uso')
    
except Exception as e:
    print(f'   ⚠️  Error cargando estadisticas: {e}')
"

echo.

:: Iniciar servidor web
echo [INFO] Iniciando servidor web en puerto 8080...
echo [INFO] El sistema estara disponible en: http://localhost:8080
echo.
echo [INTERFAZ] Acceso directo al sistema integrado:
echo   📱 URL: http://localhost:8080/index_isometricos_con_costuras.html
echo.
echo [IMPORTANTE] Para detener el servidor, presiona Ctrl+C
echo [NOTA] Los datos de instalaciones se guardan automaticamente
echo.

:: Abrir navegador automaticamente
timeout /t 3 /nobreak >nul
start http://localhost:8080/index_isometricos_con_costuras.html

:: Iniciar servidor Python
python -m http.server 8080 