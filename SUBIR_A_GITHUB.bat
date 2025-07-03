@echo off
title Sistema SINES - Subir a GitHub
color 0A

echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █                 SUBIR PROYECTO A GITHUB                     █
echo █                                                              █
echo █                 🚀 PREPARADO PARA RAILWAY                    █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.
echo 📋 ARCHIVOS PREPARADOS PARA RAILWAY:
echo.
echo   ✅ Dockerfile              - Configuración Docker
echo   ✅ requirements.txt        - Dependencias Python
echo   ✅ server_railway.py       - Servidor optimizado
echo   ✅ railway.json            - Configuración Railway
echo   ✅ .gitignore              - Archivos a ignorar
echo   ✅ README_GITHUB.md        - Documentación
echo.
echo 🔧 PASOS PARA SUBIR A GITHUB:
echo.
echo   1. 📝 Crea un repositorio en GitHub:
echo      https://github.com/new
echo.
echo   2. 🏷️ Nombre sugerido: "sistema-soportes-sines"
echo.
echo   3. 📖 Descripción: "Sistema web para búsqueda de soportes SINES"
echo.
echo   4. 🔓 Hazlo público para que Railway pueda acceder
echo.
echo   5. ❌ NO inicialices con README (ya tenemos uno)
echo.
echo ════════════════════════════════════════════════════════════════
echo.
echo 🚀 COMANDOS PARA EJECUTAR:
echo.
echo   Una vez creado el repositorio, ejecuta estos comandos:
echo.
echo   git init
echo   git add .
echo   git commit -m "Initial commit: Sistema SINES para Railway"
echo   git branch -M main
echo   git remote add origin https://github.com/TU-USUARIO/TU-REPOSITORIO.git
echo   git push -u origin main
echo.
echo ════════════════════════════════════════════════════════════════
echo.
echo 🎯 DESPUÉS DE SUBIR A GITHUB:
echo.
echo   1. 🌐 Ve a Railway.app
echo   2. 🔗 Conecta tu cuenta GitHub
echo   3. 📁 Selecciona tu repositorio
echo   4. 🚀 Railway detectará automáticamente el Dockerfile
echo   5. ✅ Tu sistema estará disponible en minutos
echo.
echo 💰 COSTO: Solo $5/mes en Railway
echo 🌍 ACCESO: Disponible mundialmente 24/7
echo 📱 MÓVIL: Versión optimizada incluida
echo.
echo ════════════════════════════════════════════════════════════════
echo.
echo 💡 CONSEJOS:
echo.
echo   • El README_GITHUB.md contiene toda la documentación
echo   • Railway detectará automáticamente la configuración
echo   • La URL será: https://tu-proyecto.railway.app
echo   • Versión móvil: https://tu-proyecto.railway.app/mobile
echo.
echo 🔄 ¿Quieres que prepare los comandos Git automáticamente?
echo.
set /p repo_url="🌐 Pega la URL de tu repositorio GitHub (opcional): "

if not "%repo_url%"=="" (
    echo.
    echo 📝 COMANDOS PERSONALIZADOS:
    echo.
    echo git init
    echo git add .
    echo git commit -m "Initial commit: Sistema SINES para Railway"
    echo git branch -M main
    echo git remote add origin %repo_url%
    echo git push -u origin main
    echo.
    echo 💡 Copia y pega estos comandos en tu terminal
    echo.
)

echo.
echo 🎉 ¡Todo listo para GitHub y Railway!
echo.
pause 