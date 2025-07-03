// Sistema de Gestión de Instalaciones SINES
// Maneja fechas de instalación y estados de soportes

class InstallationManager {
    constructor() {
        this.installations = new Map();
        this.loadFromStorage();
    }

    // Cargar datos desde localStorage
    loadFromStorage() {
        try {
            const stored = localStorage.getItem('sines_installations');
            if (stored) {
                const data = JSON.parse(stored);
                this.installations = new Map(Object.entries(data));
                console.log(`📅 Cargadas ${this.installations.size} instalaciones desde almacenamiento local`);
            }
        } catch (error) {
            console.error('Error cargando instalaciones:', error);
            this.installations = new Map();
        }
    }

    // Guardar datos en localStorage
    saveToStorage() {
        try {
            const data = Object.fromEntries(this.installations);
            localStorage.setItem('sines_installations', JSON.stringify(data));
            console.log('💾 Instalaciones guardadas en almacenamiento local');
        } catch (error) {
            console.error('Error guardando instalaciones:', error);
        }
    }

    // Crear clave única para identificar un soporte
    getSupportKey(support) {
        return `${support.support_number}_${support.support_type}_${support.position_number || '1'}`;
    }

    // Obtener información de instalación de un soporte
    getInstallationInfo(support) {
        const key = this.getSupportKey(support);
        const info = this.installations.get(key);
        
        if (info) {
            return {
                ...info,
                planned_date: info.planned_date ? new Date(info.planned_date) : null,
                actual_date: info.actual_date ? new Date(info.actual_date) : null
            };
        }
        
        return {
            status: 'pending',
            planned_date: null,
            actual_date: null,
            notes: '',
            installed_by: ''
        };
    }

    // Actualizar información de instalación
    updateInstallation(support, installationData) {
        const key = this.getSupportKey(support);
        
        const currentInfo = this.getInstallationInfo(support);
        const updatedInfo = {
            ...currentInfo,
            ...installationData,
            last_updated: new Date().toISOString()
        };

        this.installations.set(key, updatedInfo);
        this.saveToStorage();
        
        console.log(`📅 Actualizada instalación para soporte ${support.support_number}-${support.support_type}`);
        
        // Disparar evento personalizado para actualizar UI
        window.dispatchEvent(new CustomEvent('installationUpdated', {
            detail: { support, installationInfo: updatedInfo }
        }));
        
        return updatedInfo;
    }

    // Marcar como instalado
    markAsInstalled(support, installedBy = '', notes = '') {
        return this.updateInstallation(support, {
            status: 'installed',
            actual_date: new Date().toISOString(),
            installed_by: installedBy,
            notes: notes
        });
    }

    // Marcar como en proceso
    markAsInProgress(support, notes = '') {
        return this.updateInstallation(support, {
            status: 'in_progress',
            notes: notes
        });
    }

    // Planificar instalación
    planInstallation(support, plannedDate, notes = '') {
        return this.updateInstallation(support, {
            status: 'planned',
            planned_date: new Date(plannedDate).toISOString(),
            notes: notes
        });
    }

    // Obtener estadísticas de instalaciones
    getStatistics() {
        const stats = {
            total: 0,
            pending: 0,
            planned: 0,
            in_progress: 0,
            installed: 0,
            overdue: 0
        };

        const now = new Date();
        
        this.installations.forEach(info => {
            stats.total++;
            stats[info.status]++;
            
            // Verificar si está atrasado
            if (info.status !== 'installed' && info.planned_date) {
                const plannedDate = new Date(info.planned_date);
                if (plannedDate < now) {
                    stats.overdue++;
                }
            }
        });

        return stats;
    }

    // Obtener soportes por estado
    getSupportsByStatus(status) {
        const supports = [];
        this.installations.forEach((info, key) => {
            if (info.status === status) {
                supports.push({
                    key,
                    info,
                    support_number: key.split('_')[0],
                    support_type: key.split('_')[1],
                    position_number: key.split('_')[2]
                });
            }
        });
        return supports;
    }

