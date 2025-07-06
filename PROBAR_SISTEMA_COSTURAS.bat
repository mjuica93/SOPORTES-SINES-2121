@echo off
title Prueba del Sistema Integrado SINES
color 0B

echo ====================================================
echo     PRUEBA DEL SISTEMA INTEGRADO SINES v2.0
echo          Verificacion de Componentes
echo ====================================================
echo.

:: Verificar Python
echo [TEST] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [FALLO] Python no esta instalado
    goto :error
) else (
    echo [OK] Python encontrado
)

:: Verificar archivos JSON necesarios
echo.
echo [TEST] Verificando archivos de datos...

set FILES_OK=1

if not exist "support_data.json" (
    echo [FALLO] support_data.json no encontrado
    set FILES_OK=0
) else (
    echo [OK] support_data.json encontrado
)

if not exist "support_pdf_mapping.json" (
    echo [FALLO] support_pdf_mapping.json no encontrado
    set FILES_OK=0
) else (
    echo [OK] support_pdf_mapping.json encontrado
)

if not exist "isometric_data.json" (
    echo [FALLO] isometric_data.json no encontrado
    set FILES_OK=0
) else (
    echo [OK] isometric_data.json encontrado
)

if not exist "support_isometric_relation.json" (
    echo [FALLO] support_isometric_relation.json no encontrado
    set FILES_OK=0
) else (
    echo [OK] support_isometric_relation.json encontrado
)

:: Verificar archivos web
echo.
echo [TEST] Verificando archivos web...

if not exist "index_isometricos_con_costuras.html" (
    echo [FALLO] index_isometricos_con_costuras.html no encontrado
    set FILES_OK=0
) else (
    echo [OK] index_isometricos_con_costuras.html encontrado
)

:: Verificar carpetas de recursos
echo.
echo [TEST] Verificando carpetas de recursos...

if not exist "ISOMETRICOS" (
    echo [FALLO] Carpeta ISOMETRICOS no encontrada
    set FILES_OK=0
) else (
    echo [OK] Carpeta ISOMETRICOS encontrada
)

if not exist "ESTANDARES DE SOPORTES" (
    echo [FALLO] Carpeta ESTANDARES DE SOPORTES no encontrada
    set FILES_OK=0
) else (
    echo [OK] Carpeta ESTANDARES DE SOPORTES encontrada
)

:: Validar archivos JSON
echo.
echo [TEST] Validando estructura de archivos JSON...

python -c "
import json
import sys

files_to_check = [
    'support_data.json',
    'support_pdf_mapping.json', 
    'isometric_data.json',
    'support_isometric_relation.json'
]

all_valid = True
for file in files_to_check:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f'[OK] {file} - JSON valido')
    except FileNotFoundError:
        print(f'[FALLO] {file} - Archivo no encontrado')
        all_valid = False
    except json.JSONDecodeError as e:
        print(f'[FALLO] {file} - JSON invalido: {e}')
        all_valid = False
    except Exception as e:
        print(f'[FALLO] {file} - Error: {e}')
        all_valid = False

if not all_valid:
    sys.exit(1)
"

if errorlevel 1 (
    echo [FALLO] Algunos archivos JSON son invalidos
    set FILES_OK=0
)

:: Mostrar estadisticas del sistema
echo.
echo [TEST] Mostrando estadisticas del sistema...

python -c "
import json
try:
    # Cargar datos
    with open('support_data.json', 'r', encoding='utf-8') as f:
        supports = json.load(f)
    with open('isometric_data.json', 'r', encoding='utf-8') as f:
        isometrics = json.load(f)
    with open('support_isometric_relation.json', 'r', encoding='utf-8') as f:
        relations = json.load(f)
    
    print(f'[ESTADISTICAS] Soportes: {len(supports)}')
    print(f'[ESTADISTICAS] Isometricos: {len(isometrics)} lineas')
    print(f'[ESTADISTICAS] Relaciones: {len(relations)}')
    
    # Calcular hojas totales
    total_sheets = sum(len(iso['sheets']) for iso in isometrics.values())
    print(f'[ESTADISTICAS] Hojas PDF: {total_sheets}')
    
    # Calcular cobertura
    unique_supports = len(set(r['support_number'] for r in relations))
    coverage = (unique_supports / len(supports)) * 100 if len(supports) > 0 else 0
    print(f'[ESTADISTICAS] Cobertura: {coverage:.1f}%')
    
except Exception as e:
    print(f'[ERROR] No se pudieron calcular estadisticas: {e}')
"

:: Resultado final
echo.
echo ====================================================
if %FILES_OK%==1 (
    echo [EXITO] Todas las pruebas pasaron correctamente
    echo [INFO] El sistema esta listo para usar
    echo [INFO] Ejecute INICIAR_SISTEMA_COSTURAS.bat para iniciar
) else (
    echo [FALLO] Algunas pruebas fallaron
    echo [INFO] Revise los errores arriba y corrija los problemas
)
echo ====================================================
echo.

pause
exit /b %FILES_OK%

:error
echo [FALLO] Error critico encontrado
pause
exit /b 1 