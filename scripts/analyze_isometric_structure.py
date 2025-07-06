#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análisis de estructura de isométricos y soportes
Analiza los archivos Excel para entender cómo vincular los datos
"""

import pandas as pd
import os
import json
import re
from pathlib import Path

def analyze_isometric_excel():
    """Analiza el archivo LISTADO DE ISOMETRICOS.xlsx"""
    print("=== ANÁLISIS DEL ARCHIVO LISTADO DE ISOMETRICOS.xlsx ===")
    
    try:
        # Leer el archivo de isométricos
        iso_file = "ISOMETRICOS/LISTADO DE ISOMETRICOS.xlsx"
        
        # Intentar leer diferentes hojas
        xl_file = pd.ExcelFile(iso_file)
        print(f"Hojas disponibles: {xl_file.sheet_names}")
        
        for sheet_name in xl_file.sheet_names:
            print(f"\n--- Hoja: {sheet_name} ---")
            df = pd.read_excel(iso_file, sheet_name=sheet_name)
            print(f"Dimensiones: {df.shape}")
            print(f"Columnas: {list(df.columns)}")
            print(f"Primeras 3 filas:")
            print(df.head(3))
            
            # Buscar columnas relacionadas con LINE y SHEET
            line_cols = [col for col in df.columns if 'LINE' in str(col).upper()]
            sheet_cols = [col for col in df.columns if 'SHEET' in str(col).upper()]
            
            if line_cols:
                print(f"Columnas con 'LINE': {line_cols}")
            if sheet_cols:
                print(f"Columnas con 'SHEET': {sheet_cols}")
                
    except Exception as e:
        print(f"Error al leer el archivo de isométricos: {e}")

def analyze_support_files():
    """Analiza los archivos de soportes para encontrar columnas LINE y SHEET"""
    print("\n=== ANÁLISIS DE ARCHIVOS DE SOPORTES ===")
    
    support_files = [
        "4274-XH-LP-21210002-IS02_Native.xlsm",
        "4274-XH-LP-21210001-IS03_Native.xlsx"
    ]
    
    for file_name in support_files:
        print(f"\n--- Archivo: {file_name} ---")
        try:
            xl_file = pd.ExcelFile(file_name)
            print(f"Hojas disponibles: {xl_file.sheet_names}")
            
            for sheet_name in xl_file.sheet_names:
                print(f"\n  Hoja: {sheet_name}")
                df = pd.read_excel(file_name, sheet_name=sheet_name)
                print(f"  Dimensiones: {df.shape}")
                
                # Buscar columnas relacionadas con isométricos
                iso_cols = [col for col in df.columns if any(keyword in str(col).upper() for keyword in ['ISO', 'ISOMETRIC', 'PIPELINE', 'FLUID', 'SHEET'])]
                
                if iso_cols:
                    print(f"  Columnas relacionadas con isométricos: {iso_cols}")
                    
                    # Mostrar algunas muestras de datos
                    for col in iso_cols[:5]:  # Máximo 5 columnas
                        print(f"    {col}: {df[col].dropna().unique()[:3]}")
                
        except Exception as e:
            print(f"Error al leer {file_name}: {e}")

def analyze_pdf_structure():
    """Analiza la estructura de los archivos PDF de isométricos"""
    print("\n=== ANÁLISIS DE ESTRUCTURA DE PDFs ===")
    
    # Analizar isométricos normales
    iso_dir = Path("ISOMETRICOS")
    iso_pdfs = [f for f in os.listdir(iso_dir) if f.endswith('.pdf')]
    
    print(f"Isométricos normales encontrados: {len(iso_pdfs)}")
    if iso_pdfs:
        print("Ejemplos de nombres:")
        for pdf in iso_pdfs[:5]:
            print(f"  {pdf}")
    
    # Analizar isométricos prefabricados
    prefab_dir = Path("ISOMETRICOS PREFABRICADOS")
    prefab_pdfs = [f for f in os.listdir(prefab_dir) if f.endswith('.pdf')]
    
    print(f"\nIsométricos prefabricados encontrados: {len(prefab_pdfs)}")
    if prefab_pdfs:
        print("Ejemplos de nombres:")
        for pdf in prefab_pdfs[:5]:
            print(f"  {pdf}")

def extract_line_sheet_from_filenames():
    """Extrae información de LINE y SHEET de los nombres de archivos"""
    print("\n=== EXTRACCIÓN DE LINE Y SHEET DE NOMBRES DE ARCHIVOS ===")
    
    # Analizar patrones en isométricos normales
    iso_dir = Path("ISOMETRICOS")
    iso_pdfs = [f for f in os.listdir(iso_dir) if f.endswith('.pdf')]
    
    print("Patrones en isométricos normales:")
    for pdf in iso_pdfs[:10]:
        # Intentar extraer LINE y SHEET del nombre
        if 'sheet' in pdf.lower():
            parts = pdf.split('sheet')
            if len(parts) > 1:
                sheet_part = parts[1].replace('.pdf', '').strip()
                print(f"  {pdf} -> SHEET: {sheet_part}")
    
    # Analizar patrones en isométricos prefabricados
    prefab_dir = Path("ISOMETRICOS PREFABRICADOS")
    prefab_pdfs = [f for f in os.listdir(prefab_dir) if f.endswith('.pdf')]
    
    print("\nPatrones en isométricos prefabricados:")
    for pdf in prefab_pdfs[:10]:
        # Intentar extraer LINE del nombre
        if pdf.startswith('2121-'):
            line_part = pdf.replace('2121-', '').split('-')[0] if '-' in pdf else pdf
            print(f"  {pdf} -> LINE: {line_part}")

def analyze_isometric_structure():
    print("=== ANÁLISIS DE ESTRUCTURA DE ISOMÉTRICOS ===\n")
    
    # Leer el archivo Excel de isométricos
    try:
        df = pd.read_excel('ISOMETRICOS/LISTADO DE ISOMETRICOS.xlsx')
        print(f"✅ Archivo Excel cargado: {len(df)} registros")
        print(f"Columnas: {df.columns.tolist()}")
        print()
        
        # Mostrar algunas muestras
        print("=== PRIMERAS 5 FILAS ===")
        print(df[['FILE NAME', 'LINE', 'SHEET', 'FLUID']].head())
        print()
        
        # Analizar códigos de línea únicos
        unique_lines = df['LINE'].dropna().unique()
        print(f"=== CÓDIGOS DE LÍNEA ÚNICOS ===")
        print(f"Total: {len(unique_lines)}")
        print("Ejemplos:")
        for line in unique_lines[:15]:
            print(f"  - {line}")
        print()
        
        # Cargar base de datos de soportes
        with open('support_data.json', 'r', encoding='utf-8') as f:
            support_data = json.load(f)
        
        print(f"✅ Base de datos de soportes cargada: {len(support_data)} registros")
        
        # Extraer códigos de línea únicos de la base de datos de soportes
        support_lines = set()
        for support in support_data:
            if support.get('fluid_piping'):
                support_lines.add(support['fluid_piping'])
        
        print(f"Códigos de línea únicos en soportes: {len(support_lines)}")
        print("Ejemplos:")
        for line in list(support_lines)[:15]:
            print(f"  - {line}")
        print()
        
        # Buscar coincidencias
        isometric_lines = set(unique_lines)
        matching_lines = support_lines.intersection(isometric_lines)
        
        print(f"=== COINCIDENCIAS ENCONTRADAS ===")
        print(f"Líneas que coinciden: {len(matching_lines)}")
        print("Ejemplos de coincidencias:")
        for line in list(matching_lines)[:10]:
            print(f"  - {line}")
        print()
        
        # Verificar patrones en nombres de archivos
        print("=== ANÁLISIS DE ARCHIVOS PDF ===")
        pdf_files = df['FILE NAME'].tolist()
        
        # Extraer códigos de línea de los nombres de archivo
        line_codes_from_files = []
        for filename in pdf_files:
            if pd.notna(filename):
                # Patrón: "19-000-2-02-00001 sheet 2121VG40N11-4_IS01.pdf"
                match = re.search(r'sheet\s+(\d+[A-Z]+\d+[A-Z]+\d+[A-Z]*\d*-\d+)', filename)
                if match:
                    line_codes_from_files.append(match.group(1))
        
        print(f"Códigos de línea extraídos de nombres de archivo: {len(line_codes_from_files)}")
        print("Ejemplos:")
        for code in line_codes_from_files[:10]:
            print(f"  - {code}")
        print()
        
        # Crear estructura de datos para la relación
        isometric_mapping = {}
        
        for index, row in df.iterrows():
            filename = row['FILE NAME']
            line_code = row['LINE']
            sheet = row['SHEET']
            fluid = row['FLUID']
            
            # Convertir a string para evitar problemas con pandas
            filename_str = str(filename) if filename is not None and not pd.isna(filename) else ''
            line_code_str = str(line_code) if line_code is not None and not pd.isna(line_code) else ''
            
            if filename_str and line_code_str and filename_str != 'nan' and line_code_str != 'nan':
                if line_code_str not in isometric_mapping:
                    fluid_str = str(fluid) if fluid is not None and not pd.isna(fluid) else ''
                    if fluid_str == 'nan':
                        fluid_str = ''
                    
                    isometric_mapping[line_code_str] = {
                        'line_code': line_code_str,
                        'fluid': fluid_str,
                        'sheets': []
                    }
                
                # Convertir todos los valores a string de manera segura
                sheet_str = str(sheet) if sheet is not None and not pd.isna(sheet) else ''
                if sheet_str == 'nan':
                    sheet_str = ''
                
                revision_val = row.get('REVISION', '')
                revision_str = str(revision_val) if revision_val is not None and not pd.isna(revision_val) else ''
                if revision_str == 'nan':
                    revision_str = ''
                
                current_review_val = row.get('CURRENT REVIEW (YES/NO)', '')
                current_review_str = str(current_review_val) if current_review_val is not None and not pd.isna(current_review_val) else ''
                if current_review_str == 'nan':
                    current_review_str = ''
                
                lb_sb_val = row.get('LB+SB', '')
                lb_sb_str = str(lb_sb_val) if lb_sb_val is not None and not pd.isna(lb_sb_val) else ''
                if lb_sb_str == 'nan':
                    lb_sb_str = ''
                
                sheet_info = {
                    'filename': filename_str,
                    'sheet_number': sheet_str,
                    'revision': revision_str,
                    'current_review': current_review_str,
                    'type': lb_sb_str
                }
                
                isometric_mapping[line_code_str]['sheets'].append(sheet_info)
        
        # Guardar mapeo de isométricos
        with open('isometric_data.json', 'w', encoding='utf-8') as f:
            json.dump(isometric_mapping, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Mapeo de isométricos guardado: {len(isometric_mapping)} líneas")
        
        # Crear relación con base de datos de soportes
        support_isometric_relation = []
        
        for support in support_data:
            support_line = support.get('fluid_piping', '')
            if support_line in isometric_mapping:
                relation = {
                    'support_number': support['support_number'],
                    'support_type': support['support_type'],
                    'line_code': support_line,
                    'iso_sheet': support.get('iso_sheet', ''),
                    'isometric_files': [sheet['filename'] for sheet in isometric_mapping[support_line]['sheets']],
                    'fluid': isometric_mapping[support_line]['fluid']
                }
                support_isometric_relation.append(relation)
        
        # Guardar relación
        with open('support_isometric_relation.json', 'w', encoding='utf-8') as f:
            json.dump(support_isometric_relation, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Relación soportes-isométricos guardada: {len(support_isometric_relation)} relaciones")
        
        # Estadísticas finales
        print(f"\n=== ESTADÍSTICAS FINALES ===")
        print(f"Total de líneas en isométricos: {len(isometric_mapping)}")
        print(f"Total de soportes con isométricos: {len(support_isometric_relation)}")
        print(f"Total de archivos PDF de isométricos: {len(pdf_files)}")
        print(f"Porcentaje de soportes con isométricos: {len(support_isometric_relation)/len(support_data)*100:.1f}%")
        
        return isometric_mapping, support_isometric_relation
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None, None

def main():
    """Función principal"""
    print("ANÁLISIS DE ESTRUCTURA DE ISOMÉTRICOS Y SOPORTES")
    print("=" * 60)
    
    analyze_isometric_excel()
    analyze_support_files()
    analyze_pdf_structure()
    extract_line_sheet_from_filenames()
    
    print("\n" + "=" * 60)
    print("ANÁLISIS COMPLETADO")

if __name__ == "__main__":
    main() 