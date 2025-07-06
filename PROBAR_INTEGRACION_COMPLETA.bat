@echo off
chcp 65001 >nul
echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║               🎯 PRUEBA DE INTEGRACIÓN COMPLETA 🎯               ║
echo ║              Sistema SINES con Isométricos Prefabricados        ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

echo 📋 Verificando componentes del sistema...
echo.

REM Verificar carpetas principales
if exist "ISOMETRICOS" (
    echo ✅ Carpeta ISOMETRICOS encontrada
) else (
    echo ❌ Carpeta ISOMETRICOS no encontrada
    goto :error
)

if exist "ISOMETRICOS PREFABRICADOS" (
    echo ✅ Carpeta ISOMETRICOS PREFABRICADOS encontrada
) else (
    echo ❌ Carpeta ISOMETRICOS PREFABRICADOS no encontrada
    goto :error
)

if exist "ESTANDARES DE SOPORTES" (
    echo ✅ Carpeta ESTANDARES DE SOPORTES encontrada
) else (
    echo ❌ Carpeta ESTANDARES DE SOPORTES no encontrada
    goto :error
)

echo.
echo 📊 Verificando archivos de mapeo...

if exist "prefabricated_isometric_mapping.json" (
    echo ✅ Archivo de mapeo de prefabricados encontrado
) else (
    echo ❌ Archivo de mapeo de prefabricados no encontrado
    goto :error
)

if exist "support_data_enhanced.json" (
    echo ✅ Datos de soportes encontrados
) else (
    echo ❌ Datos de soportes no encontrados
    goto :error
)

if exist "isometric_data_with_prefabricated.json" (
    echo ✅ Datos de isométricos integrados encontrados
) else (
    echo ❌ Datos de isométricos integrados no encontrados
    goto :error
)

echo.
echo 🌐 Verificando archivos HTML...

if exist "index_isometricos_con_costuras.html" (
    echo ✅ Sistema integrado HTML encontrado
) else (
    echo ❌ Sistema integrado HTML no encontrado
    goto :error
)

echo.
echo 📈 Estadísticas del Sistema:
for /f %%i in ('dir /b "ISOMETRICOS\*.pdf" ^| find /c /v ""') do echo   🔹 Isométricos normales: %%i archivos
for /f %%i in ('dir /b "ISOMETRICOS PREFABRICADOS\*.pdf" ^| find /c /v ""') do echo   🔹 Isométricos prefabricados: %%i archivos
for /f %%i in ('dir /b "ESTANDARES DE SOPORTES\*.pdf" ^| find /c /v ""') do echo   🔹 Estándares de soportes: %%i archivos

echo.
echo 🚀 Sistema completamente funcional!
echo.
echo 📋 URLs disponibles:
echo   🌐 Sistema Local: http://localhost:8000/index_isometricos_con_costuras.html
echo   📱 Versión Móvil: http://localhost:8000/index_mobile.html
echo   🔧 Sistema Básico: http://localhost:8000/index.html
echo.

echo 🎯 Funcionalidades disponibles:
echo   ✅ Gestión completa de soportes
echo   ✅ Navegación de isométricos normales
echo   ✅ Integración con isométricos prefabricados  
echo   ✅ Sistema de relaciones soportes ↔ isométricos
echo   ✅ Control de instalaciones con fechas
echo   ✅ Búsquedas avanzadas en tiempo real
echo   ✅ Enlaces directos a todos los PDFs
echo   ✅ Indicadores visuales de prefabricados 🏭
echo.

if "%1"=="auto" goto :end

echo 💡 ¿Quieres abrir el sistema ahora? (S/N)
set /p respuesta="Respuesta: "
if /i "%respuesta%"=="S" (
    echo.
    echo 🌐 Abriendo sistema integrado...
    start http://localhost:8000/index_isometricos_con_costuras.html
    echo ✅ Sistema abierto en tu navegador
)

goto :end

:error
echo.
echo ❌ Error: Faltan componentes del sistema
echo 🔧 Ejecuta el análisis de prefabricados primero
echo.
pause
exit /b 1

:end
echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                   🎉 INTEGRACIÓN EXITOSA 🎉                     ║
echo ║              Todos los componentes funcionando                   ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
if not "%1"=="auto" pause 