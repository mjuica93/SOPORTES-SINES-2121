@echo off
chcp 65001 > nul
cls

echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █      🏗️ SISTEMA INTEGRADO SINES - VERSIÓN FINAL            █
echo █                                                              █
echo █        ⚡ Soportes Agrupados con Variables de Plantilla    █
echo █        🔧 Todas las Pestañas Funcionando                   █
echo █        📐 Isométricos y Relaciones Completas               █
echo █        🔗 Instalaciones y Trazabilidad                     █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████

echo.
echo ✅ Python encontrado
echo.
echo 🔍 Verificando archivos del sistema...
if exist "index_isometricos_integrado_final.html" (
    echo ✅ index_isometricos_integrado_final.html
) else (
    echo ❌ index_isometricos_integrado_final.html NO ENCONTRADO
    goto :error
)

if exist "support_data_enhanced.json" (
    echo ✅ support_data_enhanced.json
) else (
    echo ❌ support_data_enhanced.json NO ENCONTRADO
    goto :error
)

if exist "support_pdf_mapping.json" (
    echo ✅ support_pdf_mapping.json
) else (
    echo ❌ support_pdf_mapping.json NO ENCONTRADO
    goto :error
)

if exist "template_variables_mapping.json" (
    echo ✅ template_variables_mapping.json
) else (
    echo ❌ template_variables_mapping.json NO ENCONTRADO
    goto :error
)

if exist "support_dimensions_data.json" (
    echo ✅ support_dimensions_data.json
) else (
    echo ❌ support_dimensions_data.json NO ENCONTRADO
    goto :error
)

echo.
echo 🚀 INICIANDO SERVIDOR...
echo.
echo 📊 CARACTERÍSTICAS DEL SISTEMA FINAL:
echo ├─ 🔧 Soportes agrupados por número
echo ├─ 📐 Variables de plantilla (A, B, C, D, E, R, X, Y, EL, N., SH., TEMP)
echo ├─ 🏷️ Códigos de referencia (4a), (4b), (4c), (4d), etc.
echo ├─ 📏 Dimensiones técnicas completas
echo ├─ 🔗 Integración con isométricos
echo ├─ ⚡ Soporte para prefabricados
echo ├─ 🔧 Gestión de instalaciones
echo ├─ 🔗 Relaciones soportes-isométricos
echo └─ 📊 Estadísticas y filtros avanzados
echo.
echo 🔑 FUNCIONALIDADES PRINCIPALES:
echo ├─ Vista individual y agrupada de soportes
echo ├─ Variables de plantilla con títulos descriptivos
echo ├─ Mapeo directo entre Excel T22-T23 y PDFs
echo ├─ Todas las pestañas funcionando correctamente
echo ├─ Filtros avanzados por tipo, dimensiones y contenido
echo ├─ Exportación de resultados
echo └─ Interfaz responsive y moderna
echo.
echo 🌐 ACCESO AL SISTEMA:
echo ├─ URL Principal: http://localhost:8000/index_isometricos_integrado_final.html
echo ├─ Puerto: 8000
echo └─ Navegador: Se abrirá automáticamente
echo.
echo ⚠️  IMPORTANTE: Este sistema requiere autenticación
echo.
echo 🔐 Credenciales de acceso:
echo ├─ admin / sines2024 (Administrador)
echo ├─ supervisor / super2024 (Supervisor)
echo ├─ operador / op2024 (Operador)
echo └─ sines / sines123 (Usuario)
echo.
echo 🚀 Iniciando servidor seguro...
echo.

python server_secure_complete.py
if errorlevel 1 (
    echo.
    echo ❌ Error: %errorlevel%
    echo ⚠️  El servidor se ha detenido
    goto :end
)

:error
echo.
echo ❌ Error: Archivos necesarios no encontrados
echo 📋 Verifica que todos los archivos JSON estén en el directorio
echo.

:end
pause 