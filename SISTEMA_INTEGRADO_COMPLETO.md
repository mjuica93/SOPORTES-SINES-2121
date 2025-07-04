# Sistema Integrado SINES v3.0 - Documentación Completa

## 🎯 Descripción General

El **Sistema Integrado SINES v3.0** es una solución completa que unifica la gestión de soportes, isométricos, relaciones e instalaciones en una sola plataforma web optimizada. Proporciona **trazabilidad completa** y **control de progreso** para proyectos de soportación industrial.

### ✨ Características Principales

- 📋 **Gestión de Soportes**: Base de datos completa con PDFs de estándares
- 📐 **Visualización de Isométricos**: Acceso directo a planos por líneas de proceso
- 🔗 **Relaciones Integradas**: Conexión automática soportes ↔ isométricos
- 🔧 **Control de Instalaciones**: Seguimiento de fechas, estados y responsables
- 📊 **Trazabilidad Completa**: Seguimiento desde diseño hasta instalación
- ⚡ **Rendimiento Optimizado**: Paginación inteligente (12 resultados por página)

## 🚀 Instalación y Inicio

### Inicio Rápido
```bash
# Ejecutar el archivo de instalación
INICIAR_SISTEMA_INTEGRADO.bat
```

### Acceso al Sistema
- **URL Local**: http://localhost:8080/index_isometricos_con_costuras.html
- **Puerto**: 8080 (configurable)
- **Navegadores**: Chrome, Firefox, Edge (recomendado)

## 📱 Interfaz de Usuario

### Estructura de Pestañas

#### 1. 📋 **Pestaña Soportes**
Gestión completa de soportes con información de instalación integrada.

**Funcionalidades:**
- Búsqueda por número, tipo o línea de proceso
- Filtros por tipo de soporte y línea
- Enlaces directos a PDFs de estándares
- **Estado de instalación** en tiempo real
- **Control de instalación** directo desde cada soporte
- Enlaces a isométricos relacionados

**Información Mostrada:**
- Número y tipo de soporte
- Línea de proceso (fluid_piping)
- Posición, cantidad, clase material
- Estado de instalación con indicadores visuales
- Fechas planificadas y reales
- Responsable de instalación
- Notas de instalación

#### 2. 📐 **Pestaña Isométricos**
Visualización y acceso a planos isométricos por líneas de proceso.

**Funcionalidades:**
- Búsqueda por línea, fluido o archivo
- Filtros por tipo de fluido y tipo (LB/SB)
- Acceso directo a archivos PDF
- Información de revisiones y hojas

**Información Mostrada:**
- Código de línea y fluido
- Número total de hojas
- Tipos de planos (LB/SB)
- Revisiones disponibles
- Enlaces directos a PDFs

#### 3. 🔗 **Pestaña Relaciones**
Vista integrada de las conexiones entre soportes e isométricos.

**Funcionalidades:**
- Búsqueda por soporte, línea o fluido
- Filtros por tipo de soporte y fluido
- Vista agrupada por soporte
- Trazabilidad completa

**Información Mostrada:**
- Soporte con tipo
- Línea de proceso y fluido
- Hoja de isométrico (iso_sheet)
- Archivos PDF relacionados

#### 4. 🔧 **Pestaña Instalaciones** *(NUEVO)*
Control completo del progreso de instalaciones.

**Funcionalidades:**
- Búsqueda por soporte, tipo o responsable
- Filtros por estado de instalación
- Filtros por fecha (planificada o real)
- Exportación de datos a CSV
- Control de estados y fechas

**Estados de Instalación:**
- ⏳ **Pendiente**: No planificado
- 📅 **Planificado**: Fecha programada
- 🔄 **En Progreso**: Instalación iniciada
- ✅ **Instalado**: Completado

**Información Mostrada:**
- Estado actual con indicadores visuales
- Fechas planificadas y reales
- Responsable de instalación
- Notas y observaciones
- Línea y posición del soporte

## 🔧 Gestión de Instalaciones

### Actualización de Estados

#### Instalación Rápida
1. Desde cualquier tarjeta de soporte
2. Hacer clic en "✅ Marcar Instalado"
3. Ingresar nombre del responsable
4. El sistema actualiza automáticamente

#### Edición Detallada
1. Hacer clic en "✏️ Editar" en cualquier soporte
2. Se abre modal con campos completos:
   - Estado de instalación
   - Fecha planificada
   - Fecha real de instalación
   - Responsable
   - Notas detalladas

### Trazabilidad Completa

El sistema proporciona trazabilidad completa desde el diseño hasta la instalación:

```
Soporte → Línea de Proceso → Isométrico → Instalación
   ↓           ↓              ↓            ↓
 Tipo      Fluido          Planos      Estado
 PDFs      Revisión        Hojas      Fechas
Position   CWA             Archivo    Responsable
```

### Exportación de Datos

