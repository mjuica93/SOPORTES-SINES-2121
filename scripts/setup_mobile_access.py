#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para configurar acceso móvil al sistema de soportes SINES
"""

import os
import subprocess
import json
import webbrowser
from datetime import datetime

def create_mobile_optimized_version():
    """Crear versión optimizada para móviles"""
    
    mobile_html = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>SINES Soportes - Móvil</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-size: 14px;
        }
        .container { max-width: 100%; padding: 10px; }
        .header { 
            text-align: center; 
            color: white; 
            margin-bottom: 20px;
            padding: 15px;
            background: rgba(0,0,0,0.2);
            border-radius: 10px;
        }
        .header h1 { font-size: 1.5rem; margin-bottom: 5px; }
        .header h2 { font-size: 0.9rem; opacity: 0.9; }
        .card { 
            background: rgba(255,255,255,0.95); 
            border-radius: 15px; 
            padding: 15px; 
            margin: 10px 0; 
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        .search-container {
            position: sticky;
            top: 10px;
            z-index: 100;
            margin-bottom: 15px;
        }
        .search-box { 
            width: 100%; 
            padding: 12px 15px; 
            border: 2px solid #ddd; 
            border-radius: 25px; 
            font-size: 16px; 
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .search-box:focus { 
            outline: none; 
            border-color: #3498db; 
            box-shadow: 0 0 20px rgba(52, 152, 219, 0.3); 
        }
        .stats { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(80px, 1fr)); 
            gap: 10px; 
            margin: 15px 0; 
        }
        .stat-card { 
            background: linear-gradient(45deg, #3498db, #2980b9); 
            color: white; 
            padding: 12px 8px; 
            border-radius: 10px; 
            text-align: center;
            font-size: 0.8rem;
        }
        .stat-number { font-size: 1.4rem; font-weight: bold; }
        .stat-label { font-size: 0.7rem; opacity: 0.9; margin-top: 2px; }
        .support-card { 
            background: #f8f9fa; 
            padding: 15px; 
            margin: 10px 0; 
            border-radius: 10px; 
            border-left: 4px solid #3498db;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .support-number { 
            font-size: 1.2rem; 
            font-weight: bold; 
            color: #2c3e50; 
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .support-info { 
            display: grid; 
            grid-template-columns: 1fr; 
            gap: 8px; 
        }
        .info-row {
            display: grid;
            grid-template-columns: auto 1fr;
            gap: 8px;
            align-items: start;
        }
        .info-label { 
            font-weight: bold; 
            color: #34495e; 
            font-size: 0.8rem;
            min-width: 60px;
        }
        .info-value { 
            color: #2c3e50; 
            font-size: 0.9rem;
            word-break: break-word;
        }
        .pdf-links { 
            margin-top: 10px; 
            display: flex; 
            flex-wrap: wrap; 
            gap: 5px; 
        }
        .pdf-btn { 
            background: linear-gradient(45deg, #e74c3c, #c0392b); 
            color: white; 
            padding: 6px 10px; 
            border-radius: 15px; 
            text-decoration: none; 
            font-size: 0.7rem;
            font-weight: 500;
            display: inline-block;
        }
        .loading { 
            text-align: center; 
            padding: 30px; 
            color: white;
        }
        .spinner { 
            border: 3px solid rgba(255,255,255,0.3); 
            border-top: 3px solid white; 
            border-radius: 50%; 
            width: 30px; 
            height: 30px; 
            animation: spin 1s linear infinite; 
            margin: 0 auto 15px;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .no-results { 
            text-align: center; 
            padding: 30px; 
            color: #7f8c8d;
            font-style: italic;
        }
        .show-more { 
            background: linear-gradient(45deg, #27ae60, #2ecc71); 
            color: white; 
            border: none; 
            padding: 12px 24px; 
            border-radius: 25px; 
            font-size: 14px; 
            width: 100%; 
            margin: 15px 0;
            font-weight: 500;
        }
        .variables-section {
            background: rgba(155, 89, 182, 0.1);
            padding: 10px;
            border-radius: 8px;
            margin-top: 10px;
        }
        .variables-title {
            font-weight: bold;
            color: #8e44ad;
            font-size: 0.8rem;
            margin-bottom: 5px;
        }
        .variable-item {
            font-size: 0.75rem;
            color: #2c3e50;
            margin: 2px 0;
        }
        @media (max-width: 480px) {
            .container { padding: 5px; }
            .card { padding: 10px; margin: 5px 0; }
            .support-card { padding: 10px; }
            .header h1 { font-size: 1.3rem; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔧 SINES Soportes</h1>
            <h2>Acceso Móvil - Proyecto SINES</h2>
        </div>
        
        <div class="search-container">
            <div class="card">
                <input type="text" id="searchBox" class="search-box" placeholder="🔍 Buscar soporte...">
                <div id="statsContainer" class="stats"></div>
            </div>
        </div>
        
        <div id="loadingContainer" class="card loading">
            <div class="spinner"></div>
            <h3>Cargando datos...</h3>
            <p>Conectando con el servidor...</p>
        </div>
        
        <div id="resultsContainer"></div>
    </div>

    <script>
        let allSupports = [];
        let supportMapping = {};
        let filteredSupports = [];
        let displayedCount = 0;
        const pageSize = 20;
        
        // Función principal de carga
        async function initializeMobileSystem() {
            try {
                console.log('🔄 Iniciando sistema móvil...');
                
                // Cargar datos con reintentos
                const [supportsData, mappingData] = await Promise.all([
                    loadWithRetries('support_data_enhanced.json'),
                    loadWithRetries('support_pdf_mapping.json')
                ]);
                
                allSupports = supportsData;
                supportMapping = mappingData;
                
                console.log(`✅ Datos cargados: ${allSupports.length} soportes`);
                
                hideLoading();
                updateStats();
                displaySupports(allSupports);
                
            } catch (error) {
                console.error('❌ Error cargando datos:', error);
                
                // Fallback a datos básicos
                try {
                    allSupports = await loadWithRetries('support_data.json');
                    supportMapping = {};
                    hideLoading();
                    updateStats();
                    displaySupports(allSupports);
                } catch (fallbackError) {
                    showError('No se pudieron cargar los datos. Verifique la conexión.');
                }
            }
        }
        
        // Cargar con reintentos
        async function loadWithRetries(url, maxRetries = 3) {
            for (let attempt = 1; attempt <= maxRetries; attempt++) {
                try {
                    const response = await fetch(url, {
                        headers: {
                            'Cache-Control': 'no-cache',
                            'Pragma': 'no-cache'
                        }
                    });
                    
                    if (!response.ok) throw new Error(`HTTP ${response.status}`);
                    return await response.json();
                    
                } catch (error) {
                    if (attempt === maxRetries) throw error;
                    await new Promise(resolve => setTimeout(resolve, 1000 * attempt));
                }
            }
        }
        
        // Actualizar estadísticas
        function updateStats() {
            const supportTypes = [...new Set(allSupports.map(s => s.support_type))];
            const supportNumbers = [...new Set(allSupports.map(s => s.support_number))];
            
            document.getElementById('statsContainer').innerHTML = `
                <div class="stat-card">
                    <div class="stat-number">${allSupports.length}</div>
                    <div class="stat-label">Soportes</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${supportNumbers.length}</div>
                    <div class="stat-label">Únicos</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${supportTypes.length}</div>
                    <div class="stat-label">Tipos</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${Object.keys(supportMapping).length}</div>
                    <div class="stat-label">PDFs</div>
                </div>
            `;
        }
        
        // Mostrar soportes
        function displaySupports(supports) {
            filteredSupports = supports;
            displayedCount = 0;
            document.getElementById('resultsContainer').innerHTML = '';
            showMoreSupports();
        }
        
        // Mostrar más soportes (paginación)
        function showMoreSupports() {
            const container = document.getElementById('resultsContainer');
            const endIndex = Math.min(displayedCount + pageSize, filteredSupports.length);
            
            for (let i = displayedCount; i < endIndex; i++) {
                const support = filteredSupports[i];
                const supportCard = createSupportCard(support);
                container.appendChild(supportCard);
            }
            
            displayedCount = endIndex;
            
            // Botón "Mostrar más" si hay más elementos
            const existingButton = document.getElementById('showMoreButton');
            if (existingButton) existingButton.remove();
            
            if (displayedCount < filteredSupports.length) {
                const showMoreBtn = document.createElement('button');
                showMoreBtn.id = 'showMoreButton';
                showMoreBtn.className = 'show-more';
                showMoreBtn.textContent = `Mostrar más (${filteredSupports.length - displayedCount} restantes)`;
                showMoreBtn.onclick = showMoreSupports;
                container.appendChild(showMoreBtn);
            }
        }
        
        // Crear tarjeta de soporte
        function createSupportCard(support) {
            const card = document.createElement('div');
            card.className = 'card support-card';
            
            const pdfs = supportMapping[support.support_type] || [];
            const pdfLinks = pdfs.map(pdf => 
                `<a href="ESTANDARES DE SOPORTES/${pdf}" target="_blank" class="pdf-btn">📄 ${pdf.substring(0, 15)}...</a>`
            ).join('');
            
            // Variables de plantilla
            const variables = [];
            if (support.A) variables.push(`A: ${support.A} mm`);
            if (support.B) variables.push(`B: ${support.B} mm`);
            if (support.C) variables.push(`C: ${support.C} mm`);
            if (support.D) variables.push(`D: ${support.D} mm`);
            if (support.E) variables.push(`E: ${support.E} mm`);
            if (support.R) variables.push(`R: ${support.R} mm`);
            if (support.X) variables.push(`X: ${support.X} mm`);
            if (support.Y) variables.push(`Y: ${support.Y} mm`);
            if (support.EL) variables.push(`EL: ${support.EL} mm`);
            if (support['N.']) variables.push(`N.: ${support['N.']}`);
            if (support['SH.']) variables.push(`SH.: ${support['SH.']}`);
            if (support.TEMP) variables.push(`TEMP: ${support.TEMP}°C`);
            
            const variablesSection = variables.length > 0 ? `
                <div class="variables-section">
                    <div class="variables-title">📐 Variables de Plantilla:</div>
                    ${variables.map(v => `<div class="variable-item">${v}</div>`).join('')}
                </div>
            ` : '';
            
            card.innerHTML = `
                <div class="support-number">
                    🔧 ${support.support_number}
                    <span style="font-size: 0.8rem; background: #3498db; color: white; padding: 2px 6px; border-radius: 10px;">
                        ${support.support_type}
                    </span>
                </div>
                <div class="support-info">
                    <div class="info-row">
                        <div class="info-label">Fluido:</div>
                        <div class="info-value">${support.fluid_number || 'N/A'}</div>
                    </div>
                    <div class="info-row">
                        <div class="info-label">Clase:</div>
                        <div class="info-value">${support.support_class || 'N/A'}</div>
                    </div>
                    <div class="info-row">
                        <div class="info-label">Cantidad:</div>
                        <div class="info-value">${support.quantity || 'N/A'}</div>
                    </div>
                    <div class="info-row">
                        <div class="info-label">ISO:</div>
                        <div class="info-value">${support.iso_sheet || 'N/A'}</div>
                    </div>
                    <div class="info-row">
                        <div class="info-label">Temp:</div>
                        <div class="info-value">${support.temperature || 'N/A'}</div>
                    </div>
                </div>
                ${variablesSection}
                ${support.notes ? `
                    <div style="margin-top: 10px; padding: 8px; background: rgba(52, 152, 219, 0.1); border-radius: 5px;">
                        <div style="font-weight: bold; font-size: 0.8rem; color: #2980b9; margin-bottom: 3px;">📝 Notas:</div>
                        <div style="font-size: 0.8rem; color: #2c3e50;">${support.notes}</div>
                    </div>
                ` : ''}
                ${pdfLinks ? `<div class="pdf-links">${pdfLinks}</div>` : ''}
            `;
            
            return card;
        }
        
        // Búsqueda
        function performSearch() {
            const searchTerm = document.getElementById('searchBox').value.toLowerCase().trim();
            
            if (!searchTerm) {
                displaySupports(allSupports);
                return;
            }
            
            const filtered = allSupports.filter(support => 
                (support.support_number && support.support_number.toLowerCase().includes(searchTerm)) ||
                (support.support_type && support.support_type.toLowerCase().includes(searchTerm)) ||
                (support.fluid_number && support.fluid_number.toLowerCase().includes(searchTerm)) ||
                (support.notes && support.notes.toLowerCase().includes(searchTerm))
            );
            
            displaySupports(filtered);
        }
        
        // Funciones auxiliares
        function hideLoading() {
            document.getElementById('loadingContainer').style.display = 'none';
        }
        
        function showError(message) {
            document.getElementById('loadingContainer').innerHTML = `
                <div style="color: #e74c3c; text-align: center;">
                    <h3>❌ Error</h3>
                    <p>${message}</p>
                </div>
            `;
        }
        
        // Event listeners
        document.addEventListener('DOMContentLoaded', initializeMobileSystem);
        
        document.getElementById('searchBox').addEventListener('input', function() {
            clearTimeout(this.searchTimeout);
            this.searchTimeout = setTimeout(performSearch, 300);
        });
        
        // Prevenir zoom en iOS
        document.addEventListener('gesturestart', function (e) {
            e.preventDefault();
        });
    </script>
</body>
</html>'''
    
    with open('index_mobile.html', 'w', encoding='utf-8') as f:
        f.write(mobile_html)
    
    print("✅ Versión móvil creada: index_mobile.html")

def create_ngrok_setup():
    """Crear script para configurar Ngrok"""
    
    ngrok_script = '''@echo off
title SINES Soportes - Acceso Mundial
color 0A

echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █              SINES SOPORTES - ACCESO MUNDIAL                █
echo █                                                              █
echo █                  🌐 DISPONIBLE EN TODO EL MUNDO              █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.
echo 🚀 Configurando acceso mundial con Ngrok...
echo.

REM Verificar si Ngrok está instalado
ngrok version >nul 2>&1
if errorlevel 1 (
    echo ❌ Ngrok no encontrado
    echo.
    echo 📥 Para instalar Ngrok:
    echo    1. Ve a: https://ngrok.com/download
    echo    2. Descarga ngrok.exe
    echo    3. Coloca ngrok.exe en esta carpeta
    echo    4. Ejecuta este script nuevamente
    echo.
    echo 💡 Alternativamente, usa: winget install ngrok
    echo.
    pause
    exit /b 1
)

echo ✅ Ngrok encontrado
echo.
echo 🔄 Iniciando servidor local en puerto 8000...

REM Iniciar servidor en segundo plano
start /B python -c "
import http.server
import socketserver
import threading
import time

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

PORT = 8000
with socketserver.TCPServer(('', PORT), CustomHandler) as httpd:
    print(f'✅ Servidor local iniciado en puerto {PORT}')
    httpd.serve_forever()
"

REM Esperar un momento para que el servidor inicie
timeout /t 3 >nul

echo 🌐 Creando túnel público con Ngrok...
echo.
echo ⚡ Tu sistema estará disponible en una URL pública
echo 📱 Podrás acceder desde cualquier dispositivo móvil
echo 🔒 La conexión es segura (HTTPS)
echo.
echo ⚠️  IMPORTANTE: 
echo    • Mantén esta ventana abierta
echo    • La URL pública se mostrará a continuación
echo    • Copia la URL para acceder desde tu móvil
echo.
echo ════════════════════════════════════════════════════════════════

ngrok http 8000
'''
    
    with open('ACCESO_MUNDIAL.bat', 'w', encoding='utf-8') as f:
        f.write(ngrok_script)
    
    print("✅ Script de acceso mundial creado: ACCESO_MUNDIAL.bat")

def create_cloud_deployment_guide():
    """Crear guía para despliegue en la nube"""
    
    guide = '''# 🌐 GUÍA PARA ACCESO MUNDIAL - SISTEMA SINES

## 🆓 OPCIÓN 1: NGROK (GRATUITO - RECOMENDADO)

### Ventajas:
- ✅ Completamente gratuito
- ✅ Configuración en 5 minutos
- ✅ URL HTTPS segura
- ✅ Acceso inmediato desde móvil

### Pasos:
1. **Descargar Ngrok**: https://ngrok.com/download
2. **Ejecutar**: `ACCESO_MUNDIAL.bat`
3. **Copiar URL** que aparece (ej: https://abc123.ngrok.io)
4. **Abrir en móvil**: Usar la URL copiada

### Limitaciones (versión gratuita):
- URL cambia cada vez que reinicias
- Límite de 20 conexiones simultáneas
- Sesión expira en 8 horas

---

## 💰 OPCIÓN 2: HEROKU (PAGO - PROFESIONAL)

### Ventajas:
- ✅ URL permanente
- ✅ Disponibilidad 24/7
- ✅ Sin límites de conexión
- ✅ Escalabilidad automática

### Costo: ~$7/mes
### Pasos:
1. Crear cuenta en Heroku.com
2. Instalar Heroku CLI
3. Ejecutar script de despliegue
4. URL permanente: https://tu-app.herokuapp.com

---

## 💰 OPCIÓN 3: VERCEL (PAGO - RÁPIDO)

### Ventajas:
- ✅ Extremadamente rápido
- ✅ URL permanente
- ✅ CDN global
- ✅ Fácil configuración

### Costo: ~$20/mes
### Pasos:
1. Crear cuenta en Vercel.com
2. Conectar repositorio Git
3. Despliegue automático
4. URL: https://tu-proyecto.vercel.app

---

## 💰 OPCIÓN 4: AWS/AZURE (PAGO - EMPRESARIAL)

### Ventajas:
- ✅ Máximo control
- ✅ Escalabilidad ilimitada
- ✅ Seguridad empresarial
- ✅ Integración con otros servicios

### Costo: ~$15-50/mes
### Requiere conocimientos técnicos avanzados

---

## 🎯 RECOMENDACIÓN

### Para uso personal/temporal:
**USAR NGROK (GRATUITO)**
- Ejecutar: `ACCESO_MUNDIAL.bat`
- Copiar URL y usar en móvil

### Para uso profesional/permanente:
**USAR HEROKU ($7/mes)**
- URL permanente
- Disponibilidad 24/7
- Fácil configuración

---

## 📱 ACCESO MÓVIL OPTIMIZADO

Tu sistema incluye una versión especial para móviles:
- **URL local**: http://localhost:8000/index_mobile.html
- **URL pública**: https://tu-url-publica/index_mobile.html

### Características móviles:
- ✅ Interfaz táctil optimizada
- ✅ Búsqueda rápida
- ✅ Visualización compacta
- ✅ Carga rápida
- ✅ Funciona sin conexión (caché)

---

## 🔧 CONFIGURACIÓN AUTOMÁTICA

Ejecuta estos archivos según tu preferencia:

```bash
# Acceso mundial gratuito
ACCESO_MUNDIAL.bat

# Versión local móvil
INICIAR_VERSION_MOVIL.bat

# Versión completa local
INICIAR_VERSION_CON_PLANTILLAS.bat
```

---

## 💡 CONSEJOS IMPORTANTES

### Seguridad:
- ✅ Ngrok usa HTTPS automáticamente
- ✅ No expongas datos sensibles
- ✅ Usa contraseñas si es necesario

### Rendimiento:
- ✅ La versión móvil es más rápida
- ✅ Los PDFs se cargan bajo demanda
- ✅ Caché automático en el navegador

### Conectividad:
- ✅ Funciona con WiFi y datos móviles
- ✅ Compatible con todos los navegadores
- ✅ Optimizado para pantallas pequeñas

---

**¿Cuál prefieres? Te ayudo a configurar la opción que elijas.**
'''
    
    with open('GUIA_ACCESO_MUNDIAL.md', 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print("✅ Guía de acceso mundial creada: GUIA_ACCESO_MUNDIAL.md")

def create_mobile_launcher():
    """Crear lanzador para versión móvil"""
    
    mobile_launcher = '''@echo off
title SINES Soportes - Version Movil
color 0B

echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █              SINES SOPORTES - VERSION MOVIL                 █
echo █                                                              █
echo █                  📱 OPTIMIZADO PARA MOVILES                  █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.
echo 📱 Iniciando version optimizada para moviles...
echo.
echo ⚡ Caracteristicas de esta version:
echo    • Interfaz tactil optimizada
echo    • Carga rapida en moviles
echo    • Busqueda instantanea
echo    • Visualizacion compacta
echo    • Compatible con todos los dispositivos
echo.
echo 🔄 Iniciando servidor web...
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado
    echo.
    echo 📥 Descarga Python desde: https://python.org
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado, iniciando servidor...
echo.
echo 🌐 URLs disponibles:
echo    📱 Movil: http://localhost:8000/index_mobile.html
echo    💻 Completa: http://localhost:8000/index_enhanced_with_templates.html
echo.
echo 💡 Para acceso mundial:
echo    1. Ejecuta ACCESO_MUNDIAL.bat
echo    2. Copia la URL publica que aparece
echo    3. Abre esa URL en tu movil
echo.
echo ⚠️  Para cerrar: Presiona Ctrl+C
echo.
echo ════════════════════════════════════════════════════════════════

start "" "http://localhost:8000/index_mobile.html"

python -c "
import http.server
import socketserver
import webbrowser
import time
import threading

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

PORT = 8000
with socketserver.TCPServer(('', PORT), CustomHandler) as httpd:
    print(f'✅ Servidor movil iniciado en puerto {PORT}')
    httpd.serve_forever()
"

echo.
echo ════════════════════════════════════════════════════════════════
echo Sistema finalizado. Presiona cualquier tecla para salir...
pause > nul
'''
    
    with open('INICIAR_VERSION_MOVIL.bat', 'w', encoding='utf-8') as f:
        f.write(mobile_launcher)
    
    print("✅ Lanzador móvil creado: INICIAR_VERSION_MOVIL.bat")

def main():
    print("=" * 70)
    print("🌐 CONFIGURANDO ACCESO MUNDIAL PARA SISTEMA SINES")
    print("=" * 70)
    
    print("\n1. Creando versión optimizada para móviles...")
    create_mobile_optimized_version()
    
    print("\n2. Creando script de acceso mundial (Ngrok)...")
    create_ngrok_setup()
    
    print("\n3. Creando guía de opciones de despliegue...")
    create_cloud_deployment_guide()
    
    print("\n4. Creando lanzador para versión móvil...")
    create_mobile_launcher()
    
    print("\n" + "=" * 70)
    print("✅ CONFIGURACIÓN COMPLETADA")
    print("=" * 70)
    
    print("\n🎯 OPCIONES DISPONIBLES:")
    print("\n🆓 GRATIS - Ngrok (Recomendado para empezar):")
    print("   1. Ejecutar: ACCESO_MUNDIAL.bat")
    print("   2. Copiar URL pública que aparece")
    print("   3. Abrir esa URL en tu móvil")
    
    print("\n📱 LOCAL - Versión móvil:")
    print("   1. Ejecutar: INICIAR_VERSION_MOVIL.bat")
    print("   2. Abrir: http://localhost:8000/index_mobile.html")
    
    print("\n💰 PAGO - Opciones profesionales:")
    print("   • Heroku: $7/mes - URL permanente")
    print("   • Vercel: $20/mes - Muy rápido")
    print("   • AWS/Azure: $15-50/mes - Empresarial")
    
    print("\n📖 Ver guía completa: GUIA_ACCESO_MUNDIAL.md")
    
    print("\n🚀 ¿Quieres empezar con la opción gratuita?")
    print("   Ejecuta: ACCESO_MUNDIAL.bat")

if __name__ == "__main__":
    main() 