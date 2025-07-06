// Variables globales
let allSupports = [];
let supportMapping = {};
let filteredSupports = [];

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
    
    // Obtener información de instalación
    const installationInfo = window.installationManager ? 
        window.installationManager.getInstallationInfo(support) : 
        { status: 'pending', planned_date: null, actual_date: null, notes: '', installed_by: '' };
    
    return `
        <div class="support-card">
            <div class="support-header">
                <i class="fas fa-cogs"></i> Soporte ${support.support_number} - ${support.support_type}
                ${hasPDFs ? '<i class="fas fa-file-pdf ms-2"></i>' : ''}
                ${createInstallationStatusBadge(installationInfo)}
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
                
                ${createInstallationSection(support, installationInfo)}
                
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

// ===== FUNCIONES DE GESTIÓN DE INSTALACIONES =====

// Variable global para el soporte en edición
let currentEditingSupport = null;

// Crear badge de estado de instalación
function createInstallationStatusBadge(installationInfo) {
    if (!window.installationManager) return '';
    
    const statusColor = window.installationManager.getStatusColor(installationInfo.status);
    const statusText = window.installationManager.getStatusText(installationInfo.status);
    const statusIcon = window.installationManager.getStatusIcon(installationInfo.status);
    
    let overdueIndicator = '';
    if (isOverdue(installationInfo.planned_date, installationInfo.status)) {
        overdueIndicator = '<span class="overdue-indicator">ATRASADO</span>';
    }
    
    return `
        <span class="installation-status status-${installationInfo.status}" style="background-color: ${statusColor};">
            <i class="${statusIcon}"></i> ${statusText}
        </span>
        ${overdueIndicator}
    `;
}

// Crear sección de instalación en la tarjeta
function createInstallationSection(support, installationInfo) {
    if (!window.installationManager) return '';
    
    const statusText = window.installationManager.getStatusText(installationInfo.status);
    
    let dateInfo = '';
    if (installationInfo.planned_date) {
        dateInfo += `<div class="installation-date">📅 Planificado: ${formatDate(installationInfo.planned_date)}</div>`;
    }
    if (installationInfo.actual_date) {
        dateInfo += `<div class="installation-date">✅ Instalado: ${formatDate(installationInfo.actual_date)}</div>`;
    }
    if (installationInfo.installed_by) {
        dateInfo += `<div class="installation-date">👷 Por: ${installationInfo.installed_by}</div>`;
    }
    if (installationInfo.notes) {
        dateInfo += `<div class="installation-date">💬 ${installationInfo.notes}</div>`;
    }
    
    return `
        <div class="installation-section">
            <h6><i class="fas fa-calendar-check"></i> Estado de Instalación</h6>
            ${dateInfo}
            <div class="installation-actions">
                <div class="installation-controls">
                    <button class="btn btn-sm btn-primary" onclick="editInstallation('${support.support_number}', '${support.support_type}', '${support.position_number || '1'}')">
                        <i class="fas fa-edit"></i> Editar
                    </button>
                    <div class="quick-status-buttons">
                        ${installationInfo.status !== 'planned' ? `
                            <button class="btn-status-planned" onclick="quickStatusChange('${support.support_number}', '${support.support_type}', '${support.position_number || '1'}', 'planned')">
                                Planificar
                            </button>
                        ` : ''}
                        ${installationInfo.status !== 'in_progress' ? `
                            <button class="btn-status-progress" onclick="quickStatusChange('${support.support_number}', '${support.support_type}', '${support.position_number || '1'}', 'in_progress')">
                                En Proceso
                            </button>
                        ` : ''}
                        ${installationInfo.status !== 'installed' ? `
                            <button class="btn-status-installed" onclick="quickStatusChange('${support.support_number}', '${support.support_type}', '${support.position_number || '1'}', 'installed')">
                                Instalado
                            </button>
                        ` : ''}
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Filtrar por estado de instalación
function filterByStatus() {
    const statusFilter = document.getElementById('filterStatus').value;
    const searchTerm = document.getElementById('searchInput').value.toLowerCase().trim();
    const typeFilter = document.getElementById('filterType').value;
    
    filteredSupports = allSupports.filter(support => {
        const matchesSearch = !searchTerm || 
            support.support_number.toLowerCase().includes(searchTerm) ||
            support.support_type.toLowerCase().includes(searchTerm) ||
            support.fluid_piping.toLowerCase().includes(searchTerm) ||
            support.notes.toLowerCase().includes(searchTerm);
        
        const matchesType = !typeFilter || support.support_type === typeFilter;
        
        let matchesStatus = true;
        if (statusFilter && window.installationManager) {
            const installationInfo = window.installationManager.getInstallationInfo(support);
            matchesStatus = installationInfo.status === statusFilter;
        }
        
        return matchesSearch && matchesType && matchesStatus;
    });
    
    displaySupports(filteredSupports);
    updateStats();
}

