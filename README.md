# Sistema de Búsqueda de Soportes SINES

## 📊 Estado Actual del Sistema

- **Total de soportes**: 1,615 registros
- **PDFs disponibles**: 773 archivos
- **Tipos de soportes con PDF**: 70
- **Tipos de soportes sin PDF**: 56 (44.4%)
- **Soportes afectados por PDFs faltantes**: 227

## 🚀 Inicio Rápido

### Opción 1: Usar archivos .bat (Recomendado)
```bash
# Versión completa con variables de plantillas
INICIAR_VERSION_CON_PLANTILLAS.bat

# Versión robusta con manejo de errores
INICIAR_VERSION_ROBUSTA.bat

# Versión estándar
INICIAR_SISTEMA.bat
```

### Opción 2: Inicio manual
```bash
python server.py
```
Luego abrir: http://localhost:8000/index_enhanced_with_templates.html

## 🔧 Actualización del Sistema

### Cuando agregues nuevos PDFs:

1. **Copia los archivos PDF** a la carpeta `ESTANDARES DE SOPORTES`
2. **Ejecuta el actualizador**:
   ```bash
   ACTUALIZAR_SISTEMA.bat
   ```
   O manualmente:
   ```bash
   python actualizar_sistema.py
   ```

El sistema se actualizará automáticamente y mostrará las nuevas estadísticas.

## 📁 Estructura del Proyecto

```
SOPORTACION SINES/
├── 📊 DATOS/
│   ├── support_data.json              # Datos básicos (1,615 soportes)
│   ├── support_data_enhanced.json     # Datos completos (25+ campos)
│   └── support_pdf_mapping.json       # Mapeo soportes-PDFs
├── 🌐 SISTEMA WEB/
│   ├── index_enhanced_with_templates.html  # Versión completa ⭐
│   ├── index_enhanced_robust.html      # Versión robusta
│   ├── index_enhanced.html             # Versión mejorada
│   ├── index.html                      # Versión básica
│   └── server.py                       # Servidor web
├── 📄 PDFs/
│   └── ESTANDARES DE SOPORTES/         # 773 archivos PDF
├── 🔧 HERRAMIENTAS/
│   ├── actualizar_sistema.py           # Actualizador automático ⭐
│   ├── create_support_mapping.py       # Mapeo soportes-PDFs
│   └── generate_missing_pdfs_list.py   # Lista PDFs faltantes
└── 📋 DOCUMENTACIÓN/
    ├── README.md                       # Este archivo
    ├── ARCHIVOS_PDF_A_BUSCAR.txt      # Lista PDFs faltantes
    └── GUIA_VARIABLES_PLANTILLA.txt   # Guía de variables técnicas
```

## 🔍 Características del Sistema

### Versión Completa (Recomendada)
- **URL**: `http://localhost:8000/index_enhanced_with_templates.html`
- **Características**:
  - 1,615 soportes con información completa
  - Variables de plantillas técnicas (A, B, C, D, E, R, X, Y, EL, N., SH., TEMP)
  - Agrupación inteligente por número de soporte
  - Búsqueda avanzada por múltiples campos
  - Visualización directa de PDFs
  - Estadísticas en tiempo real

### Información Mostrada
- **Básica**: Número, tipo, fluido, línea, área
- **Técnica**: Especificación, clase, rating, material
- **Dimensiones**: A, B, C, D, E, R, X, Y, EL con descripciones
- **Proyecto**: Revisión, fecha, notas del proyecto
- **Variables de Plantilla**: Dimensiones técnicas para interpretación de PDFs
- **PDFs**: Enlaces directos a documentos técnicos

## 📄 PDFs Faltantes

El sistema identifica automáticamente los PDFs faltantes. Los más importantes son:

- **SPRING.pdf** (32 soportes afectados)
- **PLA.pdf** (30 soportes afectados)
- **HEA.pdf** (23 soportes afectados)
- **C1G2.pdf** (18 soportes afectados)
- **BAN.pdf** (12 soportes afectados)
- **Archivos SP-XXX.pdf** (múltiples soportes especiales)

Ver `ARCHIVOS_PDF_A_BUSCAR.txt` para la lista completa.

## 🛠️ Solución de Problemas

### Error "No se pueden cargar los datos"
1. Verificar que el servidor esté ejecutándose
2. Limpiar caché del navegador (Ctrl+F5)
3. Usar modo incógnito
4. Ejecutar `python test_server.py` para diagnóstico

### PDFs no se abren
1. Verificar que el archivo PDF existe en `ESTANDARES DE SOPORTES`
2. Ejecutar `ACTUALIZAR_SISTEMA.bat`
3. Reiniciar el servidor

### Rendimiento lento
- El sistema maneja 1,615 soportes eficientemente
- Búsquedas optimizadas a ~300ms
- Paginación automática (25 grupos por página)

## 📈 Estadísticas del Sistema

- **Registros totales**: 1,615
- **Números únicos**: 789 (agrupación inteligente)
- **Campos por registro**: 25+
- **Tiempo de carga**: < 2 segundos
- **Tiempo de búsqueda**: ~300ms
- **Cobertura de PDFs**: 55.6% (mejorando)

## 🔄 Historial de Actualizaciones

El sistema mantiene un log automático en `actualizaciones.log` con:
- Fecha y hora de actualización
- Número de PDFs disponibles
- Tipos de soportes cubiertos
- Estadísticas de cobertura

## 🎯 Próximas Mejoras

1. **Completar PDFs faltantes** (56 archivos pendientes)
2. **Optimización de búsqueda** para grandes volúmenes
3. **Exportación de datos** a Excel/CSV
4. **Filtros avanzados** por múltiples criterios
5. **Modo offline** para uso sin servidor

---

**Desarrollado para**: Proyecto SINES - Sistema de Soportes de Tuberías  
**Última actualización**: Enero 2025  
**Versión**: 2.0 - Con Variables de Plantillas 