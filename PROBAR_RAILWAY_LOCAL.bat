@echo off
title Probar Servidor Railway Local
color 0B

echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █            PROBAR SERVIDOR RAILWAY LOCAL                    █
echo █                                                              █
echo █              🧪 PRUEBA ANTES DE GITHUB                       █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.
echo 🔍 Verificando archivos para Railway...
echo.

if not exist "server_railway.py" (
    echo ❌ server_railway.py no encontrado
    pause
    exit /b 1
)

if not exist "Dockerfile" (
    echo ❌ Dockerfile no encontrado
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo ❌ requirements.txt no encontrado
    pause
    exit /b 1
)

if not exist "railway.json" (
    echo ❌ railway.json no encontrado
    pause
    exit /b 1
)

echo ✅ server_railway.py
echo ✅ Dockerfile
echo ✅ requirements.txt
echo ✅ railway.json
echo ✅ .gitignore
echo ✅ README_GITHUB.md
echo ✅ LICENSE
echo.
echo 🚀 Iniciando servidor Railway en modo local...
echo.
echo 🎯 El servidor se iniciará en: http://localhost:8000
echo 📱 Versión móvil: http://localhost:8000/mobile
echo.
echo ⚠️  Para detener: Presiona Ctrl+C
echo.
echo ════════════════════════════════════════════════════════════════

python server_railway.py 