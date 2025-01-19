import os
import json
from pathlib import Path

# Directorios y archivos
STATIC_DIR = Path(__file__).parent / 'static'
IMAGES_DIR = STATIC_DIR / 'images' / 'optimized'
DATABASE_FILE = Path(__file__).parent / 'database.json'

def rename_images():
    # Cargar la base de datos
    with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
        database = json.load(f)

    # Obtener lista de imágenes
    images = sorted([f for f in os.listdir(IMAGES_DIR) if f.endswith(('.webp', '.jpg', '.jpeg', '.png'))])
    
    # Diccionario para mantener el mapeo de nombres antiguos a nuevos
    name_mapping = {}
    
    # Renombrar imágenes
    for index, old_name in enumerate(images, 1):
        # Crear nuevo nombre
        extension = os.path.splitext(old_name)[1]
        new_name = f'imagen-{index:04d}{extension}'
        
        # Rutas completas
        old_path = IMAGES_DIR / old_name
        new_path = IMAGES_DIR / new_name
        
        # Renombrar archivo
        try:
            os.rename(old_path, new_path)
            name_mapping[old_name] = new_name
            print(f'Renombrado: {old_name} -> {new_name}')
        except Exception as e:
            print(f'Error al renombrar {old_name}: {e}')
    
    # Actualizar referencias en la base de datos
    for item in database:
        if 'media' in item and item['media']:
            old_name = os.path.basename(item['media'])
            if old_name in name_mapping:
                item['media'] = f'/static/images/optimized/{name_mapping[old_name]}'
    
    # Guardar base de datos actualizada
    with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=4, ensure_ascii=False)
    
    print('\nProceso completado.')
    print(f'Total de imágenes renombradas: {len(name_mapping)}')

if __name__ == '__main__':
    rename_images()
