#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de debug para entender el emparejamiento de isométricos con costuras
"""

import pandas as pd
import json

# Cargar isométricos
with open('isometric_data_fixed.json', 'r', encoding='utf-8') as f:
    isometric_data = json.load(f)

print("🔍 ANÁLISIS DE EMPAREJAMIENTO")
print("=" * 50)

# Mostrar algunos nombres de isométricos
iso_names = list(isometric_data['isometrics'].keys())
print(f"📋 Isométricos disponibles (primeros 10):")
for i, name in enumerate(iso_names[:10]):
    print(f"  {i+1}. '{name}'")

print(f"\n📊 Total isométricos: {len(iso_names)}")

# Cargar costuras
welding_file = "PREFABRICATING WELDING DATABASE/Welding Database updated 20250605 for 2121 Workshop.xlsx"
df_mene = pd.read_excel(welding_file, sheet_name='MENE')

weld_isos = df_mene['Isometric'].dropna().unique()
print(f"\n📋 Isométricos en costuras (primeros 10):")
for i, name in enumerate(weld_isos[:10]):
    print(f"  {i+1}. '{name}'")

print(f"\n📊 Total isométricos en costuras: {len(weld_isos)}")

# Buscar coincidencias
matches = []
for weld_iso in weld_isos:
    if weld_iso in iso_names:
        matches.append(weld_iso)

print(f"\n🎯 Coincidencias encontradas: {len(matches)}")
if matches:
    print(f"   Primeras 5 coincidencias:")
    for i, match in enumerate(matches[:5]):
        print(f"     {i+1}. '{match}'")

# Buscar coincidencias parciales
print(f"\n🔍 Búsqueda de coincidencias parciales:")
partial_matches = []
for weld_iso in weld_isos[:5]:  # Solo primeros 5 para no saturar
    for iso_name in iso_names[:20]:  # Solo primeros 20 para no saturar
        if weld_iso in iso_name or iso_name in weld_iso:
            partial_matches.append((weld_iso, iso_name))
            print(f"   Posible: '{weld_iso}' <-> '{iso_name}'")

print(f"\n📊 Coincidencias parciales: {len(partial_matches)}")

# Mostrar formatos
print(f"\n📝 ANÁLISIS DE FORMATOS:")
print(f"   Formato costuras: {weld_isos[0] if len(weld_isos) > 0 else 'N/A'}")
print(f"   Formato isométricos: {iso_names[0] if len(iso_names) > 0 else 'N/A'}")

# Buscar patrón de naming
print(f"\n🔍 PATRONES DE NAMING:")
print(f"   Costuras empiezan con '2121'? {all(str(w).startswith('2121') for w in weld_isos[:10])}")
print(f"   Isométricos empiezan con '2121'? {all(str(w).startswith('2121') for w in iso_names[:10])}") 