@echo off
title Sistema SINES - Pruebas Locales
color 0B

echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █                 PRUEBAS LOCALES SISTEMA                     █
echo █                                                              █
echo █                  🧪 TESTING COMPLETO                        █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.

echo 🎯 PRUEBAS SISTEMÁTICAS ANTES DEL DESPLIEGUE
echo.

REM Verificar que estamos en el directorio correcto
if not exist "server_railway.py" (
    echo ❌ Error: No estás en el directorio del proyecto SINES
    pause
    exit /b 1
)

echo ✅ Directorio del proyecto verificado
echo.

echo 🔍 VERIFICANDO ARCHIVOS CRÍTICOS...
echo.

REM Verificar archivos esenciales
set "missing_files="

if not exist "index.html" (
    set "missing_files=%missing_files% index.html"
)
if not exist "app.js" (
    set "missing_files=%missing_files% app.js"
)
if not exist "server_railway.py" (
    set "missing_files=%missing_files% server_railway.py"
)
if not exist "support_data_enhanced.json" (
    set "missing_files=%missing_files% support_data_enhanced.json"
)

if not "%missing_files%"=="" (
    echo ❌ Archivos críticos faltantes:%missing_files%
    pause
    exit /b 1
)

echo ✅ Todos los archivos críticos presentes
echo.

echo 🚀 INICIANDO SERVIDOR LOCAL...
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado
    echo 💡 Asegúrate de tener Python instalado
    pause
    exit /b 1
)

echo ✅ Python disponible
echo.

echo 🌐 Iniciando servidor en http://localhost:8000
echo.
echo ⚠️  IMPORTANTE: 
echo   • El servidor se iniciará en una nueva ventana
echo   • NO cierres esa ventana durante las pruebas
echo   • Usa este menú para guiar tus pruebas
echo.

REM Iniciar servidor en nueva ventana
start "SINES Local Server" cmd /k "python server_railway.py"

echo ⏱️  Esperando que el servidor inicie...
timeout /t 3 >nul

echo.
echo 🔗 Abriendo navegador...
start http://localhost:8000

timeout /t 2 >nul

echo.
echo ═══════════════════════════════════════════════════════════════
echo 🧪 CHECKLIST DE PRUEBAS OBLIGATORIAS
echo ═══════════════════════════════════════════════════════════════
echo.

echo 📋 Sigue estas pruebas paso a paso:
echo.

:test_menu
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 🧪 PRUEBAS A REALIZAR:
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo   1. 🌐 PROBAR PÁGINA PRINCIPAL
echo   2. 🔍 PROBAR BÚSQUEDA BÁSICA
echo   3. 📄 PROBAR APERTURA DE PDFS
echo   4. 📱 PROBAR VERSIÓN MÓVIL
echo   5. ⚡ PROBAR NUEVA FUNCIONALIDAD
echo   6. 🔍 VERIFICAR CONSOLA (ERRORES)
echo   7. ✅ FINALIZAR PRUEBAS
echo.
echo   0. ❌ CERRAR SERVIDOR Y SALIR
echo.

set /p test_option="🎯 Selecciona prueba (0-7): "

if "%test_option%"=="1" goto :test_main
if "%test_option%"=="2" goto :test_search
if "%test_option%"=="3" goto :test_pdfs
if "%test_option%"=="4" goto :test_mobile
if "%test_option%"=="5" goto :test_feature
if "%test_option%"=="6" goto :test_console
if "%test_option%"=="7" goto :test_complete
if "%test_option%"=="0" goto :cleanup

echo ❌ Opción no válida
timeout /t 1 >nul
goto :test_menu

:test_main
echo.
echo 🌐 PRUEBA 1: PÁGINA PRINCIPAL
echo ════════════════════════════════════════════════════════════════
echo.
echo 📋 Verifica lo siguiente:
echo   ✅ La página carga sin errores
echo   ✅ Se ve el título "Sistema de Búsqueda de Soportes SINES"
echo   ✅ El campo de búsqueda está visible
echo   ✅ No hay mensajes de error
echo   ✅ El diseño se ve correcto
echo.
echo 🔗 URL: http://localhost:8000
echo.
set /p test1_result="✅ ¿Página principal funciona correctamente? (S/N): "
echo.
goto :test_menu

:test_search
echo.
echo 🔍 PRUEBA 2: BÚSQUEDA BÁSICA
echo ════════════════════════════════════════════════════════════════
echo.
echo 📋 Prueba estas búsquedas:
echo   1. Busca: "BA01"
echo   2. Busca: "BE01" 
echo   3. Busca: "soporte"
echo   4. Busca: "general"
echo.
echo ✅ Verifica que:
echo   • Aparecen resultados
echo   • Los resultados son relevantes
echo   • La búsqueda es rápida
echo   • No hay errores
echo.
set /p test2_result="✅ ¿Búsqueda funciona correctamente? (S/N): "
echo.
goto :test_menu

:test_pdfs
echo.
echo 📄 PRUEBA 3: APERTURA DE PDFs
echo ════════════════════════════════════════════════════════════════
echo.
echo 📋 Prueba abrir PDFs:
echo   1. Busca "BA01" y haz clic en el resultado
echo   2. Verifica que el PDF se abre/descarga
echo   3. Prueba con otro soporte diferente
echo.
echo ✅ Verifica que:
echo   • Los PDFs se abren correctamente
echo   • Las URLs de PDFs son correctas
echo   • No hay errores 404
echo.
set /p test3_result="✅ ¿PDFs se abren correctamente? (S/N): "
echo.
goto :test_menu

