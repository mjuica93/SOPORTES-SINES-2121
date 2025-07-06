import json
import os

def create_ultimate_version():
    print("=== CREANDO VERSIÓN DEFINITIVA DEL SISTEMA ===\n")
    
    # Leer los datos JSON
    with open('support_data_enhanced.json', 'r', encoding='utf-8') as f:
        support_data = json.load(f)
    
    with open('support_pdf_mapping.json', 'r', encoding='utf-8') as f:
        pdf_mapping = json.load(f)
    
    # Crear HTML con datos embebidos como fallback
    html_content = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Búsqueda de Soportes SINES - Versión Definitiva</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white;
            padding: 30px;
            text-align: center;
            position: relative;
        }}
        
        .header::after {{
            content: '';
            position: absolute;
            bottom: -10px;
            left: 0;
            right: 0;
            height: 20px;
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            transform: skewY(-1deg);
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .version-badge {{
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(255,255,255,0.2);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
        }}
        
        .search-section {{
            padding: 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .search-container {{
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}
        
        .search-input {{
            flex: 1;
            min-width: 250px;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: all 0.3s;
        }}
        
        .search-input:focus {{
            outline: none;
            border-color: #3498db;
            box-shadow: 0 0 10px rgba(52, 152, 219, 0.3);
        }}
        
        .search-btn {{
            padding: 15px 30px;
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: bold;
        }}
        
        .search-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(52, 152, 219, 0.4);
        }}
        
        .filters {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }}
        
        .filter-select {{
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 14px;
            background: white;
            cursor: pointer;
        }}
        
        .stats {{
            display: flex;
            justify-content: space-around;
            padding: 20px;
            background: linear-gradient(135deg, #e8f4f8, #d4edda);
            text-align: center;
        }}
        
        .stat {{
            padding: 15px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            min-width: 120px;
        }}
        
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .stat-label {{
            color: #7f8c8d;
            font-size: 0.9em;
            margin-top: 5px;
        }}
        
        .results {{
            padding: 20px;
        }}
        
        .support-group {{
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 10px;
            margin-bottom: 15px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: all 0.3s;
        }}
        
        .support-group:hover {{
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }}
        
        .group-header {{
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            padding: 15px;
            cursor: pointer;
            border-bottom: 1px solid #e9ecef;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.3s;
        }}
        
        .group-header:hover {{
            background: linear-gradient(135deg, #e9ecef, #dee2e6);
        }}
        
        .group-title {{
            font-weight: bold;
            color: #2c3e50;
            font-size: 1.1em;
        }}
        
        .group-count {{
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
        }}
        
        .group-content {{
            display: none;
            padding: 15px;
            background: #fafafa;
        }}
        
        .group-content.show {{
            display: block;
        }}
        
        .support-item {{
            background: white;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 8px;
            border-left: 4px solid #3498db;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        
        .support-sections {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}
        
        .support-section {{
            background: #f8f9fa;
            padding: 12px;
            border-radius: 8px;
            border: 1px solid #e9ecef;
        }}
        
        .section-title {{
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 8px;
            padding-bottom: 5px;
            border-bottom: 2px solid #3498db;
            font-size: 0.9em;
        }}
        
        .section-content {{
            font-size: 0.85em;
            color: #555;
        }}
        
        .section-content div {{
            margin-bottom: 3px;
        }}
        
        .pdf-links {{
            margin-top: 15px;
            padding-top: 10px;
            border-top: 1px solid #e9ecef;
        }}
        
        .pdf-link {{
            display: inline-block;
            background: linear-gradient(135deg, #e74c3c, #c0392b);
            color: white;
            padding: 8px 12px;
            margin: 3px;
            border-radius: 5px;
            text-decoration: none;
            font-size: 0.8em;
            transition: all 0.3s;
        }}
        
        .pdf-link:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(231, 76, 60, 0.4);
        }}
        
        .pagination {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            padding: 20px;
        }}
        
        .pagination button {{
            padding: 10px 15px;
            border: 1px solid #ddd;
            background: white;
            cursor: pointer;
            border-radius: 5px;
            transition: all 0.3s;
        }}
        
        .pagination button:hover {{
            background: #f8f9fa;
            transform: translateY(-1px);
        }}
        
        .pagination button.active {{
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            border-color: #3498db;
        }}
        
        .no-results {{
            text-align: center;
            padding: 40px;
            color: #7f8c8d;
        }}
        
        .loading {{
            text-align: center;
            padding: 40px;
            color: #3498db;
            background: white;
            border-radius: 10px;
            margin: 20px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        
        .loading h3 {{
            color: #2c3e50;
            margin-bottom: 15px;
        }}
        
        .loading-spinner {{
            width: 40px;
            height: 40px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #3498db;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        .error-message {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 10px;
            padding: 20px;
            margin: 20px;
            text-align: center;
        }}
        
        .error-message h3 {{
            color: #856404;
            margin-bottom: 15px;
        }}
        
        .error-message p {{
            color: #856404;
            margin-bottom: 15px;
        }}
        
        .btn {{
            padding: 12px 24px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
            text-decoration: none;
            display: inline-block;
            margin: 5px;
            transition: all 0.3s;
        }}
        
        .btn-primary {{
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
        }}
        
        .btn-success {{
            background: linear-gradient(135deg, #28a745, #218838);
            color: white;
        }}
        
        .btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }}
        
        @media (max-width: 768px) {{
            .search-container {{
                flex-direction: column;
            }}
            
            .filters {{
                flex-direction: column;
            }}
            
            .stats {{
                flex-direction: column;
                gap: 10px;
            }}
            
            .support-sections {{
                grid-template-columns: 1fr;
            }}
            
            .header h1 {{
                font-size: 2em;
            }}
            
            .version-badge {{
                position: static;
                display: block;
                margin-top: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="version-badge">v3.0 DEFINITIVA</div>
            <h1>🔧 Sistema de Búsqueda de Soportes SINES</h1>
            <p>Versión Definitiva - Búsqueda avanzada con datos embebidos</p>
        </div>
        
        <div class="search-section">
            <div class="search-container">
                <input type="text" id="searchInput" class="search-input" placeholder="Buscar por número de soporte, tipo, fluido, notas...">
                <button id="searchBtn" class="search-btn">🔍 Buscar</button>
            </div>
            
            <div class="filters">
                <select id="typeFilter" class="filter-select">
                    <option value="">Todos los tipos</option>
                </select>
                <select id="fluidFilter" class="filter-select">
                    <option value="">Todos los fluidos</option>
                </select>
                <select id="sortFilter" class="filter-select">
                    <option value="number">Ordenar por número</option>
                    <option value="type">Ordenar por tipo</option>
                    <option value="fluid">Ordenar por fluido</option>
                </select>
            </div>
        </div>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-number" id="totalSupports">0</div>
                <div class="stat-label">Total Soportes</div>
            </div>
            <div class="stat">
                <div class="stat-number" id="totalGroups">0</div>
                <div class="stat-label">Grupos</div>
            </div>
            <div class="stat">
                <div class="stat-number" id="totalTypes">0</div>
                <div class="stat-label">Tipos</div>
            </div>
            <div class="stat">
                <div class="stat-number" id="totalWithPdfs">0</div>
                <div class="stat-label">Con PDFs</div>
            </div>
        </div>
        
        <div class="results">
            <div id="loadingMessage" class="loading">
                <h3>📊 Cargando Sistema de Soportes...</h3>
                <div class="loading-spinner"></div>
                <p>Inicializando datos del sistema...</p>
            </div>
            <div id="resultsContainer" style="display: none;"></div>
            <div id="pagination" class="pagination" style="display: none;"></div>
        </div>
    </div>
    
    <script>
        // Datos embebidos como fallback
        const EMBEDDED_SUPPORT_DATA = {json.dumps(support_data, ensure_ascii=False, indent=2)};
        const EMBEDDED_PDF_MAPPING = {json.dumps(pdf_mapping, ensure_ascii=False, indent=2)};
        
        // Variables globales
        let allSupports = [];
        let allPdfMappings = {{}};
        let currentPage = 1;
        let itemsPerPage = 25;
        let filteredSupports = [];
        let isUsingEmbeddedData = false;
        
        // Función principal de carga de datos
        async function loadData() {{
            console.log('🚀 Iniciando Sistema de Soportes SINES v3.0');
            
            const loadingDiv = document.getElementById('loadingMessage');
            const resultsDiv = document.getElementById('resultsContainer');
            
            // Mostrar mensaje de carga mejorado
            if (loadingDiv) {{
                loadingDiv.innerHTML = `
                    <h3>📊 Cargando Sistema de Soportes...</h3>
                    <div class="loading-spinner"></div>
                    <p>Intentando cargar datos desde el servidor...</p>
                    <div style="margin-top: 15px; font-size: 0.9em; color: #666;">
                        <p>🔄 Paso 1: Conectando al servidor...</p>
                        <p>📁 Paso 2: Cargando archivos JSON...</p>
                        <p>⚙️ Paso 3: Procesando datos...</p>
                    </div>
                `;
            }}
            
            try {{
                // Intentar cargar desde servidor primero
                console.log('🔄 Intentando cargar desde servidor...');
                await loadFromServer();
                console.log('✅ Datos cargados desde servidor exitosamente');
                
            }} catch (serverError) {{
                console.warn('⚠️ Error al cargar desde servidor:', serverError);
                console.log('🔄 Cambiando a datos embebidos...');
                
                // Usar datos embebidos como fallback
                try {{
                    await loadFromEmbeddedData();
                    console.log('✅ Datos embebidos cargados exitosamente');
                    
                    // Mostrar mensaje informativo
                    if (loadingDiv) {{
                        loadingDiv.innerHTML = `
                            <div style="background: #d1ecf1; border: 1px solid #bee5eb; border-radius: 8px; padding: 15px; margin: 10px 0;">
                                <h4 style="color: #0c5460; margin-bottom: 10px;">ℹ️ Modo Offline Activado</h4>
                                <p style="color: #0c5460; margin-bottom: 10px;">
                                    El sistema está funcionando con datos embebidos. 
                                    Todas las funciones están disponibles excepto la descarga de PDFs.
                                </p>
                                <p style="color: #0c5460; font-size: 0.9em;">
                                    Para acceso completo a PDFs, inicia el servidor local.
                                </p>
                            </div>
                        `;
                        setTimeout(() => {{
                            loadingDiv.style.display = 'none';
                            resultsDiv.style.display = 'block';
                        }}, 3000);
                    }}
                    
                }} catch (embeddedError) {{
                    console.error('❌ Error crítico al cargar datos embebidos:', embeddedError);
                    showCriticalError(embeddedError);
                    return;
                }}
            }}
            
            // Inicializar interfaz
            initializeFilters();
            displayResults(allSupports);
            
            // Ocultar mensaje de carga
            setTimeout(() => {{
                if (loadingDiv) loadingDiv.style.display = 'none';
                if (resultsDiv) resultsDiv.style.display = 'block';
            }}, 1000);
        }}
        
        // Cargar desde servidor
        async function loadFromServer() {{
            const urls = [
                'support_data_enhanced.json',
                'support_pdf_mapping.json'
            ];
            
            const responses = await Promise.all(
                urls.map(url => fetch(url, {{
                    method: 'GET',
                    headers: {{
                        'Cache-Control': 'no-cache',
                        'Pragma': 'no-cache'
                    }}
                }}))
            );
            
            // Verificar que todas las respuestas sean exitosas
            responses.forEach((response, index) => {{
                if (!response.ok) {{
                    throw new Error(`Error ${response.status} al cargar ${urls[index]}`);
                }}
            }});
            
            // Procesar respuestas
            const [supportData, pdfData] = await Promise.all(
                responses.map(response => response.json())
            );
            
            allSupports = supportData;
            allPdfMappings = pdfData;
            isUsingEmbeddedData = false;
        }}
        
        // Cargar desde datos embebidos
        async function loadFromEmbeddedData() {{
            console.log('📦 Cargando datos embebidos...');
            
            if (!EMBEDDED_SUPPORT_DATA || !EMBEDDED_PDF_MAPPING) {{
                throw new Error('Datos embebidos no disponibles');
            }}
            
            allSupports = EMBEDDED_SUPPORT_DATA;
            allPdfMappings = EMBEDDED_PDF_MAPPING;
            isUsingEmbeddedData = true;
            
            console.log(`✅ Datos embebidos cargados: ${allSupports.length} soportes, ${Object.keys(allPdfMappings).length} tipos con PDFs`);
        }}
        
        // Mostrar error crítico
        function showCriticalError(error) {{
            const loadingDiv = document.getElementById('loadingMessage');
            if (loadingDiv) {{
                loadingDiv.innerHTML = `
                    <div class="error-message">
                        <h3>❌ Error Crítico del Sistema</h3>
                        <p><strong>No se pudieron cargar los datos:</strong> ${error.message}</p>
                        <div style="margin: 20px 0; text-align: left;">
                            <strong>Soluciones:</strong>
                            <ol style="margin: 10px 0; padding-left: 20px;">
                                <li>Verifica que el servidor esté funcionando</li>
                                <li>Refresca la página (F5)</li>
                                <li>Limpia el caché del navegador</li>
                                <li>Usa modo incógnito</li>
                                <li>Contacta al administrador del sistema</li>
                            </ol>
                        </div>
                        <div>
                            <button class="btn btn-primary" onclick="location.reload()">
                                🔄 Reintentar
                            </button>
                            <a href="http://localhost:8000/index.html" class="btn btn-success" target="_blank">
                                📄 Versión Básica
                            </a>
                        </div>
                    </div>
                `;
            }}
        }}
        
        // Función mejorada para descargar PDFs
        function downloadPdf(filename) {{
            if (isUsingEmbeddedData) {{
                alert(`📄 Archivo PDF: ${filename}\\n\\n⚠️ Modo Offline Activado\\n\\nPara descargar PDFs necesitas:\\n• Iniciar el servidor local\\n• Tener los archivos PDF en la carpeta correspondiente\\n\\nUsa el archivo INICIAR_SISTEMA.bat para el modo completo.`);
                return;
            }}
            
            const url = `ESTANDARES DE SOPORTES/${filename}`;
            const link = document.createElement('a');
            link.href = url;
            link.download = filename;
            link.target = '_blank';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }}
        
        // Resto del código JavaScript (copiar desde app_enhanced.js)
        // [Aquí iría el resto del código JavaScript, pero por brevedad lo omito]
        
        // Inicializar cuando se carga la página
        document.addEventListener('DOMContentLoaded', loadData);
        
        // Resto de funciones del sistema...
        // (Por brevedad, incluiré las funciones principales)
    </script>
</body>
</html>'''
    
    # Leer el JavaScript completo y agregarlo
    with open('app_enhanced.js', 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    # Extraer solo las funciones que necesitamos (sin loadData)
    js_functions = js_content.split('async function loadData()')[1].split('document.addEventListener')[0]
    
    # Insertar las funciones en el HTML
    html_content = html_content.replace(
        '// Resto de funciones del sistema...\n        // (Por brevedad, incluiré las funciones principales)',
        js_functions
    )
    
    # Guardar la versión definitiva
    with open('index_ultimate.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Versión definitiva creada: index_ultimate.html")
    print("🌟 Características:")
    print("   • Carga desde servidor con fallback a datos embebidos")
    print("   • Funciona online y offline")
    print("   • Interfaz mejorada con animaciones")
    print("   • Manejo robusto de errores")
    print("   • Mensajes informativos claros")
    print("\n🌐 URL para probar:")
    print("   http://localhost:8000/index_ultimate.html")
    
    # Crear iniciador específico
    with open('INICIAR_VERSION_DEFINITIVA.bat', 'w', encoding='utf-8') as f:
        f.write('''@echo off
title Sistema de Soportes SINES - Version Definitiva
echo ================================================
echo    SISTEMA DE SOPORTES SINES - VERSION DEFINITIVA
echo ================================================
echo.
echo Esta version incluye:
echo   * Carga desde servidor con fallback embebido
echo   * Funciona online y offline
echo   * Interfaz mejorada con animaciones
echo   * Manejo robusto de errores
echo.
echo Iniciando servidor web local...
echo.
echo URL: http://localhost:8000/index_ultimate.html
echo.
echo Para detener el servidor, presiona Ctrl+C
echo ================================================
echo.

start "" "http://localhost:8000/index_ultimate.html"
python server.py
pause''')
    
    print("✅ Creado iniciador: INICIAR_VERSION_DEFINITIVA.bat")
    
    return True

if __name__ == "__main__":
    create_ultimate_version() 