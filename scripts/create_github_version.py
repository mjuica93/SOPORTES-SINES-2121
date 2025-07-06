#!/usr/bin/env python3
"""
Script para actualizar el archivo HTML para usar URLs de GitHub
"""

import re

def update_html_for_github():
    """Actualiza el archivo HTML para usar URLs de GitHub en lugar de rutas locales"""
    
    # URL base de GitHub Raw
    GITHUB_BASE = "https://raw.githubusercontent.com/mjuica93/SOPORTES-SINES-2121/main"
    
    # Leer el archivo HTML original
    with open('index_isometricos_con_costuras.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Reemplazos de rutas usando template literals
    replacements = [
        # PDFs de estándares
        (r'href="ESTANDARES DE SOPORTES/\$\{([^}]+)\}"', rf'href="{GITHUB_BASE}/ESTANDARES%20DE%20SOPORTES/${{\\1}}"'),
        
        # PDFs de isométricos normales  
        (r'href="ISOMETRICOS/\$\{([^}]+)\}"', rf'href="{GITHUB_BASE}/ISOMETRICOS/${{\\1}}"'),
        
        # Archivos JSON de datos
        (r"fetch\('([^']+\.json)'\)", rf"fetch('{GITHUB_BASE}/\\1')"),
        
        # Rutas en el mapeo de prefabricados (sheet.prefab_path)
        (r'"normal_path": "ISOMETRICOS/', rf'"normal_path": "{GITHUB_BASE}/ISOMETRICOS/'),
        (r'"prefab_path": "ISOMETRICOS PREFABRICADOS/', rf'"prefab_path": "{GITHUB_BASE}/ISOMETRICOS%20PREFABRICADOS/'),
    ]
    
    # Aplicar reemplazos
    updated_content = html_content
    changes_count = 0
    
    for pattern, replacement in replacements:
        matches = re.findall(pattern, updated_content)
        if matches:
            print(f"🔍 Encontrados {len(matches)} patrones para: {pattern}")
            changes_count += len(matches)
        updated_content = re.sub(pattern, replacement, updated_content)
    
    # Reemplazo especial para las rutas de prefabricados en el JavaScript
    # Buscar y reemplazar ${sheet.prefab_path}
    prefab_pattern = r'href="\$\{([^}]*prefab_path[^}]*)\}"'
    prefab_matches = re.findall(prefab_pattern, updated_content)
    if prefab_matches:
        print(f"🔍 Encontradas {len(prefab_matches)} rutas de prefabricados")
        # Para estas dejamos que el JavaScript maneje la URL completa que ya estará en el JSON
    
    # Guardar el archivo actualizado
    with open('index_isometricos_github.html', 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("✅ Archivo HTML actualizado para GitHub creado: index_isometricos_github.html")
    print(f"🌐 URLs base configuradas para: {GITHUB_BASE}")
    print(f"📊 Total de cambios realizados: {changes_count}")
    
    # Verificar que se crearon enlaces a GitHub
    github_links = len(re.findall(r'github\.com', updated_content))
    print(f"🔗 Enlaces a GitHub en el archivo: {github_links}")

if __name__ == "__main__":
    update_html_for_github() 