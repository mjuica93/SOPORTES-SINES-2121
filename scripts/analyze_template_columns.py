#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análisis específico de columnas T22 y T23 del Excel
Extrae los títulos de las variables de plantilla para el sistema integrado
"""

import pandas as pd
import json
import os

def analyze_template_columns():
    """Analiza las columnas T22 y T23 específicamente"""
    print("=== ANÁLISIS DE COLUMNAS T22 Y T23 (VARIABLES DE PLANTILLA) ===\n")
    
    excel_files = [
        '4274-XH-LP-21210001-IS03_Native.xlsx',
        '4274-XH-LP-21210002-IS02_Native.xlsm'
    ]
    
    template_variables = {}
    
    for excel_file in excel_files:
        if not os.path.exists(excel_file):
            print(f"❌ Archivo no encontrado: {excel_file}")
            continue
            
        print(f"📊 Analizando archivo: {excel_file}")
        
        try:
            # Leer específicamente las filas 22 y 23 (índices 21 y 22)
            df = pd.read_excel(excel_file, sheet_name='table', header=None)
            
            print(f"   Dimensiones del archivo: {df.shape}")
            
            # Extraer filas 22 y 23
            if df.shape[0] >= 24:  # Asegurar que tenemos suficientes filas
                row_22 = df.iloc[21]  # Fila 22 (índice 21)
                row_23 = df.iloc[22]  # Fila 23 (índice 22)
                
                print(f"   📋 FILA 22 (Títulos principales):")
                for i, value in enumerate(row_22):
                    if pd.notna(value) and str(value).strip():
                        print(f"      Columna {i}: '{value}'")
                
                print(f"   📋 FILA 23 (Códigos de referencia):")
                for i, value in enumerate(row_23):
                    if pd.notna(value) and str(value).strip():
                        print(f"      Columna {i}: '{value}'")
                
                # Crear mapeo de variables de plantilla
                for i in range(len(row_22)):
                    title_22 = str(row_22.iloc[i]).strip() if pd.notna(row_22.iloc[i]) else ''
                    title_23 = str(row_23.iloc[i]).strip() if pd.notna(row_23.iloc[i]) else ''
                    
                    # Solo procesar si hay contenido relevante
                    if title_22 and title_22 not in ['nan', 'NaN', '']:
                        # Identificar variables de plantilla comunes
                        if title_22 in ['A', 'B', 'C', 'D', 'E', 'R', 'X', 'Y', 'EL', 'N.', 'SH.', 'TEMP']:
                            template_variables[title_22] = {
                                'column': i,
                                'title': title_22,
                                'reference_code': title_23 if title_23 and title_23 not in ['nan', 'NaN', ''] else '',
                                'description': get_variable_description(title_22),
                                'unit': get_variable_unit(title_22),
                                'source_file': excel_file
                            }
                
                print(f"   ✅ Variables de plantilla encontradas: {len([v for v in template_variables.values() if v['source_file'] == excel_file])}")
                
            else:
                print(f"   ❌ Archivo no tiene suficientes filas")
                
        except Exception as e:
            print(f"   ❌ Error procesando {excel_file}: {e}")
    
    # Mostrar resumen de variables encontradas
    print(f"\n🎯 RESUMEN DE VARIABLES DE PLANTILLA ENCONTRADAS:")
    print("=" * 60)
    
    for var_name, var_info in template_variables.items():
        print(f"Variable: {var_name}")
        print(f"  Columna: {var_info['column']}")
        print(f"  Código de referencia: {var_info['reference_code']}")
        print(f"  Descripción: {var_info['description']}")
        print(f"  Unidad: {var_info['unit']}")
        print(f"  Archivo: {var_info['source_file']}")
        print()
    
    # Guardar mapeo de variables
    with open('template_variables_mapping.json', 'w', encoding='utf-8') as f:
        json.dump(template_variables, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Mapeo guardado en: template_variables_mapping.json")
    
    return template_variables

def get_variable_description(var_name):
    """Obtiene la descripción de una variable de plantilla"""
    descriptions = {
        'A': 'Dimensión principal A - Generalmente altura o longitud principal del soporte',
        'B': 'Dimensión principal B - Generalmente ancho o segunda dimensión principal',
        'C': 'Dimensión C - Tercera dimensión principal o profundidad',
        'D': 'Dimensión D - Cuarta dimensión o diámetro específico',
        'E': 'Dimensión E - Quinta dimensión o espesor específico',
        'R': 'Radio o distancia radial - Usado en soportes circulares o curvos',
        'X': 'Coordenada X - Posición horizontal en el sistema de coordenadas',
        'Y': 'Coordenada Y - Posición vertical en el sistema de coordenadas',
        'EL': 'Elevación - Altura o cota del soporte respecto al nivel de referencia',
        'N.': 'Número de referencia - Identificador numérico específico',
        'SH.': 'Número de hoja - Referencia al plano o drawing donde aparece',
        'TEMP': 'Temperatura de operación - Condiciones térmicas de trabajo'
    }
    return descriptions.get(var_name, f'Variable {var_name} de la plantilla')

def get_variable_unit(var_name):
    """Obtiene la unidad de una variable de plantilla"""
    units = {
        'A': 'mm',
        'B': 'mm',
        'C': 'mm',
        'D': 'mm',
        'E': 'mm',
        'R': 'mm',
        'X': 'mm',
        'Y': 'mm',
        'EL': 'mm',
        'N.': '',
        'SH.': '',
        'TEMP': '°C'
    }
    return units.get(var_name, '')

def extract_dimension_data():
    """Extrae los datos de dimensiones de los archivos Excel"""
    print(f"\n📏 EXTRAYENDO DATOS DE DIMENSIONES:")
    print("=" * 60)
    
    excel_files = [
        '4274-XH-LP-21210001-IS03_Native.xlsx',
        '4274-XH-LP-21210002-IS02_Native.xlsm'
    ]
    
    # Cargar mapeo de variables
    if not os.path.exists('template_variables_mapping.json'):
        print("❌ Mapeo de variables no encontrado. Ejecuta analyze_template_columns() primero.")
        return
    
    with open('template_variables_mapping.json', 'r', encoding='utf-8') as f:
        template_variables = json.load(f)
    
    all_dimension_data = []
    
    for excel_file in excel_files:
        if not os.path.exists(excel_file):
            continue
            
        print(f"📊 Extrayendo dimensiones de: {excel_file}")
        
        try:
            # Leer datos con encabezados en fila 9
            df = pd.read_excel(excel_file, sheet_name='table', header=8)
            
            print(f"   Registros encontrados: {len(df)}")
            
            # Procesar cada fila de datos
            for idx, row in df.iterrows():
                # Saltar filas de encabezado
                if idx < 3:
                    continue
                
                support_number = str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else ''
                support_type = str(row.iloc[5]).strip() if pd.notna(row.iloc[5]) else ''
                
                # Verificar que es un registro válido
                if (support_number and support_number not in ['nan', 'SUPPORT NUMBER', ''] and
                    support_type and support_type not in ['nan', 'SUPPORT OR ELEMENT TYPE', '']):
                    
                    # Extraer dimensiones usando el mapeo de variables
                    dimensions = {}
                    for var_name, var_info in template_variables.items():
                        col_index = var_info['column']
                        if col_index < len(row):
                            value = row.iloc[col_index]
                            if pd.notna(value) and str(value).strip() not in ['nan', '']:
                                dimensions[var_name] = {
                                    'value': str(value).strip(),
                                    'title': var_info['description'],
                                    'unit': var_info['unit'],
                                    'reference_code': var_info['reference_code']
                                }
                    
                    if dimensions:  # Solo agregar si tiene dimensiones
                        dimension_record = {
                            'support_number': support_number,
                            'support_type': support_type,
                            'dimensions': dimensions,
                            'source_file': excel_file
                        }
                        all_dimension_data.append(dimension_record)
            
            print(f"   ✅ Registros con dimensiones: {len([d for d in all_dimension_data if d['source_file'] == excel_file])}")
            
        except Exception as e:
            print(f"   ❌ Error extrayendo dimensiones de {excel_file}: {e}")
    
    # Guardar datos de dimensiones
    with open('support_dimensions_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_dimension_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Datos de dimensiones guardados: support_dimensions_data.json")
    print(f"Total registros con dimensiones: {len(all_dimension_data)}")
    
    return all_dimension_data

if __name__ == "__main__":
    # Ejecutar análisis
    template_vars = analyze_template_columns()
    
    if template_vars:
        # Extraer datos de dimensiones
        dimension_data = extract_dimension_data()
        
        print(f"\n🎯 ANÁLISIS COMPLETADO:")
        print(f"Variables de plantilla identificadas: {len(template_vars)}")
        print(f"Registros con dimensiones: {len(dimension_data) if dimension_data else 0}") 