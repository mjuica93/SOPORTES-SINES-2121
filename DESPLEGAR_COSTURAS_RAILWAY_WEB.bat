@echo off
chcp 65001 >nul
title 🚀 Desplegar Sistema de Costuras SINES a Railway (Web)
color 0E

echo.
echo ═══════════════════════════════════════════════════════════════════
echo 🚀 DESPLIEGUE DEL SISTEMA DE COSTURAS SINES A RAILWAY
echo    📱 MÉTODO: INTERFAZ WEB (Sin CLI)
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
echo 🔄 PREPARANDO REPOSITORIO PARA RAILWAY
echo ═══════════════════════════════════════════════════════════════════

echo 📦 Preparando archivos para despliegue...
echo ───────────────────────────────────────────────────────────────

:: Verificar si hay cambios en Git
git status --porcelain >nul 2>&1
if errorlevel 1 (
    echo ⚠️ No hay repositorio Git inicializado
    echo 🔄 Inicializando repositorio...
    git init
    git branch -m main
    git add .
    git commit -m "Sistema de Costuras SINES - Preparado para Railway"
    echo ✅ Repositorio Git inicializado
) else (
    echo ✅ Repositorio Git disponible
    
    :: Agregar nuevos archivos
    echo 📝 Agregando archivos del sistema de costuras...
    git add index_isometricos_con_costuras.html
    git add isometric_welding_manager.js
    git add isometric_data_with_welds.json
    git add welding_statistics.json
    git add server_railway.py
    git add SISTEMA_COSTURAS_COMPLETO.md
    git add README_RAILWAY_COSTURAS.md
    git add verificar_datos_railway.py
    git add railway.json
    git add Dockerfile
    git add requirements.txt
    
    echo 📝 Creando commit con los cambios...
    git commit -m "Sistema de Gestión de Costuras SINES - Ready for Railway deployment" 2>nul
    if errorlevel 1 (
        echo ✅ No hay cambios nuevos para commitear
    ) else (
        echo ✅ Cambios commiteados
    )
)

echo.
echo 🔗 Verificando/creando repositorio remoto...
echo ───────────────────────────────────────────────────────────────

git remote -v >nul 2>&1
if errorlevel 1 (
    echo ⚠️ No hay repositorio remoto configurado
    echo 💡 Necesitarás crear un repositorio en GitHub/GitLab
) else (
    echo ✅ Repositorio remoto configurado
    echo 🔄 Subiendo cambios al repositorio remoto...
    git push -u origin main
    if errorlevel 1 (
        echo ⚠️ Error al subir cambios. Verifica tu conexión y credenciales.
    ) else (
        echo ✅ Cambios subidos al repositorio remoto
    )
)

echo.
echo ═══════════════════════════════════════════════════════════════════
echo 🌐 INSTRUCCIONES PARA DESPLEGAR EN RAILWAY
echo ═══════════════════════════════════════════════════════════════════

echo.
echo 📋 PASO 1: Acceder a Railway
echo ───────────────────────────────────────────────────────────────
echo 🌐 Ve a: https://railway.app/
echo 🔑 Inicia sesión con tu cuenta (GitHub/GitLab/Email)
echo.

echo 📋 PASO 2: Crear nuevo proyecto
echo ───────────────────────────────────────────────────────────────
echo ➕ Haz clic en "New Project"
echo 📂 Selecciona "Deploy from GitHub repo"
echo 🔗 Conecta tu repositorio de GitHub si no lo has hecho
echo 📁 Selecciona este repositorio (SOPORTACION SINES)
echo.

echo 📋 PASO 3: Configurar despliegue
echo ───────────────────────────────────────────────────────────────
echo 🔧 Railway detectará automáticamente el Dockerfile
echo ⚙️ La configuración railway.json se aplicará automáticamente
echo 🚀 Haz clic en "Deploy" para iniciar el despliegue
echo.

echo 📋 PASO 4: Configurar dominio
echo ───────────────────────────────────────────────────────────────
echo 🌐 Ve a la pestaña "Settings" del proyecto
echo 🔗 En "Domains", haz clic en "Generate Domain"
echo 📱 Railway te asignará una URL como: https://tu-proyecto.railway.app
echo.

echo 📋 PASO 5: Verificar despliegue
echo ───────────────────────────────────────────────────────────────
echo ✅ El despliegue debería tardar 2-3 minutos
echo 📊 Verifica que no haya errores en los logs
echo 🔍 Prueba la URL asignada para confirmar que funciona
echo.

echo ═══════════════════════════════════════════════════════════════════
echo 🎯 RUTAS DISPONIBLES UNA VEZ DESPLEGADO
echo ═══════════════════════════════════════════════════════════════════
echo.
echo 🔨 Principal (Costuras):     https://tu-proyecto.railway.app/
echo 🔧 Sistema de Soportes:     https://tu-proyecto.railway.app/soportes
echo 📐 Isométricos Básicos:     https://tu-proyecto.railway.app/isometricos
echo 📱 Versión Móvil:           https://tu-proyecto.railway.app/mobile
echo 🛡️ Modo Failsafe:           https://tu-proyecto.railway.app/failsafe
echo 🔒 Modo Infalible:          https://tu-proyecto.railway.app/infalible
echo 📊 API de Datos:            https://tu-proyecto.railway.app/data
echo 📈 Estadísticas:            https://tu-proyecto.railway.app/stats
echo.

echo 📊 MÉTRICAS DEL SISTEMA PREPARADO:
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
echo ═══════════════════════════════════════════════════════════════════
echo 🎉 REPOSITORIO PREPARADO PARA RAILWAY
echo ═══════════════════════════════════════════════════════════════════
echo.
echo 💡 PRÓXIMOS PASOS:
echo    1. Ir a https://railway.app/
echo    2. Crear nuevo proyecto desde GitHub
echo    3. Seleccionar este repositorio
echo    4. Confirmar el despliegue
echo    5. Obtener la URL asignada
echo.

echo 📱 ARCHIVOS CRÍTICOS LISTOS:
echo ───────────────────────────────────────────────────────────────
echo ✅ index_isometricos_con_costuras.html (24.0 KB)
echo ✅ isometric_welding_manager.js (68.8 KB)
echo ✅ isometric_data_with_welds.json (6.8 MB)
echo ✅ server_railway.py (4.6 KB)
echo ✅ Dockerfile y configuración Railway
echo.

set /p open_railway="¿Abrir Railway en el navegador? (s/n): "
if /i "%open_railway%"=="s" (
    echo 🌐 Abriendo Railway...
    start "" "https://railway.app/"
)

echo.
echo ✅ SISTEMA LISTO PARA DESPLEGAR - ¡Ve a Railway y despliega!
pause 