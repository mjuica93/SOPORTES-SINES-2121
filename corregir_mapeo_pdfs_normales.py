#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corregir el mapeo de PDFs normales
Implementa el patrón correcto para extraer LINE y SHEET
"""

import json
import os
import re
from pathlib import Path

def mapear_pdfs_normales_corregido():
    print('🔧 CORRIGIENDO MAPEO DE PDFs NORMALES')
    print('=' * 50)
    
    # Cargar datos actuales
    with open('isometric_data_fixed.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f'📊 Isométricos cargados: {len(data["isometrics"])}')
    
    # Mapear PDFs normales
    iso_dir = Path("ISOMETRICOS")
    pdfs_normales_mapeados = 0
    ejemplos = []
    
    if iso_dir.exists():
        for pdf_file in iso_dir.glob("*.pdf"):
            # Patrón mejorado para PDFs normales
            # Ejemplo: '19-000-2-02-00001 sheet 2121BU10C13-1_IS01.pdf'
            match = re.search(r'sheet\s+2121([A-Z0-9]+)-(\d+)_IS\d+\.pdf', pdf_file.name, re.IGNORECASE)
            if match:
                line = match.group(1)  # BU10C13 (sin el prefijo 2121)
                sheet = match.group(2)  # 1
                iso_key = f"{line}-{sheet}"
                
                # Verificar si este isométrico existe en nuestros datos
                if iso_key in data['isometrics']:
                    # Convertir ruta a formato web
                    ruta_web = str(pdf_file).replace('\\', '/')
                    data['isometrics'][iso_key]['pdf_files']['normal'] = ruta_web
                    pdfs_normales_mapeados += 1
                    
                    # Guardar ejemplos para mostrar
                    if len(ejemplos) < 5:
                        ejemplos.append((pdf_file.name, line, sheet, iso_key))
                else:
                    # Si no existe, podríamos crearlo (pero mejor no para mantener consistencia)
                    pass
    
    print(f'✅ PDFs normales mapeados: {pdfs_normales_mapeados}')
    
    # Mostrar ejemplos
    print(f'\n📋 EJEMPLOS DE MAPEO:')
    for filename, line, sheet, iso_key in ejemplos:
        print(f'   {filename}')
        print(f'      → LINE: {line}, SHEET: {sheet}')
        print(f'      → Clave: {iso_key}')
        print(f'      → ✅ Mapeado exitosamente')
        print()
    
    # Actualizar estadísticas
    data['summary']['isometrics_with_normal_pdf'] = len([
        iso for iso in data['isometrics'].values() 
        if iso['pdf_files']['normal']
    ])
    
    # Guardar archivo actualizado
    print(f'💾 Guardando archivo actualizado...')
    with open('isometric_data_fixed.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    
    # Mostrar estadísticas finales
    summary = data['summary']
    print(f'\n📊 ESTADÍSTICAS FINALES:')
    print(f'   📐 Total isométricos: {summary["total_isometrics"]}')
    print(f'   🔧 Con soportes: {summary["isometrics_with_supports"]}')
    print(f'   📄 Con PDF normal: {summary["isometrics_with_normal_pdf"]}')
    print(f'   🏗️  Con PDF prefab: {summary["isometrics_with_prefab_pdf"]}')
    print(f'   📈 Total soportes: {summary["total_supports"]}')
    
    # Verificar que ambos tipos están disponibles
    print(f'\n🔍 VERIFICACIÓN DUAL:')
    ambos_tipos = 0
    solo_normal = 0
    solo_prefab = 0
    
    for iso in data['isometrics'].values():
        has_normal = bool(iso['pdf_files']['normal'])
        has_prefab = bool(iso['pdf_files']['prefab'])
        
        if has_normal and has_prefab:
            ambos_tipos += 1
        elif has_normal:
            solo_normal += 1
        elif has_prefab:
            solo_prefab += 1
    
    print(f'   🎯 Con ambos tipos: {ambos_tipos}')
    print(f'   📄 Solo PDF normal: {solo_normal}')
    print(f'   🏗️  Solo PDF prefab: {solo_prefab}')
    
    print(f'\n✅ CORRECCIÓN COMPLETADA')
    print(f'   Ahora tienes acceso a ambos tipos de isométricos!')

if __name__ == "__main__":
    mapear_pdfs_normales_corregido() 