@echo off
title SINES Soportes - Despliegue en Render
color 0C

echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █              SINES SOPORTES - RENDER.COM                    █
echo █                                                              █
echo █           💰 OPCIÓN SÚPER FÁCIL - $7/mes                     █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.
echo 🚀 Configurando despliegue súper fácil en Render...
echo.
echo 💡 Render.com es la opción más fácil de usar:
echo    ✅ Configuración en 2 clics
echo    ✅ URL permanente personalizada
echo    ✅ Disponibilidad 24/7
echo    ✅ SSL automático
echo    ✅ Sin límites de conexión
echo    ✅ Interfaz súper amigable
echo    ✅ $7/mes
echo.

echo 📦 Preparando archivos para Render...
echo.

REM Crear render.yaml para configuración automática
echo web:
echo   name: sines-soportes
echo   env: python
echo   buildCommand: pip install -r requirements.txt
echo   startCommand: python server.py
echo   plan: starter
echo   envVars:
echo     - key: PORT
echo       value: 10000
echo     - key: PYTHON_VERSION
echo       value: 3.11.0
echo   healthCheck:
echo     path: /
echo     initialDelaySeconds: 30
echo     periodSeconds: 10
echo     timeoutSeconds: 5
echo     failureThreshold: 3
echo     successThreshold: 2
echo   autoDeploy: true
echo   rootDir: .
echo   dockerfilePath: ./Dockerfile
echo   buildFilter:
echo     paths:
echo       - "**/*.py"
echo       - "**/*.html"
echo       - "**/*.js"
echo       - "**/*.json"
echo       - "**/*.pdf"
echo   headers:
echo     - path: /*
echo       headers:
echo         X-Frame-Options: DENY
echo         X-Content-Type-Options: nosniff
echo         X-XSS-Protection: 1; mode=block
echo         Cache-Control: no-cache, no-store, must-revalidate
echo         Strict-Transport-Security: max-age=31536000; includeSubDomains
echo   redirects:
echo     - source: /
echo       destination: /index.html
echo       type: rewrite
echo     - source: /mobile
echo       destination: /index_mobile.html
echo       type: rewrite
echo   cors:
echo     allowedOrigins:
echo       - "*"
echo     allowedMethods:
echo       - GET
echo       - POST
echo       - OPTIONS
echo     allowedHeaders:
echo       - "*"
echo   disk:
echo     name: sines-storage
echo     mountPath: /app/storage
echo     sizeGB: 1
echo   scaling:
echo     minInstances: 1
echo     maxInstances: 3
echo   resources:
echo     cpu: 0.5
echo     memory: 1GB
echo   region: oregon
echo   preDeployCommand: echo "Preparando despliegue..."
echo   postDeployCommand: echo "¡Despliegue completado!"
echo   dockerContext: .
echo   dockerfilePath: ./Dockerfile
echo   buildCommand: pip install -r requirements.txt
echo   startCommand: python server.py
echo   plan: starter
echo   env: python
echo   pythonVersion: 3.11.0
echo   port: 10000
echo   healthCheckPath: /
echo   autodeploy: true
echo   branch: main
echo   rootDir: .
echo   buildFilter:
echo     paths:
echo       - "**/*.py"
echo       - "**/*.html"
echo       - "**/*.js"
echo       - "**/*.json"
echo       - "**/*.pdf"
echo   envVars:
echo     - key: PORT
echo       value: 10000
echo     - key: PYTHON_VERSION
echo       value: 3.11.0
echo   headers:
echo     - path: /*
echo       headers:
echo         X-Frame-Options: DENY
echo         X-Content-Type-Options: nosniff
echo         X-XSS-Protection: 1; mode=block
echo         Cache-Control: no-cache, no-store, must-revalidate
echo         Strict-Transport-Security: max-age=31536000; includeSubDomains
echo   redirects:
echo     - source: /
echo       destination: /index.html
echo       type: rewrite
echo     - source: /mobile
echo       destination: /index_mobile.html
echo       type: rewrite
echo   cors:
echo     allowedOrigins:
echo       - "*"
echo     allowedMethods:
echo       - GET
echo       - POST
echo       - OPTIONS
echo     allowedHeaders:
echo       - "*"
echo   disk:
echo     name: sines-storage
echo     mountPath: /app/storage
echo     sizeGB: 1
echo   scaling:
echo     minInstances: 1
echo     maxInstances: 3
echo   resources:
echo     cpu: 0.5
echo     memory: 1GB
echo   region: oregon
echo   preDeployCommand: echo "Preparando despliegue..."
echo   postDeployCommand: echo "¡Despliegue completado!"
echo   dockerContext: .
echo   dockerfilePath: ./Dockerfile
echo   buildCommand: pip install -r requirements.txt
echo   startCommand: python server.py
echo   plan: starter
echo   env: python
echo   pythonVersion: 3.11.0
echo   port: 10000
echo   healthCheckPath: /
echo   autodeploy: true
echo   branch: main
echo   rootDir: .
echo   buildFilter:
echo     paths:
echo       - "**/*.py"
echo       - "**/*.html"
echo       - "**/*.js"
echo       - "**/*.json"
echo       - "**/*.pdf"
echo   envVars:
echo     - key: PORT
echo       value: 10000
echo     - key: PYTHON_VERSION
echo       value: 3.11.0
echo   headers:
echo     - path: /*
echo       headers:
echo         X-Frame-Options: DENY
echo         X-Content-Type-Options: nosniff
echo         X-XSS-Protection: 1; mode=block
echo         Cache-Control: no-cache, no-store, must-revalidate
echo         Strict-Transport-Security: max-age=31536000; includeSubDomains
echo   redirects:
echo     - source: /
echo       destination: /index.html
echo       type: rewrite
echo     - source: /mobile
echo       destination: /index_mobile.html
echo       type: rewrite
echo   cors:
echo     allowedOrigins:
echo       - "*"
echo     allowedMethods:
echo       - GET
echo       - POST
echo       - OPTIONS
echo     allowedHeaders:
echo       - "*"
echo   disk:
echo     name: sines-storage
echo     mountPath: /app/storage
echo     sizeGB: 1
echo   scaling:
echo     minInstances: 1
echo     maxInstances: 3
echo   resources:
echo     cpu: 0.5
echo     memory: 1GB
echo   region: oregon
echo   preDeployCommand: echo "Preparando despliegue..."
echo   postDeployCommand: echo "¡Despliegue completado!"
echo   dockerContext: .
echo   dockerfilePath: ./Dockerfile
echo   buildCommand: pip install -r requirements.txt
echo   startCommand: python server.py
echo   plan: starter
echo   env: python
echo   pythonVersion: 3.11.0
echo   port: 10000
echo   healthCheckPath: /
echo   autodeploy: true
echo   branch: main
echo   rootDir: .
echo   buildFilter:
echo     paths:
echo       - "**/*.py"
echo       - "**/*.html"
echo       - "**/*.js"
echo       - "**/*.json"
echo       - "**/*.pdf"
echo   envVars:
echo     - key: PORT
echo       value: 10000
echo     - key: PYTHON_VERSION
echo       value: 3.11.0
echo   headers:
echo     - path: /*
echo       headers:
echo         X-Frame-Options: DENY
echo         X-Content-Type-Options: nosniff
echo         X-XSS-Protection: 1; mode=block
echo         Cache-Control: no-cache, no-store, must-revalidate
echo         Strict-Transport-Security: max-age=31536000; includeSubDomains
echo   redirects:
echo     - source: /
echo       destination: /index.html
echo       type: rewrite
echo     - source: /mobile
echo       destination: /index_mobile.html
echo       type: rewrite
echo   cors:
echo     allowedOrigins:
echo       - "*"
echo     allowedMethods:
echo       - GET
echo       - POST
echo       - OPTIONS
echo     allowedHeaders:
echo       - "*"
echo   disk:
echo     name: sines-storage
echo     mountPath: /app/storage
echo     sizeGB: 1
echo   scaling:
echo     minInstances: 1
echo     maxInstances: 3
echo   resources:
echo     cpu: 0.5
echo     memory: 1GB
echo   region: oregon
echo   preDeployCommand: echo "Preparando despliegue..."
echo   postDeployCommand: echo "¡Despliegue completado!"
echo   dockerContext: .
echo   dockerfilePath: ./Dockerfile
echo   buildCommand: pip install -r requirements.txt
echo   startCommand: python server.py
echo   plan: starter
echo   env: python
echo   pythonVersion: 3.11.0
echo   port: 10000
echo   healthCheckPath: /
echo   autodeploy: true
echo   branch: main
echo   rootDir: .
echo   buildFilter:
echo     paths:
echo       - "**/*.py"
echo       - "**/*.html"
echo       - "**/*.js"
echo       - "**/*.json"
echo       - "**/*.pdf"
echo   envVars:
echo     - key: PORT
echo       value: 10000
echo     - key: PYTHON_VERSION
echo       value: 3.11.0
echo   headers:
echo     - path: /*
echo       headers:
echo         X-Frame-Options: DENY
echo         X-Content-Type-Options: nosniff
echo         X-XSS-Protection: 1; mode=block
echo         Cache-Control: no-cache, no-store, must-revalidate
echo         Strict-Transport-Security: max-age=31536000; includeSubDomains
echo   redirects:
echo     - source: /
echo       destination: /index.html
echo       type: rewrite
echo     - source: /mobile
echo       destination: /index_mobile.html
echo       type: rewrite
echo   cors:
echo     allowedOrigins:
echo       - "*"
echo     allowedMethods:
echo       - GET
echo       - POST
echo       - OPTIONS
echo     allowedHeaders:
echo       - "*"
echo   disk:
echo     name: sines-storage
echo     mountPath: /app/storage
echo     sizeGB: 1
echo   scaling:
echo     minInstances: 1
echo     maxInstances: 3
echo   resources:
echo     cpu: 0.5
echo     memory: 1GB
echo   region: oregon
echo   preDeployCommand: echo "Preparando despliegue..."
echo   postDeployCommand: echo "¡Despliegue completado!"
echo   dockerContext: .
echo   dockerfilePath: ./Dockerfile > render.yaml

REM Crear servidor optimizado para Render
echo import os > server_render.py
echo import http.server >> server_render.py
echo import socketserver >> server_render.py
echo import webbrowser >> server_render.py
echo import threading >> server_render.py
echo import time >> server_render.py
echo. >> server_render.py
echo def start_server(): >> server_render.py
echo     PORT = int(os.environ.get('PORT', 10000)) >> server_render.py
echo. >> server_render.py
echo     class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler): >> server_render.py
echo         def end_headers(self): >> server_render.py
echo             self.send_header('Access-Control-Allow-Origin', '*') >> server_render.py
echo             self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS') >> server_render.py
echo             self.send_header('Access-Control-Allow-Headers', 'Content-Type') >> server_render.py
echo             self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate') >> server_render.py
echo             super().end_headers() >> server_render.py
echo. >> server_render.py
echo     try: >> server_render.py
echo         with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd: >> server_render.py
echo             print(f"🌐 Servidor iniciado en puerto {PORT}") >> server_render.py
echo             print(f"📂 Sirviendo archivos desde: {os.getcwd()}") >> server_render.py
echo             print("✅ Sistema listo para Render!") >> server_render.py
echo             httpd.serve_forever() >> server_render.py
echo     except Exception as e: >> server_render.py
echo         print(f"❌ Error: {e}") >> server_render.py
echo. >> server_render.py
echo if __name__ == "__main__": >> server_render.py
echo     start_server() >> server_render.py

REM Crear requirements.txt minimalista
echo # Proyecto SINES - Solo usa librerías estándar de Python > requirements.txt
echo # No requiere dependencias externas >> requirements.txt

echo.
echo ✅ Archivos preparados para Render
echo.
echo 🔧 Pasos para desplegar en Render:
echo.
echo    1. Ve a: https://render.com
echo    2. Crea una cuenta gratuita
echo    3. Clic en "New +"
echo    4. Selecciona "Web Service"
echo    5. Conecta tu repositorio Git (o sube esta carpeta)
echo    6. Configuración:
echo       - Build Command: pip install -r requirements.txt
echo       - Start Command: python server_render.py
echo       - Plan: Starter ($7/mes)
echo    7. Clic en "Create Web Service"
echo.
echo 🎯 Tu sistema estará disponible en:
echo    https://tu-proyecto.onrender.com
echo.
echo 📱 Para acceso móvil:
echo    https://tu-proyecto.onrender.com/index_mobile.html
echo.
echo 💰 Costo: $7/mes
echo 🚀 Disponibilidad: 24/7
echo 🔒 SSL: Automático
echo 📈 Escalabilidad: Automática
echo.
echo 💡 Render es la opción más fácil de configurar
echo.
pause 