/**
 * Sistema de Gestión de Estado de Costuras con Acceso a PDFs
 * Permite modificar el estado de las costuras y acceder a PDFs regulares y prefabricados
 */

class WeldingStatusManager {
    constructor() {
        this.weldingData = [];
        this.statusOptions = {};
        this.userRole = 'operador'; // Se establecerá desde el servidor
        this.changeHistory = [];
        this.isInitialized = false;
    }

    /**
     * Inicializa el sistema de gestión de soldadura
     */
    async initialize() {
        try {
            console.log('🔧 Inicializando sistema de gestión de soldadura...');
            
            // Cargar datos de soldadura
            const response = await fetch('welding_compact_data.json');
            const data = await response.json();
            
            this.weldingData = data.welding_data || [];
            this.statusOptions = data.status_options || {};
            
            // Obtener rol del usuario desde el servidor
            await this.getUserRole();
            
            console.log(`✅ Sistema inicializado: ${this.weldingData.length} registros cargados`);
            this.isInitialized = true;
            
            return true;
        } catch (error) {
            console.error('❌ Error al inicializar sistema:', error);
            return false;
        }
    }

    /**
     * Obtiene el rol del usuario actual
     */
    async getUserRole() {
        try {
            const response = await fetch('/api/user-info');
            const userInfo = await response.json();
            this.userRole = userInfo.role || 'operador';
        } catch (error) {
            console.warn('⚠️ No se pudo obtener el rol del usuario, usando rol por defecto');
            this.userRole = 'operador';
        }
    }

    /**
     * Verifica si el usuario tiene permisos para una acción
     */
    hasPermission(action) {
        const permissions = {
            'admin': ['view', 'edit', 'delete', 'export'],
            'supervisor': ['view', 'edit', 'export'],
            'operador': ['view', 'edit'],
            'sines': ['view']
        };
        
        return permissions[this.userRole]?.includes(action) || false;
    }

    /**
     * Abre el modal para modificar el estado de una costura
     */
    openStatusModal(weldId) {
        if (!this.hasPermission('edit')) {
            this.showNotification('No tienes permisos para modificar el estado', 'error');
            return;
        }

        const weld = this.weldingData.find(w => w.weld_id === weldId);
        if (!weld) {
            this.showNotification('Costura no encontrada', 'error');
            return;
        }

        this.createStatusModal(weld);
    }

