import json
import shutil
import os

def create_robust_version():
    print("=== CREANDO VERSIÓN ROBUSTA DEL SISTEMA ===\n")
    
    # Leer el archivo JavaScript actual
    with open('app_enhanced.js', 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    # Mejorar el manejo de errores en JavaScript
    improved_js = js_content.replace(
        'async function loadData() {',
        '''async function loadData() {
    console.log('🔄 Iniciando carga de datos...');
    
    // Mostrar mensaje de carga
    const loadingDiv = document.getElementById('loadingMessage');
    const resultsDiv = document.getElementById('resultsContainer');
    
    if (loadingDiv) {
        loadingDiv.style.display = 'block';
        loadingDiv.innerHTML = `
            <h3>📊 Cargando datos del sistema...</h3>
            <p>Por favor espere mientras se cargan los datos...</p>
            <div style="margin-top: 10px; color: #666;">
                <small>Si esta pantalla persiste, intente:</small><br>
                <small>• Refrescar la página (F5)</small><br>
                <small>• Limpiar caché del navegador</small><br>
                <small>• Usar modo incógnito</small>
            </div>
        `;
    }
    
    // Función helper para cargar JSON con reintentos
    async function loadJsonWithRetry(url, maxRetries = 3) {
        for (let attempt = 1; attempt <= maxRetries; attempt++) {
            try {
                console.log(`🔄 Intento ${attempt} para cargar: ${url}`);
                const response = await fetch(url, {
                    method: 'GET',
                    headers: {
                        'Cache-Control': 'no-cache',
                        'Pragma': 'no-cache'
                    }
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                
                const data = await response.json();
                console.log(`✅ Cargado exitosamente: ${url} (${data.length || Object.keys(data).length} elementos)`);
                return data;
            } catch (error) {
                console.warn(`❌ Error en intento ${attempt} para ${url}:`, error);
                if (attempt === maxRetries) {
                    throw new Error(`Error después de ${maxRetries} intentos: ${error.message}`);
                }
                // Esperar antes del siguiente intento
                await new Promise(resolve => setTimeout(resolve, 1000 * attempt));
            }
        }
    }'''
    )
    
    # Mejorar el manejo de errores en la carga
    improved_js = improved_js.replace(
        'try {',
        '''try {
        console.log('🔄 Iniciando carga de archivos JSON...');
        
        // Cargar archivos con reintentos'''
    )
    
    # Reemplazar las llamadas fetch individuales
    improved_js = improved_js.replace(
        '''const [supportsResponse, pdfResponse] = await Promise.all([
            fetch('support_data_enhanced.json'),
            fetch('support_pdf_mapping.json')
        ]);''',
        '''const [supportData, pdfData] = await Promise.all([
            loadJsonWithRetry('support_data_enhanced.json'),
            loadJsonWithRetry('support_pdf_mapping.json')
        ]);'''
    )
    
    # Eliminar las líneas de verificación de respuesta que ya no son necesarias
    improved_js = improved_js.replace(
        '''if (!supportsResponse.ok || !pdfResponse.ok) {
            throw new Error('Error al cargar los archivos');
        }
        
        const supportData = await supportsResponse.json();
        const pdfData = await pdfResponse.json();''',
        '''// Los datos ya están cargados por loadJsonWithRetry'''
    )
    
    # Mejorar el manejo de errores
    improved_js = improved_js.replace(
        '''} catch (error) {
        console.error('Error al cargar los datos:', error);
        document.getElementById('loadingMessage').innerHTML = `
            <h3>❌ Error al cargar los datos</h3>
            <p>Error al cargar los datos. Verifica que los archivos JSON estén disponibles.</p>
            <button onclick="location.reload()" style="padding: 10px 20px; background: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer; margin-top: 10px;">
                🔄 Reintentar
            </button>
        `;
    }''',
        '''} catch (error) {
        console.error('❌ Error crítico al cargar los datos:', error);
        
        const errorMessage = `
            <div style="text-align: center; padding: 40px; background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 10px; margin: 20px;">
                <h3 style="color: #856404;">⚠️ Error al Cargar los Datos</h3>
                <p style="color: #856404; margin: 15px 0;">
                    <strong>Detalles del error:</strong> ${error.message}
                </p>
                <div style="margin: 20px 0; padding: 15px; background: #f8f9fa; border-radius: 5px; text-align: left;">
                    <strong>Soluciones recomendadas:</strong>
                    <ol style="margin: 10px 0; padding-left: 20px;">
                        <li>Presiona <strong>F5</strong> para refrescar la página</li>
                        <li>Limpia el caché del navegador (<strong>Ctrl+Shift+Delete</strong>)</li>
                        <li>Usa modo incógnito (<strong>Ctrl+Shift+N</strong>)</li>
                        <li>Verifica que el servidor esté funcionando</li>
                        <li>Intenta con otro navegador</li>
                    </ol>
                </div>
                <div style="margin-top: 20px;">
                    <button onclick="location.reload()" style="padding: 15px 30px; background: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer; margin: 5px; font-size: 16px;">
                        🔄 Reintentar Ahora
                    </button>
                    <button onclick="window.open('http://localhost:8000/index.html', '_blank')" style="padding: 15px 30px; background: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; margin: 5px; font-size: 16px;">
                        📄 Versión Básica
                    </button>
                </div>
                <p style="margin-top: 20px; font-size: 14px; color: #666;">
                    Si el problema persiste, contacta al administrador del sistema.
                </p>
            </div>
        `;
        
        const loadingDiv = document.getElementById('loadingMessage');
        if (loadingDiv) {
            loadingDiv.innerHTML = errorMessage;
        }
    }''')
    
    # Guardar la versión mejorada
    with open('app_enhanced_robust.js', 'w', encoding='utf-8') as f:
        f.write(improved_js)
    
    # Crear HTML mejorado
    with open('index_enhanced.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Reemplazar referencia al JS
    html_content = html_content.replace('app_enhanced.js', 'app_enhanced_robust.js')
    
    # Mejorar el mensaje de carga inicial
    html_content = html_content.replace(
        '<div id="loadingMessage" class="loading">',
        '''<div id="loadingMessage" class="loading" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin: 20px;">'''
    )
    
    # Guardar HTML mejorado
    with open('index_enhanced_robust.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Versión robusta creada:")
    print("   📄 index_enhanced_robust.html")
    print("   📄 app_enhanced_robust.js")
    print("\n🌐 URL para probar:")
    print("   http://localhost:8000/index_enhanced_robust.html")
    
    # Crear un archivo de inicio específico para la versión robusta
    with open('INICIAR_VERSION_ROBUSTA.bat', 'w', encoding='utf-8') as f:
        f.write('''@echo off
title Sistema de Soportes SINES - Version Robusta
echo ================================================
echo    SISTEMA DE SOPORTES SINES - VERSION ROBUSTA
echo ================================================
echo.
echo Iniciando servidor web local...
echo.
echo URLs disponibles:
echo   Version Robusta: http://localhost:8000/index_enhanced_robust.html
echo   Version Normal:  http://localhost:8000/index_enhanced.html
echo   Version Basica:  http://localhost:8000/index.html
echo.
echo Para detener el servidor, presiona Ctrl+C
echo ================================================
echo.

start "" "http://localhost:8000/index_enhanced_robust.html"
python server.py
pause''')
    
    print("✅ Creado iniciador: INICIAR_VERSION_ROBUSTA.bat")
    
    return True

if __name__ == "__main__":
    create_robust_version() 