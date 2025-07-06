#!/usr/bin/env python3
"""
Script de inicio para el Sistema SINES
Versión optimizada para GitHub
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def check_python_version():
    """Verificar versión de Python"""
    if sys.version_info < (3, 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} encontrado")

def check_dependencies():
    """Verificar e instalar dependencias"""
    requirements_file = Path("requirements.txt")
    if requirements_file.exists():
        print("🔍 Verificando dependencias...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                         check=True, capture_output=True)
            print("✅ Dependencias instaladas correctamente")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error instalando dependencias: {e}")
            sys.exit(1)
    else:
        print("⚠️  Archivo requirements.txt no encontrado")

def check_data_files():
    """Verificar archivos de datos"""
    data_dir = Path("data")
    if not data_dir.exists():
        print("❌ Error: Carpeta 'data' no encontrada")
        sys.exit(1)
    
    required_files = [
        "support_data_enhanced.json",
        "welding_enhanced_data.json",
        "support_pdf_mapping.json"
    ]
    
    missing_files = []
    for file in required_files:
        if not (data_dir / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"⚠️  Archivos de datos faltantes: {', '.join(missing_files)}")
        print("   El sistema funcionará con datos limitados")
    else:
        print("✅ Archivos de datos verificados")

def start_server():
    """Iniciar el servidor"""
    server_path = Path("src/server.py")
    if not server_path.exists():
        print("❌ Error: Archivo servidor no encontrado")
        sys.exit(1)
    
    print("🚀 Iniciando servidor SINES...")
    print("=" * 60)
    print("🏗️  SISTEMA SINES - GESTIÓN DE SOPORTES Y COSTURAS")
    print("=" * 60)
    print("📊 Características:")
    print("   ├─ 🔧 Gestión de soportes agrupados")
    print("   ├─ ⚡ Control de costuras en tiempo real")
    print("   ├─ 📐 Isométricos y relaciones")
    print("   ├─ 🔐 Sistema de autenticación seguro")
    print("   └─ 📱 Interfaz responsive")
    print("=" * 60)
    print("🌐 Acceso al sistema:")
    print("   URL: http://localhost:8000")
    print("   Puerto: 8000")
    print("=" * 60)
    print("🔑 Credenciales de acceso:")
    print("   admin / sines2024 (Administrador)")
    print("   supervisor / super2024 (Supervisor)")
    print("   operador / op2024 (Operador)")
    print("   sines / sines123 (Usuario)")
    print("=" * 60)
    
    # Cambiar al directorio src para ejecutar el servidor
    os.chdir("src")
    
    try:
        # Abrir navegador después de 3 segundos
        import threading
        import time
        
        def open_browser():
            time.sleep(3)
            webbrowser.open("http://localhost:8000")
        
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Ejecutar servidor
        subprocess.run([sys.executable, "server.py"], check=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando servidor: {e}")
        sys.exit(1)

def main():
    """Función principal"""
    print("🚀 Iniciando Sistema SINES...")
    
    # Verificaciones previas
    check_python_version()
    check_dependencies()
    check_data_files()
    
    # Iniciar servidor
    start_server()

if __name__ == "__main__":
    main() 