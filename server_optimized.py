import os
import http.server
import socketserver
import webbrowser
import threading
import time
import gzip
import json
import mimetypes
from urllib.parse import urlparse, parse_qs
import io

class OptimizedHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Initialize data structures
        self.support_data = []
        self.pdf_mapping = {}
        self.load_data()
        super().__init__(*args, **kwargs)
    
    def load_data(self):
        """Load and cache data for API endpoints"""
        try:
            # Load the most optimized version available
            data_files = [
                'support_data_enhanced.json',
                'support_data.json'
            ]
            
            for file in data_files:
                if os.path.exists(file):
                    with open(file, 'r', encoding='utf-8') as f:
                        self.support_data = json.load(f)
                    print(f"✅ Loaded {len(self.support_data)} supports from {file}")
                    break
            
            # Load PDF mappings
            if os.path.exists('support_pdf_mapping.json'):
                with open('support_pdf_mapping.json', 'r', encoding='utf-8') as f:
                    self.pdf_mapping = json.load(f)
            else:
                self.pdf_mapping = {}
                
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            self.support_data = []
            self.pdf_mapping = {}
    
    def end_headers(self):
        """Add optimized headers for performance"""
        # CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        # Performance headers
        if self.path.endswith(('.js', '.css', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf')):
            # Cache static assets for 1 hour
            self.send_header('Cache-Control', 'public, max-age=3600')
        elif self.path.endswith('.json'):
            # Cache JSON files for 5 minutes
            self.send_header('Cache-Control', 'public, max-age=300')
        else:
            # No cache for HTML files
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
        
        super().end_headers()
    
    def do_GET(self):
        """Handle GET requests with optimizations"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        
        # API endpoints for optimized data loading
        if path.startswith('/api/'):
            self.handle_api_request(path, query_params)
        elif path == '/':
            self.path = '/index.html'
            self.serve_with_compression()
        else:
            self.serve_with_compression()
    
    def handle_api_request(self, path, query_params):
        """Handle API requests for optimized data loading"""
        try:
            if path == '/api/supports':
                self.serve_paginated_supports(query_params)
            elif path == '/api/supports/search':
                self.serve_search_results(query_params)
            elif path == '/api/supports/stats':
                self.serve_support_stats()
            elif path == '/api/supports/types':
                self.serve_support_types()
            else:
                self.send_error(404, "API endpoint not found")
        except Exception as e:
            self.send_error(500, f"API error: {str(e)}")
    
    def serve_paginated_supports(self, query_params):
        """Serve paginated support data"""
        if not self.support_data:
            response = {
                'data': [],
                'pagination': {
                    'page': 1,
                    'limit': 50,
                    'total': 0,
                    'pages': 0
                }
            }
            self.send_json_response(response)
            return
            
        page = int(query_params.get('page', [1])[0])
        limit = int(query_params.get('limit', [50])[0])
        
        # Limit the maximum page size to prevent abuse
        limit = min(limit, 100)
        
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        
        paginated_data = self.support_data[start_idx:end_idx]
        
        response = {
            'data': paginated_data,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': len(self.support_data),
                'pages': (len(self.support_data) + limit - 1) // limit
            }
        }
        
        self.send_json_response(response)
    
    def serve_search_results(self, query_params):
        """Serve search results with optimized filtering"""
        if not self.support_data:
            response = {
                'data': [],
                'pagination': {
                    'page': 1,
                    'limit': 50,
                    'total': 0,
                    'pages': 0
                }
            }
            self.send_json_response(response)
            return
            
        query = query_params.get('q', [''])[0].lower()
        support_type = query_params.get('type', [''])[0]
        page = int(query_params.get('page', [1])[0])
        limit = int(query_params.get('limit', [50])[0])
        
        # Filter data
        filtered_data = []
        for support in self.support_data:
            matches_query = (not query or 
                           query in support.get('support_number', '').lower() or
                           query in support.get('support_type', '').lower() or
                           query in support.get('fluid_piping', '').lower())
            
            matches_type = (not support_type or 
                           support.get('support_type') == support_type)
            
            if matches_query and matches_type:
                filtered_data.append(support)
        
        # Paginate results
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_data = filtered_data[start_idx:end_idx]
        
        response = {
            'data': paginated_data,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': len(filtered_data),
                'pages': (len(filtered_data) + limit - 1) // limit
            }
        }
        
        self.send_json_response(response)
    
    def serve_support_stats(self):
        """Serve support statistics"""
        if not self.support_data:
            stats = {
                'total_supports': 0,
                'total_types': 0,
                'with_pdfs': 0,
                'pdf_percentage': 0
            }
            self.send_json_response(stats)
            return
            
        total_supports = len(self.support_data)
        
        # Calculate statistics
        types = set()
        with_pdfs = 0
        
        for support in self.support_data:
            support_type = support.get('support_type', '')
            types.add(support_type)
            
            if support_type in self.pdf_mapping:
                with_pdfs += 1
        
        stats = {
            'total_supports': total_supports,
            'total_types': len(types),
            'with_pdfs': with_pdfs,
            'pdf_percentage': (with_pdfs / total_supports * 100) if total_supports > 0 else 0
        }
        
        self.send_json_response(stats)
    
    def serve_support_types(self):
        """Serve list of support types"""
        if not self.support_data:
            response = {'types': []}
            self.send_json_response(response)
            return
            
        types = set()
        for support in self.support_data:
            types.add(support.get('support_type', ''))
        
        response = {
            'types': sorted(list(types))
        }
        
        self.send_json_response(response)
    
    def send_json_response(self, data):
        """Send JSON response with compression"""
        json_data = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
        
        # Compress if the client supports it
        if 'gzip' in self.headers.get('Accept-Encoding', ''):
            compressed = gzip.compress(json_data.encode('utf-8'))
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Encoding', 'gzip')
            self.send_header('Content-Length', str(len(compressed)))
            self.end_headers()
            self.wfile.write(compressed)
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(json_data.encode('utf-8'))))
            self.end_headers()
            self.wfile.write(json_data.encode('utf-8'))
    
    def serve_with_compression(self):
        """Serve files with compression when possible"""
        # Check if client supports gzip
        if 'gzip' in self.headers.get('Accept-Encoding', ''):
            # Try to serve compressed version for text files
            if self.path.endswith(('.html', '.js', '.css', '.json', '.xml', '.svg')):
                self.serve_compressed_file()
                return
        
        # Fallback to regular serving
        super().do_GET()
    
    def serve_compressed_file(self):
        """Serve compressed version of text files"""
        try:
            # Remove query parameters for file path
            file_path = self.path.split('?')[0]
            if file_path.startswith('/'):
                file_path = file_path[1:]
            
            if not os.path.exists(file_path):
                self.send_error(404, "File not found")
                return
            
            # Read and compress file
            with open(file_path, 'rb') as f:
                content = f.read()
            
            compressed_content = gzip.compress(content)
            
            # Send compressed response
            self.send_response(200)
            
            # Set appropriate content type
            content_type, _ = mimetypes.guess_type(file_path)
            if content_type:
                self.send_header('Content-Type', content_type)
            
            self.send_header('Content-Encoding', 'gzip')
            self.send_header('Content-Length', str(len(compressed_content)))
            self.end_headers()
            self.wfile.write(compressed_content)
            
        except Exception as e:
            print(f"Error serving compressed file: {e}")
            super().do_GET()

def start_optimized_server():
    PORT = int(os.environ.get('PORT', 8000))
    
    try:
        with socketserver.TCPServer(("", PORT), OptimizedHTTPRequestHandler) as httpd:
            print("=" * 60)
            print("🚀 OPTIMIZED SINES SERVER v2.0")
            print("=" * 60)
            print(f"🌐 Server running on port {PORT}")
            print(f"📂 Serving files from: {os.getcwd()}")
            print("⚡ Optimizations enabled:")
            print("   • Gzip compression for text files")
            print("   • Intelligent caching headers")
            print("   • API endpoints for data pagination")
            print("   • Optimized data loading")
            print("=" * 60)
            print("📊 API Endpoints:")
            print("   • /api/supports - Paginated support data")
            print("   • /api/supports/search - Search supports")
            print("   • /api/supports/stats - Support statistics")
            print("   • /api/supports/types - Support types")
            print("=" * 60)
            print(f"🎯 Access URLs:")
            print(f"   • Main app: http://localhost:{PORT}")
            print(f"   • API docs: http://localhost:{PORT}/api/supports/stats")
            print("=" * 60)
            
            # Open browser in development
            if os.environ.get('RAILWAY_ENVIRONMENT') != 'production':
                def open_browser():
                    time.sleep(1)
                    webbrowser.open(f'http://localhost:{PORT}')
                
                browser_thread = threading.Thread(target=open_browser)
                browser_thread.daemon = True
                browser_thread.start()
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        exit(1)

if __name__ == "__main__":
    start_optimized_server()