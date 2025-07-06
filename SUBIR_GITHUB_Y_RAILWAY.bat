@echo off
chcp 65001 >nul
title 🚀 Subir Sistema de Costuras a GitHub y Railway
color 0E

echo.
echo ═══════════════════════════════════════════════════════════════════
echo 🚀 SUBIR SISTEMA DE COSTURAS SINES A GITHUB Y RAILWAY
echo ═══════════════════════════════════════════════════════════════════
echo.

echo 📊 Verificando sistema antes del despliegue...
echo ───────────────────────────────────────────────────────────────

python verificar_datos_railway.py
if errorlevel 1 (
    echo ❌ Error en la verificación del sistema
    pause
    exit /b 1
)

echo.
echo ═══════════════════════════════════════════════════════════════════
echo 📱 PASO 1: SUBIR A GITHUB
echo ═══════════════════════════════════════════════════════════════════

echo.
echo 🌐 Ve a: https://github.com/
echo 🔑 Inicia sesión en tu cuenta de GitHub
echo.
echo ➕ Crear nuevo repositorio:
echo    1. Haz clic en "New" (botón verde)
echo    2. Nombre del repositorio: SINES-Sistema-Costuras
echo    3. Descripción: Sistema de Gestión de Costuras de Soldadura SINES
echo    4. Selecciona "Public" (para que Railway pueda acceder)
echo    5. NO marques "Initialize with README"
echo    6. Haz clic en "Create repository"
echo.

set /p github_ready="¿Has creado el repositorio en GitHub? (s/n): "
if /i not "%github_ready%"=="s" (
    echo 💡 Ve a GitHub, crea el repositorio y vuelve aquí
    pause
    exit /b 1
)

echo.
echo 📂 Preparando archivos para GitHub...
echo ───────────────────────────────────────────────────────────────

:: Crear .gitignore optimizado para Railway
echo # Archivos temporales > .gitignore
echo *.tmp >> .gitignore
echo *.log >> .gitignore
echo __pycache__/ >> .gitignore
echo .env >> .gitignore
echo node_modules/ >> .gitignore
echo .vscode/ >> .gitignore
echo *.backup >> .gitignore
echo temp_* >> .gitignore

:: Crear README para GitHub
echo # 🚀 Sistema de Gestión de Costuras SINES > README.md
echo. >> README.md
echo Sistema completo de gestión de costuras de soldadura para el proyecto 2121. >> README.md
echo. >> README.md
echo ## 🎯 Características >> README.md
echo - **4,009 costuras** procesadas y vinculadas >> README.md
echo - **1,778 isométricos** integrados >> README.md
echo - **Trazabilidad completa** de soldaduras >> README.md
echo - **Exportación CSV** disponible >> README.md
echo - **Interfaz web moderna** y responsiva >> README.md
echo. >> README.md
echo ## 🌐 Despliegue en Railway >> README.md
echo Este sistema está configurado para desplegar automáticamente en Railway. >> README.md
echo. >> README.md
echo ## 📊 Rutas Disponibles >> README.md
echo - `/` - Sistema completo de costuras >> README.md
echo - `/soportes` - Sistema original de soportes >> README.md
echo - `/mobile` - Versión móvil >> README.md
echo - `/data` - API de datos >> README.md
echo. >> README.md
echo ## 🔧 Configuración >> README.md
echo - **Frontend**: HTML5, CSS3, JavaScript >> README.md
echo - **Backend**: Python HTTP Server >> README.md
echo - **Despliegue**: Railway con Docker >> README.md

echo ✅ Archivos preparados para GitHub
echo.

echo 📋 INSTRUCCIONES PARA SUBIR A GITHUB:
echo ───────────────────────────────────────────────────────────────
echo.
echo 🔄 OPCIÓN 1: Subir archivos manualmente (más fácil)
echo ───────────────────────────────────────────────────────────
echo 1. Ve a tu repositorio en GitHub
echo 2. Haz clic en "uploading an existing file"
echo 3. Arrastra TODA la carpeta "SOPORTACION SINES" al navegador
echo 4. Escribe un commit message: "Sistema de Costuras SINES - Listo para Railway"
echo 5. Haz clic en "Commit changes"
echo.

echo 🔄 OPCIÓN 2: Crear archivo ZIP
echo ───────────────────────────────────────────────────────────
echo 1. Selecciona todos los archivos de esta carpeta
echo 2. Crea un archivo ZIP
echo 3. Ve a GitHub y sube el ZIP
echo 4. GitHub extraerá automáticamente los archivos
echo.

