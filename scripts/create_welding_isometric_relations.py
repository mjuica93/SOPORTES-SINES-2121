#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crear relaciones entre datos de soldadura e isométricos del sistema
"""

import json
import os
from collections import defaultdict

def create_welding_isometric_relations():
    """Crear relaciones entre soldadura e isométricos"""
    print('🔗 CREANDO RELACIONES SOLDADURA-ISOMÉTRICOS')
    print('=' * 60)
    
    # Cargar datos
    try:
        with open('welding_template_data.json', 'r') as f:
            welding_data = json.load(f)
        
        with open('isometric_data_with_prefabricated.json', 'r') as f:
            isometric_data = json.load(f)
        
        with open('prefabricated_isometric_mapping_github.json', 'r') as f:
            prefab_data = json.load(f)
            
        print(f"📊 Cargados {len(welding_data)} registros de soldadura")
        print(f"📐 Cargadas {len(isometric_data)} líneas de isométricos")
        print(f"🔧 Cargados {len(prefab_data.get('correspondences', {}))} prefabricados")
        
    except Exception as e:
        print(f"❌ Error cargando datos: {e}")
        return
    
    # Procesar relaciones
    welding_relations = []
    welding_by_line = defaultdict(list)
    
    print("\n🔍 Procesando relaciones...")
    
    for weld in welding_data:
        isometric_code = weld.get('isometric', '')
        if not isometric_code:
            continue
            
        # Extraer código de línea del isométrico
        # Formato: 2121-CODIGO-NUMERO -> CODIGO
        if '-' in isometric_code:
            parts = isometric_code.split('-')
            if len(parts) >= 2:
                line_code = parts[1]  # Tomar la parte del medio
                
                # Buscar en isométricos regulares
                found_in_regular = False
                for system_line, line_data in isometric_data.items():
                    if line_code in system_line:
                        relation = {
                            'welding_isometric': isometric_code,
                            'system_line': system_line,
                            'line_code': line_code,
                            'type': 'regular',
                            'weld_data': weld,
                            'isometric_files': [sheet['filename'] for sheet in line_data.get('sheets', [])],
                            'fluid': line_data.get('fluid', ''),
                            'iso_sheet': line_data.get('iso_sheet', '')
                        }
                        welding_relations.append(relation)
                        welding_by_line[system_line].append(weld)
                        found_in_regular = True
                        break
                
                # Si no se encuentra en regulares, buscar en prefabricados
                if not found_in_regular:
                    for prefab_file, prefab_info in prefab_data.get('correspondences', {}).items():
                        if line_code in prefab_file:
                            relation = {
                                'welding_isometric': isometric_code,
                                'system_line': prefab_file,
                                'line_code': line_code,
                                'type': 'prefabricated',
                                'weld_data': weld,
                                'isometric_files': [prefab_file],
                                'fluid': 'Prefabricado',
                                'iso_sheet': prefab_info.get('iso_sheet', '')
                            }
                            welding_relations.append(relation)
                            welding_by_line[prefab_file].append(weld)
                            break
    
    print(f"✅ Creadas {len(welding_relations)} relaciones")
    print(f"📋 Líneas con datos de soldadura: {len(welding_by_line)}")
    
    # Crear estadísticas por línea
    line_statistics = {}
    for line, welds in welding_by_line.items():
        total_welds = len(welds)
        completed_welds = len([w for w in welds if w.get('welded', 0) > 0])
        pending_welds = total_welds - completed_welds
        progress = round((completed_welds / total_welds) * 100) if total_welds > 0 else 0
        
        # Agrupar por diámetro
        diameter_stats = defaultdict(lambda: {'total': 0, 'completed': 0})
        for weld in welds:
            diameter = weld.get('diameter', 0)
            diameter_stats[diameter]['total'] += 1
            if weld.get('welded', 0) > 0:
                diameter_stats[diameter]['completed'] += 1
        
        line_statistics[line] = {
            'total_welds': total_welds,
            'completed_welds': completed_welds,
            'pending_welds': pending_welds,
            'progress_percentage': progress,
            'diameter_breakdown': dict(diameter_stats),
            'welds': welds
        }
    
    # Guardar resultados
    output_files = {
        'welding_isometric_relations.json': welding_relations,
        'welding_line_statistics.json': line_statistics,
        'welding_enhanced_data.json': {
            'relations': welding_relations,
            'statistics': line_statistics,
            'summary': {
                'total_welding_isometrics': len(set(w['welding_isometric'] for w in welding_relations)),
                'total_system_lines': len(welding_by_line),
                'total_welds': len(welding_data),
                'total_relations': len(welding_relations)
            }
        }
    }
    
    for filename, data in output_files.items():
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"💾 Guardado: {filename}")
        except Exception as e:
            print(f"❌ Error guardando {filename}: {e}")
    
    # Mostrar estadísticas
    print(f"\n📊 RESUMEN FINAL:")
    print(f"🔗 Total relaciones: {len(welding_relations)}")
    print(f"📐 Líneas con soldadura: {len(welding_by_line)}")
    print(f"⚡ Total costuras: {len(welding_data)}")
    
    regular_count = len([r for r in welding_relations if r['type'] == 'regular'])
    prefab_count = len([r for r in welding_relations if r['type'] == 'prefabricated'])
    print(f"📋 Regulares: {regular_count}")
    print(f"🔧 Prefabricados: {prefab_count}")
    
    print(f"\n🎯 TOP 5 LÍNEAS CON MÁS COSTURAS:")
    sorted_lines = sorted(welding_by_line.items(), key=lambda x: len(x[1]), reverse=True)
    for i, (line, welds) in enumerate(sorted_lines[:5]):
        stats = line_statistics[line]
        print(f"  {i+1}. {line}: {len(welds)} costuras ({stats['progress_percentage']}% completado)")

if __name__ == "__main__":
    create_welding_isometric_relations() 