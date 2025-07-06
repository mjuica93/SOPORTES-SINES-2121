# Sistema Integrado SINES - Soportes e Isométricos v2.0

## 🎯 Descripción General

El Sistema Integrado SINES es una aplicación web avanzada que combina la gestión de **soportes** con la funcionalidad de **isométricos**, creando un sistema completo para la gestión de proyectos de ingeniería. Esta versión 2.0 introduce la capacidad de relacionar directamente los soportes con sus isométricos correspondientes.

## ✨ Características Principales

### 🔧 Gestión de Soportes
- **Base de datos completa**: 1,615 soportes con información detallada
- **Búsqueda avanzada**: Por número, tipo, línea o fluido
- **PDFs integrados**: Acceso directo a estándares de soportes
- **Filtrado inteligente**: Por tipo de soporte y línea de proceso

### 📐 Gestión de Isométricos
- **718 líneas únicas** con 1,778 archivos PDF
- **Información detallada**: Fluido, hojas, revisiones, tipos (LB/SB)
- **Búsqueda completa**: Por línea, fluido o nombre de archivo
- **Acceso directo**: Enlaces a archivos PDF de isométricos

### 🔗 Sistema de Relaciones
- **1,471 relaciones** soportes-isométricos establecidas
- **91.1% cobertura**: De los soportes tienen isométricos relacionados
- **Navegación bidireccional**: Desde soportes a isométricos y viceversa
- **Trazabilidad completa**: Seguimiento de líneas y fluidos

## 📊 Estadísticas del Sistema

### Soportes
- **Total**: 1,615 soportes
- **Tipos únicos**: 126 diferentes
- **Con PDFs**: 1,615 (100% cobertura)
- **Archivos PDF**: 752 estándares disponibles

### Isométricos
- **Líneas únicas**: 718
- **Total hojas**: 1,778
- **Archivos PDF**: 1,778
- **Tipos**: LB (Large Bore) y SB (Small Bore)

### Relaciones
- **Total relaciones**: 1,471
- **Líneas con soportes**: 156
- **Cobertura**: 91.1% de soportes relacionados

## 🚀 Instalación y Uso

### Requisitos Previos
- **Python 3.7+** instalado
- **Navegador web** moderno (Chrome, Firefox, Edge)
- **Conexión a internet** (para librerías de Python)

### Instalación Automática
```bash
# Ejecutar el archivo de instalación
INICIAR_SISTEMA_COSTURAS.bat
```

### Instalación Manual
```bash
# 1. Instalar dependencias
pip install pandas openpyxl

# 2. Extraer datos de soportes (si es necesario)
python extract_support_data_final.py

# 3. Crear mapeo de PDFs (si es necesario)
python create_support_mapping.py

# 4. Analizar isométricos (si es necesario)
python analyze_isometric_structure.py

# 5. Iniciar servidor web
python -m http.server 8080

# 6. Abrir en navegador
# http://localhost:8080/index_isometricos_con_costuras.html
```

## 📱 Interfaz de Usuario

### Pestañas Principales

#### 1. 📋 Soportes
- **Estadísticas en tiempo real**: Total, tipos, con PDFs, resultados
- **Filtros avanzados**:
  - Búsqueda por texto (número, tipo, línea)
  - Filtro por tipo de soporte
  - Filtro por línea de proceso
- **Información mostrada**:
  - Número y tipo de soporte
  - Línea de proceso (fluid_piping)
  - Posición, cantidad, clase material
  - Dimensiones y especificaciones
  - **Enlaces a PDFs de estándares**
  - **Enlaces a isométricos relacionados**

#### 2. 📐 Isométricos
- **Estadísticas completas**: Líneas, hojas, archivos, resultados
- **Filtros especializados**:
  - Búsqueda por línea, fluido o archivo
  - Filtro por tipo de fluido
  - Filtro por tipo (LB/SB)
- **Información detallada**:
  - Código de línea y fluido
  - Número total de hojas
  - Tipos de planos (LB/SB)
  - Revisiones disponibles
  - **Enlaces directos a archivos PDF**

#### 3. 🔗 Relaciones
- **Vista integrada**: Soportes con sus isométricos
- **Filtros relacionales**:
  - Búsqueda por soporte, línea o fluido
  - Filtro por tipo de soporte
  - Filtro por fluido de proceso
- **Información cruzada**:
  - Soporte con tipo
  - Línea de proceso y fluido
  - Hoja de isométrico (iso_sheet)
  - **Archivos PDF relacionados**

### Características de la Interfaz

#### 🎨 Diseño Moderno
- **Tema visual atractivo**: Gradientes y animaciones
- **Diseño responsivo**: Adaptable a móviles y tablets
- **Navegación intuitiva**: Pestañas claramente diferenciadas
- **Feedback visual**: Efectos hover y transiciones suaves

#### ⚡ Rendimiento Optimizado
- **Carga asíncrona**: Los datos se cargan en segundo plano
- **Filtrado en tiempo real**: Resultados instantáneos
- **Búsqueda eficiente**: Algoritmos optimizados
- **Memoria inteligente**: Gestión eficiente de datos

#### 🔍 Búsqueda Avanzada
- **Búsqueda global**: Texto libre en múltiples campos
- **Filtros combinables**: Múltiples criterios simultáneos
- **Resultados dinámicos**: Actualización automática
- **Estadísticas en vivo**: Contadores actualizados

## 🗂️ Estructura de Archivos

### Archivos de Datos (JSON)
```
isometric_data.json              # Datos de isométricos organizados por línea
support_data.json                # Base de datos completa de soportes
support_pdf_mapping.json         # Mapeo soportes ↔ PDFs de estándares
support_isometric_relation.json  # Relaciones soportes ↔ isométricos
```

