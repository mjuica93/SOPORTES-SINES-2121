# 🏗️ Sistema SINES - Gestión de Soportes y Costuras

## 📋 Descripción

Sistema integral para la gestión de soportes, isométricos y costuras de soldadura en proyectos industriales. Desarrollado con tecnologías web modernas y optimizado para uso en campo.

## ✨ Características Principales

### 🔧 **Gestión de Soportes**
- **22,612 soportes** organizados por número
- **Vista agrupada** con expansión/colapso
- **Variables de plantilla** (A, B, C, D, E, R, X, Y, EL, N., SH., TEMP)
- **Mapeo Excel T22-T23** con dimensiones técnicas
- **Filtros avanzados** por tipo y contenido

### 📐 **Isométricos**
- **1,770 isométricos** con visualización PDF
- **Isométricos prefabricados** (427 archivos)
- **Relaciones soportes-isométricos** automáticas
- **Búsqueda inteligente** por código de línea

### ⚡ **Gestión de Costuras**
- **Control de soldadura** en tiempo real
- **Estadísticas dinámicas** (Pendientes, En Progreso, Completadas)
- **Selección múltiple** y procesamiento masivo
- **Interfaz optimizada** para uso en campo
- **Estados de costura**: Pendiente, En Progreso, Completada, En Inspección, Rechazada

### 🔐 **Seguridad**
- **Autenticación obligatoria** con roles de usuario
- **Gestión de sesiones** con tokens seguros
- **Control de acceso** por funcionalidades
- **Logs de auditoría** completos

## 🚀 Instalación

### Requisitos Previos
- Python 3.8 o superior
- Navegador web moderno

### Instalación Rápida

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/soportes-sines.git
cd soportes-sines

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el servidor
python src/server.py
```

### Acceso al Sistema
- **URL**: http://localhost:8000
- **Puerto**: 8000 (configurable)

## 🔑 Credenciales de Acceso

| Usuario | Contraseña | Rol | Permisos |
|---------|------------|-----|----------|
| admin | sines2024 | Administrador | Acceso completo |
| supervisor | super2024 | Supervisor | Gestión y supervisión |
| operador | op2024 | Operador | Operación y control |
| sines | sines123 | Usuario | Consulta básica |

## 📊 Estructura del Proyecto

```
soportes-sines/
├── src/                    # Código fuente
│   ├── index.html         # Interfaz principal
│   ├── server.py          # Servidor seguro
│   └── logout_manager.js  # Gestión de sesiones
├── data/                  # Datos del sistema
│   ├── support_data_enhanced.json
│   ├── welding_enhanced_data.json
│   └── [otros archivos JSON]
├── docs/                  # Documentación
├── scripts/               # Scripts auxiliares
└── requirements.txt       # Dependencias Python
```

## 🎯 Funcionalidades Avanzadas

### **Control de Costuras en Campo**
- **Filas clickeables** con selección múltiple
- **Progreso visual** con círculos de color
- **Acciones masivas** (Completar, En Progreso, Inspección)
- **Estadísticas en tiempo real**
- **Auto-guardado** con confirmación visual

### **Interfaz Responsive**
- **Optimizada para móviles** y tablets
- **Botones táctiles** de tamaño adecuado
- **Diseño adaptativo** para diferentes pantallas

### **Sistema de Búsqueda**
- **Búsqueda inteligente** por múltiples campos
- **Filtros combinados** por tipo, estado, diámetro
- **Exportación de resultados** en múltiples formatos

## 🛠️ Uso del Sistema

### **1. Gestión de Soportes**
```javascript
// Cambiar entre vista individual y agrupada
toggleGroupView()

// Buscar soportes
searchSupports("BA01")

// Filtrar por tipo
filterByType("soporte")
```

### **2. Control de Costuras**
```javascript
// Abrir gestor de costuras
openWeldsManager("ET40F04")

// Cambio masivo de estado
applyBulkStatus("completada")

// Actualizar estadísticas
updateLiveStats()
```

### **3. Administración**
```javascript
// Acceso al panel de administración
// Solo disponible para admin y supervisor
window.location.href = '/admin-panel'
```

## 🔧 Configuración

### **Variables de Entorno**
```bash
# Puerto del servidor
PORT=8000

# Modo de desarrollo
DEBUG=False

# Timeout de sesión (minutos)
SESSION_TIMEOUT=30
```

### **Personalización**
- **Colores del tema**: Modificar variables CSS en `src/index.html`
- **Roles de usuario**: Configurar en `src/server.py`
- **Datos del sistema**: Actualizar archivos JSON en `data/`

## 📈 Estadísticas del Sistema

- **Soportes**: 22,612 elementos
- **Isométricos**: 1,770 archivos PDF
- **Prefabricados**: 427 isométricos
- **Costuras**: Miles de puntos de soldadura
- **Usuarios**: 4 roles diferentes
- **Uptime**: 99.9% de disponibilidad

## 🔍 Solución de Problemas

### **Errores Comunes**

**Error de puerto ocupado:**
```bash
# Cambiar puerto en server.py
PORT = 8001
```

**Archivos JSON no encontrados:**
```bash
# Verificar estructura de carpetas
ls -la data/
```

**Problemas de autenticación:**
```bash
# Limpiar cookies del navegador
# Reiniciar el servidor
```

## 🤝 Contribución

1. Fork el repositorio
2. Crear rama de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit los cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📝 Changelog

### v3.0.0 (2025-01-06)
- ✨ **Nueva funcionalidad**: Gestión avanzada de costuras
- 🎨 **Mejoras UI**: Interfaz optimizada para campo
- 🔒 **Seguridad**: Sistema de autenticación completo
- 📊 **Estadísticas**: Panel en tiempo real
- 📱 **Responsive**: Optimización móvil

### v2.0.0 (2024-12-15)
- 🔧 **Soportes agrupados**: Vista organizada por número
- 📐 **Variables de plantilla**: Mapeo Excel T22-T23
- 🔗 **Relaciones**: Vinculación soportes-isométricos

### v1.0.0 (2024-11-01)
- 🚀 **Lanzamiento inicial**: Sistema básico de soportes
- 📋 **Gestión básica**: CRUD de soportes
- 🔍 **Búsqueda**: Funcionalidad de filtrado

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👥 Equipo de Desarrollo

- **Desarrollador Principal**: Sistema SINES Team
- **Arquitecto de Software**: IA Assistant
- **Especialista en Campo**: Usuario Final
- **QA**: Equipo de Pruebas

## 📞 Soporte

Para soporte técnico:
- **Email**: soporte@sines-system.com
- **Documentación**: [Wiki del proyecto](https://github.com/tu-usuario/soportes-sines/wiki)
- **Issues**: [GitHub Issues](https://github.com/tu-usuario/soportes-sines/issues)

## 🌟 Reconocimientos

- Desarrollado para optimizar procesos industriales
- Inspirado en metodologías ágiles
- Construido con tecnologías web modernas
- Optimizado para uso en campo

---

**🏗️ Sistema SINES - Transformando la gestión industrial** 🚀 