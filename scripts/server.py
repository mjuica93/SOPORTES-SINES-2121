import http.server
import socketserver
import webbrowser
import os
import threading
import time

def start_server():
    PORT = 8000
    
    class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            super().end_headers()
    
    try:
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            print(f"🌐 Servidor iniciado en http://localhost:{PORT}")
            print(f"📂 Sirviendo archivos desde: {os.getcwd()}")
            print("🎯 Abriendo el sistema en tu navegador...")
            
            # Esperar un momento y abrir el navegador
            def open_browser():
                time.sleep(1)
                webbrowser.open(f'http://localhost:{PORT}/index.html')
            
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.start()
            
            print("\n✅ Sistema listo! Si no se abre automáticamente, ve a:")
            print(f"   http://localhost:{PORT}/index.html")
            print("\n⚠️  Para detener el servidor, presiona Ctrl+C")
            print("="*50)
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ El puerto {PORT} ya está en uso.")
            print("💡 Intenta cerrar otros servidores o usar otro puerto.")
            print("🔄 Intentando con puerto 8001...")
            
            PORT = 8001
            with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
                print(f"🌐 Servidor iniciado en http://localhost:{PORT}")
                webbrowser.open(f'http://localhost:{PORT}/index.html')
                httpd.serve_forever()
        else:
            print(f"❌ Error al iniciar servidor: {e}")

if __name__ == "__main__":
    print("=== SERVIDOR PARA SISTEMA DE SOPORTES SINES ===\n")
    start_server() 