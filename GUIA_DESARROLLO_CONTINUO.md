# 🚀 GUÍA DE DESARROLLO CONTINUO - SISTEMA SINES

## 🎯 OBJETIVO
Añadir nuevas funcionalidades y actualizaciones al sistema sin romper la versión en producción.

---

## 🔄 FLUJO ACTUAL
- **Repositorio**: https://github.com/mjuica93/SOPORTES-SINES-2121
- **Producción**: Railway (auto-deploy desde main)
- **Estado**: ✅ Funcionando en producción

---

## 📋 PROCESO COMPLETO PASO A PASO

### **PASO 1: 🌿 CREAR RAMA DE DESARROLLO**
```bash
# Asegurarte de estar en la rama main actualizada
git checkout main
git pull origin main

# Crear nueva rama para la funcionalidad
git checkout -b feature/nueva-funcionalidad
```

### **PASO 2: 🧪 DESARROLLO LOCAL**
```bash
# Desarrollar la nueva funcionalidad
# Editar archivos necesarios
# Probar localmente con:
python server.py
# O probar versión Railway con:
python server_railway.py
```

### **PASO 3: ✅ PRUEBAS LOCALES COMPLETAS**
```bash
# Probar todas las funcionalidades:
# 1. Búsqueda funciona
# 2. PDFs se abren
# 3. Versión móvil funciona
# 4. No hay errores en consola
```

### **PASO 4: 💾 COMMIT DE CAMBIOS**
```bash
# Añadir cambios
git add .

# Commit descriptivo
git commit -m "feat: añadir [descripción de funcionalidad]"

# Subir rama a GitHub
git push origin feature/nueva-funcionalidad
```

### **PASO 5: 🔀 PULL REQUEST (RECOMENDADO)**
1. Ve a GitHub: https://github.com/mjuica93/SOPORTES-SINES-2121
2. Crea Pull Request desde tu rama a `main`
3. Revisa los cambios
4. Merge a `main`

### **PASO 6: 🚀 DESPLIEGUE AUTOMÁTICO**
- Railway detecta el cambio en `main`
- Inicia build automático
- Despliega nueva versión
- ¡Tu funcionalidad está en producción!

---

## 🛡️ ESTRATEGIAS PARA EVITAR FALLOS

### **1. 🧪 TESTING LOCAL OBLIGATORIO**
**Antes de cada commit:**
```bash
# Ejecutar servidor local
python server_railway.py

# Probar funcionalidades críticas:
# ✅ Página principal carga
# ✅ Búsqueda funciona
# ✅ PDFs se abren
# ✅ Versión móvil funciona
# ✅ No hay errores JavaScript
```

### **2. 🔄 DESARROLLO POR RAMAS**
```bash
# ❌ NUNCA hagas esto:
git checkout main
# editar archivos directamente
git commit -m "cambio rápido"
git push

# ✅ SIEMPRE haz esto:
git checkout -b feature/mi-mejora
# desarrollar y probar
git commit -m "feat: mejora específica"
git push origin feature/mi-mejora
# crear pull request
```

### **3. 📊 MONITOREO POST-DEPLOY**
**Después de cada despliegue:**
1. Verifica que Railway build fue exitoso
2. Abre la URL de producción
3. Prueba funcionalidad nueva
4. Revisa logs en Railway dashboard

### **4. 🔙 PLAN DE ROLLBACK**
```bash
# Si algo falla, volver a versión anterior:
git checkout main
git reset --hard HEAD~1  # Volver 1 commit atrás
git push --force origin main  # ⚠️ Solo en emergencia
```

---

## 🔧 TIPOS DE FUNCIONALIDADES COMUNES

### **A) 🎨 MEJORAS DE INTERFAZ**
**Archivos a modificar:**
- `index.html`, `index_mobile.html`
- `app.js`, CSS embebido
- Probar en navegador + móvil

### **B) 🔍 MEJORAS DE BÚSQUEDA**
**Archivos a modificar:**
- `app.js` (lógica de búsqueda)
- `support_data_enhanced.json` (datos)
- Probar con diferentes términos

### **C) 🚀 NUEVAS PÁGINAS/FUNCIONES**
**Archivos a crear/modificar:**
- Nuevos archivos HTML
- `server_railway.py` (rutas)
- Actualizar navegación

### **D) 📄 NUEVOS DOCUMENTOS PDF**
**Archivos a modificar:**
- Añadir PDFs a `ESTANDARES DE SOPORTES/`
- Actualizar `support_data_enhanced.json`
- Actualizar `support_pdf_mapping.json`

---

## 🛠️ HERRAMIENTAS DE DESARROLLO

### **1. 🔍 DEBUGGING LOCAL**
```bash
# Servidor con logs detallados
python -u server_railway.py

# Verificar archivos importantes
ls -la *.json
ls -la *.html
```

### **2. 📊 MONITOREO RAILWAY**
- **Dashboard**: Ver builds en tiempo real
- **Logs**: Debugging de errores
- **Metrics**: Rendimiento de la app

### **3. 🧪 TESTING AVANZADO**
```javascript
// En consola del navegador
console.log("Testing search...");
// Probar funciones JavaScript manualmente
```

---

## ⚠️ MEJORES PRÁCTICAS

### **DO's ✅**
- Siempre probar localmente antes de subir
- Usar ramas para desarrollar funcionalidades
- Commits descriptivos y pequeños
- Monitorear después de cada deploy
- Mantener backups de versiones estables

### **DON'Ts ❌**
- Nunca editar directamente en `main`
- No subir código sin probar
- No hacer cambios masivos de una vez
- No ignorar errores en Railway logs
- No olvidar probar versión móvil

---

## 🚀 EJEMPLOS DE FUNCIONALIDADES FUTURAS

### **🔍 Búsqueda Avanzada**
- Filtros por categoría
- Búsqueda por rango de fechas
- Autocompletado

### **📱 Mejoras Móviles**
- Gestos táctiles
- Modo offline
- Push notifications

### **📊 Analytics**
- Estadísticas de uso
- PDFs más consultados
- Reportes de búsqueda

### **🔐 Funcionalidades Admin**
- Subida masiva de PDFs
- Edición de metadatos
- Gestión de usuarios

---

## 📞 SOPORTE DE EMERGENCIA

### **Si algo falla en producción:**
1. **No entres en pánico**
2. **Ve a Railway dashboard** → Logs
3. **Identifica el error** específico
4. **Rollback rápido** si es necesario
5. **Arregla en local** y redespliega

### **Contactos útiles:**
- **Railway Support**: https://railway.app/help
- **GitHub Issues**: Tu repositorio
- **Documentación**: Archivos MD en tu proyecto

---

**¡Con este flujo, puedes evolucionar tu sistema de forma segura y continua!** 🎯 