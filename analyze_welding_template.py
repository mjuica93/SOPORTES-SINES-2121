#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análisis del archivo Welding Template para sistema de costuras
"""

import pandas as pd
import os
import json

def analyze_welding_template():
    """Analiza el archivo Excel de welding template"""
    print('🔍 ANÁLISIS DEL WELDING TEMPLATE')
    print('=' * 60)
    
    file_path = 'welding log template/Welding traceability Template - PIPING TEIGA TMI.xlsx'
    
    if not os.path.exists(file_path):
        print(f"❌ Archivo no encontrado: {file_path}")
        return
    
    try:
        # Leer el archivo Excel
        xl_file = pd.ExcelFile(file_path)
        print(f"📋 Hojas disponibles: {xl_file.sheet_names}")
        
        # Analizar la hoja Template
        print("\n--- ANALIZANDO HOJA TEMPLATE ---")
        
        # Leer las primeras 20 filas sin encabezados para encontrar la estructura
        df_raw = pd.read_excel(file_path, sheet_name='Template', header=None, nrows=20)
        
        print("🔍 Primeras 20 filas:")
        for i, row in df_raw.iterrows():
            non_null_values = [str(val) for val in row.values if pd.notna(val)]
            if non_null_values:
                print(f"  Fila {i}: {non_null_values[:8]}...")
        
        # Buscar la fila que contiene los encabezados reales
        print("\n🎯 Buscando encabezados con 'Dia Inch' o 'Isometric':")
        header_row = None
        for i, row in df_raw.iterrows():
            row_str = ' '.join([str(val) for val in row.values if pd.notna(val)])
            if 'Dia Inch' in row_str or 'Isometric' in row_str:
                print(f"  Fila {i}: Contiene encabezados clave")
                header_row = i
                break
        
        if header_row is not None:
            # Leer el archivo con los encabezados correctos
            df = pd.read_excel(file_path, sheet_name='Template', header=header_row)
            print(f"\n📊 Columnas encontradas (usando fila {header_row} como encabezado):")
            for i, col in enumerate(df.columns):
                print(f"  {i+1}. {col}")
            
            # Buscar columnas específicas
            print("\n🔍 Columnas clave encontradas:")
            key_columns = {}
            for col in df.columns:
                col_str = str(col)
                if 'Dia Inch' in col_str and 'Welded' not in col_str:
                    key_columns['diameter'] = col
                    print(f"  - Diámetro: {col}")
                elif 'Dia Inch' in col_str and 'Welded' in col_str:
                    key_columns['welded'] = col
                    print(f"  - Soldado: {col}")
                elif 'Isometric' in col_str:
                    key_columns['isometric'] = col
                    print(f"  - Isométrico: {col}")
                elif 'Weld' in col_str and 'Dia' not in col_str:
                    key_columns['weld_number'] = col
                    print(f"  - Número de soldadura: {col}")
            
            # Mostrar datos de ejemplo
            if key_columns:
                print("\n📋 Datos de ejemplo:")
                sample_data = df[list(key_columns.values())].head(10)
                print(sample_data.to_string())
                
                # Analizar datos no nulos
                print("\n📊 Análisis de datos:")
                for key, col in key_columns.items():
                    non_null_count = df[col].notna().sum()
                    total_count = len(df)
                    print(f"  {key} ({col}): {non_null_count}/{total_count} valores no nulos")
                    
                    if non_null_count > 0:
                        unique_values = df[col].dropna().unique()
                        print(f"    Valores únicos: {len(unique_values)}")
                        print(f"    Ejemplos: {unique_values[:5]}")
        else:
            print("❌ No se encontraron encabezados con 'Dia Inch' o 'Isometric'")
            
    except Exception as e:
        print(f"❌ Error procesando archivo: {e}")

def extract_welding_data():
    """Extrae datos de soldadura del template"""
    print('\n🔧 EXTRAYENDO DATOS DE SOLDADURA')
    print('=' * 60)
    
    file_path = 'welding log template/Welding traceability Template - PIPING TEIGA TMI.xlsx'
    
    if not os.path.exists(file_path):
        print(f"❌ Archivo no encontrado")
        return None
    
    try:
        # Primero encontrar la fila de encabezados
        df_raw = pd.read_excel(file_path, sheet_name='Template', header=None, nrows=20)
        header_row = None
        
        for i, row in df_raw.iterrows():
            row_str = ' '.join([str(val) for val in row.values if pd.notna(val)])
            if 'Dia Inch' in row_str or 'Isometric' in row_str:
                header_row = i
                break
        
        if header_row is None:
            print("❌ No se encontraron encabezados")
            return None
        
        # Leer datos con encabezados correctos
        df = pd.read_excel(file_path, sheet_name='Template', header=header_row)
        
        # Identificar columnas clave
        diameter_col = None
        welded_col = None
        isometric_col = None
        weld_number_col = None
        
        for col in df.columns:
            col_str = str(col)
            if 'Dia Inch' in col_str and 'Welded' not in col_str:
                diameter_col = col
            elif 'Dia Inch' in col_str and 'Welded' in col_str:
                welded_col = col
            elif 'Isometric' in col_str:
                isometric_col = col
            elif 'Weld' in col_str and 'Dia' not in col_str:
                weld_number_col = col
        
        if not all([diameter_col, welded_col, isometric_col]):
            print("❌ No se encontraron todas las columnas necesarias")
            return None
        
        # Extraer datos
        welding_data = []
        
        for _, row in df.iterrows():
            if pd.notna(row[isometric_col]):
                diameter = row[diameter_col] if pd.notna(row[diameter_col]) else 0
                welded = row[welded_col] if pd.notna(row[welded_col]) else 0
                
                # Determinar estado basado en si está soldado
                status = 'completada' if welded > 0 else 'pendiente'
                
                weld_record = {
                    'isometric': str(row[isometric_col]).strip(),
                    'weld_number': str(row[weld_number_col]).strip() if weld_number_col and pd.notna(row[weld_number_col]) else '',
                    'diameter': diameter,
                    'welded': welded,
                    'status': status,
                    'completion_percentage': (welded / diameter * 100) if diameter > 0 else 0
                }
                
                welding_data.append(weld_record)
        
        print(f"✅ Extraídos {len(welding_data)} registros de soldadura")
        
        # Guardar datos
        with open('welding_template_data.json', 'w', encoding='utf-8') as f:
            json.dump(welding_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Datos guardados en: welding_template_data.json")
        
        return welding_data
        
    except Exception as e:
        print(f"❌ Error extrayendo datos: {e}")
        return None

if __name__ == "__main__":
    analyze_welding_template()
    extract_welding_data() 