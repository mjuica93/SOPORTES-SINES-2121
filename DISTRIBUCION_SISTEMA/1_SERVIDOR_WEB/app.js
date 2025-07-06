// Variables globales
let allSupports = [];
let supportMapping = {};
let filteredSupports = [];

// Cargar datos al iniciar la aplicación
document.addEventListener('DOMContentLoaded', function() {
    loadData();
});

// Cargar datos desde los archivos JSON
async function loadData() {
    try {
        showLoading(true);
        
        // Cargar datos de soportes
        const supportsResponse = await fetch('support_data.json');
        allSupports = await supportsResponse.json();
        
        // Cargar mapeo de PDFs
        const mappingResponse = await fetch('support_pdf_mapping.json');
        supportMapping = await mappingResponse.json();
        
        // Inicializar la aplicación
        initializeApp();
        
    } catch (error) {
        console.error('Error cargando datos:', error);
        showError('Error al cargar los datos. Verifica que los archivos JSON estén disponibles.');
    } finally {
        showLoading(false);
    }
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
    const totalTypes = new Set(allSupports.map(s => s.support_type)).size;
    const withPDFs = allSupports.filter(s => supportMapping[s.support_type] && supportMapping[s.support_type].length > 0).length;
    const searchResults = filteredSupports.length;
    
    document.getElementById('totalSupports').textContent = totalSupports.toLocaleString();
    document.getElementById('totalTypes').textContent = totalTypes.toLocaleString();
    document.getElementById('withPDFs').textContent = withPDFs.toLocaleString();
    document.getElementById('searchResults').textContent = searchResults.toLocaleString();
}

// Poblar filtro de tipos
function populateTypeFilter() {
    const filterSelect = document.getElementById('filterType');
    const types = [...new Set(allSupports.map(s => s.support_type))].sort();
    
    // Limpiar opciones existentes (mantener "Todos los tipos")
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
    
    filteredSupports = allSupports.filter(support => {
        const matchesSearch = !searchTerm || 
            support.support_number.toLowerCase().includes(searchTerm) ||
            support.support_type.toLowerCase().includes(searchTerm) ||
            support.fluid_piping.toLowerCase().includes(searchTerm) ||
            support.notes.toLowerCase().includes(searchTerm);
        
        const matchesType = !filterType || support.support_type === filterType;
        
        return matchesSearch && matchesType;
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
    filteredSupports = allSupports;
    displaySupports(allSupports);
    updateStats();
}

// Mostrar soportes
function displaySupports(supports) {
    const container = document.getElementById('resultsContainer');
    
    if (supports.length === 0) {
        showNoResults();
        return;
    }
    
    hideNoResults();
    
    // Limitar a los primeros 50 resultados para rendimiento
    const displaySupports = supports.slice(0, 50);
    
    container.innerHTML = displaySupports.map(support => createSupportCard(support)).join('');
    
    if (supports.length > 50) {
        container.innerHTML += `
            <div class="alert alert-info text-center">
                <i class="fas fa-info-circle"></i>
                Mostrando 50 de ${supports.length} resultados. Refina tu búsqueda para ver más resultados.
            </div>
        `;
    }
}

// Crear tarjeta de soporte
function createSupportCard(support) {
    const pdfs = supportMapping[support.support_type] || [];
    const hasPDFs = pdfs.length > 0;
    
    return `
        <div class="support-card">
            <div class="support-header">
                <i class="fas fa-cogs"></i> Soporte ${support.support_number} - ${support.support_type}
                ${hasPDFs ? '<i class="fas fa-file-pdf ms-2"></i>' : ''}
            </div>
            <div class="support-body">
                <div class="support-info">
                    <div class="info-item">
                        <div class="info-label">Número de Soporte</div>
                        <div class="info-value">${support.support_number}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Tipo de Soporte</div>
                        <div class="info-value">${support.support_type}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Número de Posición</div>
                        <div class="info-value">${support.position_number || 'N/A'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Clase de Material</div>
                        <div class="info-value">${support.material_class || 'N/A'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Dimensiones</div>
                        <div class="info-value">${support.size_dimensions || 'N/A'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Cantidad</div>
                        <div class="info-value">${support.quantity || 'N/A'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Fluido y Número de Tubería</div>
                        <div class="info-value">${support.fluid_piping || 'N/A'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Hoja ISO</div>
                        <div class="info-value">${support.iso_sheet || 'N/A'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Temperatura</div>
                        <div class="info-value">${support.temperature || 'N/A'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Archivo Fuente</div>
                        <div class="info-value">${support.file_source}</div>
                    </div>
                </div>
                
                ${support.notes ? `
                    <div class="info-item" style="grid-column: 1 / -1;">
                        <div class="info-label">Notas y Referencias</div>
                        <div class="info-value">${support.notes}</div>
                    </div>
                ` : ''}
                
                ${hasPDFs ? `
                    <div class="pdf-section">
                        <h6><i class="fas fa-file-pdf"></i> Estándares de Soporte Disponibles:</h6>
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

// Búsqueda en tiempo real (opcional)
let searchTimeout;
document.getElementById('searchInput').addEventListener('input', function() {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(searchSupports, 500);
}); 