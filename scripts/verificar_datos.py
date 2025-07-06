#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar datos del sistema de isométricos
"""

import json

def verificar_datos():
    try:
        # Cargar datos
        with open('isometric_data_fixed.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print('✅ DATOS JSON VÁLIDOS')
        print('=' * 50)
        
        # Mostrar resumen
        summary = data.get('summary', {})
        print(f'📐 Total isométricos: {len(data.get("isometrics", {}))}')
        print(f'🔧 Isométricos con soportes: {summary.get("isometrics_with_supports", 0)}')
        print(f'📄 Isométricos con PDF normal: {summary.get("isometrics_with_normal_pdf", 0)}')
        print(f'🏗️  Isométricos con PDF prefab: {summary.get("isometrics_with_prefab_pdf", 0)}')
        print(f'📈 Total soportes: {summary.get("total_supports", 0)}')
        
        # Mostrar ejemplos
        isometrics = data.get('isometrics', {})
        if isometrics:
            print('\n📋 EJEMPLOS DE ISOMÉTRICOS:')
            count = 0
            for key, iso in isometrics.items():
                if count >= 5:
                    break
                supports_count = len(iso.get('supports', []))
                normal_pdf = iso.get('pdf_files', {}).get('normal')
                prefab_pdf = iso.get('pdf_files', {}).get('prefab')
                
                pdf_info = []
                if normal_pdf:
                    pdf_info.append('PDF Normal')
                if prefab_pdf:
                    pdf_info.append('PDF Prefab')
                
                pdf_str = f" ({', '.join(pdf_info)})" if pdf_info else " (Sin PDFs)"
                
                print(f'   - {key}: {iso.get("line", "N/A")} - Hoja {iso.get("sheet", "N/A")} '
                      f'({supports_count} soportes){pdf_str}')
                count += 1
        
        # Verificar estructura
        print('\n🔍 VERIFICACIÓN DE ESTRUCTURA:')
        
        # Contar isométricos con diferentes tipos de datos
        with_supports = 0
        with_normal_pdf = 0
        with_prefab_pdf = 0
        
        for iso in isometrics.values():
            if iso.get('supports'):
                with_supports += 1
            if iso.get('pdf_files', {}).get('normal'):
                with_normal_pdf += 1
            if iso.get('pdf_files', {}).get('prefab'):
                with_prefab_pdf += 1
        
        print(f'   ✅ Isométricos con soportes: {with_supports}')
        print(f'   ✅ Isométricos con PDF normal: {with_normal_pdf}')
        print(f'   ✅ Isométricos con PDF prefab: {with_prefab_pdf}')
        
        print('\n🎯 SISTEMA LISTO PARA USAR!')
        
    except FileNotFoundError:
        print('❌ Error: Archivo isometric_data_fixed.json no encontrado')
    except json.JSONDecodeError as e:
        print(f'❌ Error en JSON: {e}')
    except Exception as e:
        print(f'❌ Error inesperado: {e}')

if __name__ == "__main__":
    verificar_datos() 