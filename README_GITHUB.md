# 🔍 Sistema de Búsqueda de Soportes SINES

[![Deployed on Railway](https://img.shields.io/badge/Deployed%20on-Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white)](https://railway.app)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

## 📋 Descripción

Sistema web para la búsqueda y consulta de estándares de soportes SINES. Permite buscar, filtrar y visualizar documentos PDF de manera eficiente y optimizada.

## ✨ Características

- 🔍 **Búsqueda Avanzada**: Busca por código, descripción, tipo y más
- 📱 **Responsive**: Optimizado para móviles y escritorio
- 🎯 **Filtros Inteligentes**: Filtros por categoría, tipo, etc.
- 📄 **Visualización PDF**: Visualización directa de documentos
- 🚀 **Rápido**: Carga y búsqueda instantánea
- 🌐 **Acceso Global**: Disponible mundialmente

## 🚀 Acceso Directo

### 🌍 Versión Web
[![Abrir Sistema](https://img.shields.io/badge/🌐%20Abrir%20Sistema-4285F4?style=for-the-badge&logo=google-chrome&logoColor=white)](https://tu-proyecto.railway.app)

### 📱 Versión Móvil
[![Abrir Móvil](https://img.shields.io/badge/📱%20Versión%20Móvil-FF6B6B?style=for-the-badge&logo=mobile&logoColor=white)](https://tu-proyecto.railway.app/mobile)

## 🛠️ Tecnologías

- **Backend**: Python 3.11+ (servidor HTTP nativo)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Datos**: JSON con más de 750 documentos PDF
- **Despliegue**: Railway.app con Docker

## 📊 Datos Incluidos

- ✅ **750+ documentos PDF** de estándares SINES
- ✅ **Metadatos completos** de cada documento
- ✅ **Categorización automática** por tipo
- ✅ **Índices de búsqueda** optimizados

## 🔧 Instalación Local

### Prerrequisitos
- Python 3.11+
- Git

### Pasos

1. **Clonar repositorio**
   ```bash
   git clone https://github.com/tu-usuario/sistema-sines.git
   cd sistema-sines
   ```

2. **Ejecutar servidor**
   ```bash
   python server.py
   ```

3. **Abrir navegador**
   ```
   http://localhost:8000
   ```

## 🌐 Despliegue en Railway

### Método 1: Desde GitHub (Recomendado)

1. **Fork este repositorio**
2. **Ve a [Railway.app](https://railway.app)**
3. **Conecta tu cuenta GitHub**
4. **Selecciona este repositorio**
5. **¡Listo!** Tu sistema estará disponible en minutos

### Método 2: Deploy Button

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template/python)

## 📱 Versiones Disponibles

### 🖥️ Escritorio
- **URL**: `https://tu-proyecto.railway.app`
- **Características**: Interfaz completa con todas las funciones

### 📱 Móvil
- **URL**: `https://tu-proyecto.railway.app/mobile`
- **Características**: Interfaz optimizada para dispositivos móviles

### 🎨 Con Plantillas
- **URL**: `https://tu-proyecto.railway.app/index_enhanced_with_templates.html`
- **Características**: Interfaz con plantillas visuales avanzadas

## 🔍 Uso del Sistema

### Búsqueda Básica
1. Ingresa el código o descripción del soporte
2. Presiona Enter o haz clic en "Buscar"
3. Los resultados aparecen instantáneamente

### Filtros Avanzados
- **Por Tipo**: BA, BE, BW, C, EH, EW, etc.
- **Por Categoría**: Soportes, Notas Generales, etc.
- **Por Descripción**: Busca en el contenido

### Visualización
- **Clic en resultado**: Abre el PDF directamente
- **Vista previa**: Información detallada del documento
- **Descarga**: Descarga directa del PDF

## 📁 Estructura del Proyecto

```
sistema-sines/
├── 📄 server_railway.py          # Servidor optimizado para Railway
├── 📄 server.py                  # Servidor local
├── 📄 index.html                 # Interfaz principal
├── 📄 index_mobile.html          # Versión móvil
├── 📄 app.js                     # Lógica de la aplicación
├── 📄 support_data_enhanced.json # Base de datos de soportes
├── 📄 support_pdf_mapping.json   # Mapeo de archivos PDF
├── 📁 ESTANDARES DE SOPORTES/    # Documentos PDF (750+)
├── 🐳 Dockerfile                 # Configuración Docker
├── ⚙️ railway.json               # Configuración Railway
├── 📄 requirements.txt           # Dependencias Python
└── 📄 README.md                  # Este archivo
```

## 💡 Características Técnicas

### Performance
- ⚡ **Carga instantánea**: < 2 segundos
- 🔍 **Búsqueda rápida**: < 100ms
- 📱 **Optimizado**: Funciona en móviles 3G

### Compatibilidad
- 🌐 **Navegadores**: Chrome, Firefox, Safari, Edge
- 📱 **Móviles**: iOS, Android
- 💻 **SO**: Windows, macOS, Linux

### Seguridad
- 🔒 **HTTPS**: Conexión segura
- 🛡️ **CORS**: Configurado correctamente
- 🔐 **Headers**: Headers de seguridad incluidos

## 🤝 Contribuir

Las contribuciones son bienvenidas. Para cambios importantes:

1. Fork el proyecto
2. Crea una rama para tu función (`git checkout -b feature/nueva-funcion`)
3. Commit tus cambios (`git commit -am 'Agrega nueva función'`)
4. Push a la rama (`git push origin feature/nueva-funcion`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

## 🆘 Soporte

¿Necesitas ayuda?

- 📧 **Email**: soporte@tu-dominio.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/tu-usuario/sistema-sines/issues)
- 📖 **Documentación**: [Wiki](https://github.com/tu-usuario/sistema-sines/wiki)

---

<div align="center">
  <p>
    <strong>🌟 ¡Dale una estrella si te gusta este proyecto! 🌟</strong>
  </p>
  <p>
    Hecho con ❤️ para la comunidad SINES
  </p>
</div> 