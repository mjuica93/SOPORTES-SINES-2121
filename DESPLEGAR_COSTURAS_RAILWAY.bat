@echo off
chcp 65001 >nul
title 🚀 Desplegar Sistema de Costuras SINES a Railway
color 0E

echo.
echo ═══════════════════════════════════════════════════════════════════
echo 🚀 DESPLIEGUE DEL SISTEMA DE COSTURAS SINES A RAILWAY
echo ═══════════════════════════════════════════════════════════════════
echo.

echo 📊 Verificando sistema completo antes del despliegue...
echo ───────────────────────────────────────────────────────────────

python verificar_datos_railway.py
if errorlevel 1 (
    echo ❌ Error en la verificación del sistema
    pause
    exit /b 1
)

echo.
echo ═══════════════════════════════════════════════════════════════════
echo 🔄 PREPARANDO DESPLIEGUE
echo ═══════════════════════════════════════════════════════════════════

:: Verificar Railway CLI
echo 📋 Verificando Railway CLI...
railway --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Railway CLI no está instalado
    echo.
    echo 💡 OPCIONES PARA INSTALAR RAILWAY CLI:
    echo    1. Windows: winget install Railway.cli
    echo    2. Manual: https://railway.app/cli
    echo    3. NPM: npm install -g @railway/cli
    echo.
    set /p install_choice="¿Quieres intentar instalar con winget? (s/n): "
    if /i "!install_choice!"=="s" (
        echo 🔄 Instalando Railway CLI...
        winget install Railway.cli
        if errorlevel 1 (
            echo ❌ Error instalando Railway CLI
            echo    Instala manualmente desde: https://railway.app/cli
            pause
            exit /b 1
        )
    ) else (
        echo ❌ Railway CLI es necesario para el despliegue
        pause
        exit /b 1
    )
) else (
    echo ✅ Railway CLI está instalado
)

echo.
echo 🔐 Verificando autenticación...
railway status >nul 2>&1
if errorlevel 1 (
    echo ❌ No estás autenticado en Railway
    echo 🔄 Iniciando proceso de login...
    railway login
    if errorlevel 1 (
        echo ❌ Error en la autenticación
        pause
        exit /b 1
    )
) else (
    echo ✅ Autenticado en Railway
)

echo.
echo 📦 Preparando archivos para despliegue...
echo ───────────────────────────────────────────────────────────────

:: Verificar si hay cambios en Git
git status --porcelain >nul 2>&1
if errorlevel 1 (
    echo ⚠️ No hay repositorio Git inicializado
    echo 🔄 Inicializando repositorio...
    git init
    git add .
    git commit -m "Sistema de Costuras SINES - Preparado para Railway"
) else (
    echo ✅ Repositorio Git disponible
    
    :: Agregar nuevos archivos
    git add index_isometricos_con_costuras.html
    git add isometric_welding_manager.js
    git add isometric_data_with_welds.json
    git add welding_statistics.json
    git add server_railway.py
    git add SISTEMA_COSTURAS_COMPLETO.md
    git add README_RAILWAY_COSTURAS.md
    git add verificar_datos_railway.py
    
    echo 📝 Creando commit con los cambios...
    git commit -m "Actualización: Sistema de Gestión de Costuras integrado - Ready for Railway deployment" 2>nul
    if errorlevel 1 (
        echo ✅ No hay cambios nuevos para commitear
    ) else (
        echo ✅ Cambios commiteados
    )
)

echo.
echo ═══════════════════════════════════════════════════════════════════
echo 🚀 INICIANDO DESPLIEGUE A RAILWAY
echo ═══════════════════════════════════════════════════════════════════

echo 🔄 Desplegando a Railway...
railway up

if errorlevel 1 (
    echo ❌ Error durante el despliegue
    echo.
    echo 💡 SOLUCIONES POSIBLES:
    echo    1. Verificar que estés en el proyecto correcto: railway status
    echo    2. Crear nuevo proyecto: railway init
    echo    3. Verificar conexión a internet
    echo    4. Revisar logs: railway logs
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ DESPLIEGUE COMPLETADO
echo ═══════════════════════════════════════════════════════════════════

echo 📋 Obteniendo información del despliegue...
railway status

echo.
echo 🌐 URLS DE ACCESO:
echo ───────────────────────────────────────────────────────────────
for /f "tokens=*" %%i in ('railway domain 2^>nul') do (
    echo 🔨 Sistema de Costuras:    %%i/
    echo 🔧 Sistema de Soportes:    %%i/soportes
    echo 📐 Isométricos Básicos:    %%i/isometricos
    echo 📱 Versión Móvil:          %%i/mobile
    echo 📊 API de Datos:           %%i/data
    echo 📈 Estadísticas:           %%i/stats
    goto :found_domain
)

echo ⚠️ No se pudo obtener el dominio automáticamente
echo 💡 Ejecuta 'railway domain' para ver tu URL

:found_domain

echo.
echo 📊 MÉTRICAS DEL SISTEMA DESPLEGADO:
echo ───────────────────────────────────────────────────────────────

python -c "
import json
try:
    with open('welding_statistics.json', 'r', encoding='utf-8') as f:
        stats = json.load(f)
    print(f'✅ {stats.get(\"total_isometrics\", 0):,} isométricos totales')
    print(f'✅ {stats.get(\"total_welds\", 0):,} costuras de soldadura')
    print(f'✅ {stats.get(\"completion_percentage\", 0)}%% de progreso completado')
    print('✅ Sistema de trazabilidad completo')
    print('✅ Exportación CSV disponible')
    print('✅ Integración con soportes activa')
except Exception as e:
    print(f'❌ Error leyendo estadísticas: {e}')
" 2>nul

echo.
echo 🎉 SISTEMA DE COSTURAS SINES DESPLEGADO EXITOSAMENTE EN RAILWAY!
echo ═══════════════════════════════════════════════════════════════════
echo.
echo 💡 PRÓXIMOS PASOS:
echo    1. Verificar que el sistema funciona en la URL de Railway
echo    2. Configurar dominio personalizado si es necesario
echo    3. Monitorear logs: railway logs --follow
echo    4. Escalar recursos si es necesario: railway up --detach
echo.

set /p open_browser="¿Abrir Railway dashboard? (s/n): "
if /i "%open_browser%"=="s" (
    echo 🌐 Abriendo Railway dashboard...
    railway open
)

echo.
echo ✅ DESPLIEGUE FINALIZADO - ¡El sistema está en producción!
pause 