#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análisis específico de columnas de isométricos en archivos de soportes
"""

import pandas as pd
import json

def analyze_support_columns():
    """Analiza las columnas específicas de los archivos de soportes"""
    print("=== ANÁLISIS DE COLUMNAS DE SOPORTES ===")
    
    support_files = [
        "4274-XH-LP-21210002-IS02_Native.xlsm",
        "4274-XH-LP-21210001-IS03_Native.xlsx"
    ]
    
    for file_name in support_files:
        print(f"\n--- Archivo: {file_name} ---")
        try:
            # Leer específicamente la hoja 'table'
            df = pd.read_excel(file_name, sheet_name='table')
            print(f"Dimensiones: {df.shape}")
            print(f"Todas las columnas:")
            for i, col in enumerate(df.columns):
                print(f"  {i+1}: {col}")
            
            # Buscar columnas específicas mencionadas por el usuario
            target_keywords = ['FLUID', 'PIPING', 'ISOMETRIC', 'PIPELINE', 'ISO', 'SHEET', 'NUMBER']
            
            matching_cols = []
            for col in df.columns:
                col_upper = str(col).upper()
                if any(keyword in col_upper for keyword in target_keywords):
                    matching_cols.append(col)
            
            print(f"\nColumnas que contienen palabras clave: {matching_cols}")
            
            # Mostrar datos de las columnas relevantes
            for col in matching_cols:
                print(f"\n--- Columna: {col} ---")
                print(f"Valores únicos (primeros 10): {df[col].dropna().unique()[:10]}")
                print(f"Total valores únicos: {df[col].dropna().nunique()}")
                print(f"Valores nulos: {df[col].isnull().sum()}")
                
        except Exception as e:
            print(f"Error al leer {file_name}: {e}")

def analyze_isometric_data():
    """Analiza los datos del archivo de isométricos"""
    print("\n=== ANÁLISIS DETALLADO DEL ARCHIVO DE ISOMÉTRICOS ===")
    
    try:
        df = pd.read_excel("ISOMETRICOS/LISTADO DE ISOMETRICOS.xlsx")
        print(f"Total de registros: {len(df)}")
        
        # Analizar columnas LINE y SHEET
        print(f"\nColumna LINE:")
        print(f"  Valores únicos: {df['LINE'].dropna().nunique()}")
        print(f"  Ejemplos: {df['LINE'].dropna().unique()[:10]}")
        
        print(f"\nColumna SHEET:")
        print(f"  Valores únicos: {df['SHEET'].dropna().nunique()}")
        print(f"  Ejemplos: {df['SHEET'].dropna().unique()[:10]}")
        
        # Mostrar ejemplos de combinaciones LINE-SHEET
        print(f"\nEjemplos de combinaciones LINE-SHEET:")
        for i, row in df.head(10).iterrows():
            print(f"  {row['LINE']} - {row['SHEET']}")
            
    except Exception as e:
        print(f"Error al leer archivo de isométricos: {e}")

def create_mapping_structure():
    """Crea una estructura de mapeo para entender las relaciones"""
    print("\n=== CREACIÓN DE ESTRUCTURA DE MAPEO ===")
    
    try:
        # Leer datos de isométricos
        iso_df = pd.read_excel("ISOMETRICOS/LISTADO DE ISOMETRICOS.xlsx")
        
        # Crear estructura de mapeo
        mapping_structure = {
            "isometric_data": {
                "total_records": len(iso_df),
                "columns": list(iso_df.columns),
                "line_examples": iso_df['LINE'].dropna().unique()[:20].tolist(),
                "sheet_examples": iso_df['SHEET'].dropna().unique()[:20].tolist()
            },
            "pdf_files": {
                "normal_isometrics": {
                    "path": "ISOMETRICOS/",
                    "count": len([f for f in os.listdir("ISOMETRICOS") if f.endswith('.pdf')]),
                    "pattern": "19-000-2-02-00001 sheet {LINE-SHEET}_IS0X.pdf"
                },
                "prefab_isometrics": {
                    "path": "ISOMETRICOS PREFABRICADOS/",
                    "count": len([f for f in os.listdir("ISOMETRICOS PREFABRICADOS") if f.endswith('.pdf')]),
                    "pattern": "2121-{LINE}-X.pdf"
                }
            }
        }
        
        # Guardar estructura
        with open("isometric_mapping_structure.json", "w", encoding="utf-8") as f:
            json.dump(mapping_structure, f, indent=2, ensure_ascii=False)
        
        print("Estructura de mapeo guardada en 'isometric_mapping_structure.json'")
        
    except Exception as e:
        print(f"Error al crear estructura de mapeo: {e}")

def main():
    """Función principal"""
    print("ANÁLISIS ESPECÍFICO DE COLUMNAS DE SOPORTES E ISOMÉTRICOS")
    print("=" * 70)
    
    analyze_support_columns()
    analyze_isometric_data()
    create_mapping_structure()
    
    print("\n" + "=" * 70)
    print("ANÁLISIS COMPLETADO")

if __name__ == "__main__":
    import os
    main() 