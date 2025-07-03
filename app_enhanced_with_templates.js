
// Variables de plantillas de soporte (extraídas de filas 22-23 del Excel)
const TEMPLATE_VARIABLES = {
    "A": {
        "title": "Dimensión A",
        "description": "Variable A de la plantilla",
        "unit": "mm",
        "column": 19
    },
    "B": {
        "title": "Dimensión B",
        "description": "Variable B de la plantilla",
        "unit": "mm",
        "column": 20
    },
    "C": {
        "title": "Dimensión C",
        "description": "Variable C de la plantilla",
        "unit": "mm",
        "column": 22
    },
    "D": {
        "title": "Dimensión D",
        "description": "Variable D de la plantilla",
        "unit": "mm",
        "column": 23
    },
    "E": {
        "title": "Dimensión E",
        "description": "Variable E de la plantilla",
        "unit": "mm",
        "column": 24
    },
    "R": {
        "title": "Radio/Distancia R",
        "description": "Variable R de la plantilla",
        "unit": "mm",
        "column": 26
    },
    "X": {
        "title": "Coordenada X",
        "description": "Posición X (NB)",
        "unit": "mm",
        "column": 27
    },
    "Y": {
        "title": "Coordenada Y",
        "description": "Posición Y (NB)",
        "unit": "mm",
        "column": 28
    },
    "EL": {
        "title": "Elevación",
        "description": "Elevación del soporte",
        "unit": "mm",
        "column": 29
    },
    "N.": {
        "title": "Número",
        "description": "Número de referencia",
        "unit": "",
        "column": 33
    },
    "SH.": {
        "title": "Hoja/Sheet",
        "description": "Número de hoja",
        "unit": "",
        "column": 37
    },
    "TEMP": {
        "title": "Temperatura",
        "description": "Temperatura de operación",
        "unit": "°C",
        "column": 44
    }
};

// Función para obtener el título descriptivo de una variable
function getVariableTitle(varName, value) {
    if (TEMPLATE_VARIABLES[varName]) {
        const templateVariable = TEMPLATE_VARIABLES[varName];
        const unit = templateVariable.unit ? ` ${templateVariable.unit}` : '';
        return `${templateVariable.title} (${varName})${unit}`;
    }
    return varName;
}

// Función para formatear valor con unidad
function formatValueWithUnit(varName, value) {
    if (!value || value === 'nan' || value === '') return 'No especificado';
    
    if (TEMPLATE_VARIABLES[varName] && TEMPLATE_VARIABLES[varName].unit) {
        return `${value} ${TEMPLATE_VARIABLES[varName].unit}`;
    }
    return value;
}

// Variables globales
let allSupports = [];
let supportMapping = {};
let filteredSupports = [];
let groupedSupports = {};

// Cargar datos al iniciar la aplicación
document.addEventListener('DOMContentLoaded', function() {
    loadData();
});

// Cargar datos desde los archivos JSON

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


// Agrupar soportes por número
function groupSupportsByNumber() {
    groupedSupports = {};
    
    allSupports.forEach(support => {
        const supportNumber = support.support_number;
        if (!groupedSupports[supportNumber]) {
            groupedSupports[supportNumber] = [];
        }
        groupedSupports[supportNumber].push(support);
    });
    
    console.log(`Agrupados ${Object.keys(groupedSupports).length} números de soporte únicos`);
}

// Inicializar la aplicación
function initializeApp() {
    updateStats();
    populateTypeFilter();
    displayAllSupports();
}

// Actualizar estadísticas
function updateStats() {
    const totalSupports = allSupports.length;
    const uniqueNumbers = Object.keys(groupedSupports).length;
    const totalTypes = new Set(allSupports.map(s => s.support_type)).size;
    const withPDFs = allSupports.filter(s => supportMapping[s.support_type] && supportMapping[s.support_type].length > 0).length;
    const searchResults = Object.keys(filteredSupports).length || uniqueNumbers;
    
    document.getElementById('totalSupports').textContent = totalSupports.toLocaleString();
    document.getElementById('uniqueNumbers').textContent = uniqueNumbers.toLocaleString();
    document.getElementById('totalTypes').textContent = totalTypes.toLocaleString();
    document.getElementById('withPDFs').textContent = withPDFs.toLocaleString();
    document.getElementById('searchResults').textContent = searchResults.toLocaleString();
}

// Poblar filtro de tipos
function populateTypeFilter() {
    const filterSelect = document.getElementById('filterType');
    const types = [...new Set(allSupports.map(s => s.support_type))].sort();
    
    // Limpiar opciones existentes
    filterSelect.innerHTML = '<option value="">Todos los tipos</option>';
    
    // Agregar tipos
    types.forEach(type => {
        const option = document.createElement('option');
        option.value = type;
        option.textContent = type;
        filterSelect.appendChild(option);
    });
}

