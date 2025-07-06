import pandas as pd
import json
import os

def extract_support_data():
    support_data = []
    
    # Archivos Excel a procesar
    excel_files = [
        '4274-XH-LP-21210001-IS03_Native.xlsx',  # Soportes estándar
        '4274-XH-LP-21210002-IS02_Native.xlsm'   # Soportes especiales
    ]
    
    for file in excel_files:
        try:
            print(f"Procesando: {file}")
            
            # Leer la hoja 'table' que contiene los datos de soportes
            df = pd.read_excel(file, sheet_name='table')
            
            print(f"Dimensiones del DataFrame: {df.shape}")
            
            # Los encabezados están en la fila 8 según el análisis previo
            header_row = 8
            print(f"Usando fila {header_row} como encabezados")
            
            # Verificar que la fila 8 contiene los encabezados correctos
            header_row_data = df.iloc[header_row]
            print(f"Encabezados en fila {header_row}:")
            for i, cell in enumerate(header_row_data):
                if pd.notna(cell):
                    print(f"  Col {i}: {cell}")
            
            # Extraer datos desde la fila siguiente a los encabezados
            for idx in range(header_row + 1, len(df)):
                row = df.iloc[idx]
                
                # Extraer datos relevantes
                support_number = row.iloc[2]  # SUPPORT NUMBER
                support_type = row.iloc[5]    # SUPPORT OR ELEMENT TYPE
                
                # Verificar que tenemos datos válidos
                if pd.notna(support_number) and pd.notna(support_type):
                    # Convertir a string y limpiar
                    support_number_str = str(support_number).strip()
                    support_type_str = str(support_type).strip()
                    
                    # Verificar que no son encabezados y que son datos válidos
                    if (support_number_str and 
                        support_number_str != 'SUPPORT NUMBER' and 
                        support_type_str and 
                        support_type_str != 'SUPPORT OR ELEMENT TYPE' and
                        support_number_str != 'nan' and
                        support_type_str != 'nan'):
                        
                        support_info = {
                            'support_number': support_number_str,
                            'support_type': support_type_str,
                            'file_source': file,
                            'position_number': str(row.iloc[4]) if pd.notna(row.iloc[4]) else '',
                            'commodity_code': str(row.iloc[5]) if pd.notna(row.iloc[5]) else '',
                            'material_class': str(row.iloc[9]) if pd.notna(row.iloc[9]) else '',
                            'size_dimensions': str(row.iloc[13]) if pd.notna(row.iloc[13]) else '',
                            'quantity': str(row.iloc[33]) if pd.notna(row.iloc[33]) else '',
                            'fluid_piping': str(row.iloc[34]) if pd.notna(row.iloc[34]) else '',
                            'iso_sheet': str(row.iloc[37]) if pd.notna(row.iloc[37]) else '',
                            'notes': str(row.iloc[39]) if pd.notna(row.iloc[39]) else '',
                            'temperature': str(row.iloc[44]) if pd.notna(row.iloc[44]) else ''
                        }
                        
                        support_data.append(support_info)
                        
                        # Mostrar algunos ejemplos
                        if len(support_data) <= 10:
                            print(f"  Soporte: {support_number_str} - Tipo: {support_type_str}")
            
        except Exception as e:
            print(f"Error procesando {file}: {e}")
            import traceback
            traceback.print_exc()
    
    # Guardar datos en JSON
    with open('support_data.json', 'w', encoding='utf-8') as f:
        json.dump(support_data, f, ensure_ascii=False, indent=2)
    
    print(f"\nTotal de soportes extraídos: {len(support_data)}")
    print("Datos guardados en support_data.json")
    
    # Mostrar tipos de soportes únicos
    support_types = set(item['support_type'] for item in support_data)
    print(f"\nTipos de soportes encontrados ({len(support_types)}):")
    for st in sorted(support_types):
        print(f"  - {st}")
    
    return support_data

if __name__ == "__main__":
    extract_support_data() 