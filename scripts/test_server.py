import requests
import json
import os

def test_server_status():
    print("=== DIAGNÓSTICO DEL SERVIDOR ===\n")
    
    base_url = "http://localhost:8000"
    
    # Verificar archivos locales
    print("1. VERIFICANDO ARCHIVOS LOCALES:")
    required_files = [
        'support_data.json',
        'support_data_enhanced.json', 
        'support_pdf_mapping.json',
        'index.html',
        'index_enhanced.html',
        'app.js',
        'app_enhanced.js'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"   ✅ {file} - {size:,} bytes")
        else:
            print(f"   ❌ {file} - NO ENCONTRADO")
    
    print("\n2. VERIFICANDO ACCESO AL SERVIDOR:")
    
    # Verificar acceso básico al servidor
    try:
        response = requests.get(base_url, timeout=5)
        print(f"   ✅ Servidor respondiendo - Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Error de conexión al servidor: {e}")
        return False
    
    # Verificar archivos JSON
    print("\n3. VERIFICANDO ARCHIVOS JSON:")
    json_files = [
        'support_data.json',
        'support_data_enhanced.json',
        'support_pdf_mapping.json'
    ]
    
    for json_file in json_files:
        try:
            url = f"{base_url}/{json_file}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                try:
                    data = response.json()
                    if json_file == 'support_data.json' or json_file == 'support_data_enhanced.json':
                        print(f"   ✅ {json_file} - {len(data)} registros")
                    else:
                        print(f"   ✅ {json_file} - {len(data)} tipos de soporte")
                except json.JSONDecodeError:
                    print(f"   ❌ {json_file} - ERROR: No es JSON válido")
            else:
                print(f"   ❌ {json_file} - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ {json_file} - Error: {e}")
    
    # Verificar páginas HTML
    print("\n4. VERIFICANDO PÁGINAS HTML:")
    html_files = ['index.html', 'index_enhanced.html']
    
    for html_file in html_files:
        try:
            url = f"{base_url}/{html_file}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {html_file} - Accesible")
            else:
                print(f"   ❌ {html_file} - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ {html_file} - Error: {e}")
    
    print("\n5. VERIFICANDO ARCHIVOS JAVASCRIPT:")
    js_files = ['app.js', 'app_enhanced.js']
    
    for js_file in js_files:
        try:
            url = f"{base_url}/{js_file}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {js_file} - Accesible")
            else:
                print(f"   ❌ {js_file} - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ {js_file} - Error: {e}")
    
    print("\n6. URLS RECOMENDADAS:")
    print(f"   🌐 Versión básica: {base_url}/index.html")
    print(f"   🌐 Versión mejorada: {base_url}/index_enhanced.html")
    
    print("\n7. SOLUCIÓN DE PROBLEMAS:")
    print("   - Si hay errores de conexión, reiniciar el servidor")
    print("   - Si los JSON no cargan, verificar permisos de archivos")
    print("   - Si persiste el error, limpiar caché del navegador")
    print("   - Usar modo incógnito del navegador")
    
    return True

if __name__ == "__main__":
    test_server_status() 