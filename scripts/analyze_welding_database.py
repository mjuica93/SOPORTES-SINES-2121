#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análisis del archivo Welding Database para sistema de costuras
Analiza la estructura de datos de soldadura y trazabilidad
"""

import pandas as pd
import os
from pathlib import Path

def analyze_welding_database():
    print('🔍 ANÁLISIS DE WELDING DATABASE')
    print('=' * 60)
    
    # Ruta del archivo
    welding_file = "PREFABRICATING WELDING DATABASE/Welding Database updated 20250605 for 2121 Workshop.xlsx"
    
    if not os.path.exists(welding_file):
        print(f"❌ Archivo no encontrado: {welding_file}")
        return
    
    try:
        # Leer el archivo Excel
        xl_file = pd.ExcelFile(welding_file)
        print(f"📋 Hojas disponibles: {xl_file.sheet_names}")
        
        # Analizar cada hoja
        for sheet_name in xl_file.sheet_names:
            print(f"\n--- HOJA: {sheet_name} ---")
            
            try:
                df = pd.read_excel(welding_file, sheet_name=sheet_name)
                print(f"   Dimensiones: {df.shape}")
                print(f"   Columnas: {list(df.columns)}")
                
                # Mostrar algunas filas de muestra
                print(f"   Primeras 3 filas:")
                for i, row in df.head(3).iterrows():
                    print(f"     Fila {i}: {dict(row.dropna())}")
                
                # Buscar columnas relacionadas con isométricos
                iso_columns = []
                for col in df.columns:
                    col_str = str(col).upper()
                    if any(keyword in col_str for keyword in ['ISO', 'LINE', 'DRAWING', 'SHEET', 'WELD', 'COSTURA']):
                        iso_columns.append(col)
                
                if iso_columns:
                    print(f"   🔗 Columnas relacionadas con isométricos: {iso_columns}")
                    
                    # Mostrar valores únicos de estas columnas
                    for col in iso_columns[:3]:  # Solo las primeras 3 para no saturar
                        unique_vals = df[col].dropna().unique()
                        print(f"     {col}: {unique_vals[:10]} (total: {len(unique_vals)})")
                
                # Buscar información de estado/trazabilidad
                status_columns = []
                for col in df.columns:
                    col_str = str(col).upper()
                    if any(keyword in col_str for keyword in ['STATUS', 'STATE', 'COMPLETED', 'DONE', 'PENDING', 'TRAZAB', 'TRACE']):
                        status_columns.append(col)
                
                if status_columns:
                    print(f"   📊 Columnas de estado: {status_columns}")
                
            except Exception as e:
                print(f"   ❌ Error leyendo hoja {sheet_name}: {e}")
        
        print(f"\n" + "=" * 60)
        print(f"✅ ANÁLISIS COMPLETADO")
        
    except Exception as e:
        print(f"❌ Error general: {e}")

def analyze_welding_structure():
    """Analiza la estructura específica para vincular con isométricos"""
    print(f"\n🔗 ANÁLISIS DE VINCULACIÓN CON ISOMÉTRICOS")
    print("=" * 60)
    
    welding_file = "PREFABRICATING WELDING DATABASE/Welding Database updated 20250605 for 2121 Workshop.xlsx"
    
    if not os.path.exists(welding_file):
        print(f"❌ Archivo no encontrado")
        return
    
    try:
        # Probar diferentes hojas para encontrar la principal
        xl_file = pd.ExcelFile(welding_file)
        
        for sheet_name in xl_file.sheet_names:
            print(f"\n--- Analizando vinculación en: {sheet_name} ---")
            
            try:
                df = pd.read_excel(welding_file, sheet_name=sheet_name)
                
                # Buscar patrones de nombres de isométricos
                for col in df.columns:
                    col_str = str(col).upper()
                    if 'ISO' in col_str or 'DRAWING' in col_str or 'LINE' in col_str:
                        print(f"   Columna potencial: {col}")
                        
                        # Mostrar valores para identificar patrones
                        values = df[col].dropna().astype(str)
                        if len(values) > 0:
                            print(f"     Ejemplos: {values.head(5).tolist()}")
                            
                            # Buscar patrones que coincidan con nuestros isométricos
                            patterns_found = []
                            for val in values.head(20):
                                # Buscar patrones como "2121-XXXXX-X"
                                if "2121" in val and "-" in val:
                                    patterns_found.append(val)
                            
                            if patterns_found:
                                print(f"     🎯 Patrones encontrados: {patterns_found[:5]}")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
    
    except Exception as e:
        print(f"❌ Error: {e}")

def propose_integration_strategy():
    """Propone estrategia de integración"""
    print(f"\n💡 ESTRATEGIA DE INTEGRACIÓN")
    print("=" * 60)
    
    print(f"🎯 PASOS SUGERIDOS:")
    print(f"1. Identificar columna de vinculación (isométrico)")
    print(f"2. Extraer información de costuras")
    print(f"3. Clasificar costuras: completadas vs pendientes")
    print(f"4. Crear sistema de trazabilidad")
    print(f"5. Implementar formularios de actualización")
    
    print(f"\n📋 INFORMACIÓN A CAPTURAR:")
    print(f"- Número de costura")
    print(f"- Estado (completada/pendiente)")
    print(f"- Fecha de soldadura")
    print(f"- Soldador responsable")
    print(f"- Tipo de soldadura")
    print(f"- Resultados de inspección")
    print(f"- Certificaciones")

if __name__ == "__main__":
    analyze_welding_database()
    analyze_welding_structure()
    propose_integration_strategy() 