// Buscar soportes
function searchSupports() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase().trim();
    const filterType = document.getElementById('filterType').value;
    
    if (!searchTerm && !filterType) {
        displayAllSupports();
        return;
    }
    
    // Filtrar grupos de soportes
    filteredSupports = {};
    
    Object.entries(groupedSupports).forEach(([supportNumber, supports]) => {
        const matchesSearch = !searchTerm || 
            supportNumber.toLowerCase().includes(searchTerm) ||
            supports.some(support => 
                support.support_type.toLowerCase().includes(searchTerm) ||
                (support.fluid_piping && support.fluid_piping.toLowerCase().includes(searchTerm)) ||
                (support.notes && support.notes.toLowerCase().includes(searchTerm)) ||
                (support.object_parameters && support.object_parameters.toLowerCase().includes(searchTerm))
            );
        
        const matchesType = !filterType || supports.some(support => support.support_type === filterType);
        
        if (matchesSearch && matchesType) {
            // Si hay filtro de tipo, solo incluir soportes de ese tipo
            if (filterType) {
                filteredSupports[supportNumber] = supports.filter(support => support.support_type === filterType);
            } else {
                filteredSupports[supportNumber] = supports;
            }
        }
    });
    
    displaySupports(filteredSupports);
    updateStats();
}

// Filtrar por tipo
function filterByType() {
    searchSupports();
}

// Mostrar todos los soportes
function displayAllSupports() {
    filteredSupports = groupedSupports;
    displaySupports(groupedSupports);
    updateStats();
}

// Mostrar soportes agrupados
function displaySupports(supportGroups) {
    const container = document.getElementById('resultsContainer');
    
    const groupEntries = Object.entries(supportGroups);
    
    if (groupEntries.length === 0) {
        showNoResults();
        return;
    }
    
    hideNoResults();
    
    // Limitar a los primeros 25 grupos para rendimiento
    const displayGroups = groupEntries.slice(0, 25);
    
    container.innerHTML = displayGroups.map(([supportNumber, supports]) => 
        createSupportGroupCard(supportNumber, supports)
    ).join('');
    
    if (groupEntries.length > 25) {
        container.innerHTML += `
            <div class="alert alert-info text-center">
                <i class="fas fa-info-circle"></i>
                Mostrando 25 de ${groupEntries.length} grupos de soportes. Refina tu búsqueda para ver más resultados.
            </div>
        `;
    }
}

// Crear tarjeta de grupo de soportes
function createSupportGroupCard(supportNumber, supports) {
    const mainSupport = supports[0];
    const hasMultiple = supports.length > 1;
    
    return `
        <div class="support-group-card">
            <div class="support-group-header" onclick="toggleSupportGroup('${supportNumber}')">
                <div class="support-group-title">
                    <i class="fas fa-layer-group"></i> 
                    Soporte ${supportNumber}
                    ${hasMultiple ? `<span class="element-count">(${supports.length} elementos)</span>` : ''}
                </div>
                <div class="support-group-summary">
                    ${supports.map(s => s.support_type).join(', ')}
                </div>
                <i class="fas fa-chevron-down toggle-icon" id="toggle-${supportNumber}"></i>
            </div>
            
            <div class="support-group-body" id="group-${supportNumber}" style="display: ${hasMultiple ? 'none' : 'block'};">
                ${supports.map((support, index) => createSupportElement(support, index, supports.length)).join('')}
            </div>
        </div>
    `;
}

