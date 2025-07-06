@echo off
title Sistema SINES - Menú de Desarrollo
color 0F

:main_menu
cls
echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █               SISTEMA SINES - MENÚ DESARROLLO               █
echo █                                                              █
echo █                   🚀 DESARROLLO CONTINUO                     █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.

echo 🎯 GESTIÓN COMPLETA DE DESARROLLO Y DESPLIEGUE
echo.

REM Verificar estado del repositorio
if exist ".git" (
    echo ✅ Repositorio Git: Inicializado
    for /f "tokens=*" %%i in ('git branch --show-current 2^>nul') do set current_branch=%%i
    if defined current_branch (
        echo 🌿 Rama actual: %current_branch%
    ) else (
        echo 🌿 Rama actual: No detectada
    )
) else (
    echo ❌ Repositorio Git: No inicializado
)

REM Verificar archivos críticos
if exist "server_railway.py" (
    echo ✅ Servidor Railway: Configurado
) else (
    echo ❌ Servidor Railway: No encontrado
)

if exist "index.html" (
    echo ✅ Aplicación Web: Disponible
) else (
    echo ❌ Aplicación Web: No encontrada
)

echo.
echo ════════════════════════════════════════════════════════════════
echo 🛠️  OPCIONES DE DESARROLLO
echo ════════════════════════════════════════════════════════════════
echo.

echo   1. 🆕 NUEVA FUNCIONALIDAD
echo      Crear una nueva rama y desarrollar funcionalidad
echo.
echo   2. 🧪 PROBAR LOCALMENTE
echo      Ejecutar pruebas sistemáticas antes del despliegue
echo.
echo   3. 🚀 SUBIR A PRODUCCIÓN
echo      Desplegar funcionalidad probada a la web
echo.
echo   4. 📊 ESTADO DEL PROYECTO
echo      Ver información detallada del repositorio
echo.
echo   5. 🔧 HERRAMIENTAS ÚTILES
echo      Acceso a scripts y utilidades adicionales
echo.
echo   6. 🚨 ROLLBACK DE EMERGENCIA
echo      Revertir cambios en caso de problemas
echo.
echo   7. 📖 DOCUMENTACIÓN
echo      Ver guías y documentación del proyecto
echo.
echo   8. 🌐 ABRIR ENLACES
echo      Acceso rápido a GitHub, Railway y sistema
echo.
echo   0. ❌ SALIR
echo.

echo ════════════════════════════════════════════════════════════════
echo.

set /p menu_option="🎯 Selecciona una opción (0-8): "

if "%menu_option%"=="1" goto :new_feature
if "%menu_option%"=="2" goto :test_local
if "%menu_option%"=="3" goto :upload_feature
if "%menu_option%"=="4" goto :project_status
if "%menu_option%"=="5" goto :tools_menu
if "%menu_option%"=="6" goto :emergency_rollback
if "%menu_option%"=="7" goto :documentation
if "%menu_option%"=="8" goto :open_links
if "%menu_option%"=="0" goto :exit

echo ❌ Opción no válida
timeout /t 1 >nul
goto :main_menu

:new_feature
echo.
echo 🆕 INICIANDO NUEVA FUNCIONALIDAD...
echo.
call "NUEVA_FUNCIONALIDAD.bat"
pause
goto :main_menu

:test_local
echo.
echo 🧪 INICIANDO PRUEBAS LOCALES...
echo.
call "PROBAR_LOCAL.bat"
pause
goto :main_menu

:upload_feature
echo.
echo 🚀 SUBIENDO FUNCIONALIDAD A PRODUCCIÓN...
echo.
call "SUBIR_FUNCIONALIDAD.bat"
pause
goto :main_menu

:project_status
echo.
echo 📊 ESTADO DEL PROYECTO
echo ════════════════════════════════════════════════════════════════
echo.

REM Verificar Git
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git no disponible
    echo.
    pause
    goto :main_menu
)

echo 🔍 INFORMACIÓN DEL REPOSITORIO:
echo.

REM Rama actual
for /f "tokens=*" %%i in ('git branch --show-current') do set current_branch=%%i
echo 🌿 Rama actual: %current_branch%

REM Estado del working directory
echo.
echo 📋 Estado de archivos:
git status --porcelain

REM Últimos commits
echo.
echo 📜 Últimos 5 commits:
echo ────────────────────────────────────────────────────────────────
git log --oneline -5
echo ────────────────────────────────────────────────────────────────

REM Ramas disponibles
echo.
echo 🌿 Ramas disponibles:
git branch -a

REM Información del remoto
echo.
echo 🔗 Repositorio remoto:
git remote -v

