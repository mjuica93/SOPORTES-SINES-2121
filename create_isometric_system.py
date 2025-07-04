#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema completo de vinculación de isométricos con soportes
Crea la nueva funcionalidad con jerarquía: Isométricos -> Soportes
"""

import pandas as pd
import json
import os
from pathlib import Path
import re

class IsometricSystemCreator:
    def __init__(self):
        self.isometric_data = {}
        self.support_data = {}
        self.pdf_mapping = {}
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
                    'supports': [],  # Se llenará con los soportes asociados
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
                
                # Procesar cada soporte
                for _, row in df.iterrows():
                    # Extraer información del soporte
                    fluid_line = str(row['FLUID & NUMBER OF PIPING (ISOMETRIC PIPELINE)']).strip()
                    iso_sheet = str(row['ISO SHEET NUMBER']).strip()
                    
                    # Limpiar datos
                    if fluid_line == 'nan' or iso_sheet == 'nan':
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
                    
            except Exception as e:
                print(f"Error procesando {file_name}: {e}")
        
        print(f"Total soportes procesados: {len(all_supports)}")
        
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
        if not fluid_line or fluid_line == 'nan':
            return None
        
        # Remover sufijos como (P), (PS), (HA), etc.
        clean_line = re.sub(r'\([^)]*\)$', '', fluid_line).strip()
        
        # Remover prefijos de clasificación
        clean_line = re.sub(r'^[A-Z]+\d+[A-Z]\d+-', '', clean_line)
        
        return clean_line if clean_line else None
    
    def extract_sheet_from_iso(self, iso_sheet):
        """Extrae SHEET de ISO SHEET NUMBER"""
        if not iso_sheet or iso_sheet == 'nan':
            return None
        
        # Remover 'SH.' y otros prefijos
        clean_sheet = iso_sheet.replace('SH.', '').strip()
        
        # Convertir a número si es posible
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
                match = re.search(r'sheet\s+(.*?)_IS\d+\.pdf', pdf_file.name, re.IGNORECASE)
                if match:
                    sheet_part = match.group(1).strip()
                    # Extraer LINE (todo antes del último guión)
                    parts = sheet_part.split('-')
                    if len(parts) >= 2:
                        line = '-'.join(parts[:-1])
                        sheet = parts[-1]
                        iso_key = f"{line}-{sheet}"
                        
                        if iso_key in self.isometric_data:
                            self.isometric_data[iso_key]['pdf_files']['normal'] = str(pdf_file)
        
        # Mapear isométricos prefabricados
        prefab_dir = Path("ISOMETRICOS PREFABRICADOS")
        if prefab_dir.exists():
            for pdf_file in prefab_dir.glob("*.pdf"):
                # Extraer LINE del nombre del archivo
                match = re.search(r'2121-([^-]+)-(\d+)\.pdf', pdf_file.name)
                if match:
                    line = match.group(1)
                    sheet = match.group(2)
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
        
        # Crear estructura final optimizada para la web
        self.final_data = {
            'isometrics': {},
            'summary': {
                'total_isometrics': len(self.isometric_data),
                'isometrics_with_supports': len([iso for iso in self.isometric_data.values() if iso['supports']]),
                'isometrics_with_normal_pdf': len([iso for iso in self.isometric_data.values() if iso['pdf_files']['normal']]),
                'isometrics_with_prefab_pdf': len([iso for iso in self.isometric_data.values() if iso['pdf_files']['prefab']]),
                'total_supports': sum(len(iso['supports']) for iso in self.isometric_data.values())
            },
            'search_index': {
                'lines': list(set(iso['line'] for iso in self.isometric_data.values())),
                'sheets': list(set(iso['sheet'] for iso in self.isometric_data.values())),
                'fluids': list(set(iso['fluid'] for iso in self.isometric_data.values() if iso['fluid'])),
                'cwas': list(set(iso['cwa'] for iso in self.isometric_data.values() if iso['cwa']))
            }
        }
        
        # Copiar datos de isométricos a estructura final
        for iso_key, isometric in self.isometric_data.items():
            self.final_data['isometrics'][iso_key] = isometric
        
        print(f"Estructura final creada con {len(self.final_data['isometrics'])} isométricos")
        print(f"Resumen: {self.final_data['summary']}")
        
        return True
    
    def save_data_files(self):
        """Guarda los archivos de datos"""
        print("\n=== GUARDANDO ARCHIVOS DE DATOS ===")
        
        try:
            # Guardar datos principales
            with open('isometric_data.json', 'w', encoding='utf-8') as f:
                json.dump(self.final_data, f, ensure_ascii=False, indent=2, default=str)
            
            # Guardar mapeo simplificado para búsquedas rápidas
            quick_map = {}
            for iso_key, isometric in self.final_data['isometrics'].items():
                quick_map[iso_key] = {
                    'line': isometric['line'],
                    'sheet': isometric['sheet'],
                    'fluid': isometric['fluid'],
                    'support_count': len(isometric['supports']),
                    'has_normal_pdf': bool(isometric['pdf_files']['normal']),
                    'has_prefab_pdf': bool(isometric['pdf_files']['prefab'])
                }
            
            with open('isometric_quick_map.json', 'w', encoding='utf-8') as f:
                json.dump(quick_map, f, ensure_ascii=False, indent=2)
            
            print("✅ Archivos de datos guardados:")
            print("  - isometric_data.json (datos completos)")
            print("  - isometric_quick_map.json (mapeo rápido)")
            
            return True
            
        except Exception as e:
            print(f"Error guardando archivos: {e}")
            return False
    
    def create_system(self):
        """Crea el sistema completo"""
        print("CREANDO SISTEMA DE ISOMÉTRICOS")
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
        print("\nPróximos pasos:")
        print("1. Revisar archivos generados")
        print("2. Crear interfaz web")
        print("3. Integrar con sistema existente")
        
        return True

def main():
    """Función principal"""
    creator = IsometricSystemCreator()
    creator.create_system()

if __name__ == "__main__":
    main() 