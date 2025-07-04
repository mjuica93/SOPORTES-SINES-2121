// Gestor de Isométricos - Sistema SINES
// Funcionalidad para gestionar isométricos con jerarquía: Isométricos -> Soportes

class IsometricManager {
    constructor() {
        this.isometrics = {};
        this.filteredIsometrics = {};
        this.currentFilters = {
            line: '',
            sheet: '',
            fluid: '',
            cwa: '',
            hasSupports: false,
            hasPdfs: false
        };
        this.isLoading = false;
        this.init();
    }

    async init() {
        try {
            console.log('🔄 Inicializando gestor de isométricos...');
            await this.loadIsometricData();
            this.setupEventListeners();
            this.renderInitialView();
            console.log('✅ Gestor de isométricos inicializado');
        } catch (error) {
            console.error('❌ Error inicializando gestor de isométricos:', error);
            this.showError('Error al inicializar el sistema de isométricos');
        }
    }

    async loadIsometricData() {
        try {
            this.isLoading = true;
            this.showLoading(true);

            const response = await fetch('./isometric_data_fixed.json');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            this.isometrics = data.isometrics;
            this.filteredIsometrics = { ...this.isometrics };
            this.summary = data.summary;

            console.log('📊 Datos de isométricos cargados:', this.summary);
            this.isLoading = false;
            this.showLoading(false);
        } catch (error) {
            this.isLoading = false;
            this.showLoading(false);
            throw error;
        }
    }

    setupEventListeners() {
        // Eventos para filtros
        document.getElementById('line-filter')?.addEventListener('input', (e) => {
            this.currentFilters.line = e.target.value;
            this.applyFilters();
        });

        document.getElementById('sheet-filter')?.addEventListener('input', (e) => {
            this.currentFilters.sheet = e.target.value;
            this.applyFilters();
        });

        document.getElementById('fluid-filter')?.addEventListener('input', (e) => {
            this.currentFilters.fluid = e.target.value;
            this.applyFilters();
        });

        document.getElementById('cwa-filter')?.addEventListener('input', (e) => {
            this.currentFilters.cwa = e.target.value;
            this.applyFilters();
        });

        document.getElementById('has-supports-filter')?.addEventListener('change', (e) => {
            this.currentFilters.hasSupports = e.target.checked;
            this.applyFilters();
        });

        document.getElementById('has-pdfs-filter')?.addEventListener('change', (e) => {
            this.currentFilters.hasPdfs = e.target.checked;
            this.applyFilters();
        });

        // Evento para limpiar filtros
        document.getElementById('clear-filters')?.addEventListener('click', () => {
            this.clearFilters();
        });

        // Evento para exportar datos
        document.getElementById('export-isometrics')?.addEventListener('click', () => {
            this.exportToCSV();
        });

        // Evento para alternar vista
        document.getElementById('toggle-view')?.addEventListener('click', () => {
            this.toggleView();
        });
    }

    applyFilters() {
        const filtered = {};
        
        for (const [key, isometric] of Object.entries(this.isometrics)) {
            let includeIsometric = true;

            // Filtro por LINE
            if (this.currentFilters.line && 
                !isometric.line.toLowerCase().includes(this.currentFilters.line.toLowerCase())) {
                includeIsometric = false;
            }

            // Filtro por SHEET
            if (this.currentFilters.sheet && 
                !isometric.sheet.toLowerCase().includes(this.currentFilters.sheet.toLowerCase())) {
                includeIsometric = false;
            }

            // Filtro por FLUID
            if (this.currentFilters.fluid && 
                !isometric.fluid.toLowerCase().includes(this.currentFilters.fluid.toLowerCase())) {
                includeIsometric = false;
            }

            // Filtro por CWA
            if (this.currentFilters.cwa && 
                !isometric.cwa.toString().toLowerCase().includes(this.currentFilters.cwa.toLowerCase())) {
                includeIsometric = false;
            }

            // Filtro por tiene soportes
            if (this.currentFilters.hasSupports && isometric.supports.length === 0) {
                includeIsometric = false;
            }

            // Filtro por tiene PDFs
            if (this.currentFilters.hasPdfs && 
                !isometric.pdf_files.normal && !isometric.pdf_files.prefab) {
                includeIsometric = false;
            }

            if (includeIsometric) {
                filtered[key] = isometric;
            }
        }

        this.filteredIsometrics = filtered;
        this.renderIsometrics();
        this.updateStats();
    }

