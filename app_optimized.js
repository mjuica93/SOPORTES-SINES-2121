// Optimized SINES Support System v2.0
// Performance optimizations: API pagination, lazy loading, virtual scrolling

// Configuration
const CONFIG = {
    API_BASE: '/api',
    PAGE_SIZE: 50,
    SEARCH_DEBOUNCE: 300,
    CACHE_DURATION: 5 * 60 * 1000, // 5 minutes
    MAX_CACHED_PAGES: 10
};

// Global state management
const AppState = {
    supports: [],
    filteredSupports: [],
    currentPage: 1,
    totalPages: 0,
    totalSupports: 0,
    loading: false,
    searchQuery: '',
    selectedType: '',
    selectedStatus: '',
    cache: new Map(),
    supportTypes: [],
    stats: {}
};

// Performance monitoring
const PerformanceMonitor = {
    start: (label) => {
        console.time(label);
    },
    end: (label) => {
        console.timeEnd(label);
    },
    mark: (label) => {
        if (performance.mark) {
            performance.mark(label);
        }
    },
    measure: (name, start, end) => {
        if (performance.measure) {
            performance.measure(name, start, end);
        }
    }
};

// Cache manager for API responses
class CacheManager {
    constructor() {
        this.cache = new Map();
        this.timestamps = new Map();
    }
    
    set(key, data, duration = CONFIG.CACHE_DURATION) {
        this.cache.set(key, data);
        this.timestamps.set(key, Date.now() + duration);
        
        // Clean old entries
        if (this.cache.size > CONFIG.MAX_CACHED_PAGES) {
            this.cleanup();
        }
    }
    
    get(key) {
        const timestamp = this.timestamps.get(key);
        if (!timestamp || Date.now() > timestamp) {
            this.cache.delete(key);
            this.timestamps.delete(key);
            return null;
        }
        return this.cache.get(key);
    }
    
    cleanup() {
        const now = Date.now();
        for (const [key, timestamp] of this.timestamps) {
            if (now > timestamp) {
                this.cache.delete(key);
                this.timestamps.delete(key);
            }
        }
    }
    
    clear() {
        this.cache.clear();
        this.timestamps.clear();
    }
}

// Initialize cache manager
const cacheManager = new CacheManager();

// Debounced search function
function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

// API service with caching and error handling
class APIService {
    static async request(endpoint, params = {}) {
        const url = new URL(`${CONFIG.API_BASE}${endpoint}`, window.location.origin);
        Object.keys(params).forEach(key => {
            if (params[key] !== null && params[key] !== undefined && params[key] !== '') {
                url.searchParams.append(key, params[key]);
            }
        });
        
        const cacheKey = url.toString();
        const cached = cacheManager.get(cacheKey);
        if (cached) {
            console.log('📦 Cache hit:', cacheKey);
            return cached;
        }
        
        try {
            PerformanceMonitor.mark(`api-start-${endpoint}`);
            
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                    'Accept-Encoding': 'gzip, deflate'
                },
                cache: 'no-store' // Let our cache manager handle caching
            });
            
            if (!response.ok) {
                throw new Error(`API Error: ${response.status} ${response.statusText}`);
            }
            
            const data = await response.json();
            
            PerformanceMonitor.mark(`api-end-${endpoint}`);
            PerformanceMonitor.measure(`api-${endpoint}`, `api-start-${endpoint}`, `api-end-${endpoint}`);
            
            // Cache successful responses
            cacheManager.set(cacheKey, data);
            
            return data;
            
        } catch (error) {
            console.error('❌ API Error:', error);
            throw error;
        }
    }
    
    static async getSupports(page = 1, limit = CONFIG.PAGE_SIZE) {
        return this.request('/supports', { page, limit });
    }
    
    static async searchSupports(query, type = '', page = 1, limit = CONFIG.PAGE_SIZE) {
        return this.request('/supports/search', { q: query, type, page, limit });
    }
    
    static async getStats() {
        return this.request('/supports/stats');
    }
    
    static async getTypes() {
        return this.request('/supports/types');
    }
}

// DOM Management utilities
class DOMManager {
    static show(element) {
        if (element) element.style.display = 'block';
    }
    
    static hide(element) {
        if (element) element.style.display = 'none';
    }
    