// Crear elemento individual de soporte
function createSupportElement(support, index, totalElements) {
    const pdfs = supportMapping[support.support_type] || [];
    const hasPDFs = pdfs.length > 0;
    
    return `
        <div class="support-element ${totalElements > 1 ? 'multiple-elements' : ''}">
            ${totalElements > 1 ? `<div class="element-header">Elemento ${index + 1}: ${support.support_type}</div>` : ''}
            
            <div class="support-info-enhanced">
                <!-- Información básica -->
                <div class="info-section">
                    <h6><i class="fas fa-info-circle"></i> Información Básica</h6>
                    <div class="info-grid">
                        ${createInfoItem('Número de Soporte', support.support_number)}
                        ${createInfoItem('Tipo de Soporte', support.support_type)}
                        ${createInfoItem('Número de Posición', support.position_number)}
                        ${createInfoItem('Código CWA', support.cwa_code)}
                        ${createInfoItem('Revisión', support.revision)}
                        ${createInfoItem('Cantidad', support.quantity)}
                    </div>
                </div>
                
                <!-- Información técnica -->
                <div class="info-section">
                    <h6><i class="fas fa-cogs"></i> Información Técnica</h6>
                    <div class="info-grid">
                        ${createInfoItem('Clase de Material', support.material_class)}
                        ${createInfoItem('Clase Material Tubería', support.piping_material_class)}
                        ${createInfoItem('Parámetros del Objeto', support.object_parameters)}
                        ${createInfoItem('Opción de Restricción', support.restraint_option)}
                        ${createInfoItem('Opción de Soporte', support.support_option)}
                        ${createInfoItem('Opción de Junta', support.joint_option)}
                        ${createInfoItem('Opción de Orientación', support.orientation_option)}
                    </div>
                </div>
                
                <!-- Dimensiones -->
                ${createDimensionsSection(support)}
                
                <!-- Información de proyecto -->
                <div class="info-section">
                    <h6><i class="fas fa-project-diagram"></i> Información de Proyecto</h6>
                    <div class="info-grid">
                        ${createInfoItem('Fluido y Tubería', support.fluid_piping)}
                        ${createInfoItem('Hoja ISO', support.iso_sheet)}
                        ${createInfoItem('Temperatura', support.temperature)}
                        ${createInfoItem('Archivo Fuente', support.file_source)}
                    </div>
                </div>
                
                <!-- Notas -->
                ${support.notes ? `
                    <div class="info-section">
                        <h6><i class="fas fa-sticky-note"></i> Notas y Referencias</h6>
                        <div class="notes-content">${support.notes}</div>
                    </div>
                ` : ''}
                
                <!-- PDFs -->
                ${hasPDFs ? `
                    <div class="pdf-section">
                        <h6><i class="fas fa-file-pdf"></i> Estándares de Soporte Disponibles</h6>
                        ${pdfs.map(pdf => `
                            <a href="ESTANDARES DE SOPORTES/${pdf}" target="_blank" class="pdf-link">
                                <i class="fas fa-download"></i> ${pdf}
                            </a>
                        `).join('')}
                    </div>
                ` : `
                    <div class="alert alert-warning">
                        <i class="fas fa-exclamation-triangle"></i>
                        No se encontraron PDFs de estándares para este tipo de soporte (${support.support_type})
                    </div>
                `}
            </div>
        </div>
    `;
}

// Crear item de información
function createInfoItem(label, value) {
    if (!value || value === '' || value === 'nan') return '';
    
    return `
        <div class="info-item-enhanced">
            <div class="info-label-enhanced">${label}</div>
            <div class="info-value-enhanced">${value}</div>
        </div>
    `;
}

// Crear sección de dimensiones
function createDimensionsSection(support) {
    const dimensions = [];
    
    // Recopilar todas las dimensiones disponibles
    if (support.mto_dimensions) dimensions.push(['Dimensiones MTO', support.mto_dimensions]);
    for (let i = 1; i <= 11; i++) {
        const dimValue = support[`dim_${i}`];
        if (dimValue && dimValue !== '' && dimValue !== 'nan') {
            dimensions.push([`Dimensión ${i}`, dimValue]);
        }
    }
    
    if (dimensions.length === 0) return '';
    
    return `
        <div class="info-section">
            <h6><i class="fas fa-ruler"></i> Dimensiones</h6>
            <div class="info-grid">
                ${dimensions.map(([label, value]) => createInfoItem(label, value)).join('')}
            </div>
        </div>
    `;
}

// Toggle grupo de soportes
function toggleSupportGroup(supportNumber) {
    const body = document.getElementById(`group-${supportNumber}`);
    const icon = document.getElementById(`toggle-${supportNumber}`);
    
    if (body.style.display === 'none') {
        body.style.display = 'block';
        icon.classList.remove('fa-chevron-down');
        icon.classList.add('fa-chevron-up');
    } else {
        body.style.display = 'none';
        icon.classList.remove('fa-chevron-up');
        icon.classList.add('fa-chevron-down');
    }
}

// Mostrar estado de carga
function showLoading(show) {
    const loading = document.getElementById('loading');
    const results = document.getElementById('resultsContainer');
    
    if (show) {
        loading.style.display = 'block';
        results.style.display = 'none';
    } else {
        loading.style.display = 'none';
        results.style.display = 'block';
    }
}

// Mostrar sin resultados
function showNoResults() {
    document.getElementById('noResults').style.display = 'block';
    document.getElementById('resultsContainer').innerHTML = '';
}

// Ocultar sin resultados
function hideNoResults() {
    document.getElementById('noResults').style.display = 'none';
}

// Mostrar error
function showError(message) {
    const container = document.getElementById('resultsContainer');
    container.innerHTML = `
        <div class="alert alert-danger">
            <i class="fas fa-exclamation-circle"></i>
            ${message}
        </div>
    `;
}

// Búsqueda con Enter
document.getElementById('searchInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        searchSupports();
    }
});

// Búsqueda en tiempo real optimizada
let searchTimeout;
document.getElementById('searchInput').addEventListener('input', function() {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(searchSupports, 300); // Reducido de 500ms a 300ms
}); 