    clearFilters() {
        this.currentFilters = {
            line: '',
            sheet: '',
            fluid: '',
            cwa: '',
            hasSupports: false,
            hasPdfs: false
        };

        // Limpiar inputs
        document.getElementById('line-filter').value = '';
        document.getElementById('sheet-filter').value = '';
        document.getElementById('fluid-filter').value = '';
        document.getElementById('cwa-filter').value = '';
        document.getElementById('has-supports-filter').checked = false;
        document.getElementById('has-pdfs-filter').checked = false;

        this.filteredIsometrics = { ...this.isometrics };
        this.renderIsometrics();
        this.updateStats();
    }

    renderInitialView() {
        this.renderFilters();
        this.renderIsometrics();
        this.updateStats();
    }

    renderFilters() {
        const filtersContainer = document.getElementById('isometric-filters');
        if (!filtersContainer) return;

        filtersContainer.innerHTML = `
            <div class="filters-section">
                <h3>🔍 Filtros de Isométricos</h3>
                <div class="filters-grid">
                    <div class="filter-group">
                        <label for="line-filter">Línea (LINE):</label>
                        <input type="text" id="line-filter" placeholder="Buscar por línea...">
                    </div>
                    <div class="filter-group">
                        <label for="sheet-filter">Hoja (SHEET):</label>
                        <input type="text" id="sheet-filter" placeholder="Buscar por hoja...">
                    </div>
                    <div class="filter-group">
                        <label for="fluid-filter">Fluido:</label>
                        <input type="text" id="fluid-filter" placeholder="Buscar por fluido...">
                    </div>
                    <div class="filter-group">
                        <label for="cwa-filter">CWA:</label>
                        <input type="text" id="cwa-filter" placeholder="Buscar por CWA...">
                    </div>
                    <div class="filter-group">
                        <label>
                            <input type="checkbox" id="has-supports-filter">
                            Solo con soportes
                        </label>
                    </div>
                    <div class="filter-group">
                        <label>
                            <input type="checkbox" id="has-pdfs-filter">
                            Solo con PDFs
                        </label>
                    </div>
                </div>
                <div class="filter-actions">
                    <button id="clear-filters" class="btn btn-secondary">
                        🗑️ Limpiar Filtros
                    </button>
                    <button id="export-isometrics" class="btn btn-primary">
                        📊 Exportar CSV
                    </button>
                    <button id="toggle-view" class="btn btn-info">
                        🔄 Cambiar Vista
                    </button>
                </div>
            </div>
        `;

        // Reconfigurar eventos después de renderizar
        this.setupEventListeners();
    }

    renderIsometrics() {
        const container = document.getElementById('isometric-results');
        if (!container) return;

        const isometricCount = Object.keys(this.filteredIsometrics).length;
        
        if (isometricCount === 0) {
            container.innerHTML = `
                <div class="no-results">
                    <p>🔍 No se encontraron isométricos que coincidan con los filtros</p>
                </div>
            `;
            return;
        }

        const isometricCards = Object.entries(this.filteredIsometrics)
            .slice(0, 50) // Limitar a 50 para rendimiento
            .map(([key, isometric]) => this.createIsometricCard(key, isometric))
            .join('');

        container.innerHTML = `
            <div class="isometric-grid">
                ${isometricCards}
            </div>
            ${isometricCount > 50 ? `<p class="showing-limit">Mostrando 50 de ${isometricCount} isométricos</p>` : ''}
        `;
    }

