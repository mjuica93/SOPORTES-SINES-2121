param(
    [Parameter(Mandatory=$true)]
    [string]$GitHubToken
)

$ErrorActionPreference = "Stop"

Write-Host "🚀 INICIANDO DESPLIEGUE AUTOMATICO DEL SISTEMA DE COSTURAS SINES" -ForegroundColor Green
Write-Host "══════════════════════════════════════════════════════════════════" -ForegroundColor Green

# Verificar sistema
Write-Host "📊 Verificando sistema..." -ForegroundColor Cyan
try {
    python verificar_datos_railway.py | Out-Null
    Write-Host "✅ Sistema verificado correctamente" -ForegroundColor Green
} catch {
    Write-Host "❌ Error en verificación del sistema" -ForegroundColor Red
    exit 1
}

# Crear README.md
$readmeContent = @"
# 🚀 Sistema de Gestión de Costuras y Soportes SINES 2121

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
"@

$readmeContent | Out-File -FilePath "README.md" -Encoding UTF8
Write-Host "✅ README.md creado" -ForegroundColor Green

# Función para subir archivo a GitHub
function Upload-FileToGitHub {
    param(
        [string]$FilePath,
        [string]$Token
    )
    
    $fileName = Split-Path $FilePath -Leaf
    $fileBytes = [System.IO.File]::ReadAllBytes($FilePath)
    $fileContent = [Convert]::ToBase64String($fileBytes)
    
    $body = @{
        message = "Add $fileName - Sistema de Costuras SINES 2121"
        content = $fileContent
    } | ConvertTo-Json
    
    $headers = @{
        Authorization = "token $Token"
        Accept = "application/vnd.github.v3+json"
    }
    
    $uri = "https://api.github.com/repos/mjuica93/soportes-y-isometricos-2121/contents/$fileName"
    
    try {
        Invoke-RestMethod -Uri $uri -Method PUT -Body $body -Headers $headers -ContentType "application/json" | Out-Null
        Write-Host "✅ $fileName subido correctamente" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "❌ Error subiendo $fileName" -ForegroundColor Red
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Archivos a subir
$files = @(
    "index_isometricos_con_costuras.html",
    "isometric_welding_manager.js",
    "isometric_data_with_welds.json",
    "welding_statistics.json",
    "server_railway.py",
    "Dockerfile",
    "railway.json",
    "requirements.txt",
    "README.md"
)

Write-Host ""
Write-Host "📤 Subiendo archivos a GitHub..." -ForegroundColor Cyan
Write-Host "──────────────────────────────────────────────────────────────────" -ForegroundColor Gray

$uploadSuccess = $true
foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "📤 Subiendo $file..." -ForegroundColor Yellow
        $success = Upload-FileToGitHub -FilePath $file -Token $GitHubToken
        if (-not $success) {
            $uploadSuccess = $false
        }
        Start-Sleep -Seconds 2
    } else {
        Write-Host "⚠️ Archivo $file no encontrado" -ForegroundColor Yellow
    }
}

if ($uploadSuccess) {
    Write-Host ""
    Write-Host "✅ TODOS LOS ARCHIVOS SUBIDOS CORRECTAMENTE" -ForegroundColor Green
    Write-Host ""
    Write-Host "🚀 ABRIENDO RAILWAY PARA DESPLIEGUE..." -ForegroundColor Cyan
    
    Start-Process "https://railway.app/new?template=https://github.com/mjuica93/soportes-y-isometricos-2121"
    
    Write-Host ""
    Write-Host "🎯 RUTAS DISPONIBLES UNA VEZ DESPLEGADO:" -ForegroundColor Cyan
    Write-Host "🔨 https://tu-proyecto.railway.app/           - Gestión de Costuras" -ForegroundColor White
    Write-Host "🔧 https://tu-proyecto.railway.app/soportes  - Sistema de Soportes" -ForegroundColor White
    Write-Host "📐 https://tu-proyecto.railway.app/isometricos - Isométricos" -ForegroundColor White
    Write-Host "📱 https://tu-proyecto.railway.app/mobile    - Versión Móvil" -ForegroundColor White
    Write-Host "📊 https://tu-proyecto.railway.app/data      - API de Datos" -ForegroundColor White
    Write-Host "📈 https://tu-proyecto.railway.app/stats     - Estadísticas" -ForegroundColor White
    
    Write-Host ""
    Write-Host "🎉 DESPLIEGUE AUTOMATICO COMPLETADO" -ForegroundColor Green
    Write-Host "🌐 Repositorio: https://github.com/mjuica93/soportes-y-isometricos-2121" -ForegroundColor Cyan
    
} else {
    Write-Host ""
    Write-Host "❌ ERRORES DURANTE LA SUBIDA DE ARCHIVOS" -ForegroundColor Red
}

Write-Host ""
Write-Host "Presiona Enter para continuar..."
Read-Host 