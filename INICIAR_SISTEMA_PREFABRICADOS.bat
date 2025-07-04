@echo off
echo.
echo ================================================================
echo     SISTEMA INTEGRADO SINES v3.0 - CON ISOMETRICOS PREFABRICADOS
echo ================================================================
echo.
echo Iniciando sistema con soporte para isometricos prefabricados...
echo.

REM Verificar que existan los archivos necesarios
if not exist "index_isometricos_con_costuras.html" (
    echo ERROR: No se encuentra el archivo index_isometricos_con_costuras.html
    pause
    exit /b 1
)

if not exist "prefabricated_isometric_mapping.json" (
    echo ADVERTENCIA: No se encuentra el archivo de mapeo de prefabricados
    echo Ejecutando analisis de isometricos prefabricados...
    python analyze_prefabricated_isometrics.py
    if errorlevel 1 (
        echo ERROR: No se pudo generar el mapeo de prefabricados
        pause
        exit /b 1
    )
)

REM Mostrar estadisticas
echo.
echo --- ESTADISTICAS DEL SISTEMA ---
echo.
for /f "tokens=2 delims=:" %%a in ('findstr /c:"total_normal_files" prefabricated_isometric_mapping.json') do set NORMAL_FILES=%%a
for /f "tokens=2 delims=:" %%a in ('findstr /c:"total_prefab_files" prefabricated_isometric_mapping.json') do set PREFAB_FILES=%%a
for /f "tokens=2 delims=:" %%a in ('findstr /c:"correspondences_found" prefabricated_isometric_mapping.json') do set CORRESPONDENCES=%%a

echo ^> Isometricos normales: %NORMAL_FILES%
echo ^> Isometricos prefabricados: %PREFAB_FILES%
echo ^> Correspondencias encontradas: %CORRESPONDENCES%
echo.

REM Iniciar servidor HTTP en segundo plano
echo Iniciando servidor HTTP en puerto 8000...
start "Servidor SINES" /min python -m http.server 8000

REM Esperar un momento para que se inicie el servidor
timeout /t 3 /nobreak >nul

REM Abrir navegador
echo Abriendo navegador web...
start "" "http://localhost:8000/index_isometricos_con_costuras.html"

echo.
echo =================================================================
echo  SISTEMA INICIADO CORRECTAMENTE
echo =================================================================
echo.
echo ^> URL: http://localhost:8000/index_isometricos_con_costuras.html
echo ^> Servidor: localhost:8000
echo ^> Funcionalidades disponibles:
echo   - Gestion de soportes
echo   - Visualizacion de isometricos
echo   - Relaciones soportes-isometricos
echo   - Control de instalaciones
echo   - NUEVO: Isometricos prefabricados
echo.
echo Para detener el servidor, cierre la ventana del servidor
echo o presione Ctrl+C en la ventana del servidor
echo.
pause 