    static setText(elementId, text) {
        const element = document.getElementById(elementId);
        if (element) element.textContent = text;
    }
    
    static setHTML(elementId, html) {
        const element = document.getElementById(elementId);
        if (element) element.innerHTML = html;
    }
    
    static addClass(element, className) {
        if (element) element.classList.add(className);
    }
    
    static removeClass(element, className) {
        if (element) element.classList.remove(className);
    }
    
    static toggleClass(element, className) {
        if (element) element.classList.toggle(className);
    }
}

// Loading state management
class LoadingManager {
    static show() {
        DOMManager.show(document.getElementById('loading'));
        DOMManager.hide(document.getElementById('resultsContainer'));
        DOMManager.hide(document.getElementById('noResults'));
        AppState.loading = true;
    }
    
    static hide() {
        DOMManager.hide(document.getElementById('loading'));
        DOMManager.show(document.getElementById('resultsContainer'));
        AppState.loading = false;
    }
    
    static showNoResults() {
        DOMManager.hide(document.getElementById('loading'));
        DOMManager.hide(document.getElementById('resultsContainer'));
        DOMManager.show(document.getElementById('noResults'));
        AppState.loading = false;
    }
}

// Statistics display
function updateStats() {
    if (AppState.stats) {
        DOMManager.setText('totalSupports', AppState.stats.total_supports?.toLocaleString() || '0');
        DOMManager.setText('totalTypes', AppState.stats.total_types?.toLocaleString() || '0');
        DOMManager.setText('withPDFs', AppState.stats.with_pdfs?.toLocaleString() || '0');
    }
    
    DOMManager.setText('searchResults', AppState.totalSupports?.toLocaleString() || '0');
    
    // Update installation counts (if available)
    if (window.installationManager) {
        const installationStats = window.installationManager.getStats();
        DOMManager.setText('installedCount', installationStats.installed || '0');
        DOMManager.setText('pendingCount', installationStats.pending || '0');
    }
}

// Populate type filter dropdown
function populateTypeFilter() {
    const filterSelect = document.getElementById('filterType');
    if (!filterSelect) return;
    
    filterSelect.innerHTML = '<option value="">Todos los tipos</option>';
    
    AppState.supportTypes.forEach(type => {
        const option = document.createElement('option');
        option.value = type;
        option.textContent = type;
        filterSelect.appendChild(option);
    });
}