    // Obtener soportes instalados en un rango de fechas
    getInstallationsInDateRange(startDate, endDate) {
        const installations = [];
        const start = new Date(startDate);
        const end = new Date(endDate);
        
        this.installations.forEach((info, key) => {
            if (info.actual_date) {
                const installDate = new Date(info.actual_date);
                if (installDate >= start && installDate <= end) {
                    installations.push({
                        key,
                        info,
                        support_number: key.split('_')[0],
                        support_type: key.split('_')[1],
                        position_number: key.split('_')[2]
                    });
                }
            }
        });
        
        return installations.sort((a, b) => 
            new Date(a.info.actual_date) - new Date(b.info.actual_date)
        );
    }

    // Exportar datos de instalaciones
    exportData() {
        const data = [];
        this.installations.forEach((info, key) => {
            const [support_number, support_type, position_number] = key.split('_');
            data.push({
                support_number,
                support_type,
                position_number,
                status: info.status,
                planned_date: info.planned_date,
                actual_date: info.actual_date,
                installed_by: info.installed_by || '',
                notes: info.notes || '',
                last_updated: info.last_updated
            });
        });
        
        return data;
    }

    // Importar datos de instalaciones
    importData(data) {
        try {
            this.installations.clear();
            
            data.forEach(item => {
                const key = `${item.support_number}_${item.support_type}_${item.position_number || '1'}`;
                this.installations.set(key, {
                    status: item.status || 'pending',
                    planned_date: item.planned_date,
                    actual_date: item.actual_date,
                    installed_by: item.installed_by || '',
                    notes: item.notes || '',
                    last_updated: item.last_updated || new Date().toISOString()
                });
            });
            
            this.saveToStorage();
            console.log(`📥 Importadas ${data.length} instalaciones`);
            
            // Disparar evento para actualizar UI
            window.dispatchEvent(new CustomEvent('installationsImported'));
            
            return true;
        } catch (error) {
            console.error('Error importando instalaciones:', error);
            return false;
        }
    }

    // Limpiar todas las instalaciones
    clearAll() {
        this.installations.clear();
        this.saveToStorage();
        console.log('🗑️ Todas las instalaciones han sido eliminadas');
        
        window.dispatchEvent(new CustomEvent('installationsCleared'));
    }

    // Obtener código de color para el estado
    getStatusColor(status) {
        const colors = {
            'pending': '#ffc107',      // Amarillo
            'planned': '#17a2b8',      // Azul claro
            'in_progress': '#fd7e14',  // Naranja
            'installed': '#28a745',    // Verde
            'cancelled': '#6c757d'     // Gris
        };
        return colors[status] || '#6c757d';
    }

    // Obtener texto descriptivo para el estado
    getStatusText(status) {
        const texts = {
            'pending': 'Pendiente',
            'planned': 'Planificado',
            'in_progress': 'En Proceso',
            'installed': 'Instalado',
            'cancelled': 'Cancelado'
        };
        return texts[status] || 'Desconocido';
    }

    // Obtener icono para el estado
    getStatusIcon(status) {
        const icons = {
            'pending': 'fas fa-clock',
            'planned': 'fas fa-calendar-alt',
            'in_progress': 'fas fa-cogs',
            'installed': 'fas fa-check-circle',
            'cancelled': 'fas fa-times-circle'
        };
        return icons[status] || 'fas fa-question-circle';
    }
}

// Crear instancia global
if (typeof window !== 'undefined') {
    window.installationManager = new InstallationManager();
    console.log('📅 Sistema de gestión de instalaciones inicializado');
}

// Funciones de utilidad para formateo de fechas
function formatDate(date) {
    if (!date) return 'No definida';
    
    const d = new Date(date);
    if (isNaN(d.getTime())) return 'Fecha inválida';
    
    return d.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    });
}

function formatDateTime(date) {
    if (!date) return 'No definida';
    
    const d = new Date(date);
    if (isNaN(d.getTime())) return 'Fecha inválida';
    
    return d.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function isOverdue(plannedDate, status) {
    if (status === 'installed' || !plannedDate) return false;
    
    const planned = new Date(plannedDate);
    const now = new Date();
    
    return planned < now;
}

// Exportar funciones si estamos en un entorno de módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        InstallationManager,
        formatDate,
        formatDateTime,
        isOverdue
    };
} 