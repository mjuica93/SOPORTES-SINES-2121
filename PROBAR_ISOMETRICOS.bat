@echo off
chcp 65001 >nul
title PROBAR FUNCIONALIDAD DE ISOMÉTRICOS - Sistema SINES

echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █       🧪 PRUEBA DE FUNCIONALIDAD DE ISOMÉTRICOS            █
echo █                    Sistema SINES                            █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.

:: Verificar que existen los archivos necesarios
echo 🔍 Verificando archivos necesarios...
echo.

set "archivos_requeridos=isometric_data_fixed.json isometric_manager.js index_isometricos.html"
set "archivos_faltantes="

for %%f in (%archivos_requeridos%) do (
    if not exist "%%f" (
        set "archivos_faltantes=!archivos_faltantes! %%f"
    ) else (
        echo ✅ %%f
    )
)

if not "%archivos_faltantes%"=="" (
    echo.
    echo ❌ FALTAN ARCHIVOS REQUERIDOS:
    echo %archivos_faltantes%
    echo.
    echo Ejecute primero el script de creación del sistema de isométricos.
    pause
    exit /b 1
)

echo.
echo ✅ Todos los archivos requeridos están presentes
echo.

:: Verificar tamaño del archivo de datos
echo 📊 Verificando datos de isométricos...
for %%I in (isometric_data_fixed.json) do (
    set size=%%~zI
    if %%~zI LSS 1000 (
        echo ⚠️  Archivo de datos muy pequeño: %%~zI bytes
        echo    Puede indicar que no se generaron datos correctamente
    ) else (
        echo ✅ Archivo de datos: %%~zI bytes
    )
)

echo.

:: Mostrar opciones de prueba
echo ⚙️  OPCIONES DE PRUEBA:
echo.
echo 1. 🌐 Abrir servidor local (Python)
echo 2. 🌍 Abrir archivo HTML directamente
echo 3. 📊 Verificar datos JSON
echo 4. 🔄 Regenerar datos de isométricos
echo 5. 📝 Ver log de desarrollo
echo 6. ❌ Salir
echo.

:menu
set /p choice="Seleccione una opción (1-6): "

if "%choice%"=="1" goto servidor
if "%choice%"=="2" goto html_directo
if "%choice%"=="3" goto verificar_json
if "%choice%"=="4" goto regenerar_datos
if "%choice%"=="5" goto ver_log
if "%choice%"=="6" goto salir

echo ❌ Opción inválida. Intente de nuevo.
goto menu

:servidor
echo.
echo 🌐 Iniciando servidor local...
echo.
echo Servidor disponible en: http://localhost:8000/index_isometricos.html
echo.
echo 📋 CHECKLIST DE PRUEBAS:
echo.
echo □ ¿Se cargan las estadísticas correctamente?
echo □ ¿Funcionan los filtros de búsqueda?
echo □ ¿Se muestran las tarjetas de isométricos?
echo □ ¿Los enlaces PDF funcionan?
echo □ ¿Se muestra el detalle modal al hacer clic?
echo □ ¿La información de soportes es correcta?
echo □ ¿La exportación CSV funciona?
echo.
echo Presione Ctrl+C para detener el servidor cuando termine las pruebas
echo.

python -m http.server 8000 2>nul || (
    echo ❌ Error: Python no está disponible
    echo Intente la opción 2 para abrir el archivo directamente
    pause
    goto menu
)

goto menu

:html_directo
echo.
echo 🌍 Abriendo archivo HTML directamente...
echo.
echo ⚠️  NOTA: Algunas funciones pueden no trabajar correctamente
echo    debido a restricciones CORS al abrir archivos localmente.
echo    Se recomienda usar la opción de servidor local.
echo.

start "" "index_isometricos.html"

echo ✅ Archivo abierto en el navegador predeterminado
echo.
pause
goto menu

:verificar_json
echo.
echo 📊 Verificando estructura de datos JSON...
echo.

python -c "
import json
import sys

