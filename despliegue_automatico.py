#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 DESPLIEGUE AUTOMATICO DEL SISTEMA DE COSTURAS SINES A GITHUB Y RAILWAY
═══════════════════════════════════════════════════════════════════════════
"""

import sys
import os
import base64
import json
import requests
import time

def print_colored(text, color="white"):
    """Imprimir texto con colores"""
    colors = {
        "green": "\033[92m",
        "red": "\033[91m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "gray": "\033[90m"
    }
    reset = "\033[0m"
    print(f"{colors.get(color, colors['white'])}{text}{reset}")

def upload_file_to_github(file_path, token, owner="mjuica93", repo="soportes-y-isometricos-2121"):
    """Subir archivo a GitHub usando la API"""
    if not os.path.exists(file_path):
        print_colored(f"⚠️ Archivo {file_path} no encontrado", "yellow")
        return False
    
    file_name = os.path.basename(file_path)
    
    try:
        # Leer archivo y convertir a base64
        with open(file_path, 'rb') as f:
            file_content = base64.b64encode(f.read()).decode('utf-8')
        
        # Preparar datos para la API
        data = {
            "message": f"Add {file_name} - Sistema de Costuras SINES 2121",
            "content": file_content
        }
        
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_name}"
        
        # Hacer la petición
        response = requests.put(url, json=data, headers=headers)
        
        if response.status_code in [200, 201]:
            print_colored(f"✅ {file_name} subido correctamente", "green")
            return True
        else:
            print_colored(f"❌ Error subiendo {file_name}: {response.status_code}", "red")
            print_colored(f"Respuesta: {response.text}", "red")
            return False
            
    except Exception as e:
        print_colored(f"❌ Error subiendo {file_name}: {str(e)}", "red")
        return False

def create_readme():
    """Crear archivo README.md"""
    readme_content = """# 🚀 Sistema de Gestión de Costuras y Soportes SINES 2121