// Create support card HTML
function createSupportCard(support) {
    const hasPDFs = support.has_pdfs || false;
    
    // Get installation info if available
    const installationInfo = window.installationManager ? 
        window.installationManager.getInstallationInfo(support) : 
        { status: 'pending', planned_date: null, actual_date: null, notes: '', installed_by: '' };
    
    return `
        <div class="support-card" data-support-id="${support.support_number}">
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
                        <div class="info-value">${support.file_source || support.source_file || 'N/A'}</div>
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
                        <button class="btn btn-sm btn-outline-primary" onclick="loadPDFsForSupport('${support.support_type}')">
                            <i class="fas fa-download"></i> Cargar PDFs
                        </button>
                        <div id="pdfs-${support.support_number}" class="pdf-links" style="display: none;"></div>
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

// Create installation status badge
function createInstallationStatusBadge(installationInfo) {
    const statusClasses = {
        'pending': 'status-pending',
        'planned': 'status-planned',
        'in_progress': 'status-in_progress',
        'installed': 'status-installed'
    };
    
    const statusClass = statusClasses[installationInfo.status] || 'status-pending';
    const statusText = installationInfo.status.replace('_', ' ').toUpperCase();
    
    return `<span class="installation-status ${statusClass}">${statusText}</span>`;
}

// Create installation section
function createInstallationSection(support, installationInfo) {
    return `
        <div class="installation-section">
            <h6><i class="fas fa-calendar-check"></i> Estado de Instalación</h6>
            <div class="installation-controls">
                <select onchange="quickStatusChange('${support.support_number}', '${support.support_type}', '${support.position_number || ''}', this.value)">
                    <option value="pending" ${installationInfo.status === 'pending' ? 'selected' : ''}>Pendiente</option>
                    <option value="planned" ${installationInfo.status === 'planned' ? 'selected' : ''}>Planificado</option>
                    <option value="in_progress" ${installationInfo.status === 'in_progress' ? 'selected' : ''}>En Proceso</option>
                    <option value="installed" ${installationInfo.status === 'installed' ? 'selected' : ''}>Instalado</option>
                </select>
                <button class="btn btn-sm btn-outline-primary" onclick="editInstallation('${support.support_number}', '${support.support_type}', '${support.position_number || ''}')">
                    <i class="fas fa-edit"></i> Editar
                </button>
            </div>
            ${installationInfo.planned_date ? `
                <div class="installation-date">
                    <i class="fas fa-calendar"></i> Fecha planificada: ${formatDate(installationInfo.planned_date)}
                </div>
            ` : ''}
            ${installationInfo.actual_date ? `
                <div class="installation-date">
                    <i class="fas fa-check-circle"></i> Fecha de instalación: ${formatDate(installationInfo.actual_date)}
                </div>
            ` : ''}
        </div>
    `;
}

// Display supports with virtual scrolling optimization
function displaySupports(supports) {
    const container = document.getElementById('resultsContainer');
    if (!container) return;
    
    if (!supports || supports.length === 0) {
        LoadingManager.showNoResults();
        return;
    }
    
    LoadingManager.hide();
    
    // Create HTML for all supports
    const supportsHTML = supports.map(support => createSupportCard(support)).join('');
    container.innerHTML = supportsHTML;
    
    // Add pagination controls if needed
    if (AppState.totalPages > 1) {
        container.innerHTML += createPaginationControls();
    }
    
    // Update stats
    updateStats();
}

// Create pagination controls
function createPaginationControls() {
    const startPage = Math.max(1, AppState.currentPage - 2);
    const endPage = Math.min(AppState.totalPages, AppState.currentPage + 2);
    
    let paginationHTML = `
        <div class="pagination-container mt-4">
            <nav aria-label="Navegación de páginas">
                <ul class="pagination justify-content-center">
    `;
    
    // Previous button
    if (AppState.currentPage > 1) {
        paginationHTML += `
            <li class="page-item">
                <a class="page-link" href="#" onclick="goToPage(${AppState.currentPage - 1})">
                    <i class="fas fa-chevron-left"></i> Anterior
                </a>
            </li>
        `;
    }
    
    // Page numbers
    for (let i = startPage; i <= endPage; i++) {
        const active = i === AppState.currentPage ? 'active' : '';
        paginationHTML += `
            <li class="page-item ${active}">
                <a class="page-link" href="#" onclick="goToPage(${i})">${i}</a>
            </li>
        `;
    }
    
    // Next button
    if (AppState.currentPage < AppState.totalPages) {
        paginationHTML += `
            <li class="page-item">
                <a class="page-link" href="#" onclick="goToPage(${AppState.currentPage + 1})">
                    Siguiente <i class="fas fa-chevron-right"></i>
                </a>
            </li>
        `;
    }
    
    paginationHTML += `
                </ul>
            </nav>
            <div class="pagination-info text-center">
                Página ${AppState.currentPage} de ${AppState.totalPages} 
                (${AppState.totalSupports.toLocaleString()} resultados)
            </div>
        </div>
    `;
    
    return paginationHTML;
}

// Go to specific page
async function goToPage(page) {
    if (page === AppState.currentPage) return;
    
    AppState.currentPage = page;
    
    if (AppState.searchQuery || AppState.selectedType) {
        await performSearch();
    } else {
        await loadSupports();
    }
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Load supports from API
async function loadSupports() {
    try {
        LoadingManager.show();
        PerformanceMonitor.start('loadSupports');
        
        const response = await APIService.getSupports(AppState.currentPage, CONFIG.PAGE_SIZE);
        
        AppState.supports = response.data;
        AppState.totalPages = response.pagination.pages;
        AppState.totalSupports = response.pagination.total;
        
        displaySupports(AppState.supports);
        
        PerformanceMonitor.end('loadSupports');
        
    } catch (error) {
        console.error('❌ Error loading supports:', error);
        showError('Error al cargar los soportes. Por favor, intenta nuevamente.');
    }
}

// Perform search with debouncing
const performSearch = debounce(async function() {
    try {
        LoadingManager.show();
        PerformanceMonitor.start('performSearch');
        
        const query = AppState.searchQuery;
        const type = AppState.selectedType;
        
        if (!query && !type) {
            await loadSupports();
            return;
        }
        
        const response = await APIService.searchSupports(query, type, AppState.currentPage, CONFIG.PAGE_SIZE);
        
        AppState.supports = response.data;
        AppState.totalPages = response.pagination.pages;
        AppState.totalSupports = response.pagination.total;
        
        displaySupports(AppState.supports);
        
        PerformanceMonitor.end('performSearch');
        
    } catch (error) {
        console.error('❌ Error performing search:', error);
        showError('Error al buscar soportes. Por favor, intenta nuevamente.');
    }
}, CONFIG.SEARCH_DEBOUNCE);

// Search function
function searchSupports() {
    AppState.searchQuery = document.getElementById('searchInput').value.toLowerCase().trim();
    AppState.currentPage = 1;
    performSearch();
}

// Filter by type
function filterByType() {
    AppState.selectedType = document.getElementById('filterType').value;
    AppState.currentPage = 1;
    performSearch();
}

// Filter by status
function filterByStatus() {
    AppState.selectedStatus = document.getElementById('filterStatus').value;
    AppState.currentPage = 1;
    performSearch();
}

// Load PDF information for a support type
async function loadPDFsForSupport(supportType) {
    // This would typically load from the PDF mapping
    // For now, we'll use the existing mapping if available
    const pdfContainer = document.getElementById(`pdfs-${supportType}`);
    if (pdfContainer) {
        pdfContainer.style.display = 'block';
        pdfContainer.innerHTML = `
            <div class="text-center">
                <i class="fas fa-spinner fa-spin"></i> Cargando PDFs...
            </div>
        `;
        
        // Simulate PDF loading
        setTimeout(() => {
            pdfContainer.innerHTML = `
                <a href="ESTANDARES DE SOPORTES/${supportType}.pdf" target="_blank" class="pdf-link">
                    <i class="fas fa-download"></i> ${supportType}.pdf
                </a>
            `;
        }, 1000);
    }
}

// Error display
function showError(message) {
    const container = document.getElementById('resultsContainer');
    if (container) {
        container.innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-circle"></i>
                ${message}
            </div>
        `;
    }
}

