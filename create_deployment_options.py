import os
import shutil
import json
import zipfile
from datetime import datetime

def create_deployment_options():
    print("=== OPCIONES DE PUBLICACIÓN DEL SISTEMA ===\n")
    
    # Crear carpeta de distribución
    dist_folder = "DISTRIBUCION_SISTEMA"
    if os.path.exists(dist_folder):
        shutil.rmtree(dist_folder)
    os.makedirs(dist_folder)
    
    # Opción 1: Paquete completo para servidor web
    print("🌐 OPCIÓN 1: SERVIDOR WEB COMPLETO")
    web_folder = os.path.join(dist_folder, "1_SERVIDOR_WEB")
    os.makedirs(web_folder)
    
    # Copiar archivos del sistema web
    web_files = [
        'index.html',
        'index_enhanced.html',
        'app.js',
        'app_enhanced.js',
        'support_data.json',
        'support_data_enhanced.json',
        'support_pdf_mapping.json',
        'server.py',
        'INICIAR_SISTEMA.bat'
    ]
    
    for file in web_files:
        if os.path.exists(file):
            shutil.copy2(file, web_folder)
    
    # Copiar carpeta de PDFs
    if os.path.exists('ESTANDARES DE SOPORTES'):
        shutil.copytree('ESTANDARES DE SOPORTES', os.path.join(web_folder, 'ESTANDARES DE SOPORTES'))
    
    # Crear instrucciones para servidor web
    with open(os.path.join(web_folder, 'INSTRUCCIONES_SERVIDOR.txt'), 'w', encoding='utf-8') as f:
        f.write("INSTRUCCIONES PARA SERVIDOR WEB\n")
        f.write("=" * 40 + "\n\n")
        f.write("1. INSTALACIÓN LOCAL:\n")
        f.write("   - Ejecutar: INICIAR_SISTEMA.bat\n")
        f.write("   - Abrir navegador en: http://localhost:8000\n")
        f.write("   - Usar: index_enhanced.html (versión mejorada)\n\n")
        f.write("2. SERVIDOR PÚBLICO:\n")
        f.write("   - Subir todos los archivos a un servidor web\n")
        f.write("   - Configurar servidor para servir archivos estáticos\n")
        f.write("   - Asegurar que los archivos JSON sean accesibles\n\n")
        f.write("3. REQUISITOS:\n")
        f.write("   - Python 3.x (para servidor local)\n")
        f.write("   - Navegador web moderno\n")
        f.write("   - Acceso a carpeta ESTANDARES DE SOPORTES\n")
    
    print(f"   ✅ Creado: {web_folder}")
    
    # Opción 2: Aplicación portable
    print("\n💼 OPCIÓN 2: APLICACIÓN PORTABLE")
    portable_folder = os.path.join(dist_folder, "2_APLICACION_PORTABLE")
    os.makedirs(portable_folder)
    
    # Crear HTML autocontenido
    create_standalone_html(portable_folder)
    
    print(f"   ✅ Creado: {portable_folder}")
    
    # Opción 3: Archivo Excel mejorado
    print("\n📊 OPCIÓN 3: EXCEL MEJORADO")
    excel_folder = os.path.join(dist_folder, "3_EXCEL_MEJORADO")
    os.makedirs(excel_folder)
    
    create_excel_enhanced(excel_folder)
    
    print(f"   ✅ Creado: {excel_folder}")
    
    # Opción 4: Documentación PDF
    print("\n📄 OPCIÓN 4: DOCUMENTACIÓN COMPLETA")
    docs_folder = os.path.join(dist_folder, "4_DOCUMENTACION")
    os.makedirs(docs_folder)
    
    create_documentation(docs_folder)
    
    print(f"   ✅ Creado: {docs_folder}")
    
    # Crear archivo ZIP para distribución
    print("\n📦 CREANDO ARCHIVO DE DISTRIBUCIÓN...")
    zip_filename = f"SISTEMA_SOPORTES_SINES_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dist_folder):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, dist_folder)
                zipf.write(file_path, arcname)
    
    print(f"   ✅ Archivo ZIP creado: {zip_filename}")
    
    # Crear guía de distribución
    create_distribution_guide()
    
    print("\n🎉 OPCIONES DE PUBLICACIÓN CREADAS EXITOSAMENTE!")
    print(f"📁 Carpeta: {dist_folder}")
    print(f"📦 Archivo ZIP: {zip_filename}")
    print("📋 Guía: GUIA_DISTRIBUCION.txt")

