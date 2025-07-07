@echo off
chcp 65001 > nul
echo.
echo ==========================================
echo 🔒 SERVIDOR SEGURO HÍBRIDO SINES
echo ==========================================
echo.
echo ✅ CARACTERÍSTICAS:
echo • Autenticación dual (cookies + tokens)
echo • Compatible con ventanas múltiples
echo • Panel de configuración funcional
echo • Sesiones con timeout (30 min)
echo • Control de acceso por roles
echo.
echo 🔑 CREDENCIALES:
echo ┌─────────────┬──────────────┬───────────────┐
echo │ Usuario     │ Contraseña   │ Permisos      │
echo ├─────────────┼──────────────┼───────────────┤
echo │ admin       │ sines2024    │ ✅ Panel Config │
echo │ supervisor  │ super2024    │ ✅ Panel Config │
echo │ operador    │ op2024       │ ❌ Solo sistema │
echo │ sines       │ sines123     │ ❌ Solo sistema │
echo └─────────────┴──────────────┴───────────────┘
echo.
echo 🚀 Iniciando servidor híbrido en puerto 8003...
echo.
py server_secure_hybrid.py 