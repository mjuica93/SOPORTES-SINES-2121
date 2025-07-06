#!/usr/bin/env python3
import os
import http.server
import socketserver

def main():
    PORT = int(os.environ.get('PORT', 8000))
    
    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            print(f"Request: {self.path}")
            
            # Health check simple
            if self.path == '/health':
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'OK')
                return
            
            # Redirección raíz - probar diferentes archivos
            if self.path == '/':
                # Intentar archivos en orden de preferencia
                files_to_try = [
                    '/index_isometricos_integrado_final.html',
                    '/index_isometricos_github.html', 
                    '/index.html'
                ]
                
                for file_path in files_to_try:
                    if os.path.exists('.' + file_path):
                        print(f"Usando archivo: {file_path}")
                        self.path = file_path
                        break
                else:
                    # Si no encuentra ninguno, usar index.html por defecto
                    self.path = '/index.html'
            
            return super().do_GET()
        
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            super().end_headers()
    
    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
            print(f"🌐 Servidor iniciado en 0.0.0.0:{PORT}")
            print(f"📂 Directorio: {os.getcwd()}")
            
            # Verificar archivos disponibles
            files = ['index_isometricos_integrado_final.html', 'index_isometricos_github.html', 'index.html']
            for f in files:
                exists = "✅" if os.path.exists(f) else "❌"
                print(f"{exists} {f}")
            
            print("✅ Servidor listo")
            httpd.serve_forever()
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)

if __name__ == "__main__":
    main() 