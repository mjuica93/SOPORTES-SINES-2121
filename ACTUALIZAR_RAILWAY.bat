@echo off
title ACTUALIZAR RAILWAY - Sistema SINES Final
color 0A

echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █         🔄 ACTUALIZAR DESPLIEGUE EN RAILWAY                 █
echo █                                                              █
echo █        ⚡ FORZAR NUEVA VERSIÓN FINAL                        █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.

echo 🔍 VERIFICANDO ARCHIVOS ACTUALIZADOS...
echo ───────────────────────────────────────────────────────────────

if not exist "server_railway.py" (
    echo ❌ server_railway.py no encontrado
    pause
    exit /b 1
)

if not exist "index_isometricos_integrado_final.html" (
    echo ❌ index_isometricos_integrado_final.html no encontrado
    pause
    exit /b 1
)

echo ✅ server_railway.py - ACTUALIZADO para versión final
echo ✅ index_isometricos_integrado_final.html - Sistema integrado completo
echo ✅ Todas las funcionalidades incluidas

echo.
echo 📊 FUNCIONALIDADES DE LA NUEVA VERSIÓN:
echo ───────────────────────────────────────────────────────────────
echo ✅ Soportes agrupados por número
echo ✅ Variables de plantilla (A, B, C, D, E, R, X, Y, EL, N., SH., TEMP)
echo ✅ Códigos de referencia (4a), (4b), (4c), (4d), etc.
echo ✅ Dimensiones técnicas completas
echo ✅ Integración con isométricos
echo ✅ Soporte para prefabricados
echo ✅ Gestión de instalaciones
echo ✅ Control de soldadura
echo ✅ Estadísticas y filtros avanzados

echo.
echo 🚀 INICIANDO ACTUALIZACIÓN...
echo ───────────────────────────────────────────────────────────────

echo 📦 1. Preparando archivos para commit...
git add server_railway.py
git add index_isometricos_integrado_final.html
git add support_dimensions_data.json
git add template_variables_mapping.json
git add welding_enhanced_data.json
git add welding_compact_data.json

echo 📝 2. Creando commit con la nueva versión...
git commit -m "🚀 ACTUALIZACIÓN RAILWAY: Sistema SINES v3.0 Final - Soportes Agrupados + Variables de Plantilla + Soldadura Completa"

if errorlevel 1 (
    echo ⚠️ No hay cambios nuevos para commitear, forzando push...
) else (
    echo ✅ Commit creado exitosamente
)

echo 📤 3. Subiendo cambios a GitHub...
git push origin main

if errorlevel 1 (
    echo ❌ Error al subir a GitHub
    echo 💡 Verifica tu conexión y credenciales
    pause
    exit /b 1
)

echo ✅ Cambios subidos a GitHub correctamente

echo.
echo 🔄 4. FORZANDO REDESPLIEGUE EN RAILWAY...
echo ───────────────────────────────────────────────────────────────

echo 💡 Railway detectará automáticamente los cambios en GitHub
echo    y iniciará un nuevo despliegue en unos minutos.

echo.
echo 🌐 URLS ACTUALIZADAS (disponibles en 2-3 minutos):
echo ───────────────────────────────────────────────────────────────
echo 🎯 Principal: https://tu-proyecto.railway.app/
echo    → Sistema SINES v3.0 Final con TODAS las funcionalidades
echo.
echo 🔧 Alternativas disponibles:
echo    ├─ /sistema-mejorado → Versión con mejoras específicas
echo    ├─ /costuras → Sistema de gestión de costuras
echo    ├─ /github → Versión GitHub
echo    ├─ /mobile → Versión móvil
echo    ├─ /templates → Con plantillas
echo    └─ /basico → Versión básica

echo.
echo ⏱️ TIEMPO ESTIMADO DE DESPLIEGUE: 2-3 minutos
echo.

set /p open_railway="¿Abrir Railway Dashboard para monitorear? (s/n): "
if /i "%open_railway%"=="s" (
    echo 🌐 Abriendo Railway Dashboard...
    start "" "https://railway.app/dashboard"
)

echo.
echo ✅ ACTUALIZACIÓN INICIADA
echo ═══════════════════════════════════════════════════════════════════
echo.
echo 📋 QUÉ ESPERAR:
echo    1. Railway detectará los cambios automáticamente
echo    2. Iniciará un nuevo build con la configuración actualizada  
echo    3. Desplegará la nueva versión sin downtime
echo    4. La URL principal mostrará el sistema final actualizado
echo.
echo 🔍 PARA VERIFICAR:
echo    1. Ve a Railway Dashboard
echo    2. Revisa los logs de deployment
echo    3. Prueba la URL principal en unos minutos
echo.
echo 🎉 ¡LA NUEVA VERSIÓN SE DESPLEGARÁ AUTOMÁTICAMENTE!
echo.
pause 