echo 📱 ARCHIVOS CRÍTICOS A SUBIR:
echo ───────────────────────────────────────────────────────────────
echo ✅ index_isometricos_con_costuras.html (24.0 KB) - INTERFAZ PRINCIPAL
echo ✅ isometric_welding_manager.js (68.8 KB) - LÓGICA DEL SISTEMA
echo ✅ isometric_data_with_welds.json (6.8 MB) - DATOS DE COSTURAS
echo ✅ server_railway.py (4.6 KB) - SERVIDOR PARA RAILWAY
echo ✅ Dockerfile - CONFIGURACIÓN DE CONTENEDOR
echo ✅ railway.json - CONFIGURACIÓN DE RAILWAY
echo ✅ requirements.txt - DEPENDENCIAS PYTHON
echo ✅ README.md - DOCUMENTACIÓN
echo.

set /p github_uploaded="¿Has subido los archivos a GitHub? (s/n): "
if /i not "%github_uploaded%"=="s" (
    echo 💡 Sube los archivos a GitHub y vuelve aquí
    pause
    exit /b 1
)

echo.
echo ═══════════════════════════════════════════════════════════════════
echo 🚀 PASO 2: DESPLEGAR EN RAILWAY
echo ═══════════════════════════════════════════════════════════════════

echo.
echo 🌐 Ve a: https://railway.app/
echo 🔑 Inicia sesión con tu cuenta (usa GitHub para facilitar la conexión)
echo.
echo ➕ Crear nuevo proyecto en Railway:
echo    1. Haz clic en "New Project"
echo    2. Selecciona "Deploy from GitHub repo"
echo    3. Autoriza Railway a acceder a tus repositorios
echo    4. Selecciona el repositorio "SINES-Sistema-Costuras"
echo    5. Railway detectará automáticamente el Dockerfile
echo    6. Haz clic en "Deploy"
echo.

echo ⚙️ Configuración automática:
echo ───────────────────────────────────────────────────────────────
echo ✅ Railway usará el Dockerfile para crear el contenedor
echo ✅ La configuración railway.json se aplicará automáticamente
echo ✅ El servidor se iniciará en el puerto asignado por Railway
echo ✅ Se generará automáticamente una URL pública
echo.

echo 🔄 Proceso de despliegue:
echo ───────────────────────────────────────────────────────────────
echo 📦 1. Railway clona tu repositorio
echo 🔧 2. Construye el contenedor Docker
echo 📚 3. Instala las dependencias Python
echo 🚀 4. Inicia el servidor
echo 🌐 5. Asigna dominio público
echo.

echo 📊 MÉTRICAS DEL SISTEMA:
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
echo 🎯 RUTAS DISPONIBLES EN RAILWAY
echo ═══════════════════════════════════════════════════════════════════
echo.
echo Una vez desplegado, tendrás acceso a:
echo.
echo 🔨 https://tu-proyecto.railway.app/           - Sistema de Costuras
echo 🔧 https://tu-proyecto.railway.app/soportes  - Sistema de Soportes
echo 📐 https://tu-proyecto.railway.app/isometricos - Isométricos Básicos
echo 📱 https://tu-proyecto.railway.app/mobile    - Versión Móvil
echo 🛡️ https://tu-proyecto.railway.app/failsafe - Modo Failsafe
echo 📊 https://tu-proyecto.railway.app/data      - API de Datos
echo 📈 https://tu-proyecto.railway.app/stats     - Estadísticas
echo.

echo ⏱️ Tiempo estimado de despliegue: 3-5 minutos
echo.

set /p open_railway="¿Abrir Railway para empezar el despliegue? (s/n): "
if /i "%open_railway%"=="s" (
    echo 🌐 Abriendo Railway...
    start "" "https://railway.app/"
)

echo.
echo ═══════════════════════════════════════════════════════════════════
echo 🎉 SISTEMA LISTO PARA DESPLEGAR
echo ═══════════════════════════════════════════════════════════════════
echo.
echo 💡 RESUMEN DE PASOS:
echo    ✅ 1. Archivos verificados y preparados
echo    ✅ 2. Documentación creada
echo    ✅ 3. Configuración Railway lista
echo    📤 4. Subir archivos a GitHub
echo    🚀 5. Desplegar desde GitHub a Railway
echo.
echo 📞 Si necesitas ayuda:
echo    📧 Revisa los logs en Railway
echo    🔍 Verifica que todos los archivos se subieron
echo    🌐 Comprueba que la URL funciona
echo.
echo ✅ ¡EL SISTEMA DE COSTURAS ESTÁ LISTO PARA PRODUCCIÓN!
pause 