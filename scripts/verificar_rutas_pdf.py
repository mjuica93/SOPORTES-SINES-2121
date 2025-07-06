#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar y mostrar rutas de PDFs
"""

import json
import os
from pathlib import Path

def verificar_rutas_pdf():
    try:
        # Cargar datos
        with open('isometric_data_fixed.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print('🔍 VERIFICACIÓN DE RUTAS DE PDFs')
        print('=' * 50)
        
        # Buscar isométricos con PDFs
        with_prefab = []
        with_normal = []
        
        for key, iso in data['isometrics'].items():
            if iso['pdf_files']['prefab']:
                with_prefab.append((key, iso['pdf_files']['prefab']))
            if iso['pdf_files']['normal']:
                with_normal.append((key, iso['pdf_files']['normal']))
        
        print(f"📊 Isométricos con PDF prefabricado: {len(with_prefab)}")
        print(f"📊 Isométricos con PDF normal: {len(with_normal)}")
        
        # Mostrar ejemplos de rutas prefabricadas
        if with_prefab:
            print('\n🏗️  EJEMPLOS DE RUTAS PDF PREFABRICADAS:')
            for i, (key, ruta) in enumerate(with_prefab[:5]):
                print(f"   {i+1}. {key}: {ruta}")
                
                # Verificar si el archivo existe
                if os.path.exists(ruta):
                    print(f"      ✅ Archivo existe")
                else:
                    print(f"      ❌ Archivo NO existe")
                    
                    # Verificar ruta relativa
                    ruta_relativa = ruta.replace('ISOMETRICOS PREFABRICADOS\\', '').replace('ISOMETRICOS PREFABRICADOS/', '')
                    ruta_relativa = f"ISOMETRICOS PREFABRICADOS/{ruta_relativa}"
                    if os.path.exists(ruta_relativa):
                        print(f"      ✅ Existe como: {ruta_relativa}")
        
        # Mostrar ejemplos de rutas normales  
        if with_normal:
            print('\n📄 EJEMPLOS DE RUTAS PDF NORMALES:')
            for i, (key, ruta) in enumerate(with_normal[:5]):
                print(f"   {i+1}. {key}: {ruta}")
                
                if os.path.exists(ruta):
                    print(f"      ✅ Archivo existe")
                else:
                    print(f"      ❌ Archivo NO existe")
        
        # Verificar estructura de directorios
        print('\n📁 VERIFICACIÓN DE DIRECTORIOS:')
        
        dirs_to_check = [
            'ISOMETRICOS PREFABRICADOS',
            'ISOMETRICOS'
        ]
        
        for dir_name in dirs_to_check:
            if os.path.exists(dir_name):
                files = [f for f in os.listdir(dir_name) if f.endswith('.pdf')]
                print(f"   ✅ {dir_name}: {len(files)} PDFs")
                if files:
                    print(f"      Ejemplo: {files[0]}")
            else:
                print(f"   ❌ {dir_name}: Directorio no existe")
        
        print('\n🔧 PROBLEMA IDENTIFICADO:')
        print('   Las rutas en el JSON probablemente son rutas absolutas de Windows')
        print('   El servidor web necesita rutas relativas desde la raíz del servidor')
        
    except Exception as e:
        print(f'❌ Error: {e}')

if __name__ == "__main__":
    verificar_rutas_pdf() 