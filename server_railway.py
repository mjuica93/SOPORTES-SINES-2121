import os
import http.server
import socketserver
import webbrowser
import threading
import time

def start_server():
    # Railway proporciona el puerto a través de la variable de entorno PORT
    PORT = int(os.environ.get('PORT', 8000))
    HOST = '0.0.0.0'  # Importante: bind a todas las interfaces para Railway
    
    class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            # Headers para CORS y caché
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            super().end_headers()
        
        def do_GET(self):
            # Redirigir la raíz al sistema integrado final más actualizado
            if self.path == '/':
                self.path = '/index_isometricos_integrado_final.html'
            elif self.path == '/sistema-integrado':
                self.path = '/index_isometricos_integrado_final.html'
            elif self.path == '/sistema-mejorado':
                self.path = '/index_isometricos_integrado_mejorado.html'
            elif self.path == '/costuras':
                self.path = '/index_isometricos_con_costuras.html'
            elif self.path == '/github':
                self.path = '/index_isometricos_github.html'
            elif self.path == '/mobile':
                self.path = '/index_mobile.html'
            elif self.path == '/basico':
                self.path = '/index.html'
            elif self.path == '/templates':
                self.path = '/index_enhanced_with_templates.html'
            elif self.path == '/robusto':
                self.path = '/index_enhanced_robust.html'
            return super().do_GET()
        
        def log_message(self, format, *args):
            # Simplificar logs para Railway
            if os.environ.get('RAILWAY_ENVIRONMENT') == 'production':
                return  # No logs verbosos en producción
            super().log_message(format, *args)
    
    print("=== SISTEMA SINES v3.0 - VERSIÓN FINAL - RAILWAY DEPLOYMENT ===")
    print("🏭 Sistema Integrado Final con TODAS las funcionalidades")
    print("⚡ Soportes Agrupados + Variables de Plantilla + Soldadura + Isométricos")
    
    try:
        # Usar TCPServer con binding explícito a todas las interfaces
        httpd = socketserver.TCPServer((HOST, PORT), MyHTTPRequestHandler)
        httpd.allow_reuse_address = True  # Importante para Railway
        
        print(f"🌐 Servidor iniciado en {HOST}:{PORT}")
        print(f"📂 Sirviendo archivos desde: {os.getcwd()}")
        print("✅ Sistema SINES v3.0 - VERSIÓN FINAL listo para Railway!")
        
        if os.environ.get('RAILWAY_ENVIRONMENT') == 'production':
            print("🚀 PRODUCCIÓN: Railway detectará automáticamente el servicio")
        else:
            print("🏭 Funcionalidades COMPLETAS:")
            print("   ├─ 🔧 Soportes agrupados por número")
            print("   ├─ 📐 Variables de plantilla (A, B, C, D, E, R, X, Y, EL, N., SH., TEMP)")
            print("   ├─ 🏷️ Códigos de referencia (4a), (4b), (4c), (4d), etc.")
            print("   ├─ 📏 Dimensiones técnicas completas")
            print("   ├─ 🔗 Integración con isométricos")
            print("   ├─ ⚡ Soporte para prefabricados")
            print("   ├─ 🔧 Gestión de instalaciones")
            print("   ├─ ⚡ Control de soldadura")
            print("   └─ 📊 Estadísticas y filtros avanzados")
            print(f"🎯 Acceso local: http://localhost:{PORT}")
            print("🌍 URLS DE ACCESO MUNDIAL:")
            print("   ├─ Principal: https://tu-proyecto.railway.app/")
            print("   ├─ Sistema mejorado: https://tu-proyecto.railway.app/sistema-mejorado")
            print("   ├─ Con costuras: https://tu-proyecto.railway.app/costuras")
            print("   ├─ GitHub version: https://tu-proyecto.railway.app/github")
            print("   ├─ Móvil: https://tu-proyecto.railway.app/mobile")
            print("   ├─ Con plantillas: https://tu-proyecto.railway.app/templates")
            print("   └─ Básico: https://tu-proyecto.railway.app/basico")
        
        print("="*80)
        print("🎯 SERVIDOR LISTO - Esperando conexiones...")
        
        # En Railway no necesitamos abrir navegador
        if os.environ.get('RAILWAY_ENVIRONMENT') != 'production':
            # Solo abrir navegador en desarrollo local
            def open_browser():
                time.sleep(1)
                webbrowser.open(f'http://localhost:{PORT}')
            
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
        
        # Iniciar el servidor
        httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por usuario")
    except Exception as e:
        print(f"❌ Error al iniciar servidor: {e}")
        print(f"🔍 Puerto intentado: {PORT}")
        print(f"🔍 Host intentado: {HOST}")
        # En Railway, es importante que el proceso termine con error si no puede iniciar
        exit(1)
    finally:
        if 'httpd' in locals():
            httpd.server_close()

if __name__ == "__main__":
    start_server() 