#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procesamiento de datos de soldadura para sistema de seguimiento
"""

import json
import os
from collections import defaultdict

def process_welding_status():
    """Procesa los datos de soldadura y genera estadísticas por isométrico"""
    print('🔧 PROCESANDO ESTADO DE SOLDADURA')
    print('=' * 60)
    
    # Cargar datos del welding template
    if not os.path.exists('welding_template_data.json'):
        print("❌ Archivo welding_template_data.json no encontrado")
        return None
    
    with open('welding_template_data.json', 'r', encoding='utf-8') as f:
        welding_data = json.load(f)
    
    print(f"📊 Procesando {len(welding_data)} registros de soldadura...")
    
    # Agrupar por isométrico
    isometric_welds = defaultdict(list)
    
    for weld in welding_data:
        isometric = weld['isometric']
        # Filtrar solo isométricos que empiecen con "2121-" (nuestro proyecto)
        if isometric.startswith('2121-'):
            isometric_welds[isometric].append(weld)
    
    print(f"✅ Encontrados {len(isometric_welds)} isométricos del proyecto 2121")
    
    # Generar estadísticas por isométrico
    welding_status_data = {}
    
    for isometric, welds in isometric_welds.items():
        total_welds = len(welds)
        completed_welds = len([w for w in welds if w['status'] == 'completada'])
        pending_welds = total_welds - completed_welds
        
        # Calcular diámetros totales
        total_diameter = sum(w['diameter'] for w in welds)
        welded_diameter = sum(w['welded'] for w in welds)
        
        # Agrupar por diámetro
        diameter_stats = defaultdict(lambda: {'total': 0, 'welded': 0, 'count': 0})
        
        for weld in welds:
            diameter = weld['diameter']
            diameter_stats[diameter]['total'] += diameter
            diameter_stats[diameter]['welded'] += weld['welded']
            diameter_stats[diameter]['count'] += 1
        
        # Convertir a lista ordenada
        diameter_breakdown = []
        for diameter in sorted(diameter_stats.keys()):
            stats = diameter_stats[diameter]
            completion_pct = (stats['welded'] / stats['total'] * 100) if stats['total'] > 0 else 0
            
            diameter_breakdown.append({
                'diameter': diameter,
                'total_length': stats['total'],
                'welded_length': stats['welded'],
                'weld_count': stats['count'],
                'completion_percentage': round(completion_pct, 1)
            })
        
        # Calcular porcentaje de completitud general
        overall_completion = (welded_diameter / total_diameter * 100) if total_diameter > 0 else 0
        
        welding_status_data[isometric] = {
            'isometric': isometric,
            'total_welds': total_welds,
            'completed_welds': completed_welds,
            'pending_welds': pending_welds,
            'total_diameter': round(total_diameter, 2),
            'welded_diameter': round(welded_diameter, 2),
            'pending_diameter': round(total_diameter - welded_diameter, 2),
            'completion_percentage': round(overall_completion, 1),
            'diameter_breakdown': diameter_breakdown,
            'welds': welds
        }
    
    print(f"📊 Estadísticas generadas para {len(welding_status_data)} isométricos")
    
    # Guardar datos procesados
    with open('welding_status_data.json', 'w', encoding='utf-8') as f:
        json.dump(welding_status_data, f, indent=2, ensure_ascii=False)
    
    print("💾 Datos guardados en: welding_status_data.json")
    
    # Generar estadísticas generales
    generate_general_stats(welding_status_data)
    
    return welding_status_data

def generate_general_stats(welding_data):
    """Genera estadísticas generales del proyecto"""
    print('\n📈 ESTADÍSTICAS GENERALES DEL PROYECTO')
    print('=' * 60)
    
    total_isometrics = len(welding_data)
    total_welds = sum(data['total_welds'] for data in welding_data.values())
    completed_welds = sum(data['completed_welds'] for data in welding_data.values())
    pending_welds = sum(data['pending_welds'] for data in welding_data.values())
    
    total_diameter = sum(data['total_diameter'] for data in welding_data.values())
    welded_diameter = sum(data['welded_diameter'] for data in welding_data.values())
    pending_diameter = sum(data['pending_diameter'] for data in welding_data.values())
    
    overall_completion = (welded_diameter / total_diameter * 100) if total_diameter > 0 else 0
    
    # Agrupar por rangos de completitud
    completion_ranges = {
        '0%': 0,
        '1-25%': 0,
        '26-50%': 0,
        '51-75%': 0,
        '76-99%': 0,
        '100%': 0
    }
    
    for data in welding_data.values():
        completion = data['completion_percentage']
        if completion == 0:
            completion_ranges['0%'] += 1
        elif completion <= 25:
            completion_ranges['1-25%'] += 1
        elif completion <= 50:
            completion_ranges['26-50%'] += 1
        elif completion <= 75:
            completion_ranges['51-75%'] += 1
        elif completion < 100:
            completion_ranges['76-99%'] += 1
        else:
            completion_ranges['100%'] += 1
    
    stats = {
        'total_isometrics': total_isometrics,
        'total_welds': total_welds,
        'completed_welds': completed_welds,
        'pending_welds': pending_welds,
        'total_diameter': round(total_diameter, 2),
        'welded_diameter': round(welded_diameter, 2),
        'pending_diameter': round(pending_diameter, 2),
        'overall_completion': round(overall_completion, 1),
        'completion_ranges': completion_ranges
    }
    
    print(f"🔹 Isométricos totales: {total_isometrics}")
    print(f"🔹 Costuras totales: {total_welds}")
    print(f"🔹 Costuras completadas: {completed_welds} ({(completed_welds/total_welds)*100:.1f}%)")
    print(f"🔹 Costuras pendientes: {pending_welds} ({(pending_welds/total_welds)*100:.1f}%)")
    print(f"🔹 Diámetro total: {total_diameter:.2f} pulgadas")
    print(f"🔹 Diámetro soldado: {welded_diameter:.2f} pulgadas ({overall_completion:.1f}%)")
    print(f"🔹 Diámetro pendiente: {pending_diameter:.2f} pulgadas")
    
    print(f"\n📊 Distribución por completitud:")
    for range_name, count in completion_ranges.items():
        percentage = (count / total_isometrics * 100) if total_isometrics > 0 else 0
        print(f"  {range_name}: {count} isométricos ({percentage:.1f}%)")
    
    # Guardar estadísticas generales
    with open('welding_statistics.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print("💾 Estadísticas guardadas en: welding_statistics.json")

if __name__ == "__main__":
    process_welding_status() 