echo.
echo 📊 ARCHIVOS DEL PROYECTO:
echo.
echo 📁 Archivos principales:
if exist "index.html" echo ✅ index.html
if exist "app.js" echo ✅ app.js
if exist "server_railway.py" echo ✅ server_railway.py
if exist "support_data_enhanced.json" echo ✅ support_data_enhanced.json
if exist "Dockerfile" echo ✅ Dockerfile
if exist "requirements.txt" echo ✅ requirements.txt

echo.
echo 📁 Scripts de desarrollo:
if exist "NUEVA_FUNCIONALIDAD.bat" echo ✅ NUEVA_FUNCIONALIDAD.bat
if exist "PROBAR_LOCAL.bat" echo ✅ PROBAR_LOCAL.bat
if exist "SUBIR_FUNCIONALIDAD.bat" echo ✅ SUBIR_FUNCIONALIDAD.bat
if exist "ROLLBACK_EMERGENCY.bat" echo ✅ ROLLBACK_EMERGENCY.bat

echo.
pause
goto :main_menu

:tools_menu
echo.
echo 🔧 HERRAMIENTAS ÚTILES
echo ════════════════════════════════════════════════════════════════
echo.

echo   A. 🔄 SINCRONIZAR CON GITHUB
echo      Actualizar repositorio local
echo.
echo   B. 🧹 LIMPIAR RAMAS
echo      Eliminar ramas de funcionalidades completadas
echo.
echo   C. 🔍 VER LOGS DETALLADOS
echo      Historial completo de cambios
echo.
echo   D. 🌐 INICIAR SERVIDOR LOCAL
echo      Ejecutar sistema en local para pruebas
echo.
echo   E. 📊 VERIFICAR INTEGRIDAD
echo      Comprobar que todos los archivos están correctos
echo.
echo   0. ↩️  VOLVER AL MENÚ PRINCIPAL
echo.

set /p tools_option="🎯 Selecciona herramienta (A-E, 0): "

if /i "%tools_option%"=="A" goto :sync_github
if /i "%tools_option%"=="B" goto :clean_branches
if /i "%tools_option%"=="C" goto :detailed_logs
if /i "%tools_option%"=="D" goto :start_local_server
if /i "%tools_option%"=="E" goto :verify_integrity
if "%tools_option%"=="0" goto :main_menu

echo ❌ Opción no válida
timeout /t 1 >nul
goto :tools_menu

:sync_github
echo.
echo 🔄 SINCRONIZANDO CON GITHUB...
echo.
git checkout main
git pull origin main
echo ✅ Repositorio local actualizado
pause
goto :tools_menu

:clean_branches
echo.
echo 🧹 LIMPIANDO RAMAS COMPLETADAS...
echo.
echo 📋 Ramas locales (excepto main):
git branch | grep -v "main"
echo.
echo ⚠️  ADVERTENCIA: Esto eliminará ramas que ya no necesites
set /p confirm_clean="🗑️  ¿Confirmas limpieza? (S/N): "
if /i "%confirm_clean%"=="S" (
    git branch | grep -v "main" | xargs git branch -d
    echo ✅ Ramas limpias
) else (
    echo ❌ Limpieza cancelada
)
pause
goto :tools_menu

:detailed_logs
echo.
echo 🔍 LOGS DETALLADOS
echo ════════════════════════════════════════════════════════════════
echo.
git log --graph --pretty=format:"%%h - %%an, %%ar : %%s" --all -10
echo.
pause
goto :tools_menu

:start_local_server
echo.
echo 🌐 INICIANDO SERVIDOR LOCAL...
echo.
echo 🚀 Servidor iniciándose en http://localhost:8000
echo ⚠️  Cierra esta ventana cuando termines de probar
echo.
python server_railway.py
pause
goto :tools_menu

:verify_integrity
echo.
echo 📊 VERIFICANDO INTEGRIDAD DEL PROYECTO...
echo.

set "integrity_ok=true"

echo 🔍 Verificando archivos críticos...
if not exist "index.html" (
    echo ❌ index.html faltante
    set "integrity_ok=false"
)
if not exist "server_railway.py" (
    echo ❌ server_railway.py faltante
    set "integrity_ok=false"
)
if not exist "support_data_enhanced.json" (
    echo ❌ support_data_enhanced.json faltante
    set "integrity_ok=false"
)
if not exist "Dockerfile" (
    echo ❌ Dockerfile faltante
    set "integrity_ok=false"
)

echo.
echo 🔍 Verificando directorio de PDFs...
if exist "ESTANDARES DE SOPORTES\" (
    echo ✅ Directorio de PDFs presente
) else (
    echo ❌ Directorio de PDFs faltante
    set "integrity_ok=false"
)

