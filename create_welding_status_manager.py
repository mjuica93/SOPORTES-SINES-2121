#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de gestión de estado de costuras con acceso a PDFs de isométricos
Permite modificar el estado de las costuras y acceder a PDFs regulares y prefabricados
"""

import json
import os
from datetime import datetime

def load_data():
    """Carga todos los datos necesarios"""
    print('🔧 CARGANDO DATOS DEL SISTEMA DE SOLDADURA')
    print('=' * 60)
    
    data = {}
    
    # Cargar datos de soldadura con relaciones
    try:
        with open('welding_enhanced_data.json', 'r', encoding='utf-8') as f:
            welding_data = json.load(f)
            # El archivo tiene estructura con 'relations'
            data['welding'] = welding_data.get('relations', [])
        print(f"✅ Datos de soldadura: {len(data['welding'])} registros")
    except FileNotFoundError:
        # Usar datos del template como fallback
        try:
            with open('welding_template_data.json', 'r', encoding='utf-8') as f:
                data['welding'] = json.load(f)
            print(f"✅ Datos de soldadura (template): {len(data['welding'])} registros")
        except FileNotFoundError:
            print("❌ No se encontraron archivos de datos de soldadura")
            return None
    
    # Cargar mapeo de isométricos prefabricados
    try:
        with open('prefabricated_isometric_mapping_github.json', 'r', encoding='utf-8') as f:
            prefab_data = json.load(f)
            data['prefab_mapping'] = prefab_data.get('correspondences', {})
        print(f"✅ Mapeo prefabricados: {len(data['prefab_mapping'])} correspondencias")
    except FileNotFoundError:
        print("❌ No se encontró prefabricated_isometric_mapping_github.json")
        data['prefab_mapping'] = {}
    
    # Cargar datos de isométricos con prefabricados
    try:
        with open('isometric_data_with_prefabricated.json', 'r', encoding='utf-8') as f:
            data['isometrics'] = json.load(f)
        print(f"✅ Datos de isométricos: {len(data['isometrics'])} líneas")
    except FileNotFoundError:
        print("❌ No se encontró isometric_data_with_prefabricated.json")
        data['isometrics'] = {}
    
    return data

def enhance_welding_data_with_pdfs(data):
    """Enriquece los datos de soldadura con información de PDFs"""
    print('\n📄 ENRIQUECIENDO DATOS CON INFORMACIÓN DE PDFs')
    print('=' * 60)
    
    enhanced_welding = []
    pdf_matches = 0
    
    for weld_record in data['welding']:
        # Verificar que el registro sea un diccionario
        if not isinstance(weld_record, dict):
            print(f"⚠️ Registro inválido encontrado: {type(weld_record)}")
            continue
        
        # Extraer datos de soldadura del registro anidado
        weld_data = weld_record.get('weld_data', {})
        
        # Crear registro enriquecido combinando datos del registro principal y weld_data
        enhanced_record = {
            'welding_isometric': weld_record.get('welding_isometric', ''),
            'system_line': weld_record.get('system_line', ''),
            'line_code': weld_record.get('line_code', ''),
            'type': weld_record.get('type', ''),
            'fluid': weld_record.get('fluid', ''),
            'iso_sheet': weld_record.get('iso_sheet', ''),
            'isometric_files': weld_record.get('isometric_files', []),
            # Datos de soldadura
            'isometric': weld_data.get('isometric', weld_record.get('welding_isometric', '')),
            'weld_number': weld_data.get('weld_number', ''),
            'diameter': weld_data.get('diameter', 0),
            'welded': weld_data.get('welded', 0),
            'status': weld_data.get('status', 'pendiente'),
            'completion_percentage': weld_data.get('completion_percentage', 0)
        }
        
        # Inicializar información de PDFs
        enhanced_record['pdf_info'] = {
            'has_normal': False,
            'has_prefab': False,
            'normal_path': None,
            'prefab_path': None,
            'normal_filename': None,
            'prefab_filename': None
        }
        
        # Usar archivos de isométricos si están disponibles
        if enhanced_record['isometric_files']:
            enhanced_record['pdf_info']['has_normal'] = True
            enhanced_record['pdf_info']['normal_filename'] = enhanced_record['isometric_files'][0]
            enhanced_record['pdf_info']['normal_path'] = f"ISOMETRICOS/{enhanced_record['isometric_files'][0]}"
        
        # Buscar información de PDFs basada en el código de línea
        line_code = enhanced_record.get('line_code', '')
        
        if line_code:
            # Buscar archivos PDF prefabricados
            for normal_file, prefab_info in data['prefab_mapping'].items():
                if line_code in prefab_info.get('line_code', ''):
                    enhanced_record['pdf_info']['has_prefab'] = True
                    enhanced_record['pdf_info']['prefab_path'] = prefab_info['prefab_path']
                    enhanced_record['pdf_info']['prefab_filename'] = prefab_info['prefab_file']
                    pdf_matches += 1
                    break
        
        # Agregar ID único para el registro
        weld_id_parts = [
            str(enhanced_record.get('isometric', 'unknown')),
            str(enhanced_record.get('weld_number', 'unknown')),
            str(enhanced_record.get('diameter', 0))
        ]
        enhanced_record['weld_id'] = "_".join(weld_id_parts)
        
        # Agregar timestamp de última modificación
        enhanced_record['last_modified'] = datetime.now().isoformat()
        
        # Asegurar que el estado esté definido
        if 'status' not in enhanced_record or not enhanced_record['status']:
            enhanced_record['status'] = 'pendiente'
        
        enhanced_welding.append(enhanced_record)
    
    print(f"✅ {len(enhanced_welding)} registros de soldadura enriquecidos")
    print(f"📄 {pdf_matches} registros con PDFs prefabricados encontrados")
    
    return enhanced_welding

def create_weld_status_manager():
    """Crea el sistema de gestión de estado de costuras"""
    print('\n⚙️ CREANDO SISTEMA DE GESTIÓN DE ESTADO')
    print('=' * 60)
    
    status_manager = {
        'metadata': {
            'version': '1.0',
            'created': datetime.now().isoformat(),
            'description': 'Sistema de gestión de estado de costuras con acceso a PDFs',
            'features': [
                'Modificación de estado de costuras',
                'Acceso a PDFs regulares y prefabricados',
                'Historial de cambios',
                'Filtros avanzados',
                'Exportación de datos'
            ]
        },
        'status_options': {
            'pendiente': {
                'label': 'Pendiente',
                'color': '#ffc107',
                'icon': '⏳',
                'description': 'Costura no iniciada'
            },
            'en_progreso': {
                'label': 'En Progreso',
                'color': '#17a2b8',
                'icon': '🔄',
                'description': 'Costura en proceso de soldadura'
            },
            'completada': {
                'label': 'Completada',
                'color': '#28a745',
                'icon': '✅',
                'description': 'Costura terminada y aprobada'
            },
            'inspeccion': {
                'label': 'En Inspección',
                'color': '#fd7e14',
                'icon': '🔍',
                'description': 'Costura en proceso de inspección'
            },
            'rechazada': {
                'label': 'Rechazada',
                'color': '#dc3545',
                'icon': '❌',
                'description': 'Costura rechazada, requiere retrabajo'
            }
        },
        'change_history': [],
        'user_permissions': {
            'admin': ['view', 'edit', 'delete', 'export'],
            'supervisor': ['view', 'edit', 'export'],
            'operador': ['view', 'edit'],
            'sines': ['view']
        }
    }
    
    return status_manager

def generate_welding_status_data():
    """Genera el archivo completo de datos de soldadura con gestión de estado"""
    print('\n🔨 GENERANDO SISTEMA COMPLETO DE SOLDADURA')
    print('=' * 60)
    
    # Cargar datos
    data = load_data()
    if not data:
        return False
    
    # Enriquecer datos con PDFs
    enhanced_welding = enhance_welding_data_with_pdfs(data)
    
    # Crear gestor de estado
    status_manager = create_weld_status_manager()
    
    # Compilar sistema completo
    complete_system = {
        'metadata': {
            'title': 'Sistema de Gestión de Soldadura SINES',
            'version': '2.0',
            'generated': datetime.now().isoformat(),
            'total_welds': len(enhanced_welding),
            'unique_isometrics': len(set(w['isometric'] for w in enhanced_welding if w.get('isometric'))),
            'with_pdfs': len([w for w in enhanced_welding if w['pdf_info']['has_normal'] or w['pdf_info']['has_prefab']])
        },
        'welding_data': enhanced_welding,
        'status_manager': status_manager,
        'statistics': calculate_statistics(enhanced_welding)
    }
    
    # Guardar archivo principal
    output_file = 'welding_status_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(complete_system, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"💾 Sistema completo guardado en: {output_file}")
    
    # Crear archivo compacto para carga rápida
    compact_data = {
        'metadata': complete_system['metadata'],
        'welding_data': [
            {
                'weld_id': w['weld_id'],
                'isometric': w['isometric'],
                'weld_number': w['weld_number'],
                'diameter': w['diameter'],
                'status': w['status'],
                'completion_percentage': w.get('completion_percentage', 0),
                'pdf_info': w['pdf_info'],
                'system_line': w.get('system_line'),
                'fluid': w.get('fluid'),
                'type': w.get('type')
            } for w in enhanced_welding
        ],
        'status_options': status_manager['status_options']
    }
    
    compact_file = 'welding_compact_data.json'
    with open(compact_file, 'w', encoding='utf-8') as f:
        json.dump(compact_data, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"💾 Datos compactos guardados en: {compact_file}")
    
    return True

def calculate_statistics(welding_data):
    """Calcula estadísticas del sistema de soldadura"""
    total_welds = len(welding_data)
    
    if total_welds == 0:
        return {}
    
    # Estadísticas por estado
    status_stats = {}
    for weld in welding_data:
        status = weld.get('status', 'unknown')
        status_stats[status] = status_stats.get(status, 0) + 1
    
    # Estadísticas por diámetro
    diameter_stats = {}
    for weld in welding_data:
        diameter = weld.get('diameter', 0)
        diameter_stats[diameter] = diameter_stats.get(diameter, 0) + 1
    
    # Estadísticas de PDFs
    with_normal_pdf = len([w for w in welding_data if w['pdf_info']['has_normal']])
    with_prefab_pdf = len([w for w in welding_data if w['pdf_info']['has_prefab']])
    
    return {
        'total_welds': total_welds,
        'by_status': status_stats,
        'by_diameter': diameter_stats,
        'pdf_coverage': {
            'normal_pdfs': with_normal_pdf,
            'prefab_pdfs': with_prefab_pdf,
            'normal_percentage': round((with_normal_pdf / total_welds) * 100, 1) if total_welds > 0 else 0,
            'prefab_percentage': round((with_prefab_pdf / total_welds) * 100, 1) if total_welds > 0 else 0
        },
        'unique_isometrics': len(set(w['isometric'] for w in welding_data if w.get('isometric'))),
        'completion_rate': round((status_stats.get('completada', 0) / total_welds) * 100, 1) if total_welds > 0 else 0
    }

if __name__ == "__main__":
    print('🚀 INICIANDO SISTEMA DE GESTIÓN DE SOLDADURA')
    print('=' * 60)
    
    success = generate_welding_status_data()
    
    if success:
        print('\n✅ SISTEMA DE SOLDADURA CREADO EXITOSAMENTE')
        print('=' * 60)
        print('📋 Archivos generados:')
        print('   • welding_status_data.json - Sistema completo')
        print('   • welding_compact_data.json - Datos optimizados')
        print('\n🔧 Funcionalidades incluidas:')
        print('   • Gestión de estado de costuras')
        print('   • Acceso a PDFs regulares y prefabricados')
        print('   • Historial de cambios')
        print('   • Estadísticas avanzadas')
        print('   • Sistema de permisos')
    else:
        print('\n❌ ERROR AL CREAR EL SISTEMA')
        print('Revisa que todos los archivos necesarios estén disponibles') 