@echo off
title Abrir Páginas para Railway
color 0D

echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █                ABRIR PÁGINAS PARA RAILWAY                   █
echo █                                                              █
echo █                  🌐 GITHUB + RAILWAY                         █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.
echo 🚀 Abriendo páginas necesarias para el despliegue...
echo.

echo 📝 1. Abriendo GitHub para crear repositorio...
start https://github.com/new

timeout /t 2 >nul

echo 🚂 2. Abriendo Railway para conectar GitHub...
start https://railway.app/new

timeout /t 2 >nul

echo 📖 3. Abriendo documentación de Railway...
start https://docs.railway.app/deploy/github-repo

echo.
echo ✅ Páginas abiertas:
echo.
echo   🌐 GitHub - Crear repositorio nuevo
echo   🚂 Railway - Conectar con GitHub  
echo   📖 Documentación Railway
echo.
echo 📋 PASOS A SEGUIR:
echo.
echo   1️⃣ En GitHub:
echo      • Crea repositorio público
echo      • Nombre: "sistema-soportes-sines"
echo      • NO inicialices con README
echo.
echo   2️⃣ En tu terminal:
echo      • git init
echo      • git add .
echo      • git commit -m "Initial commit"
echo      • git remote add origin [URL-REPO]
echo      • git push -u origin main
echo.
echo   3️⃣ En Railway:
echo      • Conecta cuenta GitHub
echo      • Selecciona tu repositorio
echo      • Railway detectará Dockerfile automáticamente
echo      • ¡Deploy automático!
echo.
echo 💰 COSTO: $5/mes en Railway
echo 🌍 RESULTADO: Tu sistema disponible mundialmente
echo.
echo 🎯 URLs finales:
echo   • Principal: https://tu-proyecto.railway.app
echo   • Móvil: https://tu-proyecto.railway.app/mobile
echo.
echo ════════════════════════════════════════════════════════════════
echo.
echo 💡 ¿Necesitas ayuda con los comandos Git?
echo    Ejecuta: SUBIR_A_GITHUB.bat
echo.
echo 🧪 ¿Quieres probar localmente primero?
echo    Ejecuta: PROBAR_RAILWAY_LOCAL.bat
echo.
pause 