// Abrir panel de gestión de instalaciones
function openInstallationPanel() {
    if (!window.installationManager) {
        alert('Sistema de gestión de instalaciones no disponible');
        return;
    }
    
    updateInstallationModalStats();
    const modal = new bootstrap.Modal(document.getElementById('installationModal'));
    modal.show();
}

// Actualizar estadísticas en el modal
function updateInstallationModalStats() {
    if (!window.installationManager) return;
    
    const stats = window.installationManager.getStatistics();
    
    document.getElementById('modalPendingCount').textContent = stats.pending;
    document.getElementById('modalPlannedCount').textContent = stats.planned;
    document.getElementById('modalInProgressCount').textContent = stats.in_progress;
    document.getElementById('modalInstalledCount').textContent = stats.installed;
    document.getElementById('modalOverdueCount').textContent = stats.overdue;
}

// Editar instalación individual
function editInstallation(supportNumber, supportType, positionNumber) {
    if (!window.installationManager) return;
    
    // Encontrar el soporte en los datos
    const support = allSupports.find(s => 
        s.support_number === supportNumber && 
        s.support_type === supportType && 
        (s.position_number || '1') === positionNumber
    );
    
    if (!support) {
        alert('Soporte no encontrado');
        return;
    }
    
    currentEditingSupport = support;
    const installationInfo = window.installationManager.getInstallationInfo(support);
    
    // Llenar el formulario
    document.getElementById('supportInfo').value = `${support.support_number} - ${support.support_type} (Pos. ${support.position_number || '1'})`;
    document.getElementById('installationStatus').value = installationInfo.status;
    document.getElementById('plannedDate').value = installationInfo.planned_date ? 
        formatDateForInput(installationInfo.planned_date) : '';
    document.getElementById('actualDate').value = installationInfo.actual_date ? 
        formatDateForInput(installationInfo.actual_date) : '';
    document.getElementById('installedBy').value = installationInfo.installed_by || '';
    document.getElementById('installationNotes').value = installationInfo.notes || '';
    
    // Mostrar/ocultar campos según el estado
    toggleDateFields();
    
    // Mostrar modal
    const modal = new bootstrap.Modal(document.getElementById('editInstallationModal'));
    modal.show();
}

// Cambio rápido de estado
function quickStatusChange(supportNumber, supportType, positionNumber, newStatus) {
    if (!window.installationManager) return;
    
    const support = allSupports.find(s => 
        s.support_number === supportNumber && 
        s.support_type === supportType && 
        (s.position_number || '1') === positionNumber
    );
    
    if (!support) return;
    
    let updateData = { status: newStatus };
    
    if (newStatus === 'installed') {
        updateData.actual_date = new Date().toISOString();
        const installedBy = prompt('¿Quién instaló este soporte? (opcional)');
        if (installedBy) {
            updateData.installed_by = installedBy;
        }
    } else if (newStatus === 'planned') {
        const plannedDate = prompt('Fecha planificada (YYYY-MM-DD):');
        if (plannedDate) {
            updateData.planned_date = new Date(plannedDate).toISOString();
        }
    }
    
    window.installationManager.updateInstallation(support, updateData);
    
    // Refrescar la visualización
    if (filteredSupports.length > 0) {
        displaySupports(filteredSupports);
    } else {
        displayAllSupports();
    }
    updateStats();
}

// Guardar instalación desde el modal
function saveInstallation() {
    if (!currentEditingSupport || !window.installationManager) return;
    
    const status = document.getElementById('installationStatus').value;
    const plannedDate = document.getElementById('plannedDate').value;
    const actualDate = document.getElementById('actualDate').value;
    const installedBy = document.getElementById('installedBy').value;
    const notes = document.getElementById('installationNotes').value;
    
    const updateData = {
        status: status,
        planned_date: plannedDate ? new Date(plannedDate).toISOString() : null,
        actual_date: actualDate ? new Date(actualDate).toISOString() : null,
        installed_by: installedBy,
        notes: notes
    };
    
    window.installationManager.updateInstallation(currentEditingSupport, updateData);
    
    // Cerrar modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('editInstallationModal'));
    modal.hide();
    
    // Refrescar visualización
    if (filteredSupports.length > 0) {
        displaySupports(filteredSupports);
    } else {
        displayAllSupports();
    }
    updateStats();
    
    alert('✅ Información de instalación guardada');
}

