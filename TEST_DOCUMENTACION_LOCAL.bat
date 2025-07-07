@echo off
echo ======================================================
echo   TEST DOCUMENTACION LOCAL - SINES v4.1
echo ======================================================
echo.
echo 🧪 Probando servidor con documentacion accesible...
echo.
echo 📋 URLs de documentacion a probar:
echo    - Lanzamiento: http://localhost:8000/docs/
echo    - Mejoras: http://localhost:8000/docs/mejoras
echo    - Testing: http://localhost:8000/docs/testing
echo    - Railway: http://localhost:8000/docs/railway
echo    - GitHub: http://localhost:8000/docs/github
echo.
echo 🔗 URLs del sistema:
echo    - Login: http://localhost:8000/login.html
echo    - Sistema: http://localhost:8000/
echo    - API Status: http://localhost:8000/api/status
echo    - Health: http://localhost:8000/health
echo.
echo 🚀 Iniciando servidor corregido...
echo.
python server_railway.py 