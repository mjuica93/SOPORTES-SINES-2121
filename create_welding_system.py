#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de integración de costuras (welding) con isométricos
Procesa el archivo Welding Database y crea sistema de trazabilidad
"""

import pandas as pd
import json
import os
import re
from datetime import datetime
from pathlib import Path

def load_welding_data():
    """Carga y procesa datos de soldadura"""
    print('🔨 PROCESANDO DATOS DE SOLDADURA')
    print('=' * 60)
    
    welding_file = "PREFABRICATING WELDING DATABASE/Welding Database updated 20250605 for 2121 Workshop.xlsx"
    
    if not os.path.exists(welding_file):
        print(f"❌ Archivo no encontrado: {welding_file}")
        return None
    
    all_welds = []
    
    try:
        # Procesar hoja MENE (prefabricación)
        print("📋 Procesando hoja MENE (prefabricación)...")
        df_mene = pd.read_excel(welding_file, sheet_name='MENE')
        
        for _, row in df_mene.iterrows():
            if pd.notna(row.get('Isometric')) and pd.notna(row.get('WELD')):
                weld_num = str(row['WELD']).strip()
                # Determinar tipo basado en el prefijo de la columna WELD
                if weld_num.startswith('F'):
                    weld_type = 'campo'  # Field Weld
                elif weld_num.startswith('S'):
                    weld_type = 'prefabricada'  # Shop Weld
                else:
                    weld_type = 'desconocido'  # Por si acaso
                
                weld_record = {
                    'isometric': str(row['Isometric']).strip(),
                    'weld_number': weld_num,
                    'type': weld_type,
                    'status': 'completada',
                    'spool': row.get('SPOOL', ''),
                    'joint_type': row.get('JOINT', ''),
                    'size': row.get('SIZE', ''),
                    'pipe_fitter': row.get('Pipe Fitter', ''),
                    'weld_date': row.get('Weld date', ''),
                    'wps': row.get('WPS', ''),
                    'stamp': row.get('STAMP', ''),
                    'filler_material_1': row.get('Filler Material 1', ''),
                    'filler_material_2': row.get('Filler Material 2', ''),
                    'heat_1': row.get('HEAT #1', ''),
                    'heat_2': row.get('HEAT #2', ''),
                    'material_cert_1': row.get('Material Certificate nº', ''),
                    'material_cert_2': row.get('Material Certificate nº2', ''),
                    'welded_inches': row.get('Welded INCHES', 0),
                    'weld_class': row.get('Weld Class', ''),
                    'service': row.get('SERVICE', ''),
                    'class': row.get('CLASS', ''),
                    'ped_cat': row.get('PED Cat', ''),
                    'location': row.get('Location', ''),
                    'sent_to_paint': row.get('Sent to Paint', ''),
                    'paint_report': row.get('Paint Report', ''),
                    'sent_to_site': row.get('Sent To Site', ''),
                    'quality_release': row.get('Quality release', ''),
                    # Inspecciones
                    'vt': row.get('VT', ''),
                    'pt1': row.get('PT1', ''),
                    'mt1': row.get('MT1', ''),
                    'rt1': row.get('RT1', ''),
                    'rt_result': row.get('RT Result', ''),
                    'pt': row.get('PT', ''),
                    'mt': row.get('MT', ''),
                    'rt': row.get('RT', ''),
                    'ut': row.get('UT', ''),
                    'pmi': row.get('PMI', ''),
                    'ht': row.get('HT', ''),
                    'pn': row.get('PN', ''),
                    'ft': row.get('FT', ''),
                    'source': 'MENE'
                }
                all_welds.append(weld_record)
        
        print(f"   ✅ {len([w for w in all_welds if w['source'] == 'MENE'])} costuras prefabricadas")
        
        # Procesar hoja SIMI (soldadura en sitio)
        print("📋 Procesando hoja SIMI (soldadura en sitio)...")
        df_simi = pd.read_excel(welding_file, sheet_name='SIMI')
        
        for _, row in df_simi.iterrows():
            if pd.notna(row.get('Isometric')) and pd.notna(row.get('Weld Nº')):
                # Determinar estado basado en si tiene fecha de soldadura
                weld_date = row.get('Weld  / Installation\nDate', '')
                status = 'completada' if pd.notna(weld_date) else 'pendiente'
                
                weld_num = str(row['Weld Nº']).strip()
                # Determinar tipo basado en el prefijo de la columna WELD
                if weld_num.startswith('F'):
                    weld_type = 'campo'  # Field Weld
                elif weld_num.startswith('S'):
                    weld_type = 'prefabricada'  # Shop Weld
                else:
                    weld_type = 'desconocido'  # Por si acaso
                
                weld_record = {
                    'isometric': str(row['Isometric']).strip(),
                    'weld_number': weld_num,
                    'type': weld_type,
                    'status': status,
                    'spool': row.get('Spool Nº', ''),
                    'joint_type': row.get('Joint \nType', ''),
                    'size': row.get('Dia Inch (Inches)', ''),
                    'pipe_fitter': row.get('Pipe Fitter Stamp', ''),
                    'welder': row.get('Welder \nStamp', ''),
                    'weld_date': weld_date,
                    'fit_up_date': row.get('Fit up Date', ''),
                    'wps': row.get('WPS', ''),
                    'service': row.get('Service \n(Fluid)', ''),
                    'pip_class': row.get('Pip. Class', ''),
                    'weld_class': row.get('Weld Class', ''),
                    'ped_cat': row.get('PED  Cat', ''),
                    'reason_modification': row.get('Reason for\nmodification', ''),
                    'dia_welded': row.get('Dia Inch\nWelded', ''),
                    'sch': row.get('Sch', ''),
                    'thickness': row.get('Thck\n (mm)', ''),
                    'base_material_1': row.get('Base Material 1', ''),
                    'base_material_2': row.get('Base Material 2', ''),
                    'heat_1': row.get('Heat Nº 1', ''),
                    'heat_2': row.get('Heat Nº 2', ''),
                    'material_cert_1': row.get('Mat \nCertificate 1', ''),
                    'material_cert_2': row.get('Mat.\n Certificate 2', ''),
                    'filler_material_1': row.get('F. Mat. 1\nBatch No', ''),
                    'filler_material_2': row.get('F. Mat. 2\nBatch No', ''),
                    'filler_cert_1': row.get('F.M.1 Certificate', ''),
                    'filler_cert_2': row.get('F.M.2 Certificate', ''),
                    'quality_release': row.get('Quality Release Date', ''),
                    'sent_to_paint': row.get('Sent to Paint Date', ''),
                    'sent_to_site': row.get('Sent to Site Date', ''),
                    'erection_date': row.get('Erection Date', ''),
                    'observation': row.get('Observation', ''),
                    # Inspecciones
                    'vt': row.get('VT', ''),
                    'vt_result': row.get('VT Result', ''),
                    'pt': row.get('PT', ''),
                    'pt_result': row.get('PT Result', ''),
                    'mt': row.get('MT', ''),
                    'mt_result': row.get('MT Result', ''),
                    'rt': row.get('RT', ''),
                    'rt_result': row.get('RT Result', ''),
                    'paut': row.get(' PAUT', ''),
                    'paut_result': row.get('PAUT Result', ''),
                    'ht': row.get('HT', ''),
                    'ht_result': row.get('HT Result', ''),
                    'ft': row.get('FT', ''),
                    'ft_result': row.get('FT Result', ''),
                    'pmi': row.get('PMI', ''),
                    'pmi_result': row.get('PMI Result', ''),
                    'boroscopic': row.get('Boroscopic', ''),
                    'boroscopic_result': row.get('Boroscopic Result', ''),
                    'roughness': row.get(' Roughness', ''),
                    'ra_result': row.get('RA Result', ''),
                    'passivation': row.get('Passivation', ''),
                    'pa_result': row.get('PA Result', ''),
                    'source': 'SIMI'
                }
                all_welds.append(weld_record)
        
        print(f"   ✅ {len([w for w in all_welds if w['source'] == 'SIMI'])} costuras de campo")
        
        print(f"\n📊 TOTAL: {len(all_welds)} costuras procesadas")
        
        return all_welds
        
    except Exception as e:
        print(f"❌ Error procesando datos: {e}")
        return None

def integrate_with_isometrics():
    """Integra datos de soldadura con isométricos existentes"""
    print('\n🔗 INTEGRANDO COSTURAS CON ISOMÉTRICOS')
    print('=' * 60)
    
    # Cargar datos existentes de isométricos
    if not os.path.exists('isometric_data_fixed.json'):
        print("❌ Archivo de isométricos no encontrado")
        return None
    
    with open('isometric_data_fixed.json', 'r', encoding='utf-8') as f:
        isometric_data = json.load(f)
    
    # Cargar datos de soldadura
    welds_data = load_welding_data()
    if not welds_data:
        return None
    
    # Organizar costuras por isométrico
    welds_by_iso = {}
    for weld in welds_data:
        iso_name = weld['isometric']
        # Remover prefijo "2121-" si existe para coincidir con nuestro sistema
        if iso_name.startswith('2121-'):
            iso_name_clean = iso_name[5:]  # Remover "2121-"
        else:
            iso_name_clean = iso_name
        
        if iso_name_clean not in welds_by_iso:
            welds_by_iso[iso_name_clean] = []
        welds_by_iso[iso_name_clean].append(weld)
    
    # Integrar con isométricos
    integrated_count = 0
    
    for iso_name, iso_data in isometric_data['isometrics'].items():
        if iso_name in welds_by_iso:
            iso_data['welds'] = welds_by_iso[iso_name]
            integrated_count += 1
            
            # Calcular estadísticas de costuras
            total_welds = len(iso_data['welds'])
            completed_welds = len([w for w in iso_data['welds'] if w['status'] == 'completada'])
            pending_welds = total_welds - completed_welds
            prefab_welds = len([w for w in iso_data['welds'] if w['type'] == 'prefabricada'])
            field_welds = len([w for w in iso_data['welds'] if w['type'] == 'campo'])
            
            iso_data['weld_statistics'] = {
                'total_welds': total_welds,
                'completed_welds': completed_welds,
                'pending_welds': pending_welds,
                'prefab_welds': prefab_welds,
                'field_welds': field_welds,
                'completion_percentage': round((completed_welds / total_welds) * 100, 1) if total_welds > 0 else 0
            }
        else:
            iso_data['welds'] = []
            iso_data['weld_statistics'] = {
                'total_welds': 0,
                'completed_welds': 0,
                'pending_welds': 0,
                'prefab_welds': 0,
                'field_welds': 0,
                'completion_percentage': 0
            }
    
    print(f"✅ {integrated_count} isométricos integrados con costuras")
    print(f"📊 {len(welds_data)} costuras totales distribuidas")
    
    # Guardar datos integrados
    output_file = 'isometric_data_with_welds.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(isometric_data, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"💾 Datos guardados en: {output_file}")
    
    # Generar estadísticas generales
    generate_welding_statistics(isometric_data)
    
    return isometric_data

def generate_welding_statistics(data):
    """Genera estadísticas generales de soldadura"""
    print('\n📊 ESTADÍSTICAS GENERALES DE SOLDADURA')
    print('=' * 60)
    
    total_isos = len(data['isometrics'])
    isos_with_welds = len([iso for iso in data['isometrics'].values() if iso['weld_statistics']['total_welds'] > 0])
    
    total_welds = sum(iso['weld_statistics']['total_welds'] for iso in data['isometrics'].values())
    completed_welds = sum(iso['weld_statistics']['completed_welds'] for iso in data['isometrics'].values())
    pending_welds = sum(iso['weld_statistics']['pending_welds'] for iso in data['isometrics'].values())
    prefab_welds = sum(iso['weld_statistics']['prefab_welds'] for iso in data['isometrics'].values())
    field_welds = sum(iso['weld_statistics']['field_welds'] for iso in data['isometrics'].values())
    
    print(f"🔹 Isométricos totales: {total_isos}")
    print(f"🔹 Isométricos con costuras: {isos_with_welds} ({(isos_with_welds/total_isos)*100:.1f}%)")
    print(f"🔹 Costuras totales: {total_welds}")
    if total_welds > 0:
        print(f"🔹 Costuras completadas: {completed_welds} ({(completed_welds/total_welds)*100:.1f}%)")
        print(f"🔹 Costuras pendientes: {pending_welds} ({(pending_welds/total_welds)*100:.1f}%)")
        print(f"🔹 Costuras prefabricadas: {prefab_welds} ({(prefab_welds/total_welds)*100:.1f}%)")
        print(f"🔹 Costuras de campo: {field_welds} ({(field_welds/total_welds)*100:.1f}%)")
    else:
        print(f"🔹 Costuras completadas: {completed_welds} (0.0%)")
        print(f"🔹 Costuras pendientes: {pending_welds} (0.0%)")
        print(f"🔹 Costuras prefabricadas: {prefab_welds} (0.0%)")
        print(f"🔹 Costuras de campo: {field_welds} (0.0%)")
    
    # Guardar estadísticas
    stats = {
        'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_isometrics': total_isos,
        'isometrics_with_welds': isos_with_welds,
        'total_welds': total_welds,
        'completed_welds': completed_welds,
        'pending_welds': pending_welds,
        'prefab_welds': prefab_welds,
        'field_welds': field_welds,
        'completion_percentage': round((completed_welds/total_welds)*100, 1) if total_welds > 0 else 0
    }
    
    with open('welding_statistics.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Estadísticas guardadas en: welding_statistics.json")

if __name__ == "__main__":
    result = integrate_with_isometrics()
    if result:
        print(f"\n🎉 INTEGRACIÓN COMPLETADA EXITOSAMENTE")
        print(f"📁 Archivo generado: isometric_data_with_welds.json")
        print(f"📊 Estadísticas generadas: welding_statistics.json")
    else:
        print(f"\n❌ Error en la integración") 