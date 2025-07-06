#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificar datos del sistema antes del despliegue a Railway
"""

import json
import os
import sys

def verificar_datos():
    """Verificar integridad de datos del sistema"""
    try:
        # Verificar estadísticas
        print("📊 Verificando estadísticas del sistema...")
        with open('welding_statistics.json', 'r', encoding='utf-8') as f:
            stats = json.load(f)
        
        print(f"📐 Isométricos totales: {stats.get('total_isometrics', 0):,}")
        print(f"🔨 Isométricos con costuras: {stats.get('isometrics_with_welds', 0):,}")
        print(f"⚡ Costuras totales: {stats.get('total_welds', 0):,}")
        print(f"✅ Costuras completadas: {stats.get('completed_welds', 0):,} ({stats.get('completion_percentage', 0)}%)")
        print(f"🏭 Costuras prefabricadas: {stats.get('prefab_welds', 0):,}")
        print(f"🏗️ Costuras de campo: {stats.get('field_welds', 0):,}")
        
        # Verificar tamaño del archivo de datos
        if os.path.exists('isometric_data_with_welds.json'):
            size_mb = os.path.getsize('isometric_data_with_welds.json') / (1024 * 1024)
            print(f"💾 Tamaño de datos: {size_mb:.1f} MB")
            
            if size_mb > 50:
                print("⚠️ ADVERTENCIA: El archivo de datos es muy grande para Railway")
                print("   Considera optimizar el archivo antes del despliegue")
            else:
                print("✅ Tamaño de datos apropiado para Railway")
        else:
            print("❌ Archivo de datos no encontrado")
            return False
        
        # Verificar archivo principal
        if os.path.exists('index_isometricos_con_costuras.html'):
            size_kb = os.path.getsize('index_isometricos_con_costuras.html') / 1024
            print(f"📄 Tamaño de interfaz: {size_kb:.1f} KB")
        
        print("✅ Datos verificados correctamente")
        return True

    except Exception as e:
        print(f"❌ Error verificando datos: {e}")
        return False

def verificar_archivos_criticos():
    """Verificar que todos los archivos críticos existen"""
    archivos_criticos = [
        'index_isometricos_con_costuras.html',
        'isometric_welding_manager.js',
        'isometric_data_with_welds.json',
        'welding_statistics.json',
        'server_railway.py',
        'requirements.txt',
        'Dockerfile',
        'railway.json'
    ]
    
    print("📋 Verificando archivos críticos...")
    faltantes = []
    
    for archivo in archivos_criticos:
        if os.path.exists(archivo):
            size_kb = os.path.getsize(archivo) / 1024
            print(f"✅ {archivo} - {size_kb:.1f} KB")
        else:
            print(f"❌ {archivo} - FALTANTE")
            faltantes.append(archivo)
    
    if faltantes:
        print(f"\n❌ FALTAN {len(faltantes)} ARCHIVOS CRÍTICOS:")
        for archivo in faltantes:
            print(f"   - {archivo}")
        return False
    else:
        print("✅ TODOS LOS ARCHIVOS CRÍTICOS ESTÁN PRESENTES")
        return True

def main():
    """Función principal"""
    print("🔍 VERIFICACIÓN PRE-DESPLIEGUE")
    print("=" * 50)
    
    # Verificar archivos críticos
    if not verificar_archivos_criticos():
        sys.exit(1)
    
    print()
    
    # Verificar datos
    if not verificar_datos():
        sys.exit(1)
    
    print("\n🎉 SISTEMA LISTO PARA DESPLIEGUE A RAILWAY!")
    print("=" * 50)

if __name__ == "__main__":
    main() 