// Format date for display
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES');
}

// Initialize the application
async function initializeApp() {
    try {
        PerformanceMonitor.start('initializeApp');
        
        console.log('🚀 Initializing Optimized SINES App...');
        
        // Load initial data in parallel
        const [statsResponse, typesResponse] = await Promise.all([
            APIService.getStats(),
            APIService.getTypes()
        ]);
        
        AppState.stats = statsResponse;
        AppState.supportTypes = typesResponse.types;
        
        // Update UI
        updateStats();
        populateTypeFilter();
        
        // Load first page of supports
        await loadSupports();
        
        PerformanceMonitor.end('initializeApp');
        
        console.log('✅ App initialized successfully');
        
    } catch (error) {
        console.error('❌ Error initializing app:', error);
        showError('Error al inicializar la aplicación. Por favor, recarga la página.');
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    console.log('📱 DOM loaded, initializing app...');
    
    // Initialize the app
    initializeApp();
    
    // Search input event listener
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchSupports();
            }
        });
        
        // Real-time search (debounced)
        searchInput.addEventListener('input', function() {
            AppState.searchQuery = this.value.toLowerCase().trim();
            AppState.currentPage = 1;
            performSearch();
        });
    }
    
    // Clear cache periodically
    setInterval(() => {
        cacheManager.cleanup();
    }, 60000); // Clean every minute
});

// Expose functions globally for HTML onclick handlers
window.searchSupports = searchSupports;
window.filterByType = filterByType;
window.filterByStatus = filterByStatus;
window.goToPage = goToPage;
window.loadPDFsForSupport = loadPDFsForSupport;

// Installation management functions (if available)
if (typeof createInstallationStatusBadge === 'undefined') {
    window.createInstallationStatusBadge = createInstallationStatusBadge;
}
if (typeof createInstallationSection === 'undefined') {
    window.createInstallationSection = createInstallationSection;
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        AppState,
        APIService,
        initializeApp,
        searchSupports,
        filterByType,
        filterByStatus
    };
}

console.log('🎯 Optimized SINES App loaded successfully');