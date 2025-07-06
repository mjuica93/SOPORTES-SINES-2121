@echo off
title SINES Soportes - Despliegue en Railway
color 0B

echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █              SINES SOPORTES - RAILWAY.APP                   █
echo █                                                              █
echo █           💰 OPCIÓN PROFESIONAL - $5/mes                     █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.
echo 🚀 Configurando despliegue profesional en Railway...
echo.
echo 💡 Railway.app es la mejor opción calidad/precio:
echo    ✅ URL permanente personalizada
echo    ✅ Disponibilidad 24/7
echo    ✅ SSL automático
echo    ✅ Sin límites de conexión
echo    ✅ Escalabilidad automática
echo    ✅ $5/mes (más barato que Heroku)
echo.

REM Verificar si Railway CLI está instalado
railway --version >nul 2>&1
if errorlevel 1 (
    echo 📥 Instalando Railway CLI...
    npm install -g @railway/cli
    
    if errorlevel 1 (
        echo ❌ Error instalando Railway CLI
        echo.
        echo 🛠️ Instalación manual:
        echo    1. Ve a: https://railway.app
        echo    2. Crea una cuenta
        echo    3. Instala: npm install -g @railway/cli
        echo    4. Ejecuta: railway login
        echo.
        pause
        exit /b 1
    )
)

echo ✅ Railway CLI instalado
echo.
echo 🔑 Iniciando sesión en Railway...
echo    (Se abrirá tu navegador para autenticarte)
echo.

railway login

echo.
echo 🚀 Creando proyecto en Railway...
echo.

railway new

echo.
echo 📦 Configurando proyecto...
echo.

REM Crear archivo de configuración de Railway
echo PORT=8000 > .env
echo WEB_CONCURRENCY=1 >> .env

REM Crear railway.json
echo {
echo   "build": {
echo     "builder": "DOCKERFILE"
echo   },
echo   "deploy": {
echo     "startCommand": "python server.py",
echo     "healthcheckPath": "/",
echo     "restartPolicyType": "ON_FAILURE"
echo   }
echo } > railway.json

REM Crear Dockerfile optimizado
echo FROM python:3.11-slim > Dockerfile
echo WORKDIR /app >> Dockerfile
echo COPY . . >> Dockerfile
echo RUN pip install --no-cache-dir -r requirements.txt >> Dockerfile
echo EXPOSE 8000 >> Dockerfile
echo CMD ["python", "server.py"] >> Dockerfile

REM Crear requirements.txt
echo # No external dependencies required > requirements.txt
echo # This project uses only Python standard library >> requirements.txt

echo.
echo 🌐 Desplegando en Railway...
echo.

railway up

echo.
echo ✅ ¡Despliegue completado!
echo.
echo 🎯 Tu sistema está ahora disponible en:
echo    https://tu-proyecto.railway.app
echo.
echo 📱 Para acceso móvil optimizado:
echo    https://tu-proyecto.railway.app/index_mobile.html
echo.
echo 💰 Costo: $5/mes
echo 🔧 Administración: https://railway.app/dashboard
echo.
echo 🎉 ¡Tu sistema SINES ya está accesible mundialmente!
echo.
pause 