#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para actualizar automáticamente el sistema cuando se añaden nuevos PDFs
"""

import os
import subprocess
import json
import sys
from datetime import datetime

def contar_pdfs():
    """Contar archivos PDF en la carpeta"""
    pdf_folder = "ESTANDARES DE SOPORTES"
    if not os.path.exists(pdf_folder):
        return 0
    
    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith('.pdf')]
    return len(pdf_files)

def ejecutar_script(script_name):
    """Ejecutar un script Python y mostrar resultado"""
    try:
        print(f"🔄 Ejecutando {script_name}...")
        
        # Configurar la codificación para Windows
        if sys.platform == 'win32':
            result = subprocess.run(['python', script_name], 
                                  capture_output=True, text=True, 
                                  encoding='utf-8', errors='replace')
        else:
            result = subprocess.run(['python', script_name], 
                                  capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print(f"✅ {script_name} ejecutado correctamente")
            return True
        else:
            print(f"❌ Error en {script_name}")
            if result.stderr:
                print(f"   Error: {result.stderr[:200]}...")
            return False
    except Exception as e:
        print(f"❌ Error ejecutando {script_name}: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("🔄 ACTUALIZADOR AUTOMÁTICO DEL SISTEMA DE SOPORTES")
    print("=" * 60)
    
    # Contar PDFs disponibles
    total_pdfs = contar_pdfs()
    print(f"📁 PDFs disponibles: {total_pdfs}")
    
    if total_pdfs == 0:
        print("❌ No se encontraron archivos PDF en la carpeta 'ESTANDARES DE SOPORTES'")
        return
    
    # Actualizar mapeo de soportes
    print("\n🔄 PASO 1: Actualizando mapeo de soportes...")
    if not ejecutar_script("create_support_mapping.py"):
        print("❌ Error al actualizar el mapeo de soportes")
        return
    
    # Regenerar lista de PDFs faltantes
    print("\n🔄 PASO 2: Regenerando lista de PDFs faltantes...")
    if not ejecutar_script("generate_missing_pdfs_list.py"):
        print("⚠️ Advertencia: Error al generar lista de PDFs faltantes")
        print("   El mapeo se actualizó correctamente, pero la lista de faltantes puede no estar actualizada")
    
    # Leer estadísticas actualizadas
    try:
        with open('support_pdf_mapping.json', 'r', encoding='utf-8') as f:
            mapping = json.load(f)
        
        tipos_con_pdf = len([k for k, v in mapping.items() if v])
        tipos_sin_pdf = len([k for k, v in mapping.items() if not v])
        
        print("\n📊 ESTADÍSTICAS ACTUALIZADAS:")
        print(f"   📄 Total PDFs disponibles: {total_pdfs}")
        print(f"   ✅ Tipos de soportes con PDF: {tipos_con_pdf}")
        print(f"   ❌ Tipos de soportes sin PDF: {tipos_sin_pdf}")
        if tipos_con_pdf + tipos_sin_pdf > 0:
            porcentaje = (tipos_con_pdf/(tipos_con_pdf+tipos_sin_pdf)*100)
            print(f"   📈 Porcentaje cubierto: {porcentaje:.1f}%")
        
    except Exception as e:
        print(f"❌ Error leyendo estadísticas: {str(e)}")
    
    print("\n🌐 SISTEMA ACTUALIZADO CORRECTAMENTE")
    print("   Para usar el sistema:")
    print("   1. Ejecutar: python server.py")
    print("   2. Abrir: http://localhost:8000/index_enhanced_with_templates.html")
    print("   3. O usar: INICIAR_VERSION_CON_PLANTILLAS.bat")
    
    # Crear log de actualización
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - Sistema actualizado - {total_pdfs} PDFs disponibles\n"
        
        with open('actualizaciones.log', 'a', encoding='utf-8') as f:
            f.write(log_entry)
        
        print(f"\n📝 Actualización registrada en actualizaciones.log")
    except Exception as e:
        print(f"⚠️ No se pudo crear el log: {str(e)}")

if __name__ == "__main__":
    main() 