import json
import os
import re

def create_support_mapping():
    # Cargar datos de soportes
    with open('support_data.json', 'r', encoding='utf-8') as f:
        support_data = json.load(f)
    
    # Obtener lista de PDFs disponibles
    pdf_dir = 'ESTANDARES DE SOPORTES'
    pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    
    print(f"PDFs disponibles: {len(pdf_files)}")
    
    # Crear mapeo de tipos de soportes a PDFs
    support_mapping = {}
    
    # Obtener tipos únicos de soportes
    support_types = set(item['support_type'] for item in support_data)
    
    for support_type in support_types:
        matching_pdfs = []
        
        # Buscar PDFs que coincidan con el tipo de soporte
        for pdf_file in pdf_files:
            pdf_name = pdf_file.replace('.pdf', '').upper()
            
            # Diferentes patrones de búsqueda
            patterns = [
                support_type.upper(),
                support_type.upper().replace('-', ''),
                support_type.upper().replace('_', ''),
                support_type.upper().replace(' ', '')
            ]
            
            for pattern in patterns:
                if pattern in pdf_name:
                    matching_pdfs.append(pdf_file)
                    break
        
        if matching_pdfs:
            support_mapping[support_type] = matching_pdfs
            print(f"{support_type}: {matching_pdfs}")
        else:
            print(f"{support_type}: No se encontró PDF correspondiente")
    
    # Guardar mapeo
    with open('support_pdf_mapping.json', 'w', encoding='utf-8') as f:
        json.dump(support_mapping, f, ensure_ascii=False, indent=2)
    
    print(f"\nMapeo guardado en support_pdf_mapping.json")
    print(f"Tipos de soportes con PDF: {len([k for k, v in support_mapping.items() if v])}")
    print(f"Tipos de soportes sin PDF: {len([k for k, v in support_mapping.items() if not v])}")
    
    return support_mapping

if __name__ == "__main__":
    create_support_mapping() 