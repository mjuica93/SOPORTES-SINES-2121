import json
import os
from collections import Counter

def generate_missing_pdfs_list():
    print("=== ANÁLISIS DE SOPORTES SIN PDFs ===\n")
    
    # Cargar datos de soportes
    with open('support_data_enhanced.json', 'r', encoding='utf-8') as f:
        support_data = json.load(f)
    
    # Cargar mapeo de PDFs
    with open('support_pdf_mapping.json', 'r', encoding='utf-8') as f:
        pdf_mapping = json.load(f)
    
    # Obtener todos los tipos de soportes únicos
    all_support_types = set(item['support_type'] for item in support_data)
    
    # Identificar tipos sin PDFs
    types_without_pdfs = []
    types_with_pdfs = []
    
    for support_type in all_support_types:
        if support_type not in pdf_mapping or not pdf_mapping[support_type]:
            types_without_pdfs.append(support_type)
        else:
            types_with_pdfs.append(support_type)
    
    # Contar cuántos soportes de cada tipo sin PDF existen
    support_counts = Counter(item['support_type'] for item in support_data)
    
    # Crear lista detallada de tipos sin PDFs
    missing_pdfs_details = []
    for support_type in sorted(types_without_pdfs):
        count = support_counts[support_type]
        # Obtener ejemplos de números de soporte
        examples = [item['support_number'] for item in support_data if item['support_type'] == support_type]
        unique_examples = sorted(set(examples))[:5]  # Primeros 5 únicos
        
        missing_pdfs_details.append({
            'support_type': support_type,
            'count': count,
            'support_numbers_examples': unique_examples,
            'total_unique_numbers': len(set(examples))
        })
    
    # Mostrar estadísticas
    print(f"📊 ESTADÍSTICAS GENERALES:")
    print(f"   Total tipos de soportes: {len(all_support_types)}")
    print(f"   Tipos CON PDFs: {len(types_with_pdfs)}")
    print(f"   Tipos SIN PDFs: {len(types_without_pdfs)}")
    print(f"   Porcentaje sin PDFs: {len(types_without_pdfs)/len(all_support_types)*100:.1f}%")
    
    # Mostrar lista detallada
    print(f"\n📋 LISTA DETALLADA DE SOPORTES SIN PDFs:")
    print("="*80)
    
    total_supports_without_pdfs = 0
    for item in missing_pdfs_details:
        total_supports_without_pdfs += item['count']
        print(f"🔍 TIPO: {item['support_type']}")
        print(f"   Cantidad de soportes: {item['count']}")
        print(f"   Números únicos: {item['total_unique_numbers']}")
        print(f"   Ejemplos: {', '.join(item['support_numbers_examples'])}")
        print(f"   Archivo PDF a buscar: {item['support_type']}.pdf")
        print("-" * 60)
    
    print(f"\n📈 RESUMEN:")
    print(f"   Total soportes sin PDFs: {total_supports_without_pdfs}")
    print(f"   Total tipos sin PDFs: {len(types_without_pdfs)}")
    
    # Guardar lista en archivo de texto
    with open('SOPORTES_SIN_PDFs.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("           LISTA DE SOPORTES SIN PDFs CORRESPONDIENTES\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"📊 ESTADÍSTICAS:\n")
        f.write(f"   Total tipos de soportes: {len(all_support_types)}\n")
        f.write(f"   Tipos CON PDFs: {len(types_with_pdfs)}\n")
        f.write(f"   Tipos SIN PDFs: {len(types_without_pdfs)}\n")
        f.write(f"   Porcentaje sin PDFs: {len(types_without_pdfs)/len(all_support_types)*100:.1f}%\n")
        f.write(f"   Total soportes afectados: {total_supports_without_pdfs}\n\n")
        
        f.write("📋 ARCHIVOS PDF A BUSCAR:\n")
        f.write("-" * 40 + "\n")
        for item in missing_pdfs_details:
            f.write(f"{item['support_type']}.pdf\n")
        
        f.write(f"\n📋 LISTA DETALLADA:\n")
        f.write("=" * 80 + "\n")
        
        for item in missing_pdfs_details:
            f.write(f"\n🔍 TIPO: {item['support_type']}\n")
            f.write(f"   Archivo PDF necesario: {item['support_type']}.pdf\n")
            f.write(f"   Cantidad de soportes: {item['count']}\n")
            f.write(f"   Números únicos de soporte: {item['total_unique_numbers']}\n")
            f.write(f"   Ejemplos de números: {', '.join(item['support_numbers_examples'])}\n")
            f.write("-" * 60 + "\n")
    
    # Guardar también en JSON para procesamiento
    with open('missing_pdfs_data.json', 'w', encoding='utf-8') as f:
        json.dump({
            'statistics': {
                'total_types': len(all_support_types),
                'types_with_pdfs': len(types_with_pdfs),
                'types_without_pdfs': len(types_without_pdfs),
                'percentage_without_pdfs': len(types_without_pdfs)/len(all_support_types)*100,
                'total_supports_without_pdfs': total_supports_without_pdfs
            },
            'missing_types': missing_pdfs_details
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ ARCHIVOS GENERADOS:")
    print(f"   📄 SOPORTES_SIN_PDFs.txt - Lista legible")
    print(f"   📄 missing_pdfs_data.json - Datos estructurados")
    
    # Crear lista simple de archivos PDF a buscar
    with open('ARCHIVOS_PDF_A_BUSCAR.txt', 'w', encoding='utf-8') as f:
        f.write("ARCHIVOS PDF A BUSCAR Y AGREGAR A LA CARPETA 'ESTANDARES DE SOPORTES':\n")
        f.write("=" * 70 + "\n\n")
        for item in missing_pdfs_details:
            f.write(f"{item['support_type']}.pdf\n")
        f.write(f"\nTotal archivos a buscar: {len(missing_pdfs_details)}\n")
    
    print(f"   📄 ARCHIVOS_PDF_A_BUSCAR.txt - Lista simple para búsqueda")
    
    return missing_pdfs_details

if __name__ == "__main__":
    generate_missing_pdfs_list() 