#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corregir rutas de PDFs en el archivo JSON
Convierte rutas de Windows a rutas compatibles con servidor web
"""

import json
import os

def corregir_rutas_pdf():
    try:
        print('🔧 CORRIGIENDO RUTAS DE PDFs')
        print('=' * 50)
        
        # Cargar datos originales
        with open('isometric_data_fixed.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f'📊 Cargados {len(data["isometrics"])} isométricos')
        
        # Contadores
        prefab_corregidos = 0
        normal_corregidos = 0
        
        # Corregir rutas en cada isométrico
        for key, iso in data['isometrics'].items():
            # Corregir PDFs prefabricados
            if iso['pdf_files']['prefab']:
                ruta_original = iso['pdf_files']['prefab']
                # Convertir barras invertidas a barras normales
                ruta_corregida = ruta_original.replace('\\', '/')
                iso['pdf_files']['prefab'] = ruta_corregida
                prefab_corregidos += 1
                
                if prefab_corregidos <= 3:  # Mostrar algunos ejemplos
                    print(f'   Prefab {prefab_corregidos}: {ruta_original} → {ruta_corregida}')
            
            # Corregir PDFs normales  
            if iso['pdf_files']['normal']:
                ruta_original = iso['pdf_files']['normal']
                ruta_corregida = ruta_original.replace('\\', '/')
                iso['pdf_files']['normal'] = ruta_corregida
                normal_corregidos += 1
                
                if normal_corregidos <= 3:  # Mostrar algunos ejemplos
                    print(f'   Normal {normal_corregidos}: {ruta_original} → {ruta_corregida}')
        
        print(f'\n✅ RUTAS CORREGIDAS:')
        print(f'   📄 PDFs prefabricados: {prefab_corregidos}')
        print(f'   📄 PDFs normales: {normal_corregidos}')
        
        # Crear backup del archivo original
        print(f'\n💾 Creando backup del archivo original...')
        os.rename('isometric_data_fixed.json', 'isometric_data_fixed.json.backup')
        
        # Guardar archivo corregido
        with open('isometric_data_fixed.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        
        print(f'✅ Archivo corregido guardado como: isometric_data_fixed.json')
        print(f'✅ Backup creado como: isometric_data_fixed.json.backup')
        
        # Verificar que las rutas corregidas funcionan
        print(f'\n🔍 VERIFICANDO RUTAS CORREGIDAS:')
        ejemplos_verificados = 0
        for key, iso in data['isometrics'].items():
            if iso['pdf_files']['prefab'] and ejemplos_verificados < 3:
                ruta = iso['pdf_files']['prefab']
                # Convertir ruta URL de vuelta a ruta de sistema para verificar
                ruta_sistema = ruta.replace('/', os.sep)
                if os.path.exists(ruta_sistema):
                    print(f'   ✅ {ruta} → Archivo verificado')
                else:
                    print(f'   ❌ {ruta} → Archivo NO encontrado')
                ejemplos_verificados += 1
        
        print(f'\n🎯 CORRECCIÓN COMPLETADA')
        print(f'   Las rutas ahora usan "/" y son compatibles con servidores web')
        print(f'   Prueba nuevamente abrir los PDFs en el navegador')
        
    except Exception as e:
        print(f'❌ Error: {e}')

if __name__ == "__main__":
    corregir_rutas_pdf() 