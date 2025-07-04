# Funcionalidad de Isométricos Prefabricados - Sistema SINES v3.0

## 📋 Descripción General

El Sistema SINES v3.0 ahora incluye soporte completo para **isométricos prefabricados**, permitiendo a los usuarios acceder tanto a las versiones normales como a las versiones prefabricadas de los isométricos cuando estén disponibles.

## 🎯 Características Implementadas

### ✅ Detección Automática
- **Análisis inteligente** de correspondencias entre archivos normales y prefabricados
- **Mapeo automático** basado en códigos de línea
- **Cobertura del 24.1%** (427 correspondencias de 1,773 archivos)

### ✅ Visualización Integrada
- **Indicadores visuales** para isométricos con versions prefabricadas
- **Botones diferenciados** para cada tipo de archivo
- **Estadísticas actualizadas** en tiempo real

### ✅ Acceso Directo
- **Enlaces directos** a ambas versiones
- **Colores distintivos** para identificar fácilmente cada tipo
- **Información detallada** sobre disponibilidad

## 🔧 Estructura de Archivos

### Archivos Normales
```
ISOMETRICOS/
├── 19-000-2-02-00001 sheet 2121BU10C13-1_IS01.pdf
├── 19-000-2-02-00001 sheet 2121CO40F01-1_IS01.pdf
└── ...
```

### Archivos Prefabricados
```
ISOMETRICOS PREFABRICADOS/
├── 2121-BU10C13-1.pdf
├── 2121-CO40F01-1.pdf
└── ...
```

### Mapeo Generado
```json
{
  "metadata": {
    "total_normal_files": 1773,
    "total_prefab_files": 433,
    "correspondences_found": 427,
    "coverage_percentage": 24.1
  },
  "correspondences": {
    "19-000-2-02-00001 sheet 2121BU10C13-1_IS01.pdf": {
      "normal_file": "19-000-2-02-00001 sheet 2121BU10C13-1_IS01.pdf",
      "prefab_file": "2121-BU10C13-1.pdf",
      "line_code": "2121-BU10C13-1",
      "normal_path": "ISOMETRICOS/...",
      "prefab_path": "ISOMETRICOS PREFABRICADOS/..."
    }
  }
}
```

## 🚀 Cómo Utilizar

### 1. Inicio del Sistema
```bash
# Usar el nuevo script con soporte para prefabricados
INICIAR_SISTEMA_PREFABRICADOS.bat
```

### 2. Navegación
1. **Acceder a la pestaña "Isométricos"**
2. **Realizar búsqueda** de líneas o fluidos
3. **Identificar isométricos** con indicador 🏭
4. **Hacer clic** en botones normales (azules) o prefabricados (naranjas)

### 3. Identificación Visual
- **Botones azules**: Archivos normales
- **Botones naranjas**: Archivos prefabricados
- **Indicador 🏭**: Línea con versions prefabricadas disponibles

## 📊 Estadísticas del Sistema

### Cobertura Actual
- **1,773** archivos isométricos normales
- **433** archivos isométricos prefabricados
- **427** correspondencias establecidas
- **24.1%** de cobertura total

### Líneas con Prefabricados
Las líneas más comunes con versions prefabricadas incluyen:
- **2121-BU10C13-X**: Sistema de utilidades
- **2121-CO40F01-X**: Líneas de proceso
- **2121-CWR40B01-X**: Agua refrigerada
- **2121-VA40E01-X**: Ventilación

## 🔍 Análisis de Correspondencias

### Patrones de Nomenclatura
```
Normal:      19-000-2-02-00001 sheet 2121BU10C13-1_IS01.pdf
Prefabricado: 2121-BU10C13-1.pdf
Relación:    Código de línea 2121BU10C13-1
```

### Algoritmo de Mapeo
1. **Extracción** de código de línea del archivo normal
2. **Formateo** a estructura de prefabricado
3. **Búsqueda** de correspondencia exacta
4. **Validación** de existencia del archivo

## 🛠️ Archivos Técnicos

### Scripts de Análisis
- `analyze_prefabricated_isometrics.py`: Análisis completo
- `INICIAR_SISTEMA_PREFABRICADOS.bat`: Lanzador con prefabricados

