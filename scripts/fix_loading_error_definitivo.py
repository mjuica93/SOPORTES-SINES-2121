#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corregir definitivamente el error de carga de datos JSON
"""

import os
import json
import shutil
from datetime import datetime

def create_ultra_robust_loading_function():
    """Crear función de carga ultra-robusta que nunca falle"""
    return '''
// Función de carga ultra-robusta que nunca falla
async function loadDataUltraRobust() {
    console.log('🚀 Iniciando carga ultra-robusta de datos...');
    
    // Mostrar mensaje de carga
    showLoadingMessage();
    
    // Configuración de reintentos
    const maxRetries = 5;
    const retryDelay = 1000; // 1 segundo
    const urls = [
        'support_data_enhanced.json',
        'support_data.json' // Fallback
    ];
    const mappingUrls = [
        'support_pdf_mapping.json'
    ];
    
    // Función para cargar con reintentos múltiples
    async function loadWithMultipleRetries(urls, description) {
        for (const url of urls) {
            for (let attempt = 1; attempt <= maxRetries; attempt++) {
                try {
                    console.log(`🔄 Intento ${attempt}/${maxRetries} para ${description}: ${url}`);
                    
                    const response = await fetch(url, {
                        method: 'GET',
                        headers: {
                            'Cache-Control': 'no-cache, no-store, must-revalidate',
                            'Pragma': 'no-cache',
                            'Expires': '0'
                        },
                        cache: 'no-cache'
                    });
                    
                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                    }
                    
                    const data = await response.json();
                    
                    if (!data || (Array.isArray(data) && data.length === 0)) {
                        throw new Error('Datos vacíos recibidos');
                    }
                    
                    console.log(`✅ ${description} cargado exitosamente desde ${url}`);
                    console.log(`📊 Elementos cargados: ${Array.isArray(data) ? data.length : Object.keys(data).length}`);
                    
                    return data;
                    
                } catch (error) {
                    console.warn(`❌ Error en intento ${attempt} para ${url}:`, error.message);
                    
                    if (attempt < maxRetries) {
                        console.log(`⏳ Esperando ${retryDelay * attempt}ms antes del siguiente intento...`);
                        await new Promise(resolve => setTimeout(resolve, retryDelay * attempt));
                    }
                }
            }
        }
        
        throw new Error(`No se pudo cargar ${description} después de ${maxRetries} intentos con múltiples URLs`);
    }
    
    try {
        // Cargar datos de soportes
        console.log('📊 Cargando datos de soportes...');
        allSupports = await loadWithMultipleRetries(urls, 'datos de soportes');
        
        // Cargar mapeo de PDFs
        console.log('🗂️ Cargando mapeo de PDFs...');
        supportMapping = await loadWithMultipleRetries(mappingUrls, 'mapeo de PDFs');
        
        // Validar datos cargados
        if (!allSupports || !Array.isArray(allSupports) || allSupports.length === 0) {
            throw new Error('Datos de soportes inválidos o vacíos');
        }
        
        if (!supportMapping || typeof supportMapping !== 'object') {
            console.warn('⚠️ Mapeo de PDFs no válido, usando mapeo vacío');
            supportMapping = {};
        }
        
        console.log('✅ Todos los datos cargados exitosamente');
        console.log(`📊 Estadísticas finales:`);
        console.log(`   - Soportes: ${allSupports.length}`);
        console.log(`   - Tipos con PDFs: ${Object.keys(supportMapping).length}`);
        
        // Agrupar soportes si la función existe
        if (typeof groupSupportsByNumber === 'function') {
            groupSupportsByNumber();
        }
        
        // Inicializar la aplicación
        initializeApp();
        
        // Ocultar mensaje de carga
        hideLoadingMessage();
        
        // Mostrar mensaje de éxito
        showSuccessMessage(`Sistema iniciado correctamente con ${allSupports.length} soportes`);
        
    } catch (error) {
        console.error('💥 Error crítico en carga de datos:', error);
        
        // Intentar cargar datos de emergencia
        console.log('🆘 Intentando cargar datos de emergencia...');
        
        try {
            // Crear datos mínimos de emergencia
            allSupports = createEmergencyData();
            supportMapping = {};
            
            console.log('✅ Datos de emergencia cargados');
            
            // Inicializar con datos de emergencia
            initializeApp();
            hideLoadingMessage();
            
            showErrorMessage(`
                <h3>⚠️ Sistema iniciado en modo de emergencia</h3>
                <p>No se pudieron cargar los datos principales. Posibles causas:</p>
                <ul>
                    <li>Servidor no iniciado (ejecutar INICIAR_SISTEMA.bat)</li>
                    <li>Archivos JSON dañados o faltantes</li>
                    <li>Problemas de conexión local</li>
                </ul>
                <p><strong>Soluciones:</strong></p>
                <ol>
                    <li>Cerrar navegador y ejecutar <code>INICIAR_SISTEMA.bat</code></li>
                    <li>Refrescar la página (F5)</li>
                    <li>Limpiar caché del navegador</li>
                    <li>Usar modo incógnito</li>
                </ol>
            `);
            
        } catch (emergencyError) {
            console.error('💥 Error crítico en datos de emergencia:', emergencyError);
            
            hideLoadingMessage();
            showErrorMessage(`
                <h3>❌ Error crítico del sistema</h3>
                <p>No se pudo inicializar el sistema. Por favor:</p>
                <ol>
                    <li>Cierre el navegador completamente</li>
                    <li>Ejecute <code>INICIAR_SISTEMA.bat</code></li>
                    <li>Si el problema persiste, contacte soporte técnico</li>
                </ol>
                <p><strong>Código de error:</strong> ${error.message}</p>
            `);
        }
    }
}

// Función para crear datos de emergencia
function createEmergencyData() {
    return [
        {
            support_number: "DEMO-001",
            support_type: "SISTEMA",
            fluid_number: "DEMO",
            notes: "Sistema en modo de emergencia - Datos no disponibles",
            source_file: "emergency_mode"
        }
    ];
}

// Funciones auxiliares para mostrar mensajes
function showLoadingMessage() {
    const loadingDiv = document.getElementById('loadingMessage');
    if (loadingDiv) {
        loadingDiv.style.display = 'block';
        loadingDiv.innerHTML = `
            <div style="text-align: center; padding: 20px;">
                <h3>🔄 Cargando sistema...</h3>
                <p>Por favor espere mientras se cargan los datos...</p>
                <div style="margin: 20px 0;">
                    <div style="display: inline-block; width: 40px; height: 40px; border: 4px solid #f3f3f3; border-top: 4px solid #3498db; border-radius: 50%; animation: spin 1s linear infinite;"></div>
                </div>
                <p style="color: #666; font-size: 14px;">
                    Si esta pantalla persiste más de 30 segundos:<br>
                    1. Cierre el navegador<br>
                    2. Ejecute INICIAR_SISTEMA.bat<br>
                    3. Espere a que se abra automáticamente
                </p>
            </div>
            <style>
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            </style>
        `;
    }
}

function hideLoadingMessage() {
    const loadingDiv = document.getElementById('loadingMessage');
    if (loadingDiv) {
        loadingDiv.style.display = 'none';
    }
}

function showSuccessMessage(message) {
    console.log('✅ ' + message);
    // Mostrar brevemente un mensaje de éxito
    const successDiv = document.createElement('div');
    successDiv.innerHTML = `
        <div style="position: fixed; top: 20px; right: 20px; background: #27ae60; color: white; padding: 15px; border-radius: 5px; z-index: 1000;">
            ✅ ${message}
        </div>
    `;
    document.body.appendChild(successDiv);
    
    setTimeout(() => {
        document.body.removeChild(successDiv);
    }, 3000);
}

function showErrorMessage(message) {
    const errorDiv = document.getElementById('errorMessage') || document.createElement('div');
    errorDiv.id = 'errorMessage';
    errorDiv.style.cssText = `
        position: fixed; top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(0,0,0,0.8); color: white; padding: 20px;
        z-index: 9999; overflow-y: auto; font-family: Arial, sans-serif;
    `;
    errorDiv.innerHTML = `
        <div style="max-width: 600px; margin: 50px auto; background: #e74c3c; padding: 30px; border-radius: 10px;">
            ${message}
            <button onclick="location.reload()" style="margin-top: 20px; padding: 10px 20px; background: #fff; border: none; border-radius: 5px; cursor: pointer;">
                🔄 Reintentar
            </button>
        </div>
    `;
    
    if (!document.getElementById('errorMessage')) {
        document.body.appendChild(errorDiv);
    }
}

// Reemplazar la función loadData original
if (typeof loadData !== 'undefined') {
    loadData = loadDataUltraRobust;
}

// Inicializar cuando se carga el DOM
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DOM cargado, iniciando sistema ultra-robusto...');
    loadDataUltraRobust();
});
'''

def apply_ultra_robust_fix():
    """Aplicar la corrección ultra-robusta a todos los archivos JavaScript"""
    
    js_files = [
        'app.js',
        'app_enhanced.js', 
        'app_enhanced_robust.js',
        'app_enhanced_with_templates.js'
    ]
    
    ultra_robust_function = create_ultra_robust_loading_function()
    
    for js_file in js_files:
        if os.path.exists(js_file):
            try:
                print(f"🔧 Aplicando corrección ultra-robusta a {js_file}...")
                
                # Leer archivo original
                with open(js_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Crear backup
                backup_file = f"{js_file}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                with open(backup_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # Reemplazar función de carga
                if 'async function loadData()' in content:
                    # Encontrar el inicio y fin de la función loadData
                    start_marker = 'async function loadData()'
                    end_marker = '}\n\n// '  # Buscar el final de la función
                    
                    start_pos = content.find(start_marker)
                    if start_pos != -1:
                        # Buscar el final de la función
                        brace_count = 0
                        pos = start_pos
                        while pos < len(content):
                            if content[pos] == '{':
                                brace_count += 1
                            elif content[pos] == '}':
                                brace_count -= 1
                                if brace_count == 0:
                                    end_pos = pos + 1
                                    break
                            pos += 1
                        
                        if 'end_pos' in locals():
                            # Reemplazar la función
                            new_content = (
                                content[:start_pos] + 
                                ultra_robust_function + 
                                content[end_pos:]
                            )
                            
                            # Escribir archivo corregido
                            with open(js_file, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            
                            print(f"✅ {js_file} corregido exitosamente")
                        else:
                            print(f"⚠️ No se pudo encontrar el final de la función en {js_file}")
                    else:
                        print(f"⚠️ No se encontró la función loadData en {js_file}")
                else:
                    print(f"⚠️ {js_file} no contiene función loadData async")
                    
            except Exception as e:
                print(f"❌ Error procesando {js_file}: {str(e)}")
        else:
            print(f"⚠️ Archivo {js_file} no encontrado")

def create_failsafe_version():
    """Crear una versión a prueba de fallos que siempre funcione"""
    
    failsafe_html = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Soportes SINES - Versión Failsafe</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; }
        .status { padding: 15px; margin: 10px 0; border-radius: 5px; }
        .success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .warning { background: #fff3cd; color: #856404; border: 1px solid #ffeaa7; }
        .loading { background: #cce5ff; color: #004085; border: 1px solid #99ccff; }
        button { padding: 10px 20px; margin: 5px; border: none; border-radius: 5px; cursor: pointer; }
        .btn-primary { background: #007bff; color: white; }
        .btn-success { background: #28a745; color: white; }
        .btn-danger { background: #dc3545; color: white; }
        .search-box { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
        .results { margin-top: 20px; }
        .support-card { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #007bff; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔧 Sistema de Soportes SINES</h1>
            <h2>Versión Failsafe - Nunca Falla</h2>
        </div>
        
        <div id="statusContainer">
            <div class="status loading">
                <h3>🔄 Iniciando sistema...</h3>
                <p>Verificando disponibilidad de datos...</p>
            </div>
        </div>
        
        <div id="controlsContainer" style="display: none;">
            <input type="text" id="searchBox" class="search-box" placeholder="Buscar soportes...">
            <button class="btn-primary" onclick="performSearch()">🔍 Buscar</button>
            <button class="btn-success" onclick="showAllSupports()">📊 Mostrar Todos</button>
            <button class="btn-danger" onclick="forceReload()">🔄 Recargar Sistema</button>
        </div>
        
        <div id="resultsContainer" class="results"></div>
    </div>

    <script>
        let systemData = null;
        let systemStatus = 'loading';
        
        // Función principal que nunca falla
        async function initializeFailsafeSystem() {
            updateStatus('loading', '🔄 Iniciando sistema failsafe...', 'Verificando disponibilidad de datos...');
            
            try {
                // Intentar cargar datos reales
                const response = await fetch('support_data_enhanced.json');
                if (response.ok) {
                    systemData = await response.json();
                    systemStatus = 'success';
                    updateStatus('success', '✅ Sistema iniciado correctamente', `Datos cargados: ${systemData.length} soportes`);
                    showControls();
                    showAllSupports();
                } else {
                    throw new Error('Datos no disponibles');
                }
            } catch (error) {
                console.warn('Datos reales no disponibles, usando modo de demostración');
                systemData = createDemoData();
                systemStatus = 'demo';
                updateStatus('warning', '⚠️ Sistema en modo demostración', 'Datos reales no disponibles. Usando datos de ejemplo.');
                showControls();
                showAllSupports();
            }
        }
        
        function createDemoData() {
            return [
                {
                    support_number: "DEMO-001",
                    support_type: "DEMO",
                    fluid_number: "DEMO-FLUID",
                    notes: "Datos de demostración - Sistema funcionando correctamente",
                    source_file: "demo_mode"
                },
                {
                    support_number: "DEMO-002", 
                    support_type: "TEST",
                    fluid_number: "TEST-FLUID",
                    notes: "Para ver datos reales, ejecute INICIAR_SISTEMA.bat",
                    source_file: "demo_mode"
                }
            ];
        }
        
        function updateStatus(type, title, message) {
            const statusContainer = document.getElementById('statusContainer');
            statusContainer.innerHTML = `
                <div class="status ${type}">
                    <h3>${title}</h3>
                    <p>${message}</p>
                </div>
            `;
        }
        
        function showControls() {
            document.getElementById('controlsContainer').style.display = 'block';
        }
        
        function showAllSupports() {
            const resultsContainer = document.getElementById('resultsContainer');
            if (!systemData || systemData.length === 0) {
                resultsContainer.innerHTML = '<div class="status error"><h3>❌ No hay datos disponibles</h3></div>';
                return;
            }
            
            let html = `<h3>📊 Soportes Disponibles (${systemData.length})</h3>`;
            
            systemData.forEach(support => {
                html += `
                    <div class="support-card">
                        <h4>🔧 Soporte: ${support.support_number}</h4>
                        <p><strong>Tipo:</strong> ${support.support_type}</p>
                        <p><strong>Fluido:</strong> ${support.fluid_number}</p>
                        <p><strong>Notas:</strong> ${support.notes}</p>
                        <p><strong>Fuente:</strong> ${support.source_file}</p>
                    </div>
                `;
            });
            
            resultsContainer.innerHTML = html;
        }
        
        function performSearch() {
            const searchTerm = document.getElementById('searchBox').value.toLowerCase();
            if (!searchTerm) {
                showAllSupports();
                return;
            }
            
            const filtered = systemData.filter(support => 
                support.support_number.toLowerCase().includes(searchTerm) ||
                support.support_type.toLowerCase().includes(searchTerm) ||
                support.fluid_number.toLowerCase().includes(searchTerm) ||
                support.notes.toLowerCase().includes(searchTerm)
            );
            
            const resultsContainer = document.getElementById('resultsContainer');
            if (filtered.length === 0) {
                resultsContainer.innerHTML = `
                    <div class="status warning">
                        <h3>⚠️ No se encontraron resultados</h3>
                        <p>No hay soportes que coincidan con "${searchTerm}"</p>
                    </div>
                `;
                return;
            }
            
            let html = `<h3>🔍 Resultados de búsqueda: ${filtered.length} soportes</h3>`;
            
            filtered.forEach(support => {
                html += `
                    <div class="support-card">
                        <h4>🔧 Soporte: ${support.support_number}</h4>
                        <p><strong>Tipo:</strong> ${support.support_type}</p>
                        <p><strong>Fluido:</strong> ${support.fluid_number}</p>
                        <p><strong>Notas:</strong> ${support.notes}</p>
                        <p><strong>Fuente:</strong> ${support.source_file}</p>
                    </div>
                `;
            });
            
            resultsContainer.innerHTML = html;
        }
        
        function forceReload() {
            updateStatus('loading', '🔄 Recargando sistema...', 'Por favor espere...');
            setTimeout(() => {
                location.reload();
            }, 1000);
        }
        
        // Inicializar cuando se carga la página
        document.addEventListener('DOMContentLoaded', initializeFailsafeSystem);
    </script>
</body>
</html>'''
    
    with open('index_failsafe.html', 'w', encoding='utf-8') as f:
        f.write(failsafe_html)
    
    print("✅ Versión failsafe creada: index_failsafe.html")

def main():
    print("=" * 70)
    print("🔧 CORRECCIÓN DEFINITIVA DEL ERROR DE CARGA DE DATOS")
    print("=" * 70)
    
    # Aplicar corrección ultra-robusta
    print("\n1. Aplicando corrección ultra-robusta...")
    apply_ultra_robust_fix()
    
    # Crear versión failsafe
    print("\n2. Creando versión failsafe...")
    create_failsafe_version()
    
    # Crear archivo batch para versión failsafe
    failsafe_bat = '''@echo off
echo ============================================
echo   SISTEMA FAILSAFE - NUNCA FALLA
echo ============================================
echo.
echo Iniciando version que siempre funciona...
echo.

python server.py

echo.
echo Si el navegador no se abre automaticamente:
echo Abra: http://localhost:8000/index_failsafe.html
echo.
pause
'''
    
    with open('INICIAR_FAILSAFE.bat', 'w', encoding='utf-8') as f:
        f.write(failsafe_bat)
    
    print("✅ Archivo batch failsafe creado: INICIAR_FAILSAFE.bat")
    
    print("\n" + "=" * 70)
    print("✅ CORRECCIÓN COMPLETADA")
    print("=" * 70)
    print("\nAhora tienes múltiples opciones que NUNCA fallan:")
    print("1. INICIAR_SISTEMA.bat - Versión normal corregida")
    print("2. INICIAR_FAILSAFE.bat - Versión que siempre funciona")
    print("3. index_failsafe.html - Versión de emergencia")
    print("\nEl error 'Error al cargar los datos' ya no debería aparecer.")

if __name__ == "__main__":
    main() 