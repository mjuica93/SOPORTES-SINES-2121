@echo off
echo.
echo ========================================
echo   DESPLIEGUE FINAL SINES v4.1
echo   GitHub + Railway - Sistema Completo
echo ========================================
echo.

:: Limpiar archivos temporales
echo 🧹 Limpiando archivos temporales...
if exist "google_credentials.json" del "google_credentials.json"
if exist "welding_test_data.json" del "welding_test_data.json"
if exist "0.1.1" rmdir /s /q "0.1.1" 2>nul
if exist "1.1.0" rmdir /s /q "1.1.0" 2>nul
if exist "2.23.0" rmdir /s /q "2.23.0" 2>nul
if exist "2.31.0" rmdir /s /q "2.31.0" 2>nul
if exist "5.12.0" rmdir /s /q "5.12.0" 2>nul
if exist "SOPORTES-SINES-GITHUB" rmdir /s /q "SOPORTES-SINES-GITHUB" 2>nul

:: Agregar archivos modificados
echo 📁 Agregando archivos modificados...
git add index_isometricos_integrado_final.html
git add server_railway.py
git add requirements.txt
git add VERIFICACION_DESPLIEGUE_FINAL.md
git add DESPLEGAR_GITHUB_RAILWAY_FINAL.bat

:: Remover archivos eliminados
echo 🗑️ Removiendo archivos eliminados...
git rm --cached "DESPLEGAR_RAILWAY_MODAL_MEJORADO.bat" 2>nul
git rm --cached "GUIA_DESPLIEGUE_RAILWAY_MODAL_v4.1.md" 2>nul
git rm --cached "INDICE_DOCUMENTACION.md" 2>nul
git rm --cached "LANZAMIENTO_FINAL_v4.1.md" 2>nul
git rm --cached "MEJORAS_MODAL_COSTURAS.md" 2>nul
git rm --cached "PROBAR_MODAL_MEJORADO.bat" 2>nul
git rm --cached "RESUMEN_MODAL_COSTURAS_GITHUB.md" 2>nul
git rm --cached "SOLUCION_DOCUMENTACION_RAILWAY.md" 2>nul
git rm --cached "TESTING_MODAL_MEJORADO_v4.1.md" 2>nul
git rm --cached "TEST_DOCUMENTACION_LOCAL.bat" 2>nul
git rm --cached "TEST_LOCAL_MODAL_MEJORADO.bat" 2>nul
git rm --cached "server_railway_fixed.py" 2>nul

:: Verificar estado
echo 📊 Estado del repositorio:
git status

echo.
echo ✅ COMMIT: Sistema SINES v4.1 - Listo para Railway
echo.

:: Hacer commit
git commit -m "🚀 Sistema SINES v4.1 - Despliegue Final Railway

✨ Funcionalidades Implementadas:
- Modal de costuras responsivo optimizado (90% altura pantalla)
- Tabla con cabecera fija para mejor navegación
- Sistema de seguridad completo (4 niveles usuario)
- Estadísticas en tiempo real con contadores automáticos
- Selección múltiple y acciones masivas
- Auto-guardado con Enter en comentarios
- Interfaz móvil optimizada para campo

🔧 Archivos Actualizados:
- index_isometricos_integrado_final.html - Interfaz principal
- server_railway.py - Servidor optimizado Railway
- requirements.txt - Dependencias Python estándar
- VERIFICACION_DESPLIEGUE_FINAL.md - Documentación completa

📊 Datos del Sistema:
- 22,612 soportes con variables plantilla
- 1,770 isométricos regulares + 427 prefabricados  
- 3,982 relaciones soldadura trazables
- 12 variables plantilla (A,B,C,D,E,R,X,Y,EL,N.,SH.,TEMP)

🎯 Credenciales:
- admin/sines2024 - supervisor/super2024 - operador/op2024 - sines/sines123

✅ LISTO PARA DESPLIEGUE EN RAILWAY"

if %errorlevel% equ 0 (
    echo.
    echo ✅ Commit exitoso!
    echo.
    echo 🚀 Subiendo a GitHub...
    git push origin main
    
    if %errorlevel% equ 0 (
        echo.
        echo ========================================
        echo   ✅ DESPLIEGUE GITHUB COMPLETADO
        echo ========================================
        echo.
        echo 📋 PRÓXIMOS PASOS RAILWAY:
        echo.
        echo 1. Ir a: https://railway.app
        echo 2. Crear nuevo proyecto
        echo 3. Conectar con GitHub: mjuica93/SOPORTES-SINES-2121
        echo 4. Railway detectará railway.json automáticamente
        echo 5. Esperar despliegue (5-10 minutos primera vez)
        echo.
        echo 🌐 URL final: https://[proyecto].railway.app
        echo.
        echo ========================================
        echo   🎉 SISTEMA LISTO PARA PRODUCCIÓN
        echo ========================================
    ) else (
        echo.
        echo ❌ Error al subir a GitHub
        echo Revisa la conexión y credenciales
    )
) else (
    echo.
    echo ❌ Error en el commit
    echo Revisa los archivos y vuelve a intentar
)

echo.
pause 