### Archivos de Datos
- `prefabricated_isometric_mapping.json`: Mapeo completo
- `prefabricated_line_index.json`: Índice por línea
- `prefabricated_analysis_stats.json`: Estadísticas detalladas

### Archivos de Sistema
- `index_isometricos_con_costuras.html`: Aplicación principal actualizada
- CSS actualizado con estilos para prefabricados

## 🔄 Actualización Automática

### Regeneración del Mapeo
```bash
# Ejecutar análisis manual
python analyze_prefabricated_isometrics.py

# El script .bat ejecuta automáticamente si no existe el mapeo
INICIAR_SISTEMA_PREFABRICADOS.bat
```

### Mantenimiento
- **Verificación automática** de archivos al inicio
- **Regeneración** si faltan archivos de mapeo
- **Estadísticas actualizadas** en tiempo real

## 📈 Beneficios del Sistema

### Para Usuarios
- **Acceso inmediato** a ambas versiones
- **Identificación visual** clara
- **Navegación intuitiva**

### Para Administradores
- **Trazabilidad completa** de archivos
- **Estadísticas detalladas** de cobertura
- **Mantenimiento automático**

### Para Proyectos
- **Visibilidad** del estado de prefabricación
- **Control** de versiones disponibles
- **Integración** con sistema de instalaciones

## 🎨 Interfaz Visual

### Colores del Sistema
- **Azul (#2c5f2d)**: Archivos normales
- **Naranja (#ff6b35)**: Archivos prefabricados
- **Verde**: Elementos del sistema base

### Indicadores
- **🏭**: Prefabricado disponible
- **📐**: Isométrico normal
- **📋**: Hojas del isométrico

## 🚧 Limitaciones Actuales

### Cobertura
- **24.1%** de archivos con correspondencia
- **Dependiente** de nomenclatura estándar
- **Algunos archivos** pueden no tener correspondencia

### Mantenimiento
- **Requiere** análisis manual para nuevos archivos
- **Dependiente** de estructura de carpetas
- **Sensible** a cambios en nomenclatura

## 📋 Lista de Verificación

### Instalación
- [ ] Ejecutar `analyze_prefabricated_isometrics.py`
- [ ] Verificar generación de archivos JSON
- [ ] Usar `INICIAR_SISTEMA_PREFABRICADOS.bat`
- [ ] Confirmar carga de estadísticas

### Uso
- [ ] Navegar a pestaña "Isométricos"
- [ ] Buscar líneas específicas
- [ ] Identificar indicadores 🏭
- [ ] Probar enlaces a ambas versiones

### Mantenimiento
- [ ] Verificar estadísticas periódicamente
- [ ] Regenerar mapeo si hay nuevos archivos
- [ ] Revisar logs de correspondencias

## 🔧 Resolución de Problemas

### Error: "No se encuentra mapeo de prefabricados"
```bash
# Solución
python analyze_prefabricated_isometrics.py
```

### Error: "Correspondencias no cargadas"
- Verificar existencia de `prefabricated_isometric_mapping.json`
- Comprobar formato JSON válido
- Revisar permisos de archivo

### Error: "Enlaces prefabricados no funcionan"
- Verificar rutas en mapeo JSON
- Comprobar existencia de archivos prefabricados
- Revisar nombres de archivos

## 📞 Soporte

### Archivos de Log
- Console del navegador: Información de carga
- Salida del script Python: Análisis detallado
- Archivos JSON: Estadísticas y mapeos

### Información de Depuración
```javascript
// En consola del navegador
console.log('Prefabricados cargados:', Object.keys(prefabricatedMapping).length);
console.log('Mapeo completo:', prefabricatedMapping);
```

---

## 🎉 Resultado Final

El Sistema SINES v3.0 ahora proporciona acceso integrado a **1,773 isométricos normales** y **433 isométricos prefabricados**, con **427 correspondencias establecidas**, ofreciendo una vista completa del estado de prefabricación del proyecto y facilitando el acceso a ambas versiones según las necesidades del usuario.

La integración es **transparente** y **automática**, requiriendo únicamente el uso del nuevo script de inicio para acceder a toda la funcionalidad expandida. 