def create_standalone_html(folder):
    """Crear una versión HTML autocontenida"""
    # Leer datos
    with open('support_data_enhanced.json', 'r', encoding='utf-8') as f:
        support_data = json.load(f)
    
    with open('support_pdf_mapping.json', 'r', encoding='utf-8') as f:
        pdf_mapping = json.load(f)
    
    # Leer archivos JS y CSS
    with open('app_enhanced.js', 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    # Crear HTML autocontenido
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Búsqueda de Soportes SINES - Versión Portable</title>
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
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }}
        
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
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
            transition: border-color 0.3s;
        }}
        
        .search-input:focus {{
            outline: none;
            border-color: #3498db;
        }}
        
        .search-btn {{
            padding: 15px 30px;
            background: #3498db;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: background 0.3s;
        }}
        
        .search-btn:hover {{
            background: #2980b9;
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
        }}
        
        .stats {{
            display: flex;
            justify-content: space-around;
            padding: 20px;
            background: #e8f4f8;
            text-align: center;
        }}
        
        .stat {{
            padding: 10px;
        }}
        
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .stat-label {{
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        
        .results {{
            padding: 20px;
        }}
        
        .support-group {{
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            margin-bottom: 15px;
            overflow: hidden;
        }}
        
        .group-header {{
            background: #f8f9fa;
            padding: 15px;
            cursor: pointer;
            border-bottom: 1px solid #e9ecef;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .group-header:hover {{
            background: #e9ecef;
        }}
        
        .group-title {{
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .group-count {{
            background: #3498db;
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.8em;
        }}
        
        .group-content {{
            display: none;
            padding: 15px;
        }}
        
        .group-content.show {{
            display: block;
        }}
        
        .support-item {{
            background: #f8f9fa;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 5px;
            border-left: 4px solid #3498db;
        }}
        
        .support-sections {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
            margin-top: 10px;
        }}
        
        .support-section {{
            background: white;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #e9ecef;
        }}
        
        .section-title {{
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 8px;
            padding-bottom: 5px;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .section-content {{
            font-size: 0.9em;
            color: #555;
        }}
        
        .section-content div {{
            margin-bottom: 3px;
        }}
        
        .pdf-links {{
            margin-top: 10px;
        }}
        
        .pdf-link {{
            display: inline-block;
            background: #e74c3c;
            color: white;
            padding: 5px 10px;
            margin: 2px;
            border-radius: 3px;
            text-decoration: none;
            font-size: 0.8em;
        }}
        
        .pdf-link:hover {{
            background: #c0392b;
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
        }}
        
        .pagination button:hover {{
            background: #f8f9fa;
        }}
        
        .pagination button.active {{
            background: #3498db;
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
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔧 Sistema de Búsqueda de Soportes SINES</h1>
            <p>Versión Portable - Busca y consulta información técnica de soportes</p>
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
                <h3>📊 Cargando datos del sistema...</h3>
                <p>Por favor espere mientras se inicializa la aplicación</p>
            </div>
            <div id="resultsContainer" style="display: none;"></div>
            <div id="pagination" class="pagination" style="display: none;"></div>
        </div>
    </div>
    
    <script>
        // Datos embebidos
        const supportData = {json.dumps(support_data, ensure_ascii=False, indent=2)};
        const pdfMapping = {json.dumps(pdf_mapping, ensure_ascii=False, indent=2)};
        
        // Nota: Los PDFs no estarán disponibles en esta versión portable
        // pero se mostrará la información de qué PDFs corresponden a cada soporte
        
        {js_content}
        
        // Modificar la función loadData para usar datos embebidos
        function loadData() {{
            console.log('Cargando datos embebidos...');
            
            // Procesar datos
            allSupports = supportData;
            allPdfMappings = pdfMapping;
            
            // Inicializar filtros
            initializeFilters();
            
            // Mostrar todos los soportes inicialmente
            displayResults(allSupports);
            
            // Ocultar mensaje de carga
            document.getElementById('loadingMessage').style.display = 'none';
            document.getElementById('resultsContainer').style.display = 'block';
            
            console.log('Datos cargados exitosamente');
        }}
        
        // Modificar función de descarga de PDFs para mostrar mensaje
        function downloadPdf(filename) {{
            alert('Esta es la versión portable del sistema.\\n\\nPara acceder a los PDFs, necesitas:\\n1. La versión completa del sistema\\n2. Los archivos PDF en la carpeta "ESTANDARES DE SOPORTES"\\n\\nArchivo requerido: ' + filename);
        }}
        
        // Inicializar cuando se carga la página
        document.addEventListener('DOMContentLoaded', loadData);
    </script>
</body>
</html>"""
    
    with open(os.path.join(folder, 'SISTEMA_SOPORTES_PORTABLE.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Crear instrucciones
    with open(os.path.join(folder, 'INSTRUCCIONES_PORTABLE.txt'), 'w', encoding='utf-8') as f:
        f.write("APLICACIÓN PORTABLE - INSTRUCCIONES\n")
        f.write("=" * 40 + "\n\n")
        f.write("1. CÓMO USAR:\n")
        f.write("   - Abrir: SISTEMA_SOPORTES_PORTABLE.html\n")
        f.write("   - Funciona sin conexión a internet\n")
        f.write("   - No requiere instalación\n\n")
        f.write("2. CARACTERÍSTICAS:\n")
        f.write("   - Búsqueda completa de soportes\n")
        f.write("   - Toda la información técnica\n")
        f.write("   - Filtros y ordenamiento\n")
        f.write("   - Estadísticas en tiempo real\n")
        f.write("   - Filtros avanzados\n\n")
        f.write("3. LIMITACIONES:\n")
        f.write("   - PDFs no incluidos (archivo muy grande)\n")
        f.write("   - Para PDFs usar la versión completa\n\n")
        f.write("4. DISTRIBUCIÓN:\n")
        f.write("   - Enviar solo el archivo HTML\n")
        f.write("   - Funciona en cualquier navegador\n")
        f.write("   - Ideal para consulta rápida\n")

def create_excel_enhanced(folder):
    """Crear documentación para Excel mejorado"""
    with open(os.path.join(folder, 'INSTRUCCIONES_EXCEL.txt'), 'w', encoding='utf-8') as f:
        f.write("EXCEL MEJORADO - INSTRUCCIONES\n")
        f.write("=" * 40 + "\n\n")
        f.write("1. ARCHIVOS DISPONIBLES:\n")
        f.write("   - 4274-XH-LP-21210001-IS03_Native.xlsx\n")
        f.write("   - 4274-XH-LP-21210002-IS02_Native.xlsm\n\n")
        f.write("2. MEJORAS SUGERIDAS:\n")
        f.write("   - Agregar filtros automáticos\n")
        f.write("   - Crear tabla dinámica\n")
        f.write("   - Hipervínculos a PDFs\n")
        f.write("   - Formato condicional\n\n")
        f.write("3. CAMPOS PRINCIPALES:\n")
        f.write("   - Número de soporte\n")
        f.write("   - Tipo de soporte\n")
        f.write("   - Fluido\n")
        f.write("   - Coordenadas\n")
        f.write("   - Dimensiones\n")
        f.write("   - Notas técnicas\n\n")
        f.write("4. VENTAJAS:\n")
        f.write("   - Familiar para usuarios\n")
        f.write("   - Fácil de modificar\n")
        f.write("   - Permite cálculos\n")
        f.write("   - Exportable a otros formatos\n")
    
    # Copiar archivos Excel originales
    excel_files = [
        '4274-XH-LP-21210001-IS03_Native.xlsx',
        '4274-XH-LP-21210002-IS02_Native.xlsm'
    ]
    
    for file in excel_files:
        if os.path.exists(file):
            shutil.copy2(file, folder)

def create_documentation(folder):
    """Crear documentación completa"""
    # Copiar archivos de documentación existentes
    doc_files = [
        'README.md',
        'MEJORAS_IMPLEMENTADAS.md',
        'SOLUCION_PROBLEMAS.md',
        'INSTRUCCIONES_RAPIDAS.txt',
        'SOPORTES_SIN_PDFs.txt',
        'ARCHIVOS_PDF_A_BUSCAR.txt'
    ]
    
    for file in doc_files:
        if os.path.exists(file):
            shutil.copy2(file, folder)
    
    # Crear manual de usuario
    with open(os.path.join(folder, 'MANUAL_USUARIO.txt'), 'w', encoding='utf-8') as f:
        f.write("MANUAL DE USUARIO - SISTEMA DE SOPORTES SINES\n")
        f.write("=" * 50 + "\n\n")
        f.write("1. INTRODUCCIÓN\n")
        f.write("   El sistema permite buscar y consultar información\n")
        f.write("   técnica de soportes de tuberías de forma rápida\n")
        f.write("   y eficiente.\n\n")
        f.write("2. CARACTERÍSTICAS PRINCIPALES\n")
        f.write("   - Búsqueda por múltiples criterios\n")
        f.write("   - Visualización organizada por grupos\n")
        f.write("   - Acceso directo a PDFs técnicos\n")
        f.write("   - Estadísticas en tiempo real\n")
        f.write("   - Filtros avanzados\n\n")
        f.write("3. CÓMO BUSCAR\n")
        f.write("   - Número de soporte: '8001', '5002'\n")
        f.write("   - Tipo de soporte: 'N1G1', 'C4F1'\n")
        f.write("   - Fluido: 'P56A108', 'CWS'\n")
        f.write("   - Texto libre en notas\n\n")
        f.write("4. INTERPRETACIÓN DE RESULTADOS\n")
        f.write("   - Información Básica: Número, tipo, fluido\n")
        f.write("   - Información Técnica: CWA, revisión, parámetros\n")
        f.write("   - Dimensiones: Múltiples medidas técnicas\n")
        f.write("   - Información de Proyecto: Fechas, responsables\n")
        f.write("   - PDFs: Enlaces a documentación técnica\n\n")
        f.write("5. SOLUCIÓN DE PROBLEMAS\n")
        f.write("   - Ver archivo: SOLUCION_PROBLEMAS.md\n")
        f.write("   - Contactar administrador del sistema\n")

def create_distribution_guide():
    """Crear guía de distribución"""
    with open('GUIA_DISTRIBUCION.txt', 'w', encoding='utf-8') as f:
        f.write("GUÍA DE DISTRIBUCIÓN - SISTEMA DE SOPORTES SINES\n")
        f.write("=" * 55 + "\n\n")
        f.write("🌐 OPCIÓN 1: SERVIDOR WEB COMPLETO\n")
        f.write("   Mejor para: Acceso desde múltiples ubicaciones\n")
        f.write("   Incluye: Sistema completo + PDFs + Servidor\n")
        f.write("   Instalación: Ejecutar INICIAR_SISTEMA.bat\n")
        f.write("   URL: http://localhost:8000/index_enhanced.html\n\n")
        f.write("💼 OPCIÓN 2: APLICACIÓN PORTABLE\n")
        f.write("   Mejor para: Consulta rápida sin instalación\n")
        f.write("   Incluye: HTML autocontenido con todos los datos\n")
        f.write("   Instalación: Ninguna, solo abrir HTML\n")
        f.write("   Limitación: Sin acceso a PDFs\n\n")
        f.write("📊 OPCIÓN 3: EXCEL MEJORADO\n")
        f.write("   Mejor para: Usuarios familiarizados con Excel\n")
        f.write("   Incluye: Archivos Excel originales + instrucciones\n")
        f.write("   Instalación: Microsoft Excel requerido\n")
        f.write("   Ventaja: Familiar y editable\n\n")
        f.write("📄 OPCIÓN 4: DOCUMENTACIÓN COMPLETA\n")
        f.write("   Mejor para: Referencia y capacitación\n")
        f.write("   Incluye: Manuales, guías, listas de PDFs faltantes\n")
        f.write("   Instalación: Ninguna\n")
        f.write("   Uso: Consulta y referencia\n\n")
        f.write("🎯 RECOMENDACIONES POR ESCENARIO:\n")
        f.write("   - Oficina principal: Opción 1 (Servidor Web)\n")
        f.write("   - Trabajadores de campo: Opción 2 (Portable)\n")
        f.write("   - Análisis de datos: Opción 3 (Excel)\n")
        f.write("   - Capacitación: Opción 4 (Documentación)\n\n")
        f.write("📦 DISTRIBUCIÓN:\n")
        f.write("   - Archivo ZIP incluye todas las opciones\n")
        f.write("   - Cada opción en carpeta separada\n")
        f.write("   - Instrucciones específicas en cada carpeta\n")
        f.write("   - Listo para compartir por email o red\n\n")
        f.write("🔧 SOPORTE TÉCNICO:\n")
        f.write("   - Ver: SOLUCION_PROBLEMAS.md\n")
        f.write("   - Contactar: Administrador del sistema\n")
        f.write("   - Archivos de log disponibles para diagnóstico\n")

if __name__ == "__main__":
    create_deployment_options() 