    createIsometricCard(key, isometric) {
        const supportCount = isometric.supports.length;
        const hasNormalPdf = isometric.pdf_files.normal;
        const hasPrefabPdf = isometric.pdf_files.prefab;

        return `
            <div class="isometric-card" data-key="${key}">
                <div class="isometric-header">
                    <h4>📐 ${isometric.line} - Hoja ${isometric.sheet}</h4>
                    <div class="isometric-badges">
                        ${supportCount > 0 ? `<span class="badge badge-supports">${supportCount} soportes</span>` : ''}
                        ${hasNormalPdf ? `<span class="badge badge-normal-pdf">PDF Normal</span>` : ''}
                        ${hasPrefabPdf ? `<span class="badge badge-prefab-pdf">PDF Prefab</span>` : ''}
                    </div>
                </div>
                
                <div class="isometric-info">
                    <div class="info-grid">
                        <div class="info-item">
                            <span class="label">Fluido:</span>
                            <span class="value">${isometric.fluid || 'N/A'}</span>
                        </div>
                        <div class="info-item">
                            <span class="label">CWA:</span>
                            <span class="value">${isometric.cwa || 'N/A'}</span>
                        </div>
                        <div class="info-item">
                            <span class="label">Unidad:</span>
                            <span class="value">${isometric.unit || 'N/A'}</span>
                        </div>
                        <div class="info-item">
                            <span class="label">Revisión:</span>
                            <span class="value">${isometric.revision || 'N/A'}</span>
                        </div>
                    </div>
                </div>

                <div class="isometric-actions">
                    ${hasNormalPdf ? `
                        <button class="btn btn-sm btn-pdf" onclick="window.open('${hasNormalPdf}', '_blank')">
                            📄 Ver PDF Normal
                        </button>
                    ` : ''}
                    ${hasPrefabPdf ? `
                        <button class="btn btn-sm btn-pdf" onclick="window.open('${hasPrefabPdf}', '_blank')">
                            🏗️ Ver PDF Prefab
                        </button>
                    ` : ''}
                    <button class="btn btn-sm btn-primary" onclick="isometricManager.showIsometricDetails('${key}')">
                        🔍 Ver Detalles
                    </button>
                </div>

                ${supportCount > 0 ? `
                    <div class="supports-summary">
                        <h5>🔧 Soportes Asociados (${supportCount})</h5>
                        <div class="supports-preview">
                            ${isometric.supports.slice(0, 3).map(support => `
                                <div class="support-item">
                                    <span class="support-number">${support.support_number}</span>
                                    <span class="support-pos">(Pos: ${support.position_number})</span>
                                </div>
                            `).join('')}
                            ${supportCount > 3 ? `<span class="more-supports">+${supportCount - 3} más</span>` : ''}
                        </div>
                    </div>
                ` : ''}
            </div>
        `;
    }

    showIsometricDetails(key) {
        const isometric = this.isometrics[key];
        if (!isometric) return;

        const modalContent = `
            <div class="modal-header">
                <h3>📐 Detalles del Isométrico: ${isometric.line} - Hoja ${isometric.sheet}</h3>
                <button class="close-btn" onclick="this.closest('.modal').remove()">×</button>
            </div>
            <div class="modal-body">
                <div class="isometric-details">
                    <div class="detail-section">
                        <h4>📋 Información General</h4>
                        <div class="detail-grid">
                            <div class="detail-item">
                                <span class="label">Línea:</span>
                                <span class="value">${isometric.line}</span>
                            </div>
                            <div class="detail-item">
                                <span class="label">Hoja:</span>
                                <span class="value">${isometric.sheet}</span>
                            </div>
                            <div class="detail-item">
                                <span class="label">Fluido:</span>
                                <span class="value">${isometric.fluid || 'N/A'}</span>
                            </div>
                            <div class="detail-item">
                                <span class="label">CWA:</span>
                                <span class="value">${isometric.cwa || 'N/A'}</span>
                            </div>
                            <div class="detail-item">
                                <span class="label">Unidad:</span>
                                <span class="value">${isometric.unit || 'N/A'}</span>
                            </div>
                            <div class="detail-item">
                                <span class="label">Revisión:</span>
                                <span class="value">${isometric.revision || 'N/A'}</span>
                            </div>
                        </div>
                    </div>

                    <div class="detail-section">
                        <h4>📄 Documentos PDF</h4>
                        <div class="pdf-actions">
                            ${isometric.pdf_files.normal ? `
                                <button class="btn btn-pdf" onclick="window.open('${isometric.pdf_files.normal}', '_blank')">
                                    📄 Abrir PDF Normal
                                </button>
                            ` : '<span class="no-pdf">📄 PDF Normal no disponible</span>'}
                            ${isometric.pdf_files.prefab ? `
                                <button class="btn btn-pdf" onclick="window.open('${isometric.pdf_files.prefab}', '_blank')">
                                    🏗️ Abrir PDF Prefabricado
                                </button>
                            ` : '<span class="no-pdf">🏗️ PDF Prefabricado no disponible</span>'}
                        </div>
                    </div>

                    <div class="detail-section">
                        <h4>🔧 Soportes Asociados (${isometric.supports.length})</h4>
                        ${isometric.supports.length > 0 ? `
                            <div class="supports-table">
                                <table>
                                    <thead>
                                        <tr>
                                            <th>Número</th>
                                            <th>Posición</th>
                                            <th>CWA</th>
                                            <th>Revisión</th>
                                            <th>Código</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        ${isometric.supports.map(support => `
                                            <tr>
                                                <td>${support.support_number}</td>
                                                <td>${support.position_number}</td>
                                                <td>${support.cwa}</td>
                                                <td>${support.revision}</td>
                                                <td>${support.commodity_code}</td>
                                            </tr>
                                        `).join('')}
                                    </tbody>
                                </table>
                            </div>
                        ` : '<p class="no-supports">No hay soportes asociados a este isométrico</p>'}
                    </div>
                </div>
            </div>
        `;

        this.showModal(modalContent);
    }

