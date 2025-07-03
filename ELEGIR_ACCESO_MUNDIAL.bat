@echo off
title SINES Soportes - Selector de Acceso Mundial
color 0F

:menu
cls
echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █           SISTEMA SINES - ACCESO MUNDIAL                    █
echo █                                                              █
echo █               SELECCIONA TU OPCIÓN PREFERIDA                █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.
echo 🌐 OPCIONES DISPONIBLES:
echo.
echo ┌─────────────────────────────────────────────────────────────┐
echo │                    OPCIONES GRATUITAS                      │
echo └─────────────────────────────────────────────────────────────┘
echo.
echo  1. 🆓 NGROK - Rápido y Temporal
echo     ├─ Configuración: 5 minutos
echo     ├─ Costo: Gratis
echo     ├─ URL: Temporal (8 horas)
echo     └─ Ideal para: Pruebas y demos
echo.
echo  2. 🆓 CLOUDFLARE TUNNEL - Profesional Gratuito
echo     ├─ Configuración: 10 minutos
echo     ├─ Costo: Gratis para siempre
echo     ├─ URL: Permanente
echo     └─ Ideal para: Uso profesional sin pagar
echo.
echo ┌─────────────────────────────────────────────────────────────┐
echo │                    OPCIONES DE PAGO                        │
echo └─────────────────────────────────────────────────────────────┘
echo.
echo  3. 💰 RAILWAY - Mejor Precio
echo     ├─ Configuración: 15 minutos
echo     ├─ Costo: $5/mes
echo     ├─ URL: Permanente
echo     └─ Ideal para: Uso profesional económico
echo.
echo  4. 💰 RENDER - Más Fácil
echo     ├─ Configuración: 5 minutos
echo     ├─ Costo: $7/mes
echo     ├─ URL: Permanente
echo     └─ Ideal para: Máxima simplicidad
echo.
echo  5. 📋 VER COMPARACIÓN COMPLETA
echo     └─ Tabla detallada de todas las opciones
echo.
echo  0. ❌ SALIR
echo.
echo ════════════════════════════════════════════════════════════════
echo.
set /p choice=🎯 Selecciona una opción (0-5): 

if "%choice%"=="1" goto ngrok
if "%choice%"=="2" goto cloudflare
if "%choice%"=="3" goto railway
if "%choice%"=="4" goto render
if "%choice%"=="5" goto comparacion
if "%choice%"=="0" goto salir

echo.
echo ❌ Opción no válida. Intenta nuevamente.
timeout /t 2 >nul
goto menu

:ngrok
cls
echo.
echo 🆓 NGROK - Acceso Rápido y Temporal
echo ═══════════════════════════════════════
echo.
echo ✅ Ventajas:
echo   • Configuración en 5 minutos
echo   • Funciona inmediatamente
echo   • HTTPS automático
echo   • Ideal para pruebas
echo.
echo ⚠️  Limitaciones:
echo   • URL cambia cada reinicio
echo   • Sesión expira en 8 horas
echo   • Límite de 20 conexiones
echo.
echo 🚀 Iniciando configuración...
echo.
pause
call ACCESO_MUNDIAL.bat
goto menu

:cloudflare
cls
echo.
echo 🆓 CLOUDFLARE TUNNEL - Profesional Gratuito
echo ═══════════════════════════════════════════════
echo.
echo ✅ Ventajas:
echo   • Completamente gratuito para siempre
echo   • URL permanente
echo   • Disponibilidad 24/7
echo   • Protección DDoS
echo   • CDN global ultra-rápido
echo   • Sin límites de conexión
echo.
echo ⚠️  Consideraciones:
echo   • Requiere cuenta Cloudflare
echo   • Configuración más compleja
echo.
echo 🚀 Iniciando configuración...
echo.
pause
call ACCESO_CLOUDFLARE_GRATIS.bat
goto menu

:railway
cls
echo.
echo 💰 RAILWAY - Mejor Precio ($5/mes)
echo ═══════════════════════════════════════
echo.
echo ✅ Ventajas:
echo   • Precio más bajo
echo   • Interfaz moderna
echo   • Escalabilidad automática
echo   • Configuración automática
echo   • URL permanente
echo   • Disponibilidad 24/7
echo.
echo 💰 Costo: $5/mes
echo.
echo 🚀 Iniciando configuración...
echo.
pause
call DESPLEGAR_RAILWAY.bat
goto menu

:render
cls
echo.
echo 💰 RENDER - Máxima Facilidad ($7/mes)
echo ═══════════════════════════════════════════
echo.
echo ✅ Ventajas:
echo   • Configuración súper fácil
echo   • Interfaz intuitiva
echo   • Soporte excelente
echo   • Muy confiable
echo   • URL permanente
echo   • Disponibilidad 24/7
echo.
echo 💰 Costo: $7/mes
echo.
echo 🚀 Iniciando configuración...
echo.
pause
call DESPLEGAR_RENDER.bat
goto menu

:comparacion
cls
echo.
echo 📊 COMPARACIÓN COMPLETA DE OPCIONES
echo ═════════════════════════════════════════════════════════════════
echo.
echo ┌──────────────────┬───────────┬──────────────┬───────────────┐
echo │ Opción           │ Precio    │ URL Permanente │ Disponibilidad │
echo ├──────────────────┼───────────┼──────────────┼───────────────┤
echo │ Ngrok            │ 🆓 Gratis │ ❌ No         │ 8 horas       │
echo │ Cloudflare       │ 🆓 Gratis │ ✅ Sí         │ 24/7          │
echo │ Railway          │ 💰 $5/mes │ ✅ Sí         │ 24/7          │
echo │ Render           │ 💰 $7/mes │ ✅ Sí         │ 24/7          │
echo │ Vercel           │ 💰 $20/mes│ ✅ Sí         │ 24/7          │
echo │ AWS/Azure        │ 💰 $15-50 │ ✅ Sí         │ 24/7          │
echo └──────────────────┴───────────┴──────────────┴───────────────┘
echo.
echo 🎯 RECOMENDACIONES:
echo.
echo 🆓 Para uso gratuito: CLOUDFLARE TUNNEL
echo   • Completamente gratuito
echo   • Profesional y permanente
echo   • Protección DDoS incluida
echo.
echo 💰 Para uso de pago: RAILWAY
echo   • Precio más bajo ($5/mes)
echo   • Fácil de usar
echo   • Excelente relación precio/calidad
echo.
echo 💼 Para máxima facilidad: RENDER
echo   • Configuración súper simple
echo   • Interfaz intuitiva
echo   • Soporte técnico excelente
echo.
echo 📱 ACCESO MÓVIL:
echo   Todas las opciones incluyen versión móvil optimizada
echo   URL: [tu-url]/index_mobile.html
echo.
echo ═════════════════════════════════════════════════════════════════
echo.
pause
goto menu

:salir
cls
echo.
echo 👋 ¡Gracias por usar el Sistema SINES!
echo.
echo 💡 Recuerda:
echo   • Tu sistema local sigue funcionando en localhost:8000
echo   • Para acceso mundial, ejecuta cualquiera de las opciones
echo   • Todas incluyen versión móvil optimizada
echo.
echo 🌐 ¡Tu sistema estará disponible mundialmente en minutos!
echo.
pause
exit 