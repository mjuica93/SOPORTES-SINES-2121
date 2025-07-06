@echo off
title Sistema SINES - Rollback de Emergencia
color 0C

echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █                  ROLLBACK DE EMERGENCIA                     █
echo █                                                              █
echo █                  🚨 RESTAURAR PRODUCCIÓN                     █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.

echo 🚨 ALERTA: ROLLBACK DE EMERGENCIA ACTIVADO
echo.
echo ⚠️  ADVERTENCIA: Este script revierte cambios en producción
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
    git --version >nul 2>&1
    if errorlevel 1 (
        echo ❌ Git no encontrado
        pause
        exit /b 1
    )
)

echo ✅ Directorio y Git verificados
echo.

echo 🔍 SITUACIÓN ACTUAL:
echo.

REM Mostrar rama actual
for /f "tokens=*" %%i in ('git branch --show-current') do set current_branch=%%i
echo 🌿 Rama actual: %current_branch%

REM Mostrar últimos commits
echo.
echo 📋 ÚLTIMOS COMMITS EN MAIN:
echo ════════════════════════════════════════════════════════════════
git log --oneline -5 main
echo ════════════════════════════════════════════════════════════════
echo.

echo 🚨 MOTIVO DEL ROLLBACK:
echo.
echo ¿Qué problema está ocurriendo en producción?
echo.
echo Ejemplos:
echo   - "La página no carga"
echo   - "Búsqueda rota"
echo   - "PDFs no se abren"
echo   - "Error 500 en servidor"
echo   - "Funcionalidad nueva no funciona"
echo.
set /p problem_description="📝 Describe el problema: "

if "%problem_description%"=="" (
    echo ❌ Debes describir el problema
    pause
    exit /b 1
)

echo.
echo 🔄 OPCIONES DE ROLLBACK:
echo.
echo   1. 🔙 ROLLBACK RÁPIDO (1 commit atrás)
echo      - Revierte solo el último cambio
echo      - Más rápido y seguro
echo.
echo   2. 🔍 ROLLBACK ESPECÍFICO (elegir commit)
echo      - Revierte a un commit específico
echo      - Más control, pero más complejo
echo.
echo   3. 🚨 ROLLBACK TOTAL (versión estable conocida)
echo      - Revierte a una versión que sabemos funciona
echo      - Máxima seguridad
echo.
echo   0. ❌ CANCELAR ROLLBACK
echo.

set /p rollback_option="🎯 Selecciona opción (0-3): "

if "%rollback_option%"=="1" goto :quick_rollback
if "%rollback_option%"=="2" goto :specific_rollback
if "%rollback_option%"=="3" goto :total_rollback
if "%rollback_option%"=="0" goto :cancel

echo ❌ Opción no válida
timeout /t 1 >nul
goto :rollback_menu

:quick_rollback
echo.
echo 🔙 ROLLBACK RÁPIDO (1 COMMIT ATRÁS)
echo ════════════════════════════════════════════════════════════════
echo.

echo 🔍 Commit actual que se va a revertir:
git log --oneline -1 main
echo.

echo ⚠️  CONFIRMACIÓN FINAL:
echo.
echo Este rollback:
echo   • Revierte el último commit
echo   • Activará redeploy automático en Railway
echo   • Restaurará la versión anterior
echo.
echo 💡 La versión anterior será restaurada en 2-3 minutos
echo.

set /p confirm_quick="🚨 ¿Confirmas rollback rápido? (SI/NO): "

if /i not "%confirm_quick%"=="SI" (
    echo ❌ Rollback cancelado
    pause
    exit /b 1
)

echo.
echo ⏳ EJECUTANDO ROLLBACK RÁPIDO...
echo.

REM Cambiar a main
git checkout main

REM Actualizar main
git pull origin main

REM Rollback 1 commit
git reset --hard HEAD~1

REM Forzar push (peligroso pero necesario en emergencia)
git push --force origin main

if errorlevel 1 (
    echo ❌ Error en rollback
    pause
    exit /b 1
)

echo ✅ Rollback rápido completado
goto :rollback_success

:specific_rollback
echo.
echo 🔍 ROLLBACK ESPECÍFICO
echo ════════════════════════════════════════════════════════════════
echo.

echo 📋 Últimos 10 commits disponibles:
echo ════════════════════════════════════════════════════════════════
git log --oneline -10 main
echo ════════════════════════════════════════════════════════════════
echo.

echo 📝 Copia el HASH del commit al que quieres volver
echo.
echo Ejemplo: 3a2b1c4 (los primeros 7 caracteres)
echo.
set /p target_commit="🎯 Hash del commit objetivo: "

if "%target_commit%"=="" (
    echo ❌ Debes especificar un commit
    pause
    exit /b 1
)

echo.
echo 🔍 Commit objetivo:
git log --oneline -1 %target_commit%

if errorlevel 1 (
    echo ❌ Commit no válido
    pause
    exit /b 1
)

echo.
echo ⚠️  CONFIRMACIÓN FINAL:
echo.
echo Este rollback:
echo   • Revierte a commit: %target_commit%
echo   • Activará redeploy automático en Railway
echo   • PERDERÁ todos los commits posteriores
echo.

set /p confirm_specific="🚨 ¿Confirmas rollback específico? (SI/NO): "

if /i not "%confirm_specific%"=="SI" (
    echo ❌ Rollback cancelado
    pause
    exit /b 1
)

