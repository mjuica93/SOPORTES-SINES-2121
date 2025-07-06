/**
 * LOGOUT MANAGER - Sistema SINES
 * Maneja el cierre de sesión en todas las páginas del sistema
 */

class LogoutManager {
    constructor() {
        this.logoutButtonId = 'sines-logout-btn';
        this.sessionCheckInterval = 60000; // Verificar sesión cada minuto
        this.sessionTimer = null;
        this.init();
    }

    init() {
        // Verificar si estamos en el servidor seguro
        this.checkSecureServer();
        
        // Crear botón de logout si no existe
        this.createLogoutButton();
        
        // Iniciar verificación de sesión
        this.startSessionCheck();
        
        // Escuchar eventos de teclado para logout rápido
        this.setupKeyboardShortcuts();
    }

    checkSecureServer() {
        // Verificar si estamos en un servidor seguro (puerto 8000 con autenticación)
        const currentUrl = window.location.href;
        this.isSecureServer = currentUrl.includes('localhost:8000') || 
                            currentUrl.includes('127.0.0.1:8000');
    }

    createLogoutButton() {
        // Evitar crear múltiples botones
        if (document.getElementById(this.logoutButtonId)) {
            return;
        }

        // Crear botón de logout
        const logoutBtn = document.createElement('button');
        logoutBtn.id = this.logoutButtonId;
        logoutBtn.innerHTML = '🚪 Cerrar Sesión';
        logoutBtn.className = 'sines-logout-btn';
        logoutBtn.onclick = () => this.logout();

        // Estilos del botón
        const style = document.createElement('style');
        style.textContent = `
            .sines-logout-btn {
                position: fixed;
                top: 20px;
                right: 20px;
                background: #dc3545;
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 8px;
                font-size: 14px;
                cursor: pointer;
                z-index: 9999;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                box-shadow: 0 2px 10px rgba(220, 53, 69, 0.3);
                transition: all 0.3s ease;
            }
            
            .sines-logout-btn:hover {
                background: #c82333;
                transform: translateY(-2px);
                box-shadow: 0 4px 15px rgba(220, 53, 69, 0.4);
            }
            
            .sines-logout-btn:active {
                transform: translateY(0);
            }
            
            .sines-session-warning {
                position: fixed;
                top: 70px;
                right: 20px;
                background: #ffc107;
                color: #856404;
                padding: 10px 15px;
                border-radius: 8px;
                font-size: 12px;
                z-index: 9998;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                box-shadow: 0 2px 10px rgba(255, 193, 7, 0.3);
                animation: slideIn 0.3s ease;
            }
            
            @keyframes slideIn {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
        `;
        
        document.head.appendChild(style);
        document.body.appendChild(logoutBtn);
    }

    async logout() {
        try {
            // Confirmar logout
            const confirmed = confirm('¿Estás seguro de que quieres cerrar sesión?');
            if (!confirmed) return;

            // Mostrar mensaje de cierre
            this.showMessage('Cerrando sesión...', 'info');

            if (this.isSecureServer) {
                // Logout en servidor seguro
                const response = await fetch('/api/logout', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                if (response.ok) {
                    this.showMessage('Sesión cerrada correctamente', 'success');
                    setTimeout(() => {
                        window.location.href = '/login.html';
                    }, 1000);
                } else {
                    throw new Error('Error al cerrar sesión en el servidor');
                }
            } else {
                // Logout en servidor normal (redirigir a página de login)
                this.showMessage('Redirigiendo a página de login...', 'info');
                setTimeout(() => {
                    window.location.href = 'http://localhost:8000/login.html';
                }, 1000);
            }

        } catch (error) {
            console.error('Error al cerrar sesión:', error);
            this.showMessage('Error al cerrar sesión. Redirigiendo...', 'error');
            setTimeout(() => {
                window.location.href = '/login.html';
            }, 2000);
        }
    }

    async checkSession() {
        if (!this.isSecureServer) return;

        try {
            const response = await fetch('/api/validate_session');
            
            if (!response.ok) {
                // Sesión expirada
                this.showMessage('Sesión expirada. Redirigiendo...', 'warning');
                setTimeout(() => {
                    window.location.href = '/login.html';
                }, 2000);
                return false;
            }

            const data = await response.json();
            if (!data.valid) {
                // Sesión inválida
                this.showMessage('Sesión inválida. Redirigiendo...', 'warning');
                setTimeout(() => {
                    window.location.href = '/login.html';
                }, 2000);
                return false;
            }

            return true;

        } catch (error) {
            console.error('Error verificando sesión:', error);
            return false;
        }
    }

    startSessionCheck() {
        if (!this.isSecureServer) return;

        // Verificar sesión cada minuto
        this.sessionTimer = setInterval(() => {
            this.checkSession();
        }, this.sessionCheckInterval);
    }

    setupKeyboardShortcuts() {
        // Atajo de teclado: Ctrl+Shift+L para logout
        document.addEventListener('keydown', (event) => {
            if (event.ctrlKey && event.shiftKey && event.key === 'L') {
                event.preventDefault();
                this.logout();
            }
        });
    }

    showMessage(message, type = 'info') {
        // Remover mensaje anterior si existe
        const existingMessage = document.querySelector('.sines-session-warning');
        if (existingMessage) {
            existingMessage.remove();
        }

        // Crear nuevo mensaje
        const messageDiv = document.createElement('div');
        messageDiv.className = 'sines-session-warning';
        messageDiv.textContent = message;

        // Colores según tipo
        const colors = {
            'info': { bg: '#17a2b8', color: 'white' },
            'success': { bg: '#28a745', color: 'white' },
            'warning': { bg: '#ffc107', color: '#856404' },
            'error': { bg: '#dc3545', color: 'white' }
        };

        if (colors[type]) {
            messageDiv.style.background = colors[type].bg;
            messageDiv.style.color = colors[type].color;
        }

        document.body.appendChild(messageDiv);

        // Remover mensaje después de 3 segundos
        setTimeout(() => {
            if (messageDiv && messageDiv.parentNode) {
                messageDiv.remove();
            }
        }, 3000);
    }

    destroy() {
        // Limpiar timers y eventos
        if (this.sessionTimer) {
            clearInterval(this.sessionTimer);
        }

        // Remover botón de logout
        const logoutBtn = document.getElementById(this.logoutButtonId);
        if (logoutBtn) {
            logoutBtn.remove();
        }
    }
}

// Inicializar el LogoutManager cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    // Evitar inicializar en páginas de login
    if (window.location.pathname.includes('login.html') || 
        window.location.pathname.includes('index_isometricos_secure.html') ||
        window.location.pathname.includes('index_secure_simple.html') ||
        window.location.pathname.includes('index_secure_hybrid.html')) {
        return;
    }

    // Inicializar LogoutManager
    window.logoutManager = new LogoutManager();
});

// Limpiar al salir de la página
window.addEventListener('beforeunload', () => {
    if (window.logoutManager) {
        window.logoutManager.destroy();
    }
});

// Exportar para uso manual si es necesario
window.LogoutManager = LogoutManager; 