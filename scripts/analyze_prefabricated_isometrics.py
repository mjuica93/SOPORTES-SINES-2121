#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analizador de Isométricos Prefabricados
Encuentra relaciones entre isométricos normales y prefabricados
Genera mapeo para integración en el sistema SINES
"""

import os
import json
import re
from collections import defaultdict

def analyze_prefabricated_isometrics():
    """Analiza y relaciona isométricos normales con prefabricados"""
    
    print("=" * 60)
    print("ANÁLISIS DE ISOMÉTRICOS PREFABRICADOS")
    print("=" * 60)
    
    # Directorios de isométricos
    normal_dir = "ISOMETRICOS"
    prefab_dir = "ISOMETRICOS PREFABRICADOS"
    
    if not os.path.exists(normal_dir):
        print(f"❌ Error: No se encuentra la carpeta {normal_dir}")
        return False
        
    if not os.path.exists(prefab_dir):
        print(f"❌ Error: No se encuentra la carpeta {prefab_dir}")
        return False
    
    # Obtener archivos de ambas carpetas
    normal_files = [f for f in os.listdir(normal_dir) if f.endswith('.pdf')]
    prefab_files = [f for f in os.listdir(prefab_dir) if f.lower().endswith('.pdf')]
    
    print(f"📄 Archivos normales encontrados: {len(normal_files)}")
    print(f"🏭 Archivos prefabricados encontrados: {len(prefab_files)}")
    print()
    
    # Analizar patrones de nombres
    print("🔍 ANÁLISIS DE PATRONES DE NOMBRES")
    print("-" * 40)
    
    # Función para extraer código de línea de archivo normal
    def extract_line_code_from_normal(filename):
        """
        Extrae código de línea de archivo normal
        Ejemplo: '19-000-2-02-00001 sheet 2121BU10C13-1_IS01.pdf' -> '2121BU10C13-1'
        """
        match = re.search(r'sheet\s+(\d{4}[A-Z0-9]+\-\d+)', filename)
        if match:
            return match.group(1)
        return None
    
    # Función para convertir código a formato prefabricado
    def format_as_prefab(line_code):
        """
        Convierte código de línea a formato prefabricado
        Ejemplo: '2121BU10C13-1' -> '2121-BU10C13-1'
        """
        if not line_code:
            return None
        # Insertar guión después de los primeros 4 dígitos
        if len(line_code) > 4 and line_code[4].isalpha():
            return f"{line_code[:4]}-{line_code[4:]}"
        return line_code
    
    # Función para extraer código de archivo prefabricado
    def extract_code_from_prefab(filename):
        """
        Extrae código de archivo prefabricado
        Ejemplo: '2121-BU10C13-1.pdf' -> '2121-BU10C13-1'
        """
        return filename.replace('.pdf', '').replace('.PDF', '')
    
    # Crear mapeos
    normal_to_code = {}
    prefab_to_code = {}
    
    # Procesar archivos normales
    print("📋 Procesando archivos normales...")
    for filename in normal_files:
        line_code = extract_line_code_from_normal(filename)
        if line_code:
            prefab_format = format_as_prefab(line_code)
            if prefab_format:
                normal_to_code[filename] = prefab_format
    
    print(f"   ✅ {len(normal_to_code)} códigos extraídos de archivos normales")
    
    # Procesar archivos prefabricados
    print("🏭 Procesando archivos prefabricados...")
    for filename in prefab_files:
        code = extract_code_from_prefab(filename)
        if code:
            prefab_to_code[code] = filename
    
    print(f"   ✅ {len(prefab_to_code)} códigos extraídos de archivos prefabricados")
    print()
    
    # Encontrar correspondencias
    print("🔗 ENCONTRANDO CORRESPONDENCIAS")
    print("-" * 40)
    
    correspondences = {}
    matches_found = 0
    
    for normal_file, expected_prefab_code in normal_to_code.items():
        if expected_prefab_code in prefab_to_code:
            prefab_file = prefab_to_code[expected_prefab_code]
            correspondences[normal_file] = {
                'normal_file': normal_file,
                'prefab_file': prefab_file,
                'line_code': expected_prefab_code,
                'normal_path': f"ISOMETRICOS/{normal_file}",
                'prefab_path': f"ISOMETRICOS PREFABRICADOS/{prefab_file}"
            }
            matches_found += 1
    
    print(f"✅ Correspondencias encontradas: {matches_found}")
    print(f"📊 Porcentaje de cobertura: {(matches_found/len(normal_files)*100):.1f}%")
    print()
    
    # Mostrar algunos ejemplos
    print("📝 EJEMPLOS DE CORRESPONDENCIAS ENCONTRADAS")
    print("-" * 50)
    example_count = 0
    for normal_file, data in correspondences.items():
        if example_count < 5:
            print(f"Normal: {normal_file}")
            print(f"Prefab: {data['prefab_file']}")
            print(f"Código: {data['line_code']}")
            print()
            example_count += 1
    
    if matches_found > 5:
        print(f"... y {matches_found - 5} correspondencias más")
        print()
    
    # Guardar mapeo completo
    output_file = "prefabricated_isometric_mapping.json"
    
    mapping_data = {
        'metadata': {
            'total_normal_files': len(normal_files),
            'total_prefab_files': len(prefab_files),
            'correspondences_found': matches_found,
            'coverage_percentage': round((matches_found/len(normal_files)*100), 1),
            'generated_date': None  # Will be set by JSON encoder
        },
        'correspondences': correspondences
    }
    
    # Añadir fecha de generación
    from datetime import datetime
    mapping_data['metadata']['generated_date'] = datetime.now().isoformat()
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(mapping_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Mapeo guardado en: {output_file}")
    print()
    
    # Crear índice rápido por línea de código
    line_code_index = {}
    for data in correspondences.values():
        line_code = data['line_code']
        if line_code not in line_code_index:
            line_code_index[line_code] = []
        line_code_index[line_code].append(data)
    
    # Guardar índice rápido
    index_file = "prefabricated_line_index.json"
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(line_code_index, f, indent=2, ensure_ascii=False)
    
    print(f"📇 Índice por línea guardado en: {index_file}")
    
    # Análisis de archivos sin correspondencia
    orphan_normal = [f for f in normal_files if f not in correspondences]
    orphan_prefab = [f for f in prefab_files if extract_code_from_prefab(f) not in [data['line_code'] for data in correspondences.values()]]
    
    print()
    print("📋 ARCHIVOS SIN CORRESPONDENCIA")
    print("-" * 35)
    print(f"Normal sin prefabricado: {len(orphan_normal)}")
    print(f"Prefabricado sin normal: {len(orphan_prefab)}")
    
    if orphan_prefab:
        print("\n🏭 Prefabricados únicos (sin normal correspondiente):")
        for i, filename in enumerate(orphan_prefab[:10]):  # Mostrar solo los primeros 10
            print(f"   {filename}")
        if len(orphan_prefab) > 10:
            print(f"   ... y {len(orphan_prefab) - 10} más")
    
    # Guardar estadísticas detalladas
    stats_file = "prefabricated_analysis_stats.json"
    stats_data = {
        'analysis_summary': {
            'total_normal_files': len(normal_files),
            'total_prefab_files': len(prefab_files),
            'correspondences_found': matches_found,
            'coverage_percentage': round((matches_found/len(normal_files)*100), 1),
            'orphan_normal_files': len(orphan_normal),
            'orphan_prefab_files': len(orphan_prefab),
            'unique_line_codes': len(line_code_index)
        },
        'orphan_normal_files': orphan_normal[:50],  # Límite para no sobrecargar
        'orphan_prefab_files': orphan_prefab,
        'line_code_statistics': {
            code: len(files) for code, files in line_code_index.items()
        }
    }
    
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats_data, f, indent=2, ensure_ascii=False)
    
    print(f"📊 Estadísticas detalladas guardadas en: {stats_file}")
    print()
    
    # Resumen final
    print("✅ ANÁLISIS COMPLETADO")
    print("=" * 25)
    print(f"✓ {matches_found} correspondencias establecidas")
    print(f"✓ {len(line_code_index)} códigos de línea únicos")
    print(f"✓ Cobertura del {(matches_found/len(normal_files)*100):.1f}%")
    print("✓ Archivos JSON generados para integración")
    print()
    
    return True

if __name__ == "__main__":
    success = analyze_prefabricated_isometrics()
    if success:
        print("🎉 Análisis de isométricos prefabricados completado exitosamente")
    else:
        print("❌ Error durante el análisis de isométricos prefabricados") 