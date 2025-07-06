#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para analizar patrones de PDFs normales en carpeta ISOMETRICOS
"""

import os
import re
from collections import defaultdict

def analizar_pdfs_normales():
    print('🔍 ANÁLISIS DE PDFs NORMALES')
    print('=' * 50)
    
    iso_dir = "ISOMETRICOS"
    if not os.path.exists(iso_dir):
        print(f"❌ Carpeta {iso_dir} no existe")
        return
    
    # Obtener todos los PDFs
    pdfs = [f for f in os.listdir(iso_dir) if f.endswith('.pdf')]
    print(f"📊 Total PDFs encontrados: {len(pdfs)}")
    
    # Mostrar ejemplos de nombres
    print(f"\n📋 EJEMPLOS DE NOMBRES DE ARCHIVOS:")
    for i, pdf in enumerate(pdfs[:10]):
        print(f"   {i+1}. {pdf}")
    
    # Analizar patrones usando regex
    print(f"\n🔍 ANÁLISIS DE PATRONES:")
    
    # Patrón actual que está fallando
    patron_actual = r'sheet\s+(.+?)_IS\d+\.pdf'
    print(f"Patrón actual: {patron_actual}")
    
    coincidencias = 0
    for pdf in pdfs[:10]:
        match = re.search(patron_actual, pdf, re.IGNORECASE)
        if match:
            coincidencias += 1
            sheet_part = match.group(1).strip()
            print(f"   ✅ {pdf} → sheet_part: {sheet_part}")
        else:
            print(f"   ❌ {pdf} → NO coincide")
    
    print(f"\nCoincidencias con patrón actual: {coincidencias}/{len(pdfs[:10])} ejemplos")
    
    # Analizar estructura para proponer mejor patrón
    print(f"\n🔧 ANÁLISIS PARA MEJOR PATRÓN:")
    
    for pdf in pdfs[:5]:
        print(f"\nAnalizando: {pdf}")
        
        # Buscar diferentes partes
        if "sheet" in pdf.lower():
            parts = pdf.split('sheet')
            if len(parts) > 1:
                after_sheet = parts[1].strip()
                print(f"   Después de 'sheet': {after_sheet}")
                
                # Buscar patrón LINE-SHEET
                if after_sheet.startswith(' '):
                    after_sheet = after_sheet[1:]  # Remover espacio inicial
                
                # Intentar extraer usando diferentes patrones
                patterns_to_try = [
                    r'(\d+)([A-Z]+\d+[A-Z]+\d+)-(\d+)_IS',  # 2121BU10C13-1_IS
                    r'([A-Z]+\d+[A-Z]+\d+)-(\d+)_IS',       # BU10C13-1_IS
                    r'(\d+)([A-Z]+\d+[A-Z]+\d+)-(\d+)',     # Sin _IS
                    r'([A-Z]+\d+[A-Z]+\d+)-(\d+)',         # Más simple
                ]
                
                for i, pattern in enumerate(patterns_to_try):
                    match = re.search(pattern, after_sheet)
                    if match:
                        groups = match.groups()
                        print(f"   Patrón {i+1} funciona: {groups}")
                        
                        if len(groups) >= 2:
                            if len(groups) == 3:  # Incluye prefijo numérico
                                line = groups[1]
                                sheet = groups[2]
                            else:  # Solo LINE-SHEET
                                line = groups[0]
                                sheet = groups[1]
                            print(f"      → LINE: {line}, SHEET: {sheet}")
                        break

def proponer_solucion():
    print(f"\n💡 PROPUESTA DE SOLUCIÓN:")
    print(f"1. Actualizar patrón de búsqueda en fix_isometric_system.py")
    print(f"2. Regenerar archivo JSON con mapeo corregido")
    print(f"3. Verificar que ambos tipos de PDFs están disponibles")

if __name__ == "__main__":
    analizar_pdfs_normales()
    proponer_solucion() 