    /**
     * Crea el modal de modificación de estado
     */
    createStatusModal(weld) {
        // Crear modal
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.id = 'statusModal';
        modal.setAttribute('tabindex', '-1');
        
        const statusOptionsHtml = Object.entries(this.statusOptions).map(([key, option]) => `
            <div class="form-check mb-2">
                <input class="form-check-input" type="radio" name="weldStatus" 
                       id="status_${key}" value="${key}" 
                       ${weld.status === key ? 'checked' : ''}>
                <label class="form-check-label d-flex align-items-center" for="status_${key}">
                    <span class="me-2" style="font-size: 1.2em;">${option.icon}</span>
                    <div>
                        <strong style="color: ${option.color};">${option.label}</strong>
                        <br>
                        <small class="text-muted">${option.description}</small>
                    </div>
                </label>
            </div>
        `).join('');

        modal.innerHTML = `
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header bg-primary text-white">
                        <h5 class="modal-title">
                            <i class="fas fa-edit me-2"></i>
                            Modificar Estado de Costura
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="row">
                            <div class="col-md-6">
                                <h6 class="text-primary mb-3">📋 Información de la Costura</h6>
                                <div class="card bg-light">
                                    <div class="card-body">
                                        <p><strong>Isométrico:</strong> ${weld.isometric}</p>
                                        <p><strong>Número:</strong> ${weld.weld_number || 'N/A'}</p>
                                        <p><strong>Diámetro:</strong> ${weld.diameter}"</p>
                                        <p><strong>Línea:</strong> ${weld.system_line || 'N/A'}</p>
                                        <p><strong>Fluido:</strong> ${weld.fluid || 'N/A'}</p>
                                        <p><strong>Progreso:</strong> ${weld.completion_percentage}%</p>
                                    </div>
                                </div>
                                
                                ${this.createPDFAccessSection(weld)}
                            </div>
                            <div class="col-md-6">
                                <h6 class="text-primary mb-3">⚙️ Cambiar Estado</h6>
                                <div class="status-options">
                                    ${statusOptionsHtml}
                                </div>
                                
                                <div class="mt-3">
                                    <label for="statusComment" class="form-label">
                                        <i class="fas fa-comment me-1"></i>
                                        Comentario (opcional)
                                    </label>
                                    <textarea class="form-control" id="statusComment" rows="3" 
                                              placeholder="Agregar comentario sobre el cambio..."></textarea>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                            <i class="fas fa-times me-1"></i>Cancelar
                        </button>
                        <button type="button" class="btn btn-primary" onclick="weldingStatusManager.saveStatusChange('${weld.weld_id}')">
                            <i class="fas fa-save me-1"></i>Guardar Cambios
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        
        // Mostrar modal
        const bootstrapModal = new bootstrap.Modal(modal);
        bootstrapModal.show();
        
        // Limpiar modal al cerrar
        modal.addEventListener('hidden.bs.modal', () => {
            document.body.removeChild(modal);
        });
    }

    /**
     * Crea la sección de acceso a PDFs
     */
    createPDFAccessSection(weld) {
        const pdfInfo = weld.pdf_info || {};
        let pdfSection = '<h6 class="text-primary mb-3 mt-4">📄 Acceso a PDFs</h6>';
        
        if (pdfInfo.has_normal || pdfInfo.has_prefab) {
            pdfSection += '<div class="d-grid gap-2">';
            
            if (pdfInfo.has_normal) {
                pdfSection += `
                    <button type="button" class="btn btn-outline-primary btn-sm" 
                            onclick="weldingStatusManager.openPDF('${pdfInfo.normal_path}', 'normal')">
                        <i class="fas fa-file-pdf me-1"></i>
                        PDF Regular: ${pdfInfo.normal_filename}
                    </button>
                `;
            }
            
            if (pdfInfo.has_prefab) {
                pdfSection += `
                    <button type="button" class="btn btn-outline-success btn-sm" 
                            onclick="weldingStatusManager.openPDF('${pdfInfo.prefab_path}', 'prefab')">
                        <i class="fas fa-file-pdf me-1"></i>
                        PDF Prefabricado: ${pdfInfo.prefab_filename}
                    </button>
                `;
            }
            
            pdfSection += '</div>';
        } else {
            pdfSection += '<p class="text-muted"><i class="fas fa-info-circle me-1"></i>No hay PDFs disponibles</p>';
        }
        
        return pdfSection;
    }

    /**
     * Abre un PDF en una nueva ventana
     */
    openPDF(pdfPath, type) {
        if (!pdfPath) {
            this.showNotification('Ruta del PDF no disponible', 'error');
            return;
        }

        const fullPath = pdfPath.startsWith('http') ? pdfPath : `/${pdfPath}`;
        
        try {
            window.open(fullPath, '_blank', 'width=1200,height=800,scrollbars=yes,resizable=yes');
            
            // Registrar acceso al PDF
            this.logPDFAccess(pdfPath, type);
            
        } catch (error) {
            console.error('Error al abrir PDF:', error);
            this.showNotification('Error al abrir el PDF', 'error');
        }
    }

    /**
     * Registra el acceso a un PDF
     */
    logPDFAccess(pdfPath, type) {
        const logEntry = {
            timestamp: new Date().toISOString(),
            action: 'pdf_access',
            pdf_path: pdfPath,
            pdf_type: type,
            user_role: this.userRole
        };
        
        // Enviar log al servidor (opcional)
        fetch('/api/log-pdf-access', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(logEntry)
        }).catch(error => {
            console.warn('No se pudo registrar el acceso al PDF:', error);
        });
    }

    /**
     * Guarda el cambio de estado de una costura
     */
    async saveStatusChange(weldId) {
        try {
            const modal = document.getElementById('statusModal');
            const selectedStatus = modal.querySelector('input[name="weldStatus"]:checked');
            const comment = modal.querySelector('#statusComment').value;
            
            if (!selectedStatus) {
                this.showNotification('Selecciona un estado', 'error');
                return;
            }

            const newStatus = selectedStatus.value;
            const weld = this.weldingData.find(w => w.weld_id === weldId);
            
            if (!weld) {
                this.showNotification('Costura no encontrada', 'error');
                return;
            }

            const oldStatus = weld.status;
            
            // Crear registro de cambio
            const changeRecord = {
                weld_id: weldId,
                old_status: oldStatus,
                new_status: newStatus,
                comment: comment,
                timestamp: new Date().toISOString(),
                user_role: this.userRole
            };

            // Actualizar estado local
            weld.status = newStatus;
            weld.last_modified = new Date().toISOString();
            
            // Agregar al historial
            this.changeHistory.push(changeRecord);
            
            // Enviar cambio al servidor
            await this.sendStatusChangeToServer(changeRecord);
            
            // Cerrar modal
            const bootstrapModal = bootstrap.Modal.getInstance(modal);
            bootstrapModal.hide();
            
            // Actualizar interfaz
            this.updateWeldingDisplay();
            
            this.showNotification(
                `Estado cambiado de "${this.statusOptions[oldStatus]?.label}" a "${this.statusOptions[newStatus]?.label}"`,
                'success'
            );
            
        } catch (error) {
            console.error('Error al guardar cambio:', error);
            this.showNotification('Error al guardar el cambio', 'error');
        }
    }

    /**
     * Envía el cambio de estado al servidor
     */
    async sendStatusChangeToServer(changeRecord) {
        try {
            const response = await fetch('/api/update-weld-status', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(changeRecord)
            });
            
            if (!response.ok) {
                throw new Error('Error del servidor');
            }
            
            return await response.json();
            
        } catch (error) {
            console.warn('No se pudo sincronizar con el servidor:', error);
            // Continuar con cambio local
        }
    }

    /**
     * Actualiza la visualización de soldadura
     */
    updateWeldingDisplay() {
        // Disparar evento personalizado para actualizar la interfaz
        const event = new CustomEvent('weldingStatusUpdated', {
            detail: {
                weldingData: this.weldingData,
                changeHistory: this.changeHistory
            }
        });
        
        document.dispatchEvent(event);
    }
    
    /**
     * Muestra una notificación
     */
    showNotification(message, type = 'info') {
        const alertClass = {
            'success': 'alert-success',
            'error': 'alert-danger',
            'warning': 'alert-warning',
            'info': 'alert-info'
        }[type] || 'alert-info';
        
        const alert = document.createElement('div');
        alert.className = `alert ${alertClass} alert-dismissible fade show position-fixed`;
        alert.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 400px;';
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alert);
        
        // Auto-remover después de 5 segundos
        setTimeout(() => {
            if (alert.parentNode) {
                alert.parentNode.removeChild(alert);
            }
        }, 5000);
    }

    /**
     * Obtiene estadísticas del sistema
     */
    getStatistics() {
        const stats = {
            total: this.weldingData.length,
            by_status: {},
            by_diameter: {},
            pdf_coverage: {
                normal: 0,
                prefab: 0
            }
        };
        
        this.weldingData.forEach(weld => {
            // Estadísticas por estado
            stats.by_status[weld.status] = (stats.by_status[weld.status] || 0) + 1;
            
            // Estadísticas por diámetro
            stats.by_diameter[weld.diameter] = (stats.by_diameter[weld.diameter] || 0) + 1;
            
            // Cobertura de PDFs
            if (weld.pdf_info?.has_normal) stats.pdf_coverage.normal++;
            if (weld.pdf_info?.has_prefab) stats.pdf_coverage.prefab++;
        });
        
        return stats;
    }
    
    /**
     * Exporta datos de soldadura
     */
    exportWeldingData(format = 'json') {
        if (!this.hasPermission('export')) {
            this.showNotification('No tienes permisos para exportar datos', 'error');
            return;
        }

        const timestamp = new Date().toISOString().split('T')[0];
        const filename = `soldadura_${timestamp}.${format}`;
        
        if (format === 'json') {
            const dataToExport = {
                metadata: {
                    exported: new Date().toISOString(),
                    user_role: this.userRole,
                    total_records: this.weldingData.length
                },
                welding_data: this.weldingData,
                change_history: this.changeHistory,
                statistics: this.getStatistics()
            };
            
            this.downloadFile(filename, JSON.stringify(dataToExport, null, 2), 'application/json');
        }
        
        this.showNotification(`Datos exportados como ${filename}`, 'success');
    }

    /**
     * Descarga un archivo
     */
    downloadFile(filename, content, mimeType) {
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
}

// Instancia global del gestor
const weldingStatusManager = new WeldingStatusManager();

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    weldingStatusManager.initialize();
});

// Exponer funciones globales para uso en HTML
window.weldingStatusManager = weldingStatusManager;
