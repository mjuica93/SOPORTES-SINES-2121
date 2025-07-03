import json
import pandas as pd

def create_enhanced_support_display():
    print("=== MEJORANDO VISUALIZACIÓN CON TÍTULOS DE PLANTILLAS ===\n")
    
    # Cargar datos existentes
    with open('support_data_enhanced.json', 'r', encoding='utf-8') as f:
        support_data = json.load(f)
    
    with open('column_titles_mapping.json', 'r', encoding='utf-8') as f:
        column_titles = json.load(f)
    
    print(f"📊 Datos cargados: {len(support_data)} soportes")
    print(f"📋 Títulos de columnas: {len(column_titles)} columnas")
    
    # Crear mapeo de variables de plantillas
    template_variables = {
        'A': {'title': 'Dimensión A', 'description': 'Variable A de la plantilla', 'unit': 'mm', 'column': 19},
        'B': {'title': 'Dimensión B', 'description': 'Variable B de la plantilla', 'unit': 'mm', 'column': 20},
        'C': {'title': 'Dimensión C', 'description': 'Variable C de la plantilla', 'unit': 'mm', 'column': 22},
        'D': {'title': 'Dimensión D', 'description': 'Variable D de la plantilla', 'unit': 'mm', 'column': 23},
        'E': {'title': 'Dimensión E', 'description': 'Variable E de la plantilla', 'unit': 'mm', 'column': 24},
        'R': {'title': 'Radio/Distancia R', 'description': 'Variable R de la plantilla', 'unit': 'mm', 'column': 26},
        'X': {'title': 'Coordenada X', 'description': 'Posición X (NB)', 'unit': 'mm', 'column': 27},
        'Y': {'title': 'Coordenada Y', 'description': 'Posición Y (NB)', 'unit': 'mm', 'column': 28},
        'EL': {'title': 'Elevación', 'description': 'Elevación del soporte', 'unit': 'mm', 'column': 29},
        'N.': {'title': 'Número', 'description': 'Número de referencia', 'unit': '', 'column': 33},
        'SH.': {'title': 'Hoja/Sheet', 'description': 'Número de hoja', 'unit': '', 'column': 37},
        'TEMP': {'title': 'Temperatura', 'description': 'Temperatura de operación', 'unit': '°C', 'column': 44}
    }
    
    # Crear versión mejorada del JavaScript
    create_enhanced_javascript(template_variables)
    
    # Crear versión mejorada del HTML
    create_enhanced_html()
    
    print("✅ Sistema mejorado creado con títulos de plantillas")
    
    return template_variables