    updateStats() {
        const statsContainer = document.getElementById('isometric-stats');
        if (!statsContainer) return;

        const filteredCount = Object.keys(this.filteredIsometrics).length;
        const totalCount = Object.keys(this.isometrics).length;
        const withSupports = Object.values(this.filteredIsometrics).filter(iso => iso.supports.length > 0).length;
        const withPdfs = Object.values(this.filteredIsometrics).filter(iso => iso.pdf_files.normal || iso.pdf_files.prefab).length;

        statsContainer.innerHTML = `
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">${filteredCount}</div>
                    <div class="stat-label">Isométricos Mostrados</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${totalCount}</div>
                    <div class="stat-label">Total Isométricos</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${withSupports}</div>
                    <div class="stat-label">Con Soportes</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${withPdfs}</div>
                    <div class="stat-label">Con PDFs</div>
                </div>
            </div>
        `;
    }

    exportToCSV() {
        const data = Object.values(this.filteredIsometrics);
        const csvContent = this.generateCSV(data);
        this.downloadCSV(csvContent, 'isometricos_sines.csv');
    }

    generateCSV(data) {
        const headers = ['Línea', 'Hoja', 'Fluido', 'CWA', 'Unidad', 'Revisión', 'Soportes', 'PDF Normal', 'PDF Prefab'];
        const rows = data.map(iso => [
            iso.line,
            iso.sheet,
            iso.fluid || '',
            iso.cwa || '',
            iso.unit || '',
            iso.revision || '',
            iso.supports.length,
            iso.pdf_files.normal ? 'Sí' : 'No',
            iso.pdf_files.prefab ? 'Sí' : 'No'
        ]);

        return [headers, ...rows].map(row => row.join(',')).join('\n');
    }

    downloadCSV(content, filename) {
        const blob = new Blob([content], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = filename;
        link.click();
    }

    showModal(content) {
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                ${content}
            </div>
        `;
        document.body.appendChild(modal);
        
        // Cerrar modal al hacer clic fuera
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });
    }

    showLoading(show) {
        const loader = document.getElementById('loading');
        if (loader) {
            loader.style.display = show ? 'block' : 'none';
        }
    }

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        document.body.appendChild(errorDiv);
        
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }

    toggleView() {
        // Implementar alternancia entre vista de cards y vista de tabla
        console.log('🔄 Alternando vista...');
    }
}

// Inicializar el gestor cuando se carga la página
let isometricManager;
document.addEventListener('DOMContentLoaded', () => {
    isometricManager = new IsometricManager();
}); 