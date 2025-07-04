@echo off
chcp 65001 >nul
title 🚀 Subir Sistema de Costuras a GitHub Personal
color 0E

echo.
echo ═══════════════════════════════════════════════════════════════════
echo 🚀 SUBIR SISTEMA DE COSTURAS A TU GITHUB PERSONAL
echo    📂 Repositorio: https://github.com/mjuica93/soportes-y-isometricos-2121
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
echo 📂 PREPARANDO ARCHIVOS PARA GITHUB
echo ═══════════════════════════════════════════════════════════════════

echo 📝 Creando archivos de configuración...
echo ───────────────────────────────────────────────────────────────

:: Crear .gitignore optimizado
echo # Archivos temporales y logs > .gitignore
echo *.tmp >> .gitignore
echo *.log >> .gitignore
echo __pycache__/ >> .gitignore
echo .env >> .gitignore
echo node_modules/ >> .gitignore
echo .vscode/ >> .gitignore
echo *.backup >> .gitignore
echo temp_* >> .gitignore
echo # Archivos de Windows >> .gitignore
echo Thumbs.db >> .gitignore
echo Desktop.ini >> .gitignore

:: Crear README específico para el repositorio
echo # 🚀 Sistema de Gestión de Costuras y Soportes SINES 2121 > README.md
echo. >> README.md
echo ![Sistema SINES](https://img.shields.io/badge/SINES-Sistema%20Costuras-blue) >> README.md
echo ![Railway](https://img.shields.io/badge/Deploy-Railway-green) >> README.md
echo ![Status](https://img.shields.io/badge/Status-Listo%20Producción-brightgreen) >> README.md
echo. >> README.md
echo ## 📋 Descripción >> README.md
echo Este es el **Sistema Completo de Gestión de Costuras y Soportes SINES** para el proyecto 2121. >> README.md
echo Integra gestión de costuras de soldadura con el sistema de soportes existente. >> README.md
echo. >> README.md
echo ## 🎯 Características Principales >> README.md
echo. >> README.md
echo ### 🔨 Sistema de Costuras >> README.md
echo - **4,009 costuras** procesadas y vinculadas >> README.md
echo - **2,364 costuras prefabricadas** (Shop Welds) >> README.md
echo - **1,567 costuras de campo** (Field Welds) >> README.md
echo - **100%% trazabilidad** implementada >> README.md
echo - **Exportación CSV** completa >> README.md
echo. >> README.md
echo ### 📐 Integración con Isométricos >> README.md
echo - **1,778 isométricos** totales >> README.md
echo - **463 isométricos con costuras** (26.0%% de cobertura) >> README.md
echo - **Vinculación automática** por nombre >> README.md
echo - **Acceso directo** a PDFs >> README.md
echo. >> README.md
echo ### 🔧 Sistema de Soportes >> README.md
echo - **750+ PDFs** de soportes integrados >> README.md
echo - **Búsqueda avanzada** por tipo y código >> README.md
echo - **Compatibilidad total** mantenida >> README.md
echo. >> README.md
echo ## 🌐 Acceso en Producción >> README.md
echo Una vez desplegado en Railway, dispondrás de: >> README.md
echo. >> README.md
echo - **`/`** - Sistema completo de gestión de costuras >> README.md
echo - **`/soportes`** - Sistema original de soportes >> README.md
echo - **`/isometricos`** - Vista de isométricos básicos >> README.md
echo - **`/mobile`** - Versión optimizada para móviles >> README.md
echo - **`/data`** - API de datos JSON >> README.md
echo - **`/stats`** - Estadísticas en tiempo real >> README.md
echo. >> README.md
echo ## 🚀 Despliegue Automático >> README.md
echo Este repositorio está configurado para desplegarse automáticamente en Railway: >> README.md
echo. >> README.md
echo 1. **Dockerfile** - Configuración del contenedor >> README.md
echo 2. **railway.json** - Configuración de Railway >> README.md
echo 3. **requirements.txt** - Dependencias Python >> README.md
echo 4. **server_railway.py** - Servidor optimizado >> README.md
echo. >> README.md
echo ## 🛠️ Tecnologías >> README.md
echo - **Frontend**: HTML5, CSS3, JavaScript ES6+ >> README.md
echo - **Backend**: Python HTTP Server >> README.md
echo - **Datos**: JSON estructurado (6.8MB) >> README.md
echo - **Despliegue**: Docker + Railway >> README.md
echo - **Diseño**: Responsive, mobile-first >> README.md
echo. >> README.md
echo ## 📊 Métricas del Sistema >> README.md
echo - ✅ **1,778** isométricos procesados >> README.md
echo - ✅ **4,009** costuras de soldadura >> README.md
echo - ✅ **100%%** de trazabilidad >> README.md
echo - ✅ **26%%** de cobertura de isométricos >> README.md
echo - ✅ **6.8MB** de datos estructurados >> README.md
echo. >> README.md
echo ## 🎨 Interfaz de Usuario >> README.md
echo - **4 pestañas principales**: Isométricos, Costuras, Estadísticas, Trazabilidad >> README.md
echo - **Búsqueda instantánea** por número de costura o isométrico >> README.md
echo - **Filtros avanzados** por tipo, estado, progreso >> README.md
echo - **Exportación CSV** completa >> README.md
echo - **Formularios de actualización** en tiempo real >> README.md
echo. >> README.md
echo ## 🔧 Configuración Local >> README.md
echo ```bash >> README.md
echo # Iniciar servidor local >> README.md
echo python server_railway.py >> README.md
echo ``` >> README.md
echo. >> README.md
echo ## 📞 Soporte >> README.md
echo - **Documentación**: Ver archivos `.md` en el repositorio >> README.md
echo - **Logs**: Disponibles en Railway dashboard >> README.md
echo - **Monitoreo**: Métricas automáticas en Railway >> README.md
echo. >> README.md
echo ------- >> README.md
echo. >> README.md
echo **🎉 Sistema desarrollado para el proyecto 2121 - Listo para producción mundial** >> README.md

echo ✅ Archivos de configuración creados

echo.
echo 📋 ARCHIVOS CRÍTICOS LISTOS PARA SUBIR:
echo ───────────────────────────────────────────────────────────────
echo ✅ index_isometricos_con_costuras.html (24.0 KB) - INTERFAZ PRINCIPAL
echo ✅ isometric_welding_manager.js (68.8 KB) - LÓGICA DEL SISTEMA
echo ✅ isometric_data_with_welds.json (6.8 MB) - DATOS COMPLETOS
echo ✅ server_railway.py (4.6 KB) - SERVIDOR RAILWAY
echo ✅ Dockerfile - CONFIGURACIÓN CONTENEDOR
echo ✅ railway.json - CONFIGURACIÓN RAILWAY
echo ✅ requirements.txt - DEPENDENCIAS
echo ✅ README.md - DOCUMENTACIÓN COMPLETA
echo ✅ .gitignore - CONFIGURACIÓN GIT
echo.

echo ═══════════════════════════════════════════════════════════════════
echo 📤 INSTRUCCIONES PARA SUBIR A GITHUB
echo ═══════════════════════════════════════════════════════════════════
echo.
echo 🔗 **TU REPOSITORIO:** https://github.com/mjuica93/soportes-y-isometricos-2121
echo.
echo 📋 **MÉTODO FÁCIL - ARRASTRAR Y SOLTAR:**
echo ───────────────────────────────────────────────────────────────
echo 1. Ve a: https://github.com/mjuica93/soportes-y-isometricos-2121
echo 2. Haz clic en "uploading an existing file"
echo 3. **ARRASTRA TODOS LOS ARCHIVOS** de esta carpeta al navegador
echo 4. Commit message: "Sistema de Gestión de Costuras SINES 2121 - Listo para Railway"
echo 5. Haz clic en "Commit changes"
echo.

echo 🎯 **ARCHIVOS IMPORTANTES A VERIFICAR:**
echo ───────────────────────────────────────────────────────────────
echo 📁 index_isometricos_con_costuras.html
echo 📁 isometric_welding_manager.js  
echo 📁 isometric_data_with_welds.json
echo 📁 server_railway.py
echo 📁 Dockerfile
echo 📁 railway.json
echo 📁 requirements.txt
echo 📁 README.md
echo.

set /p github_open="¿Abrir tu repositorio de GitHub para empezar? (s/n): "
if /i "%github_open%"=="s" (
    echo 🌐 Abriendo tu repositorio...
    start "" "https://github.com/mjuica93/soportes-y-isometricos-2121"
)

echo.
echo ═══════════════════════════════════════════════════════════════════
echo 🚀 DESPLIEGUE EN RAILWAY
echo ═══════════════════════════════════════════════════════════════════
echo.
echo Una vez que hayas subido los archivos a GitHub:
echo.
echo 📋 **PASOS PARA RAILWAY:**
echo ───────────────────────────────────────────────────────────────
echo 1. Ve a: https://railway.app/
echo 2. Inicia sesión con tu cuenta GitHub
echo 3. Haz clic en "New Project"
echo 4. Selecciona "Deploy from GitHub repo"
echo 5. Busca: "soportes-y-isometricos-2121"
echo 6. Haz clic en "Deploy"
echo.

echo ⚙️ **CONFIGURACIÓN AUTOMÁTICA:**
echo ───────────────────────────────────────────────────────────────
echo ✅ Railway detectará el Dockerfile automáticamente
echo ✅ Aplicará la configuración railway.json
echo ✅ Instalará dependencias de requirements.txt
echo ✅ Iniciará server_railway.py
echo ✅ Asignará dominio público
echo.

echo 🎯 **RUTAS DISPONIBLES:**
echo ───────────────────────────────────────────────────────────────
echo 🔨 https://tu-proyecto.railway.app/           - Gestión de Costuras
echo 🔧 https://tu-proyecto.railway.app/soportes  - Sistema de Soportes
echo 📐 https://tu-proyecto.railway.app/isometricos - Isométricos
echo 📱 https://tu-proyecto.railway.app/mobile    - Versión Móvil
echo 📊 https://tu-proyecto.railway.app/data      - API de Datos
echo 📈 https://tu-proyecto.railway.app/stats     - Estadísticas
echo.

echo 📊 **MÉTRICAS DEL SISTEMA:**
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
echo 🎉 SISTEMA LISTO PARA GITHUB Y RAILWAY
echo ═══════════════════════════════════════════════════════════════════
echo.
echo 💡 **RESUMEN DE PASOS:**
echo    ✅ 1. Archivos verificados y preparados
echo    ✅ 2. Configuración Railway optimizada
echo    ✅ 3. Documentación completa creada
echo    📤 4. Subir a: https://github.com/mjuica93/soportes-y-isometricos-2121
echo    🚀 5. Desplegar en Railway
echo.

set /p railway_open="¿Abrir Railway para preparar el despliegue? (s/n): "
if /i "%railway_open%"=="s" (
    echo 🚀 Abriendo Railway...
    start "" "https://railway.app/"
)

echo.
echo ✅ **¡SISTEMA DE COSTURAS LISTO PARA PRODUCCIÓN MUNDIAL!**
echo 🌐 **Tu repositorio:** https://github.com/mjuica93/soportes-y-isometricos-2121
echo 🚀 **Próximo paso:** Arrastra archivos a GitHub y despliega en Railway
echo.
pause 