// Mostrar/ocultar campos de fecha según el estado
function toggleDateFields() {
    const status = document.getElementById('installationStatus').value;
    const plannedGroup = document.getElementById('plannedDateGroup');
    const actualGroup = document.getElementById('actualDateGroup');
    const installedByGroup = document.getElementById('installedByGroup');
    
    // Mostrar fecha planificada para estados que no sea 'pending'
    plannedGroup.style.display = (status === 'pending') ? 'none' : 'block';
    
    // Mostrar fecha actual y quién instaló solo para 'installed'
    actualGroup.style.display = (status === 'installed') ? 'block' : 'none';
    installedByGroup.style.display = (status === 'installed') ? 'block' : 'none';
}

// Exportar datos de instalaciones
function exportInstallations() {
    if (!window.installationManager) return;
    
    const data = window.installationManager.exportData();
    const csv = convertToCSV(data);
    downloadCSV(csv, 'instalaciones_soportes.csv');
}

// Convertir a CSV
function convertToCSV(data) {
    const headers = ['Número Soporte', 'Tipo Soporte', 'Posición', 'Estado', 'Fecha Planificada', 'Fecha Instalación', 'Instalado Por', 'Notas'];
    const rows = data.map(item => [
        item.support_number,
        item.support_type,
        item.position_number,
        item.status,
        item.planned_date ? formatDate(item.planned_date) : '',
        item.actual_date ? formatDate(item.actual_date) : '',
        item.installed_by || '',
        item.notes || ''
    ]);
    
    return [headers, ...rows].map(row => row.map(cell => `"${cell}"`).join(',')).join('\n');
}

// Descargar CSV
function downloadCSV(csv, filename) {
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Mostrar reporte de instalaciones
function showInstallationReport() {
    alert('🚧 Función de reportes en desarrollo.\nPróximamente: gráficos de progreso, timeline, estadísticas avanzadas.');
}

// Planificar instalaciones múltiples
function planBulkInstallations() {
    alert('🚧 Función de planificación múltiple en desarrollo.\nPróximamente: selección masiva, fechas automáticas, asignación de equipos.');
}

// Formatear fecha para input type="date"
function formatDateForInput(date) {
    if (!date) return '';
    const d = new Date(date);
    if (isNaN(d.getTime())) return '';
    return d.toISOString().split('T')[0];
}

// Actualizar estadísticas con información de instalaciones
function updateStats() {
    const originalUpdateStats = arguments.callee;
    
    const totalSupports = allSupports.length;
    const totalTypes = new Set(allSupports.map(s => s.support_type)).size;
    const withPDFs = allSupports.filter(s => supportMapping[s.support_type] && supportMapping[s.support_type].length > 0).length;
    const searchResults = filteredSupports.length;
    
    document.getElementById('totalSupports').textContent = totalSupports.toLocaleString();
    document.getElementById('totalTypes').textContent = totalTypes.toLocaleString();
    document.getElementById('withPDFs').textContent = withPDFs.toLocaleString();
    document.getElementById('searchResults').textContent = searchResults.toLocaleString();
    
    // Estadísticas de instalación
    if (window.installationManager) {
        const installationStats = window.installationManager.getStatistics();
        document.getElementById('installedCount').textContent = installationStats.installed.toLocaleString();
        document.getElementById('pendingCount').textContent = installationStats.pending.toLocaleString();
    }
}

// Escuchar eventos de actualización de instalaciones
if (typeof window !== 'undefined') {
    window.addEventListener('installationUpdated', function(event) {
        console.log('📅 Instalación actualizada:', event.detail);
        updateStats();
    });
    
    window.addEventListener('installationsImported', function() {
        console.log('📥 Instalaciones importadas');
        if (filteredSupports.length > 0) {
            displaySupports(filteredSupports);
        } else {
            displayAllSupports();
        }
        updateStats();
    });
    
    window.addEventListener('installationsCleared', function() {
        console.log('🗑️ Instalaciones eliminadas');
        if (filteredSupports.length > 0) {
            displaySupports(filteredSupports);
        } else {
            displayAllSupports();
        }
        updateStats();
    });
} 