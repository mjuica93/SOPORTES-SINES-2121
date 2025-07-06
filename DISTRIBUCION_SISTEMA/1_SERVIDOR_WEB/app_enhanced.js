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
async function loadData() {
    try {
        showLoading(true);
        
        // Cargar datos mejorados de soportes
        const supportsResponse = await fetch('support_data_enhanced.json');
        allSupports = await supportsResponse.json();
        
        // Cargar mapeo de PDFs
        const mappingResponse = await fetch('support_pdf_mapping.json');
        supportMapping = await mappingResponse.json();
        
        // Agrupar soportes por número
        groupSupportsByNumber();
        
        // Inicializar la aplicación
        initializeApp();
        
    } catch (error) {
        console.error('Error cargando datos:', error);
        // Fallback a datos originales si los mejorados no están disponibles
        try {
            const supportsResponse = await fetch('support_data.json');
            allSupports = await supportsResponse.json();
            groupSupportsByNumber();
            initializeApp();
        } catch (fallbackError) {
            showError('Error al cargar los datos. Verifica que los archivos JSON estén disponibles.');
        }
    } finally {
        showLoading(false);
    }
}

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