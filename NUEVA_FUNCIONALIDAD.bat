@echo off
title Sistema SINES - Nueva Funcionalidad
color 0E

echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █              AÑADIR NUEVA FUNCIONALIDAD                     █
echo █                                                              █
echo █                🚀 DESARROLLO SEGURO                          █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.

echo 🎯 PROCESO AUTOMATIZADO PARA NUEVA FUNCIONALIDAD
echo.
echo ⚠️  IMPORTANTE: Este proceso evita romper la versión en producción
echo.

REM Verificar que estamos en el directorio correcto
if not exist "server_railway.py" (
    echo ❌ Error: No estás en el directorio del proyecto SINES
    echo 📁 Asegúrate de ejecutar este script desde la carpeta del proyecto
    pause
    exit /b 1
)

echo ✅ Directorio del proyecto verificado
echo.

REM Verificar Git
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git no está disponible
    echo 💡 Refrescando variables de entorno...
    call :refresh_env
)

:refresh_env
set "PATH=%PATH%;C:\Program Files\Git\cmd"
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git no encontrado. Instala Git primero.
    pause
    exit /b 1
)
echo ✅ Git disponible
echo.

REM Verificar que estamos en main y actualizar
echo 🔄 Actualizando rama main...
git checkout main
git pull origin main

echo.
echo 📝 ¿Qué funcionalidad vas a añadir?
echo.
echo Ejemplos:
echo   - busqueda-avanzada
echo   - nuevos-filtros  
echo   - modo-oscuro
echo   - exportar-resultados
echo   - mejora-mobile
echo.
set /p feature_name="🏷️  Nombre de la funcionalidad (sin espacios): "

if "%feature_name%"=="" (
    echo ❌ Debes especificar un nombre para la funcionalidad
    pause
    exit /b 1
)

echo.
echo 🌿 Creando rama para: %feature_name%
git checkout -b feature/%feature_name%

if errorlevel 1 (
    echo ❌ Error creando la rama
    pause
    exit /b 1
)

echo ✅ Rama 'feature/%feature_name%' creada y activa
echo.

echo 🛠️  SIGUIENTE PASO: DESARROLLAR LA FUNCIONALIDAD
echo.
echo 📋 Pasos a seguir:
echo.
echo   1️⃣  Edita los archivos necesarios para tu funcionalidad
echo   2️⃣  Prueba localmente ejecutando: python server_railway.py
echo   3️⃣  Verifica que todo funciona correctamente:
echo      ✅ Página principal carga
echo      ✅ Búsqueda funciona  
echo      ✅ PDFs se abren
echo      ✅ Versión móvil funciona
echo      ✅ Nueva funcionalidad funciona
echo.
echo   4️⃣  Cuando esté todo listo, ejecuta: SUBIR_FUNCIONALIDAD.bat
echo.

echo 🔧 Archivos principales que puedes modificar:
echo.
echo   🎨 INTERFAZ:
echo      • index.html (página principal)
echo      • index_mobile.html (versión móvil)
echo      • app.js (lógica JavaScript)
echo.
echo   🔍 DATOS:
echo      • support_data_enhanced.json (datos de soportes)
echo      • support_pdf_mapping.json (mapeo de PDFs)
echo.
echo   🚀 SERVIDOR:
echo      • server_railway.py (para nuevas rutas)
echo.
echo   📄 DOCUMENTOS:
echo      • ESTANDARES DE SOPORTES/ (añadir nuevos PDFs)
echo.

echo ═══════════════════════════════════════════════════════════════
echo.
echo 💡 CONSEJOS:
echo   • Haz cambios pequeños e incrementales
echo   • Prueba frecuentemente en local
echo   • Comenta tu código para futuras mejoras
echo   • Mantén la funcionalidad existente intacta
echo.

echo 🚨 IMPORTANTE:
echo   • NO hagas cambios directamente en la rama 'main'
echo   • SIEMPRE prueba localmente antes de subir
echo   • Si algo no funciona, no tengas miedo de preguntar
echo.

echo 🎯 Estás en la rama: feature/%feature_name%
echo 🌍 Producción sigue funcionando normal en Railway
echo.

echo ¿Quieres abrir los archivos principales para editar?
set /p open_files="📝 (S/N): "

if /i "%open_files%"=="S" (
    echo.
    echo 📂 Abriendo archivos principales...
    start notepad index.html
    timeout /t 1 >nul
    start notepad app.js
    timeout /t 1 >nul
    start notepad server_railway.py
    echo ✅ Archivos abiertos en Notepad
)

echo.
echo ¡Listo para desarrollar! 🚀
echo.
echo Recuerda: Cuando termines, ejecuta SUBIR_FUNCIONALIDAD.bat
echo.
pause 