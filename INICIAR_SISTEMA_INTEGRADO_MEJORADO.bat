@echo off
chcp 65001 > nul
title Sistema SINES - Integrado Mejorado con Variables de Plantilla
color 0A

echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █      🏗️ SISTEMA INTEGRADO SINES - VERSIÓN MEJORADA         █
echo █                                                              █
echo █        ⚡ Con Variables de Plantilla T22-T23               █
echo █        🔧 Agrupación de Soportes                           █
echo █        📐 Dimensiones Técnicas Completas                   █
echo █        🔗 Isométricos y Relaciones                         █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.

REM Verificar si Python está instalado
py --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado
    echo.
    echo 📥 Descarga Python desde: https://python.org
    echo    Asegurate de marcar "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.

REM Verificar archivos necesarios
echo 🔍 Verificando archivos del sistema...

set "archivos_requeridos=index_isometricos_integrado_mejorado.html support_data_enhanced.json support_pdf_mapping.json template_variables_mapping.json support_dimensions_data.json"

for %%f in (%archivos_requeridos%) do (
    if not exist "%%f" (
        echo ❌ Archivo faltante: %%f
        set "archivos_faltantes=1"
    ) else (
        echo ✅ %%f
    )
)

if defined archivos_faltantes (
    echo.
    echo ⚠️  Algunos archivos están faltantes
    echo 🔧 Ejecutando análisis de variables de plantilla...
    py analyze_template_columns.py
    echo.
)

echo.
echo 🚀 INICIANDO SERVIDOR...
echo.

REM Mostrar información del sistema
echo 📊 CARACTERÍSTICAS DEL SISTEMA MEJORADO:
echo ├─ 🔧 Soportes agrupados por número
echo ├─ 📐 Variables de plantilla (A, B, C, D, E, R, X, Y, EL, N., SH., TEMP)
echo ├─ 🏷️ Códigos de referencia (4a), (4b), (4c), (4d), etc.
echo ├─ 📏 Dimensiones técnicas completas
echo ├─ 🔗 Integración con isométricos
echo ├─ ⚡ Soporte para prefabricados
echo └─ 📊 Estadísticas y filtros avanzados
echo.

echo 🔑 FUNCIONALIDADES PRINCIPALES:
echo ├─ Agrupación inteligente de soportes
echo ├─ Visualización de variables de plantilla con títulos
echo ├─ Mapeo de dimensiones desde Excel T22-T23
echo ├─ Filtros por tipo, dimensiones y contenido
echo ├─ Exportación de resultados
echo └─ Interfaz responsive y moderna
echo.

echo 🌐 ACCESO AL SISTEMA:
echo ├─ URL Principal: http://localhost:8000/index_isometricos_integrado_mejorado.html
echo ├─ Puerto: 8000
echo └─ Navegador: Se abrirá automáticamente
echo.

REM Iniciar servidor seguro completo
echo ⚠️  IMPORTANTE: Este sistema requiere autenticación
echo 🔐 Credenciales de acceso:
echo ├─ admin / sines2024 (Administrador)
echo ├─ supervisor / super2024 (Supervisor)  
echo ├─ operador / op2024 (Operador)
echo └─ sines / sines123 (Usuario)
echo.

echo 🚀 Iniciando servidor seguro...
py server_secure_complete.py

REM Si el servidor se detiene
echo.
echo ⚠️  El servidor se ha detenido
echo.
pause 