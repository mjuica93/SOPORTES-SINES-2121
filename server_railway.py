import os
import http.server
import socketserver
import webbrowser
import threading
import time

def start_server():
    # Railway proporciona el puerto a través de la variable de entorno PORT
    PORT = int(os.environ.get('PORT', 8000))
    
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
            # Redirigir la raíz al index.html
            if self.path == '/':
                self.path = '/index.html'
            elif self.path == '/mobile':
                self.path = '/index_mobile.html'
            return super().do_GET()
    
    try:
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            print(f"🌐 Servidor iniciado en puerto {PORT}")
            print(f"📂 Sirviendo archivos desde: {os.getcwd()}")
            print("✅ Sistema SINES listo para Railway!")
            print(f"🎯 Acceso local: http://localhost:{PORT}")
            print("🌍 Acceso mundial: https://tu-proyecto.railway.app")
            print("📱 Versión móvil: https://tu-proyecto.railway.app/mobile")
            print("="*50)
            
            # En Railway no necesitamos abrir navegador
            if os.environ.get('RAILWAY_ENVIRONMENT') != 'production':
                # Solo abrir navegador en desarrollo local
                def open_browser():
                    time.sleep(1)
                    webbrowser.open(f'http://localhost:{PORT}')
                
                browser_thread = threading.Thread(target=open_browser)
                browser_thread.daemon = True
                browser_thread.start()
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido")
    except Exception as e:
        print(f"❌ Error al iniciar servidor: {e}")
        # En Railway, es importante que el proceso termine con error si no puede iniciar
        exit(1)

if __name__ == "__main__":
    print("=== SISTEMA SINES - RAILWAY DEPLOYMENT ===")
    start_server() 