#!/usr/bin/env python3
import os
import http.server
import socketserver
from pathlib import Path

def main():
    # Puerto de Railway
    PORT = int(os.environ.get('PORT', 8000))
    
    # Cambiar al directorio del script
    os.chdir(Path(__file__).parent)
    
    class SimpleHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            # Redirección simple
            if self.path == '/':
                self.path = '/index_isometricos_integrado_final.html'
            elif self.path == '/health':
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'OK')
                return
            
            return super().do_GET()
        
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            super().end_headers()
    
    # Servidor simple
    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), SimpleHandler) as httpd:
            print(f"🌐 Servidor iniciado en 0.0.0.0:{PORT}")
            print("✅ Sistema SINES listo")
            httpd.serve_forever()
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)

if __name__ == "__main__":
    main() 