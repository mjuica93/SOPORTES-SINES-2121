import os
import json

def cleanup_and_verify():
    print("=== LIMPIEZA Y VERIFICACIÓN DEL SISTEMA ===\n")
    
    # Lista de archivos temporales a eliminar
    temp_files = [
        'analyze_excel.py',
        'analyze_excel_detailed.py',
        'extract_support_data.py',
        'extract_support_data_v2.py'
    ]
    
    # Eliminar archivos temporales
    print("Eliminando archivos temporales...")
    for file in temp_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"  ✓ Eliminado: {file}")
        else:
            print(f"  - No encontrado: {file}")
    
    print()
    
    # Verificar archivos esenciales
    essential_files = [
        'index.html',
        'app.js',
        'support_data.json',
        'support_pdf_mapping.json',
        'README.md'
    ]
    
    print("Verificando archivos esenciales...")
    missing_files = []
    for file in essential_files:
        if os.path.exists(file):
            print(f"  ✓ Presente: {file}")
        else:
            print(f"  ✗ Faltante: {file}")
            missing_files.append(file)
    
    print()
    
    # Verificar carpeta de PDFs
    pdf_dir = 'ESTANDARES DE SOPORTES'
    if os.path.exists(pdf_dir):
        pdf_count = len([f for f in os.listdir(pdf_dir) if f.endswith('.pdf')])
        print(f"✓ Carpeta de PDFs encontrada: {pdf_count} archivos")
    else:
        print("✗ Carpeta de PDFs no encontrada")
        missing_files.append(pdf_dir)
    
    print()
    
    # Verificar datos JSON
    print("Verificando datos JSON...")
    try:
        with open('support_data.json', 'r', encoding='utf-8') as f:
            support_data = json.load(f)
        print(f"  ✓ support_data.json: {len(support_data)} soportes")
    except Exception as e:
        print(f"  ✗ Error en support_data.json: {e}")
        missing_files.append('support_data.json')
    
    try:
        with open('support_pdf_mapping.json', 'r', encoding='utf-8') as f:
            mapping_data = json.load(f)
        print(f"  ✓ support_pdf_mapping.json: {len(mapping_data)} tipos mapeados")
    except Exception as e:
        print(f"  ✗ Error en support_pdf_mapping.json: {e}")
        missing_files.append('support_pdf_mapping.json')
    
    print()
    
    # Resumen final
    if missing_files:
        print("⚠️  ADVERTENCIA: Faltan algunos archivos:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nPara completar la instalación, ejecuta:")
        print("1. python extract_support_data_final.py")
        print("2. python create_support_mapping.py")
    else:
        print("🎉 ¡Sistema completamente instalado y listo!")
        print("\nPara usar el sistema:")
        print("1. Abre index.html en tu navegador web")
        print("2. ¡Disfruta buscando soportes!")
    
    print("\n=== FIN DE VERIFICACIÓN ===")

if __name__ == "__main__":
    cleanup_and_verify() 