def create_enhanced_javascript(template_variables):
    print("🔧 Creando JavaScript mejorado...")
    
    # Leer el JavaScript actual
    with open('app_enhanced_robust.js', 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    # Agregar las variables de plantilla al inicio
    template_vars_js = f"""
// Variables de plantillas de soporte (extraídas de filas 22-23 del Excel)
const TEMPLATE_VARIABLES = {json.dumps(template_variables, ensure_ascii=False, indent=4)};

// Función para obtener el título descriptivo de una variable
function getVariableTitle(varName, value) {{
    if (TEMPLATE_VARIABLES[varName]) {{
        const templateVariable = TEMPLATE_VARIABLES[varName];
        const unit = templateVariable.unit ? ` ${{templateVariable.unit}}` : '';
        return `${{templateVariable.title}} (${{varName}})${{unit}}`;
    }}
    return varName;
}}

// Función para formatear valor con unidad
function formatValueWithUnit(varName, value) {{
    if (!value || value === 'nan' || value === '') return 'No especificado';
    
    if (TEMPLATE_VARIABLES[varName] && TEMPLATE_VARIABLES[varName].unit) {{
        return `${{value}} ${{TEMPLATE_VARIABLES[varName].unit}}`;
    }}
    return value;
}}

"""
    
    # Insertar las variables al inicio del archivo
    enhanced_js = template_vars_js + js_content
    
    # Mejorar la función de creación de secciones de soporte
    enhanced_js = enhanced_js.replace(
        'function createSupportSections(support) {',
        '''function createSupportSections(support) {
    const sections = [];
    
    // Sección de Información Básica (mejorada)
    const basicSection = createBasicInfoSection(support);
    sections.push(basicSection);
    
    // Sección de Variables de Plantilla (NUEVA)
    const templateSection = createTemplateVariablesSection(support);
    if (templateSection) sections.push(templateSection);
    
    // Sección de Información Técnica
    const technicalSection = createTechnicalInfoSection(support);
    sections.push(technicalSection);
    
    // Sección de Dimensiones (mejorada)
    const dimensionsSection = createDimensionsSection(support);
    sections.push(dimensionsSection);
    
    // Sección de Información de Proyecto
    const projectSection = createProjectInfoSection(support);
    sections.push(projectSection);
    
    // Sección de Notas
    const notesSection = createNotesSection(support);
    sections.push(notesSection);
    
    return sections.filter(section => section !== null);
}

function createBasicInfoSection(support) {'''
    )
    
    # Agregar nueva función para variables de plantilla
    template_section_function = '''

function createTemplateVariablesSection(support) {
    const templateVars = [];
    
    // Buscar variables de plantilla en los datos
    Object.keys(TEMPLATE_VARIABLES).forEach(varName => {
        const variable = TEMPLATE_VARIABLES[varName];
        let value = null;
        
        // Buscar el valor en diferentes secciones del soporte
        if (support.dimensions && support.dimensions[`dim_${variable.column}`]) {
            value = support.dimensions[`dim_${variable.column}`];
        } else if (support.basic_info && support.basic_info[varName.toLowerCase()]) {
            value = support.basic_info[varName.toLowerCase()];
        } else if (support.technical_info && support.technical_info[varName.toLowerCase()]) {
            value = support.technical_info[varName.toLowerCase()];
        }
        
        if (value && value !== 'nan' && value !== '') {
            templateVars.push({
                name: varName,
                title: variable.title,
                description: variable.description,
                value: value,
                unit: variable.unit,
                formatted: formatValueWithUnit(varName, value)
            });
        }
    });
    
    if (templateVars.length === 0) return null;
    
    const content = templateVars.map(variable => 
        `<div style="display: flex; justify-content: space-between; align-items: center; padding: 5px 0; border-bottom: 1px solid #eee;">
            <div style="flex: 1;">
                <strong style="color: #2c3e50; font-size: 0.9em;">${variable.name}:</strong>
                <span style="color: #666; font-size: 0.8em; margin-left: 5px;">${variable.title}</span>
            </div>
            <div style="flex: 1; text-align: right;">
                <span style="color: #2c3e50; font-weight: bold;">${variable.formatted}</span>
            </div>
        </div>`
    ).join('');
    
    return {
        title: '📐 Variables de Plantilla',
        icon: '📐',
        content: content,
        description: 'Variables específicas del PDF de la plantilla de soporte'
    };
}

function createDimensionsSection(support) {
    if (!support.dimensions) return null;
    
    const dimensionEntries = Object.entries(support.dimensions)
        .filter(([key, value]) => value && value !== 'nan' && value !== '')
        .map(([key, value]) => {
            // Intentar mapear con variables de plantilla
            const columnIndex = parseInt(key.replace('dim_', ''));
            const templateVar = Object.keys(TEMPLATE_VARIABLES).find(varName => 
                TEMPLATE_VARIABLES[varName].column === columnIndex
            );
            
            let displayName = key;
            let description = '';
            
            if (templateVar) {
                displayName = `${templateVar} (${TEMPLATE_VARIABLES[templateVar].title})`;
                description = TEMPLATE_VARIABLES[templateVar].description;
                value = formatValueWithUnit(templateVar, value);
            }
            
            return `<div style="margin-bottom: 5px;">
                <strong style="color: #2c3e50;">${displayName}:</strong> 
                <span style="color: #555;">${value}</span>
                ${description ? `<br><small style="color: #888; margin-left: 10px;">${description}</small>` : ''}
            </div>`;
        });
    
    if (dimensionEntries.length === 0) return null;
    
    return {
        title: '📏 Dimensiones Técnicas',
        icon: '📏',
        content: dimensionEntries.join(''),
        description: 'Medidas y dimensiones específicas del soporte'
    };
}

'''
    
    # Insertar la nueva función antes de la función displayResults
    enhanced_js = enhanced_js.replace(
        'function displayResults(supports) {',
        template_section_function + '\nfunction displayResults(supports) {'
    )
    
    # Guardar el JavaScript mejorado
    with open('app_enhanced_with_templates.js', 'w', encoding='utf-8') as f:
        f.write(enhanced_js)
    
    print("✅ JavaScript mejorado guardado: app_enhanced_with_templates.js")

def create_enhanced_html():
    print("🎨 Creando HTML mejorado...")
    
    # Leer el HTML actual
    with open('index_enhanced_robust.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Reemplazar referencia al JavaScript
    html_content = html_content.replace('app_enhanced_robust.js', 'app_enhanced_with_templates.js')
    
    # Mejorar el título y descripción
    html_content = html_content.replace(
        '<h1>🔧 Sistema de Búsqueda de Soportes SINES</h1>',
        '<h1>🔧 Sistema de Búsqueda de Soportes SINES</h1>'
    )
    
    html_content = html_content.replace(
        '<p>Versión Robusta - Busca y consulta información técnica de soportes</p>',
        '<p>Versión con Plantillas - Variables técnicas extraídas del Excel con títulos descriptivos</p>'
    )
    
    # Agregar estilos específicos para variables de plantilla
    template_styles = '''
        .template-variables {
            background: linear-gradient(135deg, #e8f5e8, #f0f8f0);
            border-left: 4px solid #27ae60;
        }
        
        .template-variable {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid #d5e8d5;
        }
        
        .template-variable:last-child {
            border-bottom: none;
        }
        
        .variable-name {
            font-weight: bold;
            color: #27ae60;
            font-size: 1.1em;
            min-width: 30px;
        }
        
        .variable-title {
            color: #2c3e50;
            font-size: 0.9em;
            margin-left: 10px;
        }
        
        .variable-value {
            color: #27ae60;
            font-weight: bold;
            font-size: 1.1em;
        }
        
        .pdf-hint {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 5px;
            padding: 10px;
            margin-top: 10px;
            font-size: 0.85em;
            color: #856404;
        }
        
        .pdf-hint .icon {
            color: #f39c12;
            margin-right: 5px;
        }
    '''
    
    # Insertar estilos antes del cierre de </style>
    html_content = html_content.replace('</style>', template_styles + '\n    </style>')
    
    # Guardar HTML mejorado
    with open('index_enhanced_with_templates.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ HTML mejorado guardado: index_enhanced_with_templates.html")

def create_template_guide():
    print("📖 Creando guía de variables de plantilla...")
    
    template_info = {
        'A': 'Dimensión principal A - Generalmente altura o longitud principal del soporte',
        'B': 'Dimensión principal B - Generalmente ancho o segunda dimensión principal',
        'C': 'Dimensión C - Tercera dimensión principal o profundidad',
        'D': 'Dimensión D - Cuarta dimensión o diámetro específico',
        'E': 'Dimensión E - Quinta dimensión o espesor específico',
        'R': 'Radio o distancia radial - Usado en soportes circulares o curvos',
        'X': 'Coordenada X - Posición horizontal en el sistema de coordenadas',
        'Y': 'Coordenada Y - Posición vertical en el sistema de coordenadas',
        'EL': 'Elevación - Altura o cota del soporte respecto al nivel de referencia',
        'N.': 'Número de referencia - Identificador numérico específico',
        'SH.': 'Número de hoja - Referencia al plano o drawing donde aparece',
        'TEMP': 'Temperatura de operación - Condiciones térmicas de trabajo'
    }
    
    with open('GUIA_VARIABLES_PLANTILLA.txt', 'w', encoding='utf-8') as f:
        f.write("GUÍA DE VARIABLES DE PLANTILLAS DE SOPORTE\n")
        f.write("=" * 50 + "\n\n")
        f.write("Las siguientes variables aparecen en los PDFs de las plantillas\n")
        f.write("de soporte y corresponden a las dimensiones y parámetros técnicos\n")
        f.write("específicos de cada tipo de soporte.\n\n")
        
        f.write("VARIABLES PRINCIPALES:\n")
        f.write("-" * 30 + "\n\n")
        
        for var, description in template_info.items():
            f.write(f"{var:4} - {description}\n")
        
        f.write(f"\nESTAS VARIABLES SE EXTRAEN DE:\n")
        f.write("- Fila 22: Nombres de variables (A, B, C, D, E, R, X, Y, EL, N., SH.)\n")
        f.write("- Fila 23: Códigos de referencia ((4a), (4b), (4c), etc.)\n")
        f.write("- Los valores se toman de las columnas correspondientes del Excel\n\n")
        
        f.write("CÓMO SE MUESTRAN EN EL SISTEMA:\n")
        f.write("- Cada variable se muestra con su nombre y título descriptivo\n")
        f.write("- Los valores incluyen unidades cuando corresponde (mm, °C)\n")
        f.write("- Solo se muestran las variables que tienen valores\n")
        f.write("- Se agrupan en una sección específica 'Variables de Plantilla'\n\n")
        
        f.write("RELACIÓN CON LOS PDFs:\n")
        f.write("- Estas variables aparecen en los diagramas de los PDFs\n")
        f.write("- Permiten entender las dimensiones específicas de cada soporte\n")
        f.write("- Facilitan la interpretación de los planos técnicos\n")
    
    print("✅ Guía creada: GUIA_VARIABLES_PLANTILLA.txt")

if __name__ == "__main__":
    template_vars = create_enhanced_support_display()
    create_template_guide()
    
    print(f"\n🎉 SISTEMA MEJORADO CREADO!")
    print(f"📄 Nuevos archivos:")
    print(f"   • index_enhanced_with_templates.html")
    print(f"   • app_enhanced_with_templates.js") 
    print(f"   • GUIA_VARIABLES_PLANTILLA.txt")
    print(f"\n🌐 URL para probar:")
    print(f"   http://localhost:8000/index_enhanced_with_templates.html") 