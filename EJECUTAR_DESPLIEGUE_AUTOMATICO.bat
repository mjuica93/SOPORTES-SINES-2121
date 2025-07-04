@echo off
chcp 65001 >nul
title 🚀 Despliegue Automático Sistema de Costuras SINES
color 0E

echo.
echo ═══════════════════════════════════════════════════════════════════
echo 🚀 DESPLIEGUE AUTOMATICO SISTEMA DE COSTURAS SINES
echo    📂 Repositorio: https://github.com/mjuica93/soportes-y-isometricos-2121
echo ═══════════════════════════════════════════════════════════════════
echo.

echo 🔑 Para hacer el despliegue automático necesito tu TOKEN de GitHub
echo.
echo 📋 CÓMO OBTENER TU TOKEN DE GITHUB:
echo ───────────────────────────────────────────────────────────────
echo 1. Ve a: https://github.com/settings/tokens
echo 2. Haz clic en "Generate new token" ^> "Generate new token (classic)"
echo 3. Nombre: "SINES Sistema Costuras"
echo 4. Expiration: "30 days" (o más)
echo 5. Scopes: Marca "repo" (incluye todos los sub-permisos)
echo 6. Haz clic en "Generate token"
echo 7. ¡COPIA EL TOKEN INMEDIATAMENTE! (solo se muestra una vez)
echo.

set /p open_github="¿Abrir GitHub para crear el token? (s/n): "
if /i "%open_github%"=="s" (
    echo 🌐 Abriendo GitHub Settings...
    start "" "https://github.com/settings/tokens"
    echo.
    echo 💡 Después de crear el token, vuelve aquí y pégalo abajo
    echo.
)

set /p github_token="🔑 Pega tu token de GitHub aquí: "

if "%github_token%"=="" (
    echo ❌ No proporcionaste un token. El despliegue automático no puede continuar.
    pause
    exit /b 1
)

echo.
echo ✅ Token recibido. Iniciando despliegue automático...
echo.

echo 🚀 Ejecutando script PowerShell de despliegue...
echo ───────────────────────────────────────────────────────────────

powershell -ExecutionPolicy Bypass -File "DESPLIEGUE_AUTOMATICO.ps1" -GitHubToken "%github_token%"

if errorlevel 1 (
    echo.
    echo ❌ Error durante el despliegue automático
    echo.
    echo 💡 POSIBLES SOLUCIONES:
    echo    1. Verifica que el token de GitHub sea correcto
    echo    2. Asegúrate que el token tenga permisos "repo"
    echo    3. Verifica tu conexión a internet
    echo    4. Intenta crear un nuevo token
    echo.
    pause
    exit /b 1
)

echo.
echo 🎉 DESPLIEGUE AUTOMATICO FINALIZADO
echo ═══════════════════════════════════════════════════════════════════
echo.
echo 📋 PRÓXIMOS PASOS:
echo    1. Railway se abrió automáticamente en tu navegador
echo    2. Inicia sesión con tu cuenta GitHub
echo    3. Autoriza Railway a acceder a tus repositorios
echo    4. Selecciona el repositorio "soportes-y-isometricos-2121"
echo    5. Haz clic en "Deploy"
echo.
echo 🌐 Una vez desplegado, tendrás acceso a:
echo    🔨 https://tu-proyecto.railway.app/           - Sistema de Costuras
echo    🔧 https://tu-proyecto.railway.app/soportes  - Sistema de Soportes
echo    📱 https://tu-proyecto.railway.app/mobile    - Versión Móvil
echo.
echo ✅ ¡Tu sistema está listo para producción mundial!
pause 