# Sistema de Búsqueda de Soportes - SINES

## Descripción

Este sistema permite buscar y consultar información sobre soportes de tuberías del proyecto ALBA - PP AND PEL PLANTS en SINES, Portugal. El sistema incluye:

- **1,615 soportes** extraídos de los archivos Excel
- **126 tipos diferentes** de soportes
- **752 PDFs** de estándares de soportes
- **70 tipos** con PDFs correspondientes

## Archivos del Sistema

### Archivos de Datos
- `support_data.json` - Datos extraídos de los archivos Excel
- `support_pdf_mapping.json` - Mapeo entre tipos de soportes y PDFs
- `ESTANDARES DE SOPORTES/` - Carpeta con todos los PDFs de estándares

### Archivos de la Aplicación
- `index.html` - Interfaz principal del sistema
- `app.js` - Lógica de la aplicación
- `README.md` - Este archivo de documentación

### Archivos de Procesamiento
- `extract_support_data_final.py` - Script para extraer datos de Excel
- `create_support_mapping.py` - Script para crear mapeo de PDFs

## Funcionalidades

### 1. Búsqueda de Soportes
- **Búsqueda por número de soporte**: Ej: "8001", "681"
- **Búsqueda por tipo de soporte**: Ej: "N1G1", "TR34", "ST01"
- **Búsqueda por fluido/tubería**: Ej: "P56A108", "LPN91S10"
- **Búsqueda en notas**: Cualquier texto en las notas y referencias

### 2. Filtros
- **Filtro por tipo**: Selecciona un tipo específico de soporte
- **Combinación de filtros**: Búsqueda + filtro por tipo

### 3. Información Mostrada
Para cada soporte se muestra:
- Número de soporte
- Tipo de soporte
- Número de posición
- Clase de material
- Dimensiones
- Cantidad
- Fluido y número de tubería
- Hoja ISO
- Temperatura
- Archivo fuente
- Notas y referencias

### 4. PDFs de Estándares
- Enlaces directos a los PDFs correspondientes
- Descarga automática al hacer clic
- Indicador visual cuando hay PDFs disponibles

## Tipos de Soportes Principales

### Soportes Estándar
- **N1G1, N1B1, N1F1** - Soportes tipo N1
- **TR34, TR31, TR06, TR05** - Soportes tipo TR
- **ST01, ST02, ST04, ST05, ST08, ST09, ST10, ST13, ST42, ST46, ST48** - Soportes tipo ST
- **C1A1, C1B1, C1F1, C1G1, C3A1, C3B1, C4A1, C4B1, C4F1, C4G1, C5A1, C5B1, C5G1** - Soportes tipo C
- **SB01, SB02, SB03, SB04, SB18, SB30, SB31, SB32, SB33, SB35** - Soportes tipo SB
- **EW01, EW05, EW06, EW09, EW10** - Soportes tipo EW
- **P02D, P69A, P70, P73** - Soportes tipo P
- **BA04, BE01, BE02, BE03, BW01** - Soportes tipo B
- **F2A1, F2G1** - Soportes tipo F

### Soportes Especiales
- **SP-001 a SP-047** - Soportes especiales numerados
- **FP-00210, GP-00200, SP-00200** - Soportes con códigos específicos

## Instrucciones de Uso

### 1. Abrir el Sistema
1. Abre el archivo `index.html` en tu navegador web
2. El sistema cargará automáticamente todos los datos

### 2. Realizar Búsquedas
1. **Búsqueda simple**: Escribe en el campo de búsqueda
2. **Filtro por tipo**: Selecciona un tipo específico del menú desplegable
3. **Búsqueda combinada**: Usa ambos filtros simultáneamente

### 3. Ver Información
1. Los resultados se muestran en tarjetas
2. Cada tarjeta contiene toda la información del soporte
3. Si hay PDFs disponibles, aparecen enlaces de descarga

### 4. Descargar PDFs
1. Haz clic en cualquier enlace de PDF
2. El archivo se abrirá en una nueva pestaña
3. Puedes descargarlo desde el navegador

## Estadísticas del Sistema

- **Total de soportes**: 1,615
- **Tipos diferentes**: 126
- **Soportes con PDFs**: 1,615 (todos tienen al menos un PDF)
- **PDFs disponibles**: 752 archivos

## Estructura de Datos

### Archivos Excel Originales
- `4274-XH-LP-21210001-IS03_Native.xlsx` - Soportes estándar
- `4274-XH-LP-21210002-IS02_Native.xlsm` - Soportes especiales

### Columnas Extraídas
- **SUPPORT NUMBER**: Número identificador del soporte
- **SUPPORT OR ELEMENT TYPE**: Tipo de soporte o elemento
- **POSITION NUMBER**: Número de posición
- **COMMODITY CODE**: Código de mercancía
- **SUPPORT MATERIAL CLASS**: Clase de material del soporte
- **SIZE OR CHARACTERISTICS DIMENSIONS**: Dimensiones
- **QUANTITY**: Cantidad
- **FLUID & NUMBER OF PIPING**: Fluido y número de tubería
- **ISO SHEET NUMBER**: Número de hoja ISO
- **REFERENCES - NOTES**: Notas y referencias
- **PIPING OPERATING TEMPERATURE**: Temperatura de operación

## Notas Técnicas

### Rendimiento
- El sistema limita los resultados a 50 por página para mejor rendimiento
- La búsqueda es en tiempo real con un delay de 500ms
- Los datos se cargan una sola vez al inicio

### Compatibilidad
- Funciona en navegadores modernos (Chrome, Firefox, Safari, Edge)
- Requiere JavaScript habilitado
- Los PDFs se abren en el navegador o se descargan automáticamente

### Seguridad
- Todos los archivos se sirven localmente
- No hay conexiones externas
- Los PDFs se abren en nuevas pestañas

## Soporte

Para cualquier problema o consulta sobre el sistema:
1. Verifica que todos los archivos estén en la misma carpeta
2. Asegúrate de que el navegador tenga JavaScript habilitado
3. Comprueba que los archivos JSON se generaron correctamente

## Actualización de Datos

Si necesitas actualizar los datos:
1. Ejecuta `python extract_support_data_final.py` para extraer datos de Excel
2. Ejecuta `python create_support_mapping.py` para actualizar el mapeo de PDFs
3. Recarga la página web

---

**Desarrollado para el Proyecto ALBA - PP AND PEL PLANTS - SINES PORTUGAL** 