:test_mobile
echo.
echo 📱 PRUEBA 4: VERSIÓN MÓVIL
echo ════════════════════════════════════════════════════════════════
echo.
echo 🔗 Abriendo versión móvil...
start http://localhost:8000/mobile
echo.
echo 📋 Verifica lo siguiente:
echo   ✅ Interfaz optimizada para móvil
echo   ✅ Búsqueda funciona en móvil
echo   ✅ Botones son táctiles
echo   ✅ Texto es legible
echo   ✅ No hay elementos cortados
echo.
echo 💡 Puedes redimensionar la ventana del navegador para simular móvil
echo.
set /p test4_result="✅ ¿Versión móvil funciona correctamente? (S/N): "
echo.
goto :test_menu

:test_feature
echo.
echo ⚡ PRUEBA 5: NUEVA FUNCIONALIDAD
echo ════════════════════════════════════════════════════════════════
echo.
echo 📋 Prueba tu nueva funcionalidad específica:
echo.
echo 💡 Esta prueba depende de lo que hayas desarrollado:
echo   • Si añadiste filtros, pruébalos
echo   • Si mejoraste la interfaz, verifica los cambios
echo   • Si añadiste nuevas páginas, navega a ellas
echo   • Si corregiste errores, verifica que estén solucionados
echo.
echo ⚠️  IMPORTANTE: Esta es la prueba más crítica
echo.
set /p test5_result="✅ ¿Tu nueva funcionalidad funciona correctamente? (S/N): "
echo.
goto :test_menu

:test_console
echo.
echo 🔍 PRUEBA 6: VERIFICAR CONSOLA
echo ════════════════════════════════════════════════════════════════
echo.
echo 📋 Verifica la consola del navegador:
echo.
echo 🛠️  Cómo abrir la consola:
echo   • Chrome/Edge: F12 → Console
echo   • Firefox: F12 → Console
echo   • Safari: Cmd+Alt+I → Console
echo.
echo ✅ Verifica que NO hay:
echo   • Errores en rojo
echo   • Warnings importantes
echo   • Mensajes de archivos no encontrados
echo   • Errores JavaScript
echo.
echo 💡 Errores menores como "favicon.ico not found" son normales
echo.
set /p test6_result="✅ ¿No hay errores importantes en consola? (S/N): "
echo.
goto :test_menu

:test_complete
echo.
echo ✅ PRUEBAS COMPLETADAS
echo ════════════════════════════════════════════════════════════════
echo.
echo 📊 RESUMEN DE RESULTADOS:
echo.

if not defined test1_result set test1_result=❓
if not defined test2_result set test2_result=❓
if not defined test3_result set test3_result=❓
if not defined test4_result set test4_result=❓
if not defined test5_result set test5_result=❓
if not defined test6_result set test6_result=❓

echo   1. Página principal: %test1_result%
echo   2. Búsqueda básica: %test2_result%
echo   3. Apertura PDFs: %test3_result%
echo   4. Versión móvil: %test4_result%
echo   5. Nueva funcionalidad: %test5_result%
echo   6. Sin errores consola: %test6_result%
echo.

REM Verificar si todas las pruebas pasaron
set "all_passed=true"
if /i not "%test1_result%"=="S" set "all_passed=false"
if /i not "%test2_result%"=="S" set "all_passed=false"
if /i not "%test3_result%"=="S" set "all_passed=false"
if /i not "%test4_result%"=="S" set "all_passed=false"
if /i not "%test5_result%"=="S" set "all_passed=false"
if /i not "%test6_result%"=="S" set "all_passed=false"

if "%all_passed%"=="true" (
    echo 🎉 ¡TODAS LAS PRUEBAS PASARON!
    echo.
    echo ✅ Tu funcionalidad está lista para producción
    echo.
    echo 🚀 PRÓXIMO PASO: Ejecuta SUBIR_FUNCIONALIDAD.bat
    echo.
) else (
    echo ⚠️  ALGUNAS PRUEBAS FALLARON
    echo.
    echo ❌ NO subas a producción hasta corregir los problemas
    echo.
    echo 🔧 ACCIONES RECOMENDADAS:
    echo   1. Corrige los problemas identificados
    echo   2. Vuelve a ejecutar este script
    echo   3. Solo sube cuando todas las pruebas pasen
    echo.
)

echo ════════════════════════════════════════════════════════════════
echo.
set /p continue_testing="🔄 ¿Quieres continuar probando? (S/N): "

if /i "%continue_testing%"=="S" goto :test_menu

:cleanup
echo.
echo 🛑 CERRANDO SERVIDOR LOCAL...
echo.

REM Intentar cerrar el servidor local
taskkill /f /im python.exe /fi "WINDOWTITLE eq SINES Local Server*" >nul 2>&1

echo ✅ Servidor local cerrado
echo.
echo 💡 RESUMEN:
echo   • Pruebas locales completadas
echo   • Servidor cerrado
echo   • Listo para el siguiente paso
echo.

echo 🎯 PRÓXIMOS PASOS:
echo   • Si todo funciona: SUBIR_FUNCIONALIDAD.bat
echo   • Si hay problemas: Corregir y probar nuevamente
echo   • Para nueva funcionalidad: NUEVA_FUNCIONALIDAD.bat
echo.

pause 