**Desde Pestaña Instalaciones:**
- Botón "📊 Exportar"
- Formato CSV con todos los campos
- Compatible con Excel
- Incluye fechas, estados, responsables y notas

## 📊 Estadísticas en Tiempo Real

### Dashboard de Métricas

Cada pestaña muestra estadísticas actualizadas:

#### Soportes
- Total de soportes en sistema
- Tipos diferentes disponibles
- Soportes con PDFs asociados
- Resultados de búsqueda actual

#### Isométricos
- Total de líneas de proceso
- Total de hojas de planos
- Archivos PDF disponibles
- Resultados filtrados

#### Relaciones
- Total de relaciones establecidas
- Líneas con soportes asociados
- Soportes con isométricos
- Cobertura de relaciones

#### Instalaciones
- Total de instalaciones
- Instalaciones pendientes
- Instalaciones completadas
- Resultados de búsqueda

## ⚡ Optimizaciones de Rendimiento

### Sistema de Paginación
- **12 resultados por página** (optimizado para rendimiento)
- Navegación con botones "Anterior/Siguiente"
- Información de página actual
- Carga bajo demanda (no automática)

### Búsqueda Optimizada
- Búsqueda **no automática** - requiere clic en "Buscar"
- Filtros combinables
- Resultados instantáneos una vez ejecutada
- Botón "Limpiar" para resetear filtros

### Características Técnicas
- **Carga asíncrona** de datos JSON
- **Memoria inteligente** para instalaciones (localStorage)
- **Actualización en tiempo real** de estadísticas
- **Diseño responsivo** para móviles y tablets

## 💾 Almacenamiento de Datos

### Datos de Instalaciones
- **Persistencia automática** en localStorage del navegador
- **Sin pérdida de datos** al cerrar/reabrir navegador
- **Backup automático** en cada actualización
- **Importación/Exportación** disponible

### Archivos del Sistema
```
support_data.json                    # Base datos de soportes
isometric_data.json                  # Datos de isométricos
support_isometric_relation.json     # Relaciones establecidas
support_pdf_mapping.json            # Mapeo a PDFs
installation_manager.js              # Gestor de instalaciones
```

## 🔄 Flujo de Trabajo Típico

### 1. Planificación
1. Acceder a **Pestaña Soportes**
2. Buscar soportes por línea/tipo
3. Revisar isométricos relacionados
4. Planificar instalaciones con fechas

### 2. Ejecución
1. Acceder a **Pestaña Instalaciones**
2. Filtrar por estado "Planificado"
3. Marcar como "En Progreso"
4. Completar instalación

### 3. Seguimiento
1. Dashboard de estadísticas
2. Filtrar instalaciones por fechas
3. Exportar reportes
4. Trazabilidad completa

## 🛠️ Mantenimiento y Soporte

### Archivos de Configuración
- `INICIAR_SISTEMA_INTEGRADO.bat` - Lanzador principal
- `installation_manager.js` - Gestor de instalaciones
- `index_isometricos_con_costuras.html` - Aplicación principal

### Resolución de Problemas
1. **Datos no aparecen**: Verificar archivos JSON en directorio
2. **Instalaciones no se guardan**: Verificar localStorage del navegador
3. **PDFs no abren**: Verificar rutas de carpetas ESTANDARES e ISOMETRICOS
4. **Rendimiento lento**: Usar funciones de búsqueda específica

### Backup y Restauración
- **Exportar instalaciones** regularmente a CSV
- **Copiar archivos JSON** para backup completo
- **localStorage** se mantiene por navegador

## 📈 Beneficios del Sistema Integrado

### Para Gestión de Proyectos
- **Visibilidad completa** del progreso
- **Identificación rápida** de retrasos
- **Trazabilidad** desde diseño a instalación
- **Reportes automáticos** de estado

### Para Equipos de Campo
- **Acceso rápido** a estándares PDF
- **Información contextual** por soporte
- **Actualización simple** de estados
- **Histórico completo** de instalaciones

### Para Control de Calidad
- **Seguimiento** de responsables
- **Fechas reales** vs planificadas
- **Notas detalladas** por instalación
- **Cobertura completa** de relaciones

## 🔮 Funcionalidades Futuras

El sistema está diseñado para expansión futura:
- Integración con sistemas ERP
- Notificaciones automáticas
- Reportes avanzados con gráficos
- API para integración externa
- Gestión de materiales
- Control de calidad integrado

---

## 📞 Soporte Técnico

- **Documentación**: Este archivo y archivos MD relacionados
- **Logs**: Consola del navegador (F12)
- **Archivos de prueba**: `PROBAR_SISTEMA_COSTURAS.bat`
- **Versión**: 3.0 - Sistema Integrado Completo

**Sistema desarrollado para optimizar la gestión de soportación industrial con trazabilidad completa y control de progreso en tiempo real.** 