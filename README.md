# 🏗️ SISTEMA SINES v4.0 - Control de Costuras Mejorado

Sistema integral para gestión de soportes, isométricos y control de soldadura con funcionalidades avanzadas para trabajo en campo.

## ✨ Nuevas Funcionalidades v4.0

### 🔧 **Control de Costuras Mejorado para Campo**
- **Visualización en tabla de filas** con información completa
- **Selección múltiple** con checkboxes para procesamiento masivo
- **Estadísticas en tiempo real** con contadores dinámicos
- **Acciones rápidas** para cambios de estado masivos
- **Interfaz optimizada** para dispositivos móviles y tablets
- **Auto-guardado** y confirmaciones visuales

### 📊 **Gestión Avanzada de Estados**
- **5 estados de soldadura**: Pendiente, En Progreso, Completada, En Inspección, Rechazada
- **Progreso visual** con círculos de colores dinámicos
- **Comentarios por costura** con guardado automático al presionar Enter
- **Filtros inteligentes** por estado, diámetro y búsqueda
- **Procesamiento masivo** de costuras seleccionadas

### 🛡️ **Sistema de Seguridad Completo**
- **Autenticación obligatoria** para todos los accesos
- **4 niveles de usuario**: Administrador, Supervisor, Operador, Usuario
- **Gestión de sesiones** con timeout automático (30 minutos)
- **Protección contra ataques** con bloqueo temporal de IP
- **Headers de seguridad** HTTP completos

## 🚀 Características Principales

### 📋 **Gestión de Soportes**
- **22,612 soportes** organizados y agrupados
- **Vista individual y agrupada** con alternador
- **Variables de plantilla** (A, B, C, D, E, R, X, Y, EL, N., SH., TEMP)
- **Mapeo Excel T22-T23** a dimensiones técnicas
- **Filtros avanzados** por tipo, dimensiones y contenido

### 📐 **Sistema de Isométricos**
- **1,770 isométricos regulares** + **427 prefabricados**
- **Visualización PDF integrada** con enlaces directos
- **Sistema de relaciones** soportes-isométricos
- **Búsqueda inteligente** por código de línea
- **Estadísticas de completado** por isométrico

### ⚡ **Control de Soldadura**
- **3,982 relaciones** entre soldadura e isométricos
- **Gestión de costuras** con estados dinámicos
- **Progreso por línea** con barras visuales
- **Exportación de datos** de soldadura
- **Trazabilidad completa** del proceso

### 🔗 **Gestión de Instalaciones**
- **Fechas de instalación** planificadas y reales
- **Estados de progreso** por soporte
- **Reportes de avance** por área
- **Integración con cronogramas** de obra

## 🔐 Credenciales de Acceso

| Usuario | Contraseña | Rol | Permisos |
|---------|------------|-----|----------|
| `admin` | `sines2024` | Administrador | Acceso completo + panel de configuración |
| `supervisor` | `super2024` | Supervisor | Gestión de costuras + reportes |
| `operador` | `op2024` | Operador | Control de campo + actualización de estados |
| `sines` | `sines123` | Usuario | Consulta y visualización |

## 🌐 Despliegue

### **Railway (Producción)**
```bash
# Configuración automática
git push origin main
# Railway detecta cambios y despliega automáticamente
```

### **Local (Desarrollo)**
```bash
# Servidor seguro completo
python server_secure_complete.py

# Servidor Railway (testing)
python server_railway.py
```

## 📱 Acceso al Sistema

### **URLs Principales**
- **Sistema Integrado**: `/` o `/sistema-integrado`
- **Versión Móvil**: `/mobile`
- **Versión Básica**: `/basico`
- **API Status**: `/api/status`
- **Health Check**: `/health`

### **Funcionalidades por Pestaña**
1. **📋 Soportes**: Vista agrupada con variables de plantilla
2. **📐 Isométricos**: Gestión completa con prefabricados
3. **🔗 Relaciones**: Vínculos soportes-isométricos
4. **⚡ Soldadura**: Control de costuras mejorado
5. **🔧 Instalaciones**: Gestión de fechas y progreso

## 🔧 Uso del Control de Costuras

### **Para Supervisores de Campo**
1. **Acceder a pestaña Soldadura**
2. **Filtrar por línea** o estado
3. **Seleccionar costuras** con checkboxes
4. **Usar acciones rápidas** para cambios masivos
5. **Monitorear estadísticas** en tiempo real

### **Cambio Individual de Estado**
1. **Seleccionar estado** en dropdown
2. **Agregar comentario** (opcional)
3. **Presionar Enter** o botón guardar
4. **Verificar confirmación** visual

### **Procesamiento Masivo**
1. **Marcar múltiples costuras** con checkboxes
2. **Clic en "Procesar Seleccionadas"**
3. **Elegir acción**: Completar, En Progreso, Inspección
4. **Confirmar cambios** automáticos

## 📊 Estadísticas del Sistema

- **📋 Soportes**: 22,612 elementos
- **📐 Isométricos**: 1,770 regulares + 427 prefabricados
- **⚡ Costuras**: 3,982 relaciones de soldadura
- **🔗 Relaciones**: Mapeo completo soportes-isométricos
- **📏 Variables**: 12 variables de plantilla técnicas
- **🛡️ Seguridad**: Sistema completo con 4 niveles de acceso

## 🔄 Actualizaciones v4.0

### **Mejoras de Interfaz**
- ✅ Tabla de costuras con filas clickeables
- ✅ Selección múltiple con checkboxes
- ✅ Estadísticas en tiempo real
- ✅ Progreso visual con círculos de colores
- ✅ Responsive design para móviles

### **Funcionalidades de Campo**
- ✅ Botones de acción rápida
- ✅ Auto-guardado con Enter
- ✅ Comentarios por costura
- ✅ Procesamiento masivo
- ✅ Notificaciones visuales

### **Seguridad y Estabilidad**
- ✅ Autenticación obligatoria
- ✅ Gestión de sesiones
- ✅ Protección contra ataques
- ✅ Headers de seguridad HTTP
- ✅ Logs de eventos

## 📝 Notas Técnicas

### **Tecnologías Utilizadas**
- **Backend**: Python 3.11+ (librerías estándar)
- **Frontend**: HTML5, CSS3, JavaScript ES6+
- **UI Framework**: Bootstrap 5.1.3
- **Iconos**: Font Awesome 6.0.0
- **Despliegue**: Railway.app

### **Estructura de Archivos**
```
├── index_isometricos_integrado_final.html  # Sistema principal
├── server_secure_complete.py               # Servidor local seguro
├── server_railway.py                       # Servidor para Railway
├── support_data_enhanced.json              # Datos de soportes
├── welding_enhanced_data.json              # Datos de soldadura
├── template_variables_mapping.json         # Variables de plantilla
├── logout_manager.js                       # Gestión de sesiones
└── welding_status_manager.js               # Control de costuras
```

### **APIs Disponibles**
- `GET /api/status` - Estado del sistema
- `POST /api/login` - Autenticación
- `POST /api/logout` - Cierre de sesión
- `GET /api/validate_session` - Validar sesión
- `GET /api/user-info` - Información del usuario

## 🤝 Soporte

Para soporte técnico o reportar problemas:
1. Verificar logs del servidor
2. Revisar estado de autenticación
3. Confirmar archivos JSON presentes
4. Validar permisos de usuario

---

**Sistema SINES v4.0** - Control de Costuras Mejorado  
*Desarrollado para optimizar el trabajo de supervisión en campo*
