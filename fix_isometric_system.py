#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script corregido para crear el sistema de isométricos
Maneja correctamente los nombres de columnas y datos reales
"""

import pandas as pd
import json
import os
from pathlib import Path
import re

class IsometricSystemFixed:
    def __init__(self):
        self.isometric_data = {}
        self.support_data = {}
        self.final_data = {}
        
    def extract_isometric_data(self):
        """Extrae datos del archivo LISTADO DE ISOMETRICOS.xlsx"""
        print("=== EXTRAYENDO DATOS DE ISOMÉTRICOS ===")
        
        try:
            df = pd.read_excel("ISOMETRICOS/LISTADO DE ISOMETRICOS.xlsx")
            print(f"Total registros de isométricos: {len(df)}")
            
            # Crear estructura de datos de isométricos
            for _, row in df.iterrows():
                line = str(row['LINE']).strip()
                sheet = str(row['SHEET']).strip()
                
                # Crear clave única para el isométrico
                iso_key = f"{line}-{sheet}"
                
                self.isometric_data[iso_key] = {
                    'line': line,
                    'sheet': sheet,
                    'file_name': row['FILE NAME'],
                    'unit': row['UNIT'],
                    'cwa': row['CWA'],
                    'fluid': row['FLUID'],
                    'revision': row['REVISION'],
                    'current_review': row['CURRENT REVIEW (YES/NO)'],
                    'lb_sb': row['LB+SB'],
                    'supports': [],
                    'pdf_files': {
                        'normal': None,
                        'prefab': None
                    }
                }
            
            print(f"Procesados {len(self.isometric_data)} isométricos únicos")
            return True
            
        except Exception as e:
            print(f"Error al extraer datos de isométricos: {e}")
            return False
    
    def extract_support_data(self):
        """Extrae datos de los archivos de soportes"""
        print("\n=== EXTRAYENDO DATOS DE SOPORTES ===")
        
        support_files = [
            "4274-XH-LP-21210002-IS02_Native.xlsm",
            "4274-XH-LP-21210001-IS03_Native.xlsx"
        ]
        
        all_supports = []
        
        for file_name in support_files:
            print(f"Procesando {file_name}...")
            try:
                # Leer con encabezados en fila 9
                df = pd.read_excel(file_name, sheet_name='table', header=9)
                print(f"  Registros encontrados: {len(df)}")
                
                # Limpiar nombres de columnas (remover espacios extra)
                df.columns = df.columns.str.strip()
                
                # Mostrar columnas disponibles
                print(f"  Columnas disponibles: {list(df.columns)}")
                
                # Buscar las columnas correctas
                fluid_col = None
                sheet_col = None
                
                for col in df.columns:
                    if 'FLUID' in col and 'PIPING' in col:
                        fluid_col = col
                    elif 'ISO SHEET' in col:
                        sheet_col = col
                
                print(f"  Columna FLUID encontrada: {fluid_col}")
                print(f"  Columna SHEET encontrada: {sheet_col}")
                
                if not fluid_col or not sheet_col:
                    print(f"  ⚠️  No se encontraron las columnas necesarias")
                    continue
                
                # Saltar filas de encabezado adicionales (primeras filas suelen ser títulos)
                df_data = df.iloc[3:].copy()  # Saltar las primeras 3 filas después del encabezado
                print(f"  Datos reales después de saltar encabezados: {len(df_data)}")
                
                # Procesar cada soporte
                processed_count = 0
                for _, row in df_data.iterrows():
                    # Extraer información del soporte
                    fluid_line = str(row[fluid_col]).strip()
                    iso_sheet = str(row[sheet_col]).strip()
                    
                    # Limpiar datos
                    if fluid_line in ['nan', 'NaN', ''] or iso_sheet in ['nan', 'NaN', '']:
                        continue
                    
                    # Extraer LINE de FLUID & NUMBER
                    line = self.extract_line_from_fluid(fluid_line)
                    if not line:
                        continue
                    
                    # Extraer SHEET de ISO SHEET NUMBER
                    sheet = self.extract_sheet_from_iso(iso_sheet)
                    if not sheet:
                        continue
                    
                    # Crear registro de soporte
                    support_record = {
                        'line': line,
                        'sheet': sheet,
                        'iso_key': f"{line}-{sheet}",
                        'support_number': row['SUPPORT NUMBER'],
                        'position_number': row['POSITION NUMBER'],
                        'cwa': row['CWA'],
                        'revision': row['REVISION'],
                        'commodity_code': row['COMMODITY CODE'],
                        'fluid_line_full': fluid_line,
                        'iso_sheet_full': iso_sheet,
                        'source_file': file_name
                    }
                    
                    all_supports.append(support_record)
                    processed_count += 1
                    
                    # Mostrar algunos ejemplos
                    if processed_count <= 5:
                        print(f"    Ejemplo {processed_count}: {fluid_line} -> {line}-{sheet}")
                
                print(f"  ✅ Procesados: {processed_count} soportes")
                    
            except Exception as e:
                print(f"  ❌ Error procesando {file_name}: {e}")
        
        print(f"\nTotal soportes procesados: {len(all_supports)}")
        
        # Agrupar soportes por isométrico
        self.support_data = {}
        for support in all_supports:
            iso_key = support['iso_key']
            if iso_key not in self.support_data:
                self.support_data[iso_key] = []
            self.support_data[iso_key].append(support)
        
        print(f"Soportes agrupados en {len(self.support_data)} isométricos")
        return True
    
    def extract_line_from_fluid(self, fluid_line):
        """Extrae LINE de FLUID & NUMBER OF PIPING"""
        if not fluid_line or fluid_line in ['nan', 'NaN']:
            return None
        
        # Ejemplo: 'CWS40G02-B1(P)' -> 'CWS40G02'
        # Remover sufijos como (P), (PS), (HA), etc.
        clean_line = re.sub(r'\([^)]*\)$', '', fluid_line).strip()
        
        # Separar por guión y tomar la primera parte
        parts = clean_line.split('-')
        if len(parts) >= 1:
            return parts[0]
        
        return clean_line if clean_line else None
    
    def extract_sheet_from_iso(self, iso_sheet):
        """Extrae SHEET de ISO SHEET NUMBER"""
        if not iso_sheet or iso_sheet in ['nan', 'NaN']:
            return None
        
        # Ejemplo: 'SH.003' -> '3'
        clean_sheet = iso_sheet.replace('SH.', '').strip()
        
        # Convertir a número si es posible y luego a string
        try:
            return str(int(clean_sheet))
        except:
            return clean_sheet if clean_sheet else None
    
    def map_pdf_files(self):
        """Mapea archivos PDF a isométricos"""
        print("\n=== MAPEANDO ARCHIVOS PDF ===")
        
        # Mapear isométricos normales
        iso_dir = Path("ISOMETRICOS")
        if iso_dir.exists():
            for pdf_file in iso_dir.glob("*.pdf"):
                # Extraer LINE y SHEET del nombre del archivo
                # Ejemplo: '19-000-2-02-00001 sheet 2121BU10C13-1_IS01.pdf'
                match = re.search(r'sheet\s+(.+?)_IS\d+\.pdf', pdf_file.name, re.IGNORECASE)
                if match:
                    sheet_part = match.group(1).strip()
                    # Dividir por guión y tomar los componentes
                    parts = sheet_part.split('-')
                    if len(parts) >= 2:
                        line = parts[0]  # Ejemplo: 'BU10C13'
                        sheet = parts[1]  # Ejemplo: '1'
                        iso_key = f"{line}-{sheet}"
                        
                        if iso_key in self.isometric_data:
                            self.isometric_data[iso_key]['pdf_files']['normal'] = str(pdf_file)
        
        # Mapear isométricos prefabricados
        prefab_dir = Path("ISOMETRICOS PREFABRICADOS")
        if prefab_dir.exists():
            for pdf_file in prefab_dir.glob("*.pdf"):
                # Extraer LINE del nombre del archivo
                # Ejemplo: '2121-BU10C13-1.pdf'
                match = re.search(r'2121-([^-]+)-(\d+)\.pdf', pdf_file.name)
                if match:
                    line = match.group(1)  # Ejemplo: 'BU10C13'
                    sheet = match.group(2)  # Ejemplo: '1'
                    iso_key = f"{line}-{sheet}"
                    
                    if iso_key in self.isometric_data:
                        self.isometric_data[iso_key]['pdf_files']['prefab'] = str(pdf_file)
        
        # Contar archivos mapeados
        normal_count = sum(1 for iso in self.isometric_data.values() if iso['pdf_files']['normal'])
        prefab_count = sum(1 for iso in self.isometric_data.values() if iso['pdf_files']['prefab'])
        
        print(f"Archivos PDF normales mapeados: {normal_count}")
        print(f"Archivos PDF prefabricados mapeados: {prefab_count}")
        
        return True
    
    def create_final_structure(self):
        """Crea la estructura final de datos"""
        print("\n=== CREANDO ESTRUCTURA FINAL ===")
        
        # Vincular soportes con isométricos
        for iso_key, isometric in self.isometric_data.items():
            if iso_key in self.support_data:
                isometric['supports'] = self.support_data[iso_key]
        
        # Crear estructura final
        self.final_data = {
            'isometrics': self.isometric_data,
            'summary': {
                'total_isometrics': len(self.isometric_data),
                'isometrics_with_supports': len([iso for iso in self.isometric_data.values() if iso['supports']]),
                'isometrics_with_normal_pdf': len([iso for iso in self.isometric_data.values() if iso['pdf_files']['normal']]),
                'isometrics_with_prefab_pdf': len([iso for iso in self.isometric_data.values() if iso['pdf_files']['prefab']]),
                'total_supports': sum(len(iso['supports']) for iso in self.isometric_data.values())
            }
        }
        
        print(f"Estructura final creada:")
        print(f"  - Total isométricos: {self.final_data['summary']['total_isometrics']}")
        print(f"  - Isométricos con soportes: {self.final_data['summary']['isometrics_with_supports']}")
        print(f"  - Isométricos con PDF normal: {self.final_data['summary']['isometrics_with_normal_pdf']}")
        print(f"  - Isométricos con PDF prefabricado: {self.final_data['summary']['isometrics_with_prefab_pdf']}")
        print(f"  - Total soportes: {self.final_data['summary']['total_supports']}")
        
        return True
    
    def save_data_files(self):
        """Guarda los archivos de datos"""
        print("\n=== GUARDANDO ARCHIVOS DE DATOS ===")
        
        try:
            # Guardar datos principales
            with open('isometric_data_fixed.json', 'w', encoding='utf-8') as f:
                json.dump(self.final_data, f, ensure_ascii=False, indent=2, default=str)
            
            print("✅ Archivos de datos guardados:")
            print("  - isometric_data_fixed.json (datos completos)")
            
            return True
            
        except Exception as e:
            print(f"❌ Error guardando archivos: {e}")
            return False
    
    def create_system(self):
        """Crea el sistema completo"""
        print("CREANDO SISTEMA DE ISOMÉTRICOS - VERSIÓN CORREGIDA")
        print("=" * 60)
        
        steps = [
            ("Extraer datos de isométricos", self.extract_isometric_data),
            ("Extraer datos de soportes", self.extract_support_data),
            ("Mapear archivos PDF", self.map_pdf_files),
            ("Crear estructura final", self.create_final_structure),
            ("Guardar archivos de datos", self.save_data_files)
        ]
        
        for step_name, step_func in steps:
            print(f"\n🔄 {step_name}...")
            if not step_func():
                print(f"❌ Error en: {step_name}")
                return False
        
        print("\n" + "=" * 60)
        print("✅ SISTEMA DE ISOMÉTRICOS CREADO EXITOSAMENTE")
        
        return True

def main():
    """Función principal"""
    creator = IsometricSystemFixed()
    creator.create_system()

if __name__ == "__main__":
    main() 