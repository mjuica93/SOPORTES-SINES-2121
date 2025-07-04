// Sistema de Gestión de Isométricos y Costuras SINES
// Gestor principal de funcionalidades

class IsometricWeldingManager {
    constructor() {
        this.data = null;
        this.filteredData = null;
        this.currentTab = 'isometrics';
        this.currentWeldingTab = 'info';
        this.traceabilityData = JSON.parse(localStorage.getItem('traceabilityData') || '{}');
        this.init();
    }

    async init() {
        try {
            console.log('🔄 Iniciando sistema de costuras...');
            await this.loadData();
            this.setupEventListeners();
            this.updateStatistics();
            this.displayIsometrics();
            console.log('✅ Sistema iniciado correctamente');
        } catch (error) {
            console.error('❌ Error al inicializar:', error);
            this.showError('Error al cargar los datos del sistema');
        }
    }

    async loadData() {
        try {
            const response = await fetch('isometric_data_with_welds.json');
            if (!response.ok) {
                throw new Error('No se pudo cargar el archivo de datos');
            }
            this.data = await response.json();
            this.filteredData = this.data;
            console.log('📊 Datos cargados:', this.data.summary);
        } catch (error) {
            console.error('Error cargando datos:', error);
            // Datos de ejemplo para desarrollo
            this.data = {
                isometrics: {},
                summary: {
                    total_isometrics: 0,
                    total_welds: 0,
                    completed_welds: 0,
                    pending_welds: 0
                }
            };
            this.filteredData = this.data;
        }
    }