### Archivos de Configuración
```
analyze_isometric_structure.py   # Script de análisis de isométricos
extract_support_data_final.py    # Extractor de datos de soportes
create_support_mapping.py        # Creador de mapeo de PDFs
```

### Interfaz Web
```
index_isometricos_con_costuras.html  # Aplicación web principal
INICIAR_SISTEMA_COSTURAS.bat        # Instalador y lanzador automático
```

### Carpetas de Recursos
```
ISOMETRICOS/                     # 1,778 archivos PDF de isométricos
ESTANDARES DE SOPORTES/          # 752 archivos PDF de estándares
```

## 🔄 Flujo de Trabajo

### Para Buscar un Soporte
1. **Ir a pestaña "Soportes"**
2. **Buscar** por número o tipo en el campo de búsqueda
3. **Filtrar** por tipo o línea si es necesario
4. **Ver información** completa del soporte
5. **Acceder** a PDFs de estándares
6. **Navegar** a isométricos relacionados

### Para Encontrar Isométricos
1. **Ir a pestaña "Isométricos"**
2. **Buscar** por línea, fluido o archivo
3. **Filtrar** por fluido o tipo (LB/SB)
4. **Ver detalles** de la línea
5. **Abrir** archivos PDF específicos

### Para Explorar Relaciones
1. **Ir a pestaña "Relaciones"**
2. **Buscar** por cualquier criterio
3. **Ver conexiones** soportes ↔ isométricos
4. **Navegar** entre documentos relacionados

## 🛠️ Mantenimiento y Actualización

### Actualización de Datos
```bash
# Para actualizar datos de soportes
python extract_support_data_final.py

# Para actualizar mapeo de PDFs
python create_support_mapping.py

# Para actualizar análisis de isométricos
python analyze_isometric_structure.py
```

### Verificación de Integridad
```bash
# Verificar archivos JSON
python -c "import json; print('✓ JSON válido')" # Para cada archivo JSON
```

### Backup de Datos
```bash
# Respaldar archivos importantes
copy *.json backup\
copy *.py backup\
```

## 🎯 Casos de Uso Principales

### 1. Ingeniero de Diseño
- **Busca soporte específico** → Ve estándares → Revisa isométrico relacionado
- **Verifica especificaciones** → Accede a PDFs técnicos
- **Valida diseño** → Cruza información soporte-isométrico

### 2. Supervisor de Construcción
- **Identifica línea de proceso** → Encuentra soportes necesarios
- **Verifica instalación** → Consulta estándares y planos
- **Controla avance** → Usa trazabilidad completa

### 3. Inspector de Calidad
- **Audita instalaciones** → Verifica contra estándares
- **Valida conformidad** → Cruza datos soporte-isométrico
- **Genera reportes** → Exporta información integrada

### 4. Gerente de Proyecto
- **Monitorea progreso** → Ve estadísticas en tiempo real
- **Controla recursos** → Verifica cobertura de documentos
- **Toma decisiones** → Accede a información consolidada

## 📈 Beneficios del Sistema

### ⏱️ Eficiencia Operacional
- **Búsqueda rápida**: Encuentra información en segundos
- **Navegación intuitiva**: Interfaz fácil de usar
- **Acceso centralizado**: Todo en una sola aplicación
- **Filtrado avanzado**: Encuentra exactamente lo que necesitas

### 🎯 Precisión y Calidad
- **Datos validados**: Información verificada y consistente
- **Relaciones automáticas**: Conexiones establecidas automáticamente
- **Trazabilidad completa**: Seguimiento total de documentos
- **Estándares integrados**: Acceso directo a especificaciones

### 💰 Reducción de Costos
- **Menos tiempo perdido**: Búsquedas más eficientes
- **Menor duplicación**: Información centralizada
- **Mejor planificación**: Datos completos disponibles
- **Errores reducidos**: Información consistente y actualizada

### 📊 Visibilidad y Control
- **Estadísticas en tiempo real**: Métricas actualizadas
- **Cobertura completa**: 91.1% de relaciones establecidas
- **Monitoreo continuo**: Seguimiento de todos los elementos
- **Reportes integrados**: Información consolidada

## 🔮 Planes Futuros

### Funcionalidades Planificadas
- **Exportación avanzada**: Excel, PDF, CSV
- **Reportes personalizados**: Plantillas configurables
- **Integración con CAD**: Enlaces directos a modelos 3D
- **API REST**: Acceso programático a datos
- **Dashboard ejecutivo**: Métricas de alto nivel
- **Control de versiones**: Historial de cambios

### Mejoras Técnicas
- **Base de datos**: Migración a PostgreSQL/MySQL
- **Autenticación**: Sistema de usuarios y permisos
- **Cache inteligente**: Mejora de rendimiento
- **Sincronización**: Actualización automática de datos

## 📞 Soporte y Contacto

Para soporte técnico, sugerencias o reportar problemas:

- **Documentación**: Revisar archivos README y MD
- **Logs**: Verificar consola del navegador
- **Archivos**: Asegurar integridad de JSON y PDFs
- **Python**: Verificar instalación y dependencias

## 📄 Licencia y Términos

Este sistema es de uso interno para el proyecto SINES. Todos los datos, documentos y archivos son propiedad del proyecto y deben manejarse según las políticas de seguridad establecidas.

---

**Sistema Integrado SINES v2.0**  
*Gestión Completa de Soportes e Isométricos*  
*Desarrollado para máxima eficiencia y precisión* 