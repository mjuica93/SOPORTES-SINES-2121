#!/usr/bin/env python3
"""
Script para actualizar el archivo JSON de mapeo de prefabricados para usar URLs de GitHub
"""

import json

def update_prefab_mapping_for_github():
    """Actualiza el archivo JSON de mapeo para usar URLs de GitHub"""
    
    # URL base de GitHub Raw
    GITHUB_BASE = "https://raw.githubusercontent.com/mjuica93/SOPORTES-SINES-2121/main"
    
    # Leer el archivo JSON original
    with open('prefabricated_isometric_mapping.json', 'r', encoding='utf-8') as f:
        mapping_data = json.load(f)
    
    # Actualizar las rutas en las correspondencias
    changes_count = 0
    
    for filename, mapping in mapping_data.get('correspondences', {}).items():
        # Actualizar rutas normal y prefab
        if 'normal_path' in mapping and mapping['normal_path'].startswith('ISOMETRICOS/'):
            mapping['normal_path'] = f"{GITHUB_BASE}/{mapping['normal_path']}"
            changes_count += 1
            
        if 'prefab_path' in mapping and mapping['prefab_path'].startswith('ISOMETRICOS PREFABRICADOS/'):
            # Codificar espacios en la URL
            prefab_path = mapping['prefab_path'].replace('ISOMETRICOS PREFABRICADOS/', 'ISOMETRICOS%20PREFABRICADOS/')
            mapping['prefab_path'] = f"{GITHUB_BASE}/{prefab_path}"
            changes_count += 1
    
    # Actualizar metadatos
    if 'metadata' in mapping_data:
        mapping_data['metadata']['updated_for_github'] = True
        mapping_data['metadata']['github_base_url'] = GITHUB_BASE
    
    # Guardar el archivo actualizado
    with open('prefabricated_isometric_mapping_github.json', 'w', encoding='utf-8') as f:
        json.dump(mapping_data, f, indent=2, ensure_ascii=False)
    
    print("✅ Archivo JSON de mapeo actualizado para GitHub creado: prefabricated_isometric_mapping_github.json")
    print(f"🌐 URLs base configuradas para: {GITHUB_BASE}")
    print(f"📊 Total de rutas actualizadas: {changes_count}")
    print(f"📋 Correspondencias procesadas: {len(mapping_data.get('correspondences', {}))}")

if __name__ == "__main__":
    update_prefab_mapping_for_github() 