    setupEventListeners() {
        // Filtros y búsqueda
        document.getElementById('searchInput').addEventListener('input', () => this.applyFilters());
        document.getElementById('lineFilter').addEventListener('change', () => this.applyFilters());
        document.getElementById('statusFilter').addEventListener('change', () => this.applyFilters());
        document.getElementById('weldTypeFilter').addEventListener('change', () => this.applyFilters());
        
        // Formularios
        document.getElementById('weldSearch').addEventListener('input', () => this.searchWelds());
        document.getElementById('weldIsometric').addEventListener('input', () => this.searchWelds());
        document.getElementById('weldStatus').addEventListener('change', () => this.searchWelds());

        // Cerrar modal con Escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeModal();
            }
        });

        // Clicks fuera del modal
        document.getElementById('detailModal').addEventListener('click', (e) => {
            if (e.target.id === 'detailModal') {
                this.closeModal();
            }
        });
    }

    showTab(tabName) {
        // Ocultar todas las pestañas
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.classList.remove('active');
        });

        // Mostrar pestaña seleccionada
        document.getElementById(tabName).classList.add('active');
        event.target.classList.add('active');
        
        this.currentTab = tabName;

        // Cargar contenido específico
        if (tabName === 'statistics') {
            this.loadStatistics();
        } else if (tabName === 'traceability') {
            this.loadTraceabilityHistory();
        }
    }

    showWeldingTab(tabName) {
        // Ocultar todas las pestañas de soldadura
        document.querySelectorAll('.welding-content').forEach(content => {
            content.classList.remove('active');
        });
        document.querySelectorAll('.welding-tab').forEach(tab => {
            tab.classList.remove('active');
        });

        // Mostrar pestaña seleccionada
        document.getElementById(`welding${tabName.charAt(0).toUpperCase() + tabName.slice(1)}`).classList.add('active');
        event.target.classList.add('active');
        
        this.currentWeldingTab = tabName;
    }

    updateStatistics() {
        const stats = this.calculateStatistics();
        
        // Actualizar contadores principales
        document.getElementById('totalIsometrics').textContent = stats.totalIsometrics;
        document.getElementById('isometricsWithWelds').textContent = stats.isometricsWithWelds;
        document.getElementById('totalWelds').textContent = stats.totalWelds;
        document.getElementById('completedWelds').textContent = stats.completedWelds;

        // Actualizar contadores de estadísticas
        document.getElementById('statTotalWelds').textContent = stats.totalWelds;
        document.getElementById('statPrefabWelds').textContent = stats.prefabWelds;
        document.getElementById('statFieldWelds').textContent = stats.fieldWelds;
        document.getElementById('statPendingWelds').textContent = stats.pendingWelds;

        // Actualizar filtros
        this.updateFilters();
    }

    calculateStatistics() {
        const isometrics = Object.values(this.data.isometrics || {});
        
        const stats = {
            totalIsometrics: isometrics.length,
            isometricsWithWelds: 0,
            totalWelds: 0,
            completedWelds: 0,
            pendingWelds: 0,
            prefabWelds: 0,
            fieldWelds: 0
        };

        isometrics.forEach(iso => {
            const weldStats = iso.weld_statistics || {};
            if (weldStats.total_welds > 0) {
                stats.isometricsWithWelds++;
            }
            stats.totalWelds += weldStats.total_welds || 0;
            stats.completedWelds += weldStats.completed_welds || 0;
            stats.pendingWelds += weldStats.pending_welds || 0;
            stats.prefabWelds += weldStats.prefab_welds || 0;
            stats.fieldWelds += weldStats.field_welds || 0;
        });

        return stats;
    }

    updateFilters() {
        const lineFilter = document.getElementById('lineFilter');
        const lines = new Set();
        
        Object.values(this.data.isometrics || {}).forEach(iso => {
            if (iso.line) {
                lines.add(iso.line);
            }
        });
        
        lineFilter.innerHTML = '<option value="">Todas las líneas</option>';
        Array.from(lines).sort().forEach(line => {
            lineFilter.innerHTML += `<option value="${line}">${line}</option>`;
        });
    }

    applyFilters() {
        const searchTerm = document.getElementById('searchInput').value.toLowerCase();
        const lineFilter = document.getElementById('lineFilter').value;
        const statusFilter = document.getElementById('statusFilter').value;
        const weldTypeFilter = document.getElementById('weldTypeFilter').value;

        const filtered = {};
        
        Object.entries(this.data.isometrics || {}).forEach(([key, iso]) => {
            let matches = true;

            // Filtro de búsqueda
            if (searchTerm && !key.toLowerCase().includes(searchTerm)) {
                matches = false;
            }

            // Filtro de línea
            if (lineFilter && iso.line !== lineFilter) {
                matches = false;
            }

            // Filtro de estado de costuras
            if (statusFilter) {
                const weldStats = iso.weld_statistics || {};
                if (statusFilter === 'completed' && weldStats.completed_welds === 0) {
                    matches = false;
                }
                if (statusFilter === 'pending' && weldStats.pending_welds === 0) {
                    matches = false;
                }
            }

            // Filtro de tipo de soldadura
            if (weldTypeFilter) {
                const weldStats = iso.weld_statistics || {};
                if (weldTypeFilter === 'prefabricada' && weldStats.prefab_welds === 0) {
                    matches = false;
                }
                if (weldTypeFilter === 'campo' && weldStats.field_welds === 0) {
                    matches = false;
                }
            }

            if (matches) {
                filtered[key] = iso;
            }
        });

        this.filteredData = { ...this.data, isometrics: filtered };
        this.displayIsometrics();
    }

    displayIsometrics() {
        const grid = document.getElementById('isometricsGrid');
        const isometrics = Object.entries(this.filteredData.isometrics || {});

        if (isometrics.length === 0) {
            grid.innerHTML = `
                <div class="empty-state">
                    <i>🔍</i>
                    <h3>No se encontraron isométricos</h3>
                    <p>Intenta ajustar los filtros de búsqueda</p>
                </div>
            `;
            return;
        }

        grid.innerHTML = isometrics.map(([key, iso]) => {
            const weldStats = iso.weld_statistics || {};
            const completionPercentage = weldStats.completion_percentage || 0;
            
            return `
                <div class="iso-card">
                    <div class="iso-card-header">
                        <h3>${key}</h3>
                        <p>${iso.fluid || 'Sin fluido'} • ${iso.cwa || 'Sin CWA'}</p>
                    </div>
                    <div class="iso-card-body">
                        <div class="badges">
                            ${iso.has_normal_pdf ? '<span class="badge badge-pdf">PDF Normal</span>' : ''}
                            ${iso.has_prefab_pdf ? '<span class="badge badge-prefab">PDF Prefab</span>' : ''}
                            ${weldStats.total_welds > 0 ? `<span class="badge badge-welds">${weldStats.total_welds} Costuras</span>` : ''}
                        </div>
                        
                        ${weldStats.total_welds > 0 ? `
                            <div class="weld-stats">
                                <div class="weld-stat">
                                    <div class="number">${weldStats.completed_welds || 0}</div>
                                    <div class="label">Completadas</div>
                                </div>
                                <div class="weld-stat">
                                    <div class="number">${weldStats.pending_welds || 0}</div>
                                    <div class="label">Pendientes</div>
                                </div>
                                <div class="weld-stat">
                                    <div class="number">${weldStats.prefab_welds || 0}</div>
                                    <div class="label">Prefabricadas</div>
                                </div>
                                <div class="weld-stat">
                                    <div class="number">${weldStats.field_welds || 0}</div>
                                    <div class="label">Campo</div>
                                </div>
                            </div>
                            
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: ${completionPercentage}%"></div>
                            </div>
                            <p style="text-align: center; margin-bottom: 15px;">
                                ${completionPercentage}% Completado
                            </p>
                        ` : ''}
                        
                        <div class="card-actions">
                            <button class="btn btn-primary" onclick="weldingManager.showDetails('${key}')">
                                📋 Ver Detalles
                            </button>
                            ${iso.has_normal_pdf ? `<button class="btn btn-success" onclick="weldingManager.openPDF('${iso.normal_pdf_path}')">PDF Normal</button>` : ''}
                            ${iso.has_prefab_pdf ? `<button class="btn btn-warning" onclick="weldingManager.openPDF('${iso.prefab_pdf_path}')">PDF Prefab</button>` : ''}
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    }

    showDetails(isoKey) {
        const iso = this.data.isometrics[isoKey];
        if (!iso) return;

        document.getElementById('modalTitle').textContent = `Detalles: ${isoKey}`;
        
        // Mostrar información general
        const modalContent = document.getElementById('modalContent');
        modalContent.innerHTML = `
            <div class="form-grid">
                <div class="form-group">
                    <label>Isométrico</label>
                    <input type="text" value="${isoKey}" readonly>
                </div>
                <div class="form-group">
                    <label>Línea</label>
                    <input type="text" value="${iso.line || 'N/A'}" readonly>
                </div>
                <div class="form-group">
                    <label>Hoja</label>
                    <input type="text" value="${iso.sheet || 'N/A'}" readonly>
                </div>
                <div class="form-group">
                    <label>Fluido</label>
                    <input type="text" value="${iso.fluid || 'N/A'}" readonly>
                </div>
                <div class="form-group">
                    <label>CWA</label>
                    <input type="text" value="${iso.cwa || 'N/A'}" readonly>
                </div>
                <div class="form-group">
                    <label>Estado</label>
                    <input type="text" value="${iso.status || 'N/A'}" readonly>
                </div>
            </div>
            
            <h4>📊 Estadísticas de Soldadura</h4>
            <div class="weld-stats" style="grid-template-columns: repeat(4, 1fr); margin-top: 15px;">
                <div class="weld-stat">
                    <div class="number">${iso.weld_statistics?.total_welds || 0}</div>
                    <div class="label">Total</div>
                </div>
                <div class="weld-stat">
                    <div class="number">${iso.weld_statistics?.completed_welds || 0}</div>
                    <div class="label">Completadas</div>
                </div>
                <div class="weld-stat">
                    <div class="number">${iso.weld_statistics?.pending_welds || 0}</div>
                    <div class="label">Pendientes</div>
                </div>
                <div class="weld-stat">
                    <div class="number">${iso.weld_statistics?.completion_percentage || 0}%</div>
                    <div class="label">Progreso</div>
                </div>
            </div>
        `;

        // Mostrar costuras
        this.displayWeldsInModal(iso.welds || []);

        // Mostrar soportes
        this.displaySupportsInModal(iso.supports || []);

        // Mostrar modal
        document.getElementById('detailModal').style.display = 'block';
    }

    displayWeldsInModal(welds) {
        const modalWelds = document.getElementById('modalWelds');
        
        if (welds.length === 0) {
            modalWelds.innerHTML = `
                <div class="empty-state">
                    <i>🔨</i>
                    <h3>No hay costuras registradas</h3>
                    <p>Este isométrico no tiene costuras asociadas</p>
                </div>
            `;
            return;
        }

        modalWelds.innerHTML = `
            <h4>🔨 Costuras de Soldadura (${welds.length})</h4>
            <div class="welds-table-container">
                <table class="welds-table">
                    <thead>
                        <tr>
                            <th>Número</th>
                            <th>Tipo</th>
                            <th>Estado</th>
                            <th>Fecha</th>
                            <th>Soldador</th>
                            <th>WPS</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${welds.map(weld => `
                            <tr>
                                <td><strong>${weld.weld_number}</strong></td>
                                <td>
                                    <span class="badge ${weld.type === 'prefabricada' ? 'badge-prefab' : 'badge-pdf'}">
                                        ${weld.type === 'prefabricada' ? 'Shop' : 'Field'}
                                    </span>
                                </td>
                                <td>
                                    <span class="badge ${weld.status === 'completada' ? 'badge-completed' : 'badge-pending'}">
                                        ${weld.status === 'completada' ? 'Completada' : 'Pendiente'}
                                    </span>
                                </td>
                                <td>${weld.weld_date ? new Date(weld.weld_date).toLocaleDateString() : 'N/A'}</td>
                                <td>${weld.welder || weld.pipe_fitter || 'N/A'}</td>
                                <td>${weld.wps || 'N/A'}</td>
                                <td>
                                    <button class="btn btn-primary" onclick="weldingManager.editWeld('${weld.isometric}', '${weld.weld_number}')">
                                        ✏️ Editar
                                    </button>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    }

    displaySupportsInModal(supports) {
        const modalSupports = document.getElementById('modalSupports');
        
        if (supports.length === 0) {
            modalSupports.innerHTML = `
                <div class="empty-state">
                    <i>🔧</i>
                    <h3>No hay soportes registrados</h3>
                    <p>Este isométrico no tiene soportes asociados</p>
                </div>
            `;
            return;
        }

        modalSupports.innerHTML = `
            <h4>🔧 Soportes Asociados (${supports.length})</h4>
            <div class="welds-table-container">
                <table class="welds-table">
                    <thead>
                        <tr>
                            <th>Código</th>
                            <th>Tipo</th>
                            <th>Estado</th>
                            <th>Instalación</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${supports.map(support => `
                            <tr>
                                <td><strong>${support.support_code || 'N/A'}</strong></td>
                                <td>${support.support_type || 'N/A'}</td>
                                <td>
                                    <span class="badge ${support.installation_status === 'installed' ? 'badge-completed' : 'badge-pending'}">
                                        ${support.installation_status === 'installed' ? 'Instalado' : 'Pendiente'}
                                    </span>
                                </td>
                                <td>${support.installation_date ? new Date(support.installation_date).toLocaleDateString() : 'N/A'}</td>
                                <td>
                                    <button class="btn btn-primary" onclick="weldingManager.viewSupport('${support.support_code}')">
                                        👁️ Ver
                                    </button>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    }

    editWeld(isometric, weldNumber) {
        // Cambiar a la pestaña de trazabilidad
        this.showTab('traceability');
        
        // Rellenar el formulario
        document.getElementById('traceIsometric').value = isometric;
        document.getElementById('traceWeldNumber').value = weldNumber;
        
        // Buscar la costura para rellenar más datos
        const iso = this.data.isometrics[isometric];
        if (iso && iso.welds) {
            const weld = iso.welds.find(w => w.weld_number === weldNumber);
            if (weld) {
                document.getElementById('traceStatus').value = weld.status;
                if (weld.weld_date) {
                    document.getElementById('traceWeldDate').value = new Date(weld.weld_date).toISOString().split('T')[0];
                }
                document.getElementById('traceWelder').value = weld.welder || weld.pipe_fitter || '';
                document.getElementById('traceWPS').value = weld.wps || '';
            }
        }
        
        this.closeModal();
    }

    searchWelds() {
        const weldSearch = document.getElementById('weldSearch').value.toLowerCase();
        const weldIsometric = document.getElementById('weldIsometric').value.toLowerCase();
        const weldStatus = document.getElementById('weldStatus').value;

        const results = [];
        
        Object.entries(this.data.isometrics || {}).forEach(([isoKey, iso]) => {
            if (iso.welds) {
                iso.welds.forEach(weld => {
                    let matches = true;
                    
                    if (weldSearch && !weld.weld_number.toLowerCase().includes(weldSearch)) {
                        matches = false;
                    }
                    
                    if (weldIsometric && !isoKey.toLowerCase().includes(weldIsometric)) {
                        matches = false;
                    }
                    
                    if (weldStatus && weld.status !== weldStatus) {
                        matches = false;
                    }
                    
                    if (matches) {
                        results.push({ isoKey, ...weld });
                    }
                });
            }
        });

        this.displayWeldResults(results);
    }

    displayWeldResults(results) {
        const weldResults = document.getElementById('weldResults');
        
        if (results.length === 0) {
            weldResults.innerHTML = `
                <div class="empty-state">
                    <i>🔍</i>
                    <h3>No se encontraron costuras</h3>
                    <p>Intenta ajustar los criterios de búsqueda</p>
                </div>
            `;
            return;
        }

        weldResults.innerHTML = `
            <h4>🔍 Resultados de Búsqueda (${results.length} costuras)</h4>
            <div class="welds-table-container">
                <table class="welds-table">
                    <thead>
                        <tr>
                            <th>Isométrico</th>
                            <th>Costura</th>
                            <th>Tipo</th>
                            <th>Estado</th>
                            <th>Fecha</th>
                            <th>Soldador</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${results.map(weld => `
                            <tr>
                                <td><strong>${weld.isoKey}</strong></td>
                                <td>${weld.weld_number}</td>
                                <td>
                                    <span class="badge ${weld.type === 'prefabricada' ? 'badge-prefab' : 'badge-pdf'}">
                                        ${weld.type === 'prefabricada' ? 'Shop' : 'Field'}
                                    </span>
                                </td>
                                <td>
                                    <span class="badge ${weld.status === 'completada' ? 'badge-completed' : 'badge-pending'}">
                                        ${weld.status === 'completada' ? 'Completada' : 'Pendiente'}
                                    </span>
                                </td>
                                <td>${weld.weld_date ? new Date(weld.weld_date).toLocaleDateString() : 'N/A'}</td>
                                <td>${weld.welder || weld.pipe_fitter || 'N/A'}</td>
                                <td>
                                    <button class="btn btn-primary" onclick="weldingManager.editWeld('${weld.isoKey}', '${weld.weld_number}')">
                                        ✏️ Editar
                                    </button>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    }

    updateWeldTraceability() {
        const isometric = document.getElementById('traceIsometric').value;
        const weldNumber = document.getElementById('traceWeldNumber').value;
        const status = document.getElementById('traceStatus').value;
        const weldDate = document.getElementById('traceWeldDate').value;
        const welder = document.getElementById('traceWelder').value;
        const inspector = document.getElementById('traceInspector').value;
        const wps = document.getElementById('traceWPS').value;
        const notes = document.getElementById('traceNotes').value;

        if (!isometric || !weldNumber) {
            alert('Por favor, complete al menos el isométrico y número de costura');
            return;
        }

        const traceKey = `${isometric}_${weldNumber}`;
        this.traceabilityData[traceKey] = {
            isometric,
            weldNumber,
            status,
            weldDate,
            welder,
            inspector,
            wps,
            notes,
            updatedAt: new Date().toISOString(),
            updatedBy: 'Usuario' // En un sistema real, esto vendría de la sesión
        };

        // Guardar en localStorage
        localStorage.setItem('traceabilityData', JSON.stringify(this.traceabilityData));

        // Limpiar formulario
        document.getElementById('traceIsometric').value = '';
        document.getElementById('traceWeldNumber').value = '';
        document.getElementById('traceStatus').value = 'pendiente';
        document.getElementById('traceWeldDate').value = '';
        document.getElementById('traceWelder').value = '';
        document.getElementById('traceInspector').value = '';
        document.getElementById('traceWPS').value = '';
        document.getElementById('traceNotes').value = '';

        // Actualizar vista
        this.loadTraceabilityHistory();
        this.updateStatistics();
        this.displayIsometrics();

        alert('Trazabilidad actualizada correctamente');
    }

    loadTraceabilityHistory() {
        const traceabilityHistory = document.getElementById('traceabilityHistory');
        const entries = Object.values(this.traceabilityData);

        if (entries.length === 0) {
            traceabilityHistory.innerHTML = `
                <div class="empty-state">
                    <i>📋</i>
                    <h3>No hay registros de trazabilidad</h3>
                    <p>Use el formulario arriba para agregar registros de trazabilidad</p>
                </div>
            `;
            return;
        }

        traceabilityHistory.innerHTML = `
            <h4>📋 Historial de Trazabilidad (${entries.length} registros)</h4>
            <div class="welds-table-container">
                <table class="welds-table">
                    <thead>
                        <tr>
                            <th>Isométrico</th>
                            <th>Costura</th>
                            <th>Estado</th>
                            <th>Fecha Soldadura</th>
                            <th>Soldador</th>
                            <th>Inspector</th>
                            <th>Actualizado</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${entries.map(entry => `
                            <tr>
                                <td><strong>${entry.isometric}</strong></td>
                                <td>${entry.weldNumber}</td>
                                <td>
                                    <span class="badge ${entry.status === 'completada' ? 'badge-completed' : 'badge-pending'}">
                                        ${entry.status === 'completada' ? 'Completada' : 'Pendiente'}
                                    </span>
                                </td>
                                <td>${entry.weldDate ? new Date(entry.weldDate).toLocaleDateString() : 'N/A'}</td>
                                <td>${entry.welder || 'N/A'}</td>
                                <td>${entry.inspector || 'N/A'}</td>
                                <td>${new Date(entry.updatedAt).toLocaleDateString()}</td>
                                <td>
                                    <button class="btn btn-primary" onclick="weldingManager.editTraceabilityEntry('${entry.isometric}', '${entry.weldNumber}')">
                                        ✏️ Editar
                                    </button>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    }

    editTraceabilityEntry(isometric, weldNumber) {
        const traceKey = `${isometric}_${weldNumber}`;
        const entry = this.traceabilityData[traceKey];
        
        if (entry) {
            document.getElementById('traceIsometric').value = entry.isometric;
            document.getElementById('traceWeldNumber').value = entry.weldNumber;
            document.getElementById('traceStatus').value = entry.status;
            document.getElementById('traceWeldDate').value = entry.weldDate || '';
            document.getElementById('traceWelder').value = entry.welder || '';
            document.getElementById('traceInspector').value = entry.inspector || '';
            document.getElementById('traceWPS').value = entry.wps || '';
            document.getElementById('traceNotes').value = entry.notes || '';
        }
    }

    exportTraceability() {
        const entries = Object.values(this.traceabilityData);
        
        if (entries.length === 0) {
            alert('No hay datos de trazabilidad para exportar');
            return;
        }

        const csv = this.convertToCSV(entries, [
            'isometric', 'weldNumber', 'status', 'weldDate', 'welder', 
            'inspector', 'wps', 'notes', 'updatedAt', 'updatedBy'
        ]);

        const filename = `trazabilidad_costuras_${new Date().toISOString().split('T')[0]}.csv`;
        this.downloadCSV(csv, filename);
    }

    loadStatistics() {
        const stats = this.calculateStatistics();
        const statisticsCharts = document.getElementById('statisticsCharts');
        
        statisticsCharts.innerHTML = `
            <div class="weld-form">
                <h4>📊 Análisis Detallado</h4>
                <div class="form-grid">
                    <div class="form-group">
                        <label>Porcentaje de Completitud</label>
                        <div class="progress-bar" style="height: 20px; margin-top: 5px;">
                            <div class="progress-fill" style="width: ${((stats.completedWelds / stats.totalWelds) * 100).toFixed(1)}%"></div>
                        </div>
                        <p style="margin-top: 5px;">${((stats.completedWelds / stats.totalWelds) * 100).toFixed(1)}% completado</p>
                    </div>
                    <div class="form-group">
                        <label>Distribución por Tipo</label>
                        <p>Prefabricadas: ${stats.prefabWelds} (${((stats.prefabWelds / stats.totalWelds) * 100).toFixed(1)}%)</p>
                        <p>Campo: ${stats.fieldWelds} (${((stats.fieldWelds / stats.totalWelds) * 100).toFixed(1)}%)</p>
                    </div>
                    <div class="form-group">
                        <label>Isométricos</label>
                        <p>Con costuras: ${stats.isometricsWithWelds} de ${stats.totalIsometrics}</p>
                        <p>Cobertura: ${((stats.isometricsWithWelds / stats.totalIsometrics) * 100).toFixed(1)}%</p>
                    </div>
                </div>
            </div>
        `;
    }

    clearFilters() {
        document.getElementById('searchInput').value = '';
        document.getElementById('lineFilter').value = '';
        document.getElementById('statusFilter').value = '';
        document.getElementById('weldTypeFilter').value = '';
        this.applyFilters();
    }

    openPDF(pdfPath) {
        if (pdfPath) {
            window.open(pdfPath, '_blank');
        } else {
            alert('PDF no disponible');
        }
    }

    closeModal() {
        document.getElementById('detailModal').style.display = 'none';
    }

    viewSupport(supportCode) {
        alert(`Ver soporte: ${supportCode}\n\nEsta funcionalidad se integrará con el sistema de soportes existente.`);
    }

    convertToCSV(data, headers) {
        const csvHeaders = headers.join(',');
        const csvRows = data.map(row => {
            return headers.map(header => {
                const value = row[header] || '';
                return `"${value.toString().replace(/"/g, '""')}"`;
            }).join(',');
        });
        return [csvHeaders, ...csvRows].join('\n');
    }

    downloadCSV(csv, filename) {
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        
        if (link.download !== undefined) {
            const url = URL.createObjectURL(blob);
            link.setAttribute('href', url);
            link.setAttribute('download', filename);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }

    showError(message) {
        alert(`Error: ${message}`);
    }
}

// Funciones globales para compatibilidad
function showTab(tabName) {
    weldingManager.showTab(tabName);
}

function showWeldingTab(tabName) {
    weldingManager.showWeldingTab(tabName);
}

function clearFilters() {
    weldingManager.clearFilters();
}

function searchWelds() {
    weldingManager.searchWelds();
}

function updateWeldTraceability() {
    weldingManager.updateWeldTraceability();
}

function exportTraceability() {
    weldingManager.exportTraceability();
}

function closeModal() {
    weldingManager.closeModal();
}

// Inicializar cuando se carga la página
let weldingManager;
document.addEventListener('DOMContentLoaded', function() {
    weldingManager = new IsometricWeldingManager();
});