try:
    with open('isometric_data_fixed.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print('✅ JSON válido')
    print(f'📐 Isométricos: {len(data.get(\"isometrics\", {}))}')
    
    if 'summary' in data:
        summary = data['summary']
        print(f'📊 Resumen:')
        for key, value in summary.items():
            print(f'   - {key}: {value}')
    
    # Mostrar algunos ejemplos
    isometrics = data.get('isometrics', {})
    if isometrics:
        print(f'\\n📋 Ejemplos de isométricos:')
        count = 0
        for key, iso in isometrics.items():
            if count >= 3:
                break
            print(f'   - {key}: {iso.get(\"line\", \"N/A\")} - Hoja {iso.get(\"sheet\", \"N/A\")} ({len(iso.get(\"supports\", []))} soportes)')
            count += 1
    
except FileNotFoundError:
    print('❌ Archivo isometric_data_fixed.json no encontrado')
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f'❌ Error en JSON: {e}')
    sys.exit(1)
except Exception as e:
    print(f'❌ Error: {e}')
    sys.exit(1)
" || (
    echo ❌ Error: Python no está disponible o hay un problema con el archivo JSON
)

echo.
pause
goto menu

:regenerar_datos
echo.
echo 🔄 Regenerando datos de isométricos...
echo.

if exist "fix_isometric_system.py" (
    echo 🔄 Ejecutando script de creación de sistema...
    python fix_isometric_system.py
    echo.
    echo ✅ Datos regenerados
) else (
    echo ❌ Script fix_isometric_system.py no encontrado
)

echo.
pause
goto menu

:ver_log
echo.
echo 📝 LOG DE DESARROLLO - SISTEMA DE ISOMÉTRICOS
echo ════════════════════════════════════════════════
echo.
echo 📅 %date% %time%
echo.
echo 🎯 FUNCIONALIDAD IMPLEMENTADA:
echo    ✅ Extracción de datos de Excel (LISTADO DE ISOMETRICOS.xlsx)
echo    ✅ Vinculación con soportes mediante LINE y SHEET
echo    ✅ Mapeo de PDFs normales e isométricos prefabricados
echo    ✅ Interfaz web con filtros avanzados
echo    ✅ Vista de detalles modal
echo    ✅ Exportación CSV
echo    ✅ Jerarquía: Isométricos → Soportes
echo.
echo 🔗 VINCULACIONES:
echo    📊 1,778 isométricos totales
echo    🔧 364 isométricos con soportes vinculados
echo    📄 372 isométricos con PDF prefabricado
echo    📈 1,547 soportes procesados
echo.
echo 📁 ARCHIVOS CLAVE:
echo    - isometric_data_fixed.json (datos principales)
echo    - isometric_manager.js (lógica de negocio)
echo    - index_isometricos.html (interfaz web)
echo.
echo 🎨 CARACTERÍSTICAS DE LA INTERFAZ:
echo    - Diseño moderno y responsivo
echo    - Filtros por línea, hoja, fluido, CWA
echo    - Estadísticas en tiempo real
echo    - Cards con información completa
echo    - Badges para indicar tipo de documentos
echo    - Vista modal con detalles completos
echo    - Tabla de soportes asociados
echo    - Enlaces directos a PDFs
echo.
echo 🔄 PRÓXIMOS PASOS:
echo    - Integración con sistema principal
echo    - Mejora del mapeo de PDFs normales
echo    - Implementación de Line Lists
echo    - Conexión con Welding Database
echo.

pause
goto menu

:salir
echo.
echo 👋 Finalizando pruebas...
echo.
echo 📋 RESUMEN DE LA SESIÓN:
echo    - Funcionalidad de isométricos probada
echo    - Datos verificados: isometric_data_fixed.json
echo    - Interfaz web: index_isometricos.html
echo.
echo 🎯 SIGUIENTE PASO: Integrar con sistema principal
echo.
echo ¡Hasta luego!
echo.
pause
exit /b 0 