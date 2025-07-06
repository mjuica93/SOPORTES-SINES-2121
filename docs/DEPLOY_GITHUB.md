# 🚀 Guía de Despliegue en GitHub

## 📋 Pasos para Subir a GitHub

### 1. Crear Repositorio en GitHub
1. Ve a [GitHub.com](https://github.com)
2. Haz clic en **"New repository"**
3. Nombre sugerido: `soportes-sines`
4. Descripción: `Sistema integral para gestión de soportes, isométricos y costuras de soldadura`
5. **NO** inicializar con README (ya tenemos uno)
6. Haz clic en **"Create repository"**

### 2. Conectar Repositorio Local con GitHub

```bash
# Agregar origen remoto (reemplaza TU-USUARIO con tu nombre de usuario)
git remote add origin https://github.com/TU-USUARIO/soportes-sines.git

# Verificar conexión
git remote -v

# Subir código a GitHub
git push -u origin master
```

### 3. Configurar GitHub Pages (Opcional)

Si quieres que sea accesible públicamente:

1. Ve a **Settings** del repositorio
2. Scroll down hasta **Pages**
3. Source: **Deploy from a branch**
4. Branch: **master**
5. Folder: **/ (root)**
6. Haz clic en **Save**

**⚠️ Nota**: GitHub Pages solo sirve archivos estáticos. Para el servidor Python necesitarás otros servicios.

## 🌐 Opciones de Despliegue

### Opción 1: Heroku (Recomendado)
```bash
# Instalar Heroku CLI
# Crear Procfile
echo "web: python src/server.py" > Procfile

# Desplegar
heroku create tu-app-sines
git push heroku master
```

### Opción 2: Railway
```bash
# Crear railway.json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python src/server.py",
    "healthcheckPath": "/api/status"
  }
}
```

### Opción 3: Render
1. Conectar repositorio en [Render.com](https://render.com)
2. Build Command: `pip install -r requirements.txt`
3. Start Command: `python src/server.py`

### Opción 4: Local/VPS
```bash
# Clonar repositorio
git clone https://github.com/TU-USUARIO/soportes-sines.git
cd soportes-sines

# Ejecutar
python start.py
```

## 🔧 Variables de Entorno

Para producción, configura estas variables:

```bash
# Puerto (opcional, default: 8000)
PORT=8000

# Modo debug (opcional, default: False)
DEBUG=False

# Timeout de sesión en minutos (opcional, default: 30)
SESSION_TIMEOUT=30

# Clave secreta para sesiones (recomendado cambiar)
SECRET_KEY=tu-clave-secreta-aqui
```

## 📊 Estructura Final del Repositorio

```
soportes-sines/
├── 📁 src/                 # Código fuente
│   ├── index.html         # Interfaz principal
│   ├── server.py          # Servidor seguro
│   └── logout_manager.js  # Gestión de sesiones
├── 📁 data/               # Datos JSON
│   ├── support_data_enhanced.json
│   ├── welding_enhanced_data.json
│   └── [85 archivos JSON]
├── 📁 docs/               # Documentación
│   └── DEPLOY_GITHUB.md   # Esta guía
├── 📁 scripts/            # Scripts auxiliares
├── 📄 README.md           # Documentación principal
├── 📄 start.py            # Script de inicio
├── 📄 requirements.txt    # Dependencias
├── 📄 LICENSE             # Licencia MIT
└── 📄 .gitignore          # Archivos ignorados
```

## ✅ Verificación Post-Despliegue

1. **Funcionalidad básica**:
   - [ ] Página de login carga correctamente
   - [ ] Autenticación funciona
   - [ ] Pestañas principales accesibles

2. **Gestión de soportes**:
   - [ ] Vista agrupada funciona
   - [ ] Variables de plantilla se muestran
   - [ ] Búsqueda y filtros operativos

3. **Control de costuras**:
   - [ ] Modal de gestión abre
   - [ ] Estadísticas en tiempo real
   - [ ] Cambios de estado funcionan

4. **Seguridad**:
   - [ ] Logout funciona
   - [ ] Sesiones expiran correctamente
   - [ ] Acceso por roles operativo

## 🆘 Solución de Problemas

### Error: "Port already in use"
```bash
# Cambiar puerto en src/server.py línea ~15
PORT = 8001  # o cualquier puerto libre
```

### Error: "Module not found"
```bash
# Instalar dependencias
pip install -r requirements.txt
```

### Error: "JSON files not found"
```bash
# Verificar estructura de carpetas
ls -la data/
# Debe contener los archivos JSON
```

### Error de autenticación
```bash
# Limpiar cookies del navegador
# Reiniciar servidor
python start.py
```

## 📞 Soporte

- **Documentación**: README.md principal
- **Issues**: GitHub Issues del repositorio
- **Wiki**: GitHub Wiki (si está habilitado)

---

**🎉 ¡Tu Sistema SINES está listo para GitHub!** 🚀 