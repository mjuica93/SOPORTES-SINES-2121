@echo off
title Sistema SINES - Subir Funcionalidad
color 0A

echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █              SUBIR FUNCIONALIDAD A PRODUCCIÓN               █
echo █                                                              █
echo █                ⚡ DESPLIEGUE SEGURO                          █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.

echo 🔍 VERIFICACIONES PRE-DESPLIEGUE
echo.

REM Verificar que estamos en el directorio correcto
if not exist "server_railway.py" (
    echo ❌ Error: No estás en el directorio del proyecto SINES
    pause
    exit /b 1
)

REM Verificar Git
git --version >nul 2>&1
if errorlevel 1 (
    set "PATH=%PATH%;C:\Program Files\Git\cmd"
)

echo ✅ Directorio del proyecto verificado
echo.

REM Verificar que no estamos en main
for /f "tokens=*" %%i in ('git branch --show-current') do set current_branch=%%i

if "%current_branch%"=="main" (
    echo ❌ PELIGRO: Estás en la rama 'main'
    echo.
    echo 🚨 NO debes hacer cambios directamente en main
    echo 💡 Ejecuta primero: NUEVA_FUNCIONALIDAD.bat
    echo.
    pause
    exit /b 1
)

echo ✅ Estás en la rama: %current_branch%
echo.

echo 🧪 PRUEBAS OBLIGATORIAS ANTES DE SUBIR
echo.
echo ⚠️  IMPORTANTE: Tu funcionalidad debe pasar todas estas pruebas
echo.

echo 📋 Checklist de pruebas locales:
echo.
echo   1. ✅ ¿Has probado que la página principal carga correctamente?
echo   2. ✅ ¿La búsqueda sigue funcionando?
echo   3. ✅ ¿Los PDFs se abren sin problemas?
echo   4. ✅ ¿La versión móvil funciona correctamente?
echo   5. ✅ ¿Tu nueva funcionalidad funciona como esperabas?
echo   6. ✅ ¿No hay errores en la consola del navegador?
echo.

set /p tests_passed="🎯 ¿Han pasado TODAS las pruebas? (S/N): "

if /i not "%tests_passed%"=="S" (
    echo.
    echo ⚠️  NO subas funcionalidad que no ha sido probada
    echo.
    echo 💡 Para probar localmente:
    echo    1. Ejecuta: python server_railway.py
    echo    2. Ve a: http://localhost:8000
    echo    3. Prueba todas las funcionalidades
    echo    4. Corrige cualquier error
    echo    5. Vuelve a ejecutar este script
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Pruebas confirmadas
echo.

echo 📝 Describe brevemente tu funcionalidad:
echo.
echo Ejemplos:
echo   - "Añadida búsqueda por categoría"
echo   - "Mejorada interfaz móvil"
echo   - "Corregido error en carga de PDFs"
echo   - "Añadido modo oscuro"
echo.
set /p commit_message="📋 Descripción de la funcionalidad: "

if "%commit_message%"=="" (
    echo ❌ Debes describir los cambios realizados
    pause
    exit /b 1
)

echo.
echo 💾 GUARDANDO CAMBIOS...
echo.

REM Añadir todos los cambios
git add .

if errorlevel 1 (
    echo ❌ Error añadiendo archivos
    pause
    exit /b 1
)

REM Hacer commit
git commit -m "feat: %commit_message%"

if errorlevel 1 (
    echo ❌ Error haciendo commit
    echo 💡 ¿Hay cambios para guardar?
    pause
    exit /b 1
)

echo ✅ Cambios guardados localmente
echo.

echo 🚀 SUBIENDO A GITHUB...
echo.

REM Subir rama a GitHub
git push origin %current_branch%

if errorlevel 1 (
    echo ❌ Error subiendo a GitHub
    pause
    exit /b 1
)

echo ✅ Rama subida a GitHub
echo.

echo 🔀 CREANDO PULL REQUEST...
echo.

echo 📋 Opciones para merge a producción:
echo.
echo   A) 🔄 MERGE AUTOMÁTICO (directo a main)
echo      - Más rápido
echo      - Riesgo medio
echo.
echo   B) 📋 PULL REQUEST (recomendado)
echo      - Más seguro
echo      - Permite revisión
echo.

set /p merge_option="🎯 Selecciona opción (A/B): "

if /i "%merge_option%"=="A" (
    goto :auto_merge
) else (
    goto :pull_request
)

:auto_merge
echo.
echo ⚡ MERGE AUTOMÁTICO A MAIN...
echo.

REM Cambiar a main
git checkout main

REM Actualizar main
git pull origin main

REM Merge de la rama feature
git merge %current_branch%

if errorlevel 1 (
    echo ❌ Error en merge automático
    echo 💡 Hay conflictos que resolver manualmente
    echo 🔧 Resuelve los conflictos y ejecuta: git commit
    pause
    exit /b 1
)

REM Subir main actualizado
git push origin main

if errorlevel 1 (
    echo ❌ Error subiendo main
    pause
    exit /b 1
)

echo ✅ ¡Funcionalidad desplegada automáticamente!
goto :success

:pull_request
echo.
echo 📋 CREANDO PULL REQUEST...
echo.

REM Abrir GitHub para crear Pull Request
start https://github.com/mjuica93/SOPORTES-SINES-2121/compare/%current_branch%?expand=1

echo ✅ GitHub abierto para crear Pull Request
echo.
echo 📋 Pasos en GitHub:
echo   1. Revisa los cambios mostrados
echo   2. Añade título descriptivo
echo   3. Describe la funcionalidad en detalle
echo   4. Clic en "Create Pull Request"
echo   5. Clic en "Merge Pull Request" cuando esté listo
echo.

echo 🎯 Una vez que hagas merge en GitHub, Railway desplegará automáticamente

:success
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo 🎉 ¡PROCESO COMPLETADO!
echo.
echo 🚀 QUÉ PASA AHORA:
echo.
echo   1. 🔄 Railway detecta el cambio en 'main'
echo   2. 🏗️  Inicia build automático (2-3 minutos)
echo   3. 🌍 Despliega nueva versión a producción
echo   4. ✅ Tu funcionalidad estará disponible mundialmente
echo.

echo 📊 MONITOREO:
echo   • Dashboard Railway: Logs del build
echo   • GitHub: Historial de cambios
echo   • Producción: Probar nueva funcionalidad
echo.

echo 🌐 Para verificar que todo funciona:
echo   1. Espera 3-5 minutos (tiempo de build)
echo   2. Ve a tu URL de Railway
echo   3. Prueba la nueva funcionalidad
echo   4. Verifica que todo sigue funcionando
echo.

echo 💡 PRÓXIMOS PASOS:
echo   • Para nueva funcionalidad: NUEVA_FUNCIONALIDAD.bat
echo   • Para emergency rollback: ROLLBACK_EMERGENCY.bat
echo   • Para ver estado: git status
echo.

echo ⚠️  IMPORTANTE:
echo   Si algo falla en producción, ve inmediatamente al
echo   dashboard de Railway para revisar los logs de error.
echo.

pause 