echo.
if "%integrity_ok%"=="true" (
    echo ✅ INTEGRIDAD VERIFICADA: Todos los archivos críticos presentes
) else (
    echo ❌ INTEGRIDAD COMPROMETIDA: Faltan archivos críticos
)

pause
goto :tools_menu

:emergency_rollback
echo.
echo 🚨 ROLLBACK DE EMERGENCIA...
echo.
call "ROLLBACK_EMERGENCY.bat"
pause
goto :main_menu

:documentation
echo.
echo 📖 DOCUMENTACIÓN DISPONIBLE
echo ════════════════════════════════════════════════════════════════
echo.

echo   1. 📋 GUÍA DE DESARROLLO CONTINUO
echo      Proceso completo paso a paso
echo.
echo   2. 🚀 ESTADO FINAL DEL SISTEMA
echo      Resumen de funcionalidades
echo.
echo   3. 🔧 MEJORAS IMPLEMENTADAS
echo      Historial de cambios
echo.
echo   4. 📞 INSTRUCCIONES RÁPIDAS
echo      Comandos más usados
echo.
echo   0. ↩️  VOLVER AL MENÚ PRINCIPAL
echo.

set /p doc_option="📖 Selecciona documentación (1-4, 0): "

if "%doc_option%"=="1" (
    if exist "GUIA_DESARROLLO_CONTINUO.md" (
        start notepad "GUIA_DESARROLLO_CONTINUO.md"
    ) else (
        echo ❌ Guía no encontrada
    )
)
if "%doc_option%"=="2" (
    if exist "ESTADO_FINAL_SISTEMA.md" (
        start notepad "ESTADO_FINAL_SISTEMA.md"
    ) else (
        echo ❌ Estado final no encontrado
    )
)
if "%doc_option%"=="3" (
    if exist "MEJORAS_IMPLEMENTADAS.md" (
        start notepad "MEJORAS_IMPLEMENTADAS.md"
    ) else (
        echo ❌ Mejoras no encontradas
    )
)
if "%doc_option%"=="4" (
    if exist "INSTRUCCIONES_RAPIDAS.txt" (
        start notepad "INSTRUCCIONES_RAPIDAS.txt"
    ) else (
        echo ❌ Instrucciones no encontradas
    )
)
if "%doc_option%"=="0" goto :main_menu

timeout /t 1 >nul
goto :documentation

:open_links
echo.
echo 🌐 ENLACES RÁPIDOS
echo ════════════════════════════════════════════════════════════════
echo.

echo   1. 🐙 GITHUB - Repositorio
echo      https://github.com/mjuica93/SOPORTES-SINES-2121
echo.
echo   2. 🚄 RAILWAY - Dashboard
echo      https://railway.app/dashboard
echo.
echo   3. 🌍 SISTEMA EN PRODUCCIÓN
echo      (URL de Railway cuando esté disponible)
echo.
echo   4. 🏠 SISTEMA LOCAL
echo      http://localhost:8000
echo.
echo   0. ↩️  VOLVER AL MENÚ PRINCIPAL
echo.

set /p link_option="🔗 Selecciona enlace (1-4, 0): "

if "%link_option%"=="1" (
    start https://github.com/mjuica93/SOPORTES-SINES-2121
    echo ✅ GitHub abierto
)
if "%link_option%"=="2" (
    start https://railway.app/dashboard
    echo ✅ Railway abierto
)
if "%link_option%"=="3" (
    echo 💡 URL de producción será proporcionada cuando Railway complete el deploy
)
if "%link_option%"=="4" (
    start http://localhost:8000
    echo ✅ Sistema local abierto (si está ejecutándose)
)
if "%link_option%"=="0" goto :main_menu

timeout /t 2 >nul
goto :open_links

:exit
echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █                   ¡HASTA LUEGO!                             █
echo █                                                              █
echo █              SISTEMA SINES - DESARROLLO                     █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.

echo 🎯 RESUMEN DE HERRAMIENTAS DISPONIBLES:
echo.
echo   • NUEVA_FUNCIONALIDAD.bat - Crear nueva funcionalidad
echo   • PROBAR_LOCAL.bat - Probar antes de subir
echo   • SUBIR_FUNCIONALIDAD.bat - Desplegar a producción
echo   • ROLLBACK_EMERGENCY.bat - Revertir en emergencia
echo   • MENU_DESARROLLO.bat - Este menú (¡recomendado!)
echo.

echo 💡 CONSEJO: Usa MENU_DESARROLLO.bat como punto de partida
echo    para todas tus tareas de desarrollo.
echo.

echo 🚀 ¡Tu sistema está listo para evolucionar!
echo.
pause
exit 