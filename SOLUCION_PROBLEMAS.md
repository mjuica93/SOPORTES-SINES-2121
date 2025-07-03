# Solución de Problemas - Sistema de Soportes SINES

## ❌ Problema: "Error al cargar los datos. Verifica que los archivos JSON estén disponibles."

### 🔍 Causa:
Este error se debe a restricciones de seguridad del navegador (CORS) que impiden cargar archivos JSON localmente.

### ✅ Soluciones:

#### **SOLUCIÓN 1 (RECOMENDADA): Usar el Servidor Local**
1. Haz doble clic en `INICIAR_SISTEMA.bat`
2. Se abrirá una ventana de comando y el navegador automáticamente
3. El sistema funcionará en `http://localhost:8000`

#### **SOLUCIÓN 2: Ejecutar Servidor Manualmente**
1. Abre una terminal/cmd en la carpeta del proyecto
2. Ejecuta: `python server.py`
3. Ve a `http://localhost:8000/index.html` en tu navegador

#### **SOLUCIÓN 3: Cambiar Navegador**
- **Chrome**: Normalmente tiene restricciones CORS estrictas
- **Firefox**: A veces permite archivos locales
- **Edge**: Comportamiento similar a Chrome

#### **SOLUCIÓN 4: Configurar Chrome para Desarrollo**
1. Cierra completamente Chrome
2. Ejecuta Chrome con: `chrome.exe --allow-file-access-from-files --disable-web-security --user-data-dir=temp`
3. ⚠️ **ADVERTENCIA**: Solo para pruebas, no uses para navegación normal

---

## ❌ Problema: "No se pueden descargar los PDFs"

### ✅ Solución:
1. Verifica que la carpeta `ESTANDARES DE SOPORTES` esté presente
2. Usa el servidor local (Solución 1 arriba)
3. Los PDFs se abrirán en nuevas pestañas

---

## ❌ Problema: "El servidor no inicia"

### 🔍 Posibles Causas y Soluciones:

#### **Python no instalado:**
- Descarga Python desde https://python.org
- Asegúrate de marcar "Add to PATH" durante la instalación

#### **Puerto 8000 ocupado:**
- El script intentará usar puerto 8001 automáticamente
- O cambia el puerto en `server.py`

#### **Permisos insuficientes:**
- Ejecuta como administrador
- O cambia a un puerto mayor (ej: 8080)

---

## ❌ Problema: "La búsqueda no funciona"

### ✅ Verificaciones:
1. Los archivos JSON deben estar presentes:
   - `support_data.json` (588 KB)
   - `support_pdf_mapping.json` (2.7 KB)

2. Usa el servidor local (no abras index.html directamente)

3. Verifica en la consola del navegador (F12) si hay errores

---

## ❌ Problema: "No aparecen los PDFs"

### ✅ Solución:
1. Verifica que la carpeta `ESTANDARES DE SOPORTES` contenga 752 PDFs
2. Los nombres de archivos deben coincidir exactamente
3. Usa el servidor local para acceso correcto a archivos

---

## 🔧 Verificación del Sistema

Ejecuta estos comandos para verificar que todo esté bien:

```bash
# Verificar archivos JSON
python -c "import json; print('JSON OK' if json.load(open('support_data.json')) else 'Error')"

# Verificar PDFs
python -c "import os; print(f'PDFs: {len([f for f in os.listdir(\"ESTANDARES DE SOPORTES\") if f.endswith(\".pdf\")])}')"

# Iniciar servidor
python server.py
```

---

## 📞 Contacto de Soporte

Si los problemas persisten:
1. Verifica que todos los archivos estén en la misma carpeta
2. Asegúrate de tener Python instalado
3. Usa el servidor local siempre
4. Revisa la consola del navegador para errores específicos

---

## 📋 Lista de Archivos Necesarios

✅ **Archivos Esenciales:**
- `index.html` - Interfaz principal
- `app.js` - Lógica de la aplicación  
- `support_data.json` - Datos de soportes (588 KB)
- `support_pdf_mapping.json` - Mapeo de PDFs (2.7 KB)
- `server.py` - Servidor web local
- `INICIAR_SISTEMA.bat` - Iniciador automático

✅ **Carpetas Necesarias:**
- `ESTANDARES DE SOPORTES/` - 752 archivos PDF

✅ **Archivos Opcionales:**
- `README.md` - Documentación completa
- `INSTRUCCIONES_RAPIDAS.txt` - Guía rápida
- `SOLUCION_PROBLEMAS.md` - Este archivo 