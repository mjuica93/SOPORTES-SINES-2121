import pandas as pd
import json

def analyze_excel_headers():
    print("=== ANÁLISIS DE TÍTULOS DE PLANTILLAS DE SOPORTE ===\n")
    
    # Leer archivos Excel
    excel_files = [
        '4274-XH-LP-21210001-IS03_Native.xlsx',
        '4274-XH-LP-21210002-IS02_Native.xlsm'
    ]
    
    all_headers = {}
    
    for excel_file in excel_files:
        try:
            print(f"📊 Analizando archivo: {excel_file}")
            
            # Leer las filas específicas (22 y 23)
            df = pd.read_excel(excel_file, sheet_name='table', header=None, skiprows=21, nrows=2)
            
            print(f"   Dimensiones: {df.shape}")
            print(f"   Columnas disponibles: {df.shape[1]}")
            
            # Mostrar contenido de las filas 22 y 23
            print(f"\n📋 FILA 22 (Títulos principales):")
            row_22 = df.iloc[0].fillna('').astype(str)
            for i, value in enumerate(row_22):
                if value.strip():
                    print(f"   Columna {i}: '{value}'")
            
            print(f"\n📋 FILA 23 (Subtítulos/Descripciones):")
            row_23 = df.iloc[1].fillna('').astype(str)
            for i, value in enumerate(row_23):
                if value.strip():
                    print(f"   Columna {i}: '{value}'")
            
            # Crear mapeo de columnas con títulos
            column_mapping = {}
            for i in range(len(row_22)):
                title_22 = str(row_22.iloc[i]).strip() if i < len(row_22) else ''
                title_23 = str(row_23.iloc[i]).strip() if i < len(row_23) else ''
                
                if title_22 or title_23:
                    column_mapping[f'col_{i}'] = {
                        'index': i,
                        'title_row_22': title_22,
                        'title_row_23': title_23,
                        'combined_title': f"{title_22} - {title_23}".strip(' -') if title_22 and title_23 else title_22 or title_23
                    }
            
            all_headers[excel_file] = column_mapping
            
            print(f"\n✅ Procesadas {len(column_mapping)} columnas con títulos")
            
        except Exception as e:
            print(f"❌ Error procesando {excel_file}: {e}")
    
    # Crear mapeo consolidado
    print(f"\n🔄 CONSOLIDANDO TÍTULOS...")
    
    # Usar el primer archivo como base (suelen tener la misma estructura)
    if excel_files[0] in all_headers:
        consolidated_headers = all_headers[excel_files[0]]
        
        print(f"\n📊 MAPEO CONSOLIDADO DE TÍTULOS:")
        print("=" * 80)
        
        for col_key, col_info in consolidated_headers.items():
            print(f"Columna {col_info['index']:2d}: {col_info['combined_title']}")
        
        # Guardar mapeo en archivo JSON
        with open('column_titles_mapping.json', 'w', encoding='utf-8') as f:
            json.dump(consolidated_headers, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Mapeo guardado en: column_titles_mapping.json")
        
        # Crear mapeo específico para campos conocidos
        create_field_mapping(consolidated_headers)
        
    return all_headers

def create_field_mapping(headers):
    print(f"\n🎯 CREANDO MAPEO DE CAMPOS ESPECÍFICOS...")
    
    # Mapeo de campos conocidos basado en los títulos
    field_mapping = {
        'basic_info': {},
        'technical_info': {},
        'dimensions': {},
        'project_info': {},
        'coordinates': {}
    }
    
    # Buscar campos por palabras clave en los títulos
    for col_key, col_info in headers.items():
        title = col_info['combined_title'].lower()
        index = col_info['index']
        
        # Información básica
        if 'support' in title and 'number' in title:
            field_mapping['basic_info']['support_number'] = {
                'column': index,
                'title': col_info['combined_title'],
                'description': 'Número de soporte'
            }
        elif 'support' in title and 'type' in title:
            field_mapping['basic_info']['support_type'] = {
                'column': index,
                'title': col_info['combined_title'],
                'description': 'Tipo de soporte'
            }
        elif 'fluid' in title or 'line' in title:
            field_mapping['basic_info']['fluid'] = {
                'column': index,
                'title': col_info['combined_title'],
                'description': 'Fluido/Línea'
            }
        
        # Coordenadas
        elif 'x' in title and ('coord' in title or 'pos' in title):
            field_mapping['coordinates']['x'] = {
                'column': index,
                'title': col_info['combined_title'],
                'description': 'Coordenada X'
            }
        elif 'y' in title and ('coord' in title or 'pos' in title):
            field_mapping['coordinates']['y'] = {
                'column': index,
                'title': col_info['combined_title'],
                'description': 'Coordenada Y'
            }
        elif 'z' in title and ('coord' in title or 'pos' in title):
            field_mapping['coordinates']['z'] = {
                'column': index,
                'title': col_info['combined_title'],
                'description': 'Coordenada Z'
            }
        
        # Información técnica
        elif 'cwa' in title:
            field_mapping['technical_info']['cwa'] = {
                'column': index,
                'title': col_info['combined_title'],
                'description': 'CWA'
            }
        elif 'rev' in title:
            field_mapping['technical_info']['revision'] = {
                'column': index,
                'title': col_info['combined_title'],
                'description': 'Revisión'
            }
        
        # Dimensiones (buscar patrones comunes)
        elif any(dim in title for dim in ['length', 'width', 'height', 'diameter', 'thickness']):
            field_name = next(dim for dim in ['length', 'width', 'height', 'diameter', 'thickness'] if dim in title)
            field_mapping['dimensions'][field_name] = {
                'column': index,
                'title': col_info['combined_title'],
                'description': f'Dimensión: {field_name}'
            }
        
        # Información de proyecto
        elif 'date' in title or 'created' in title:
            field_mapping['project_info']['date'] = {
                'column': index,
                'title': col_info['combined_title'],
                'description': 'Fecha'
            }
        elif 'note' in title or 'comment' in title:
            field_mapping['project_info']['notes'] = {
                'column': index,
                'title': col_info['combined_title'],
                'description': 'Notas'
            }
    
    # Guardar mapeo de campos
    with open('field_titles_mapping.json', 'w', encoding='utf-8') as f:
        json.dump(field_mapping, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Mapeo de campos guardado en: field_titles_mapping.json")
    
    # Mostrar resumen
    print(f"\n📋 RESUMEN DE CAMPOS MAPEADOS:")
    for category, fields in field_mapping.items():
        if fields:
            print(f"\n{category.upper().replace('_', ' ')}:")
            for field_name, field_info in fields.items():
                print(f"   {field_name}: {field_info['title']}")
    
    return field_mapping

if __name__ == "__main__":
    analyze_excel_headers() 