echo.
echo ⏳ EJECUTANDO ROLLBACK ESPECÍFICO...
echo.

REM Cambiar a main
git checkout main

REM Actualizar main
git pull origin main

REM Rollback al commit específico
git reset --hard %target_commit%

REM Forzar push
git push --force origin main

if errorlevel 1 (
    echo ❌ Error en rollback
    pause
    exit /b 1
)

echo ✅ Rollback específico completado
goto :rollback_success

:total_rollback
echo.
echo 🚨 ROLLBACK TOTAL (VERSIÓN ESTABLE)
echo ════════════════════════════════════════════════════════════════
echo.

echo ⚠️  ROLLBACK TOTAL ACTIVADO
echo.
echo Este es el rollback más drástico:
echo   • Revierte a una versión conocida como estable
echo   • Elimina TODOS los cambios recientes
echo   • Restaura funcionalidad básica garantizada
echo.

echo 🔍 Buscando versión estable conocida...
echo.

REM Buscar commits con "Initial commit" o "stable"
echo 📋 Commits potencialmente estables:
git log --oneline --grep="Initial\|stable\|fix\|working" -5 main

echo.
echo 💡 Recomendación: Usar el commit inicial del proyecto
echo.
set /p use_initial="🎯 ¿Usar commit inicial? (S/N): "

if /i "%use_initial%"=="S" (
    REM Obtener primer commit
    for /f "tokens=*" %%i in ('git log --pretty=format:%%H main ^| tail -1') do set initial_commit=%%i
    set target_commit=%initial_commit%
) else (
    set /p target_commit="📝 Especifica hash del commit estable: "
)

if "%target_commit%"=="" (
    echo ❌ No se pudo determinar commit objetivo
    pause
    exit /b 1
)

echo.
echo 🔍 Commit objetivo:
git log --oneline -1 %target_commit%

echo.
echo 🚨 CONFIRMACIÓN CRÍTICA:
echo.
echo ATENCIÓN: Este rollback:
echo   • Revierte a: %target_commit%
echo   • ELIMINA TODO el trabajo reciente
echo   • Restaura versión básica funcional
echo   • Requiere rehacer funcionalidades perdidas
echo.

set /p confirm_total="🚨 ¿CONFIRMAS ROLLBACK TOTAL? (SI/NO): "

if /i not "%confirm_total%"=="SI" (
    echo ❌ Rollback cancelado
    pause
    exit /b 1
)

echo.
echo ⏳ EJECUTANDO ROLLBACK TOTAL...
echo.

REM Cambiar a main
git checkout main

REM Rollback total
git reset --hard %target_commit%

REM Forzar push
git push --force origin main

if errorlevel 1 (
    echo ❌ Error en rollback total
    pause
    exit /b 1
)

echo ✅ Rollback total completado
goto :rollback_success

:rollback_success
echo.
echo ═══════════════════════════════════════════════════════════════
echo 🎉 ROLLBACK COMPLETADO EXITOSAMENTE
echo ═══════════════════════════════════════════════════════════════
echo.

echo 📊 ESTADO ACTUAL:
echo   • Problema: %problem_description%
echo   • Rollback: Ejecutado
echo   • Rama: main restaurada
echo   • Deploy: En proceso (Railway)
echo.

echo 🕒 TIEMPO DE RESTAURACIÓN:
echo   • Railway build: 2-3 minutos
echo   • Sistema online: 3-5 minutos
echo   • Verificación: Inmediata después
echo.

echo 🔍 MONITOREO REQUERIDO:
echo   1. 📊 Dashboard Railway (logs del build)
echo   2. 🌐 URL de producción (verificar funcionalidad)
echo   3. 🔍 Consola del navegador (errores)
echo.

echo 🚀 ACCIONES INMEDIATAS:
echo   • ✅ Esperar 5 minutos
echo   • ✅ Verificar que el sistema funciona
echo   • ✅ Confirmar que el problema está resuelto
echo   • ✅ Analizar causa del problema original
echo.

echo 🔧 PRÓXIMOS PASOS:
echo   • Identificar qué causó el problema
echo   • Corregir el problema en desarrollo local
echo   • Probar exhaustivamente antes de redeploy
echo   • Documentar la incidencia
echo.

echo 📞 SOPORTE:
echo   • Railway Dashboard: Logs detallados
echo   • GitHub: Historial de cambios
echo   • Este script: Para futuros rollbacks
echo.

echo ⚠️  IMPORTANTE:
echo   El rollback solo es una solución temporal.
echo   Debes corregir la causa raíz del problema.
echo.

set /p open_monitoring="🔍 ¿Abrir herramientas de monitoreo? (S/N): "

if /i "%open_monitoring%"=="S" (
    echo.
    echo 🔗 Abriendo herramientas de monitoreo...
    start https://railway.app/dashboard
    timeout /t 1 >nul
    start https://github.com/mjuica93/SOPORTES-SINES-2121
    echo ✅ Herramientas abiertas
)

echo.
echo 🎯 ROLLBACK DE EMERGENCIA COMPLETADO
echo.
echo El sistema debería estar restaurado en unos minutos.
echo.

pause
exit /b 0

:cancel
echo.
echo ❌ Rollback cancelado
echo.
echo 💡 Si el problema persiste, puedes:
echo   • Revisar logs de Railway
echo   • Intentar corrección rápida
echo   • Ejecutar este script nuevamente
echo.
pause 