![Sistema SINES](https://img.shields.io/badge/SINES-Sistema%20Costuras-blue)
![Railway](https://img.shields.io/badge/Deploy-Railway-green)
![Status](https://img.shields.io/badge/Status-Producción-brightgreen)

## 📋 Descripción

Sistema completo de gestión de costuras de soldadura y soportes para el proyecto 2121.
Integra 4,009 costuras de soldadura con 1,778 isométricos y 750+ soportes.

## 🎯 Características

### 🔨 Sistema de Costuras
- **4,009 costuras** procesadas y vinculadas
- **2,364 costuras prefabricadas** (Shop Welds)
- **1,567 costuras de campo** (Field Welds)
- **100% trazabilidad** implementada
- **Exportación CSV** completa

### 📐 Integración con Isométricos
- **1,778 isométricos** totales
- **463 isométricos con costuras** (26.0% de cobertura)
- **Vinculación automática** por nombre
- **Acceso directo** a PDFs

### 🔧 Sistema de Soportes
- **750+ PDFs** de soportes integrados
- **Búsqueda avanzada** por tipo y código
- **Compatibilidad total** mantenida

## 🌐 Rutas Disponibles

- **/** - Sistema completo de gestión de costuras
- **/soportes** - Sistema original de soportes
- **/isometricos** - Vista de isométricos básicos
- **/mobile** - Versión optimizada para móviles
- **/data** - API de datos JSON
- **/stats** - Estadísticas en tiempo real

## 🚀 Despliegue

Sistema configurado para Railway con despliegue automático:

1. **Dockerfile** - Configuración del contenedor
2. **railway.json** - Configuración de Railway  
3. **requirements.txt** - Dependencias Python
4. **server_railway.py** - Servidor optimizado

## 🛠️ Tecnologías

- **Frontend**: HTML5, CSS3, JavaScript ES6+
- **Backend**: Python HTTP Server
- **Datos**: JSON estructurado (6.8MB)
- **Despliegue**: Docker + Railway
- **Diseño**: Responsive, mobile-first

## 📊 Métricas

- ✅ **1,778** isométricos procesados
- ✅ **4,009** costuras de soldadura
- ✅ **100%** de trazabilidad
- ✅ **26%** de cobertura de isométricos
- ✅ **6.8MB** de datos estructurados

---

**🎉 Sistema desarrollado para el proyecto 2121 - En producción mundial**
"""
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print_colored("✅ README.md creado", "green")

def main():
    """Función principal"""
    if len(sys.argv) != 2:
        print_colored("❌ Uso: python despliegue_automatico.py <token_github>", "red")
        sys.exit(1)
    
    token = sys.argv[1]
    
    print_colored("🚀 INICIANDO DESPLIEGUE AUTOMATICO DEL SISTEMA DE COSTURAS SINES", "green")
    print_colored("══════════════════════════════════════════════════════════════════", "green")
    print()
    
    # Verificar sistema
    print_colored("📊 Verificando sistema...", "cyan")
    try:
        import subprocess
        result = subprocess.run(["python", "verificar_datos_railway.py"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print_colored("✅ Sistema verificado correctamente", "green")
        else:
            print_colored("❌ Error en verificación del sistema", "red")
            sys.exit(1)
    except Exception as e:
        print_colored(f"❌ Error verificando sistema: {e}", "red")
        sys.exit(1)
    
    # Crear README
    print_colored("📝 Creando documentación...", "cyan")
    create_readme()
    
    # Archivos a subir
    files_to_upload = [
        "index_isometricos_con_costuras.html",
        "isometric_welding_manager.js",
        "isometric_data_with_welds.json",
        "welding_statistics.json",
        "server_railway.py",
        "Dockerfile",
        "railway.json",
        "requirements.txt",
        "README.md"
    ]
    
    print()
    print_colored("📤 Subiendo archivos a GitHub...", "cyan")
    print_colored("──────────────────────────────────────────────────────────────────", "gray")
    
    upload_success = True
    total_files = len(files_to_upload)
    
    for i, file_path in enumerate(files_to_upload, 1):
        print_colored(f"📤 [{i}/{total_files}] Subiendo {file_path}...", "yellow")
        success = upload_file_to_github(file_path, token)
        if not success:
            upload_success = False
        time.sleep(2)  # Evitar rate limiting
    
    print()
    if upload_success:
        print_colored("✅ TODOS LOS ARCHIVOS SUBIDOS CORRECTAMENTE", "green")
        print()
        print_colored("🚀 ABRIENDO RAILWAY PARA DESPLIEGUE...", "cyan")
        
        # Abrir Railway
        try:
            import webbrowser
            webbrowser.open("https://railway.app/new?template=https://github.com/mjuica93/soportes-y-isometricos-2121")
        except:
            print_colored("🌐 Ve a: https://railway.app/new?template=https://github.com/mjuica93/soportes-y-isometricos-2121", "cyan")
        
        print()
        print_colored("🎯 RUTAS DISPONIBLES UNA VEZ DESPLEGADO:", "cyan")
        print_colored("🔨 https://tu-proyecto.railway.app/           - Gestión de Costuras", "white")
        print_colored("🔧 https://tu-proyecto.railway.app/soportes  - Sistema de Soportes", "white")
        print_colored("📐 https://tu-proyecto.railway.app/isometricos - Isométricos", "white")
        print_colored("📱 https://tu-proyecto.railway.app/mobile    - Versión Móvil", "white")
        print_colored("📊 https://tu-proyecto.railway.app/data      - API de Datos", "white")
        print_colored("📈 https://tu-proyecto.railway.app/stats     - Estadísticas", "white")
        
        print()
        print_colored("🎉 DESPLIEGUE AUTOMATICO COMPLETADO", "green")
        print_colored("🌐 Repositorio: https://github.com/mjuica93/soportes-y-isometricos-2121", "cyan")
        print_colored("🚀 Tiempo estimado de despliegue en Railway: 3-5 minutos", "cyan")
        
    else:
        print_colored("❌ ERRORES DURANTE LA SUBIDA DE ARCHIVOS", "red")
        sys.exit(1)

if __name__ == "__main__":
    main() 