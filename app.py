from flask import Flask, render_template, jsonify, request, send_from_directory, url_for, abort, redirect
from flask_assets import Environment, Bundle
from flask_caching import Cache
from flask_compress import Compress
import json
import os
from random import choice, sample
from datetime import datetime
import logging
from livereload import Server
from collections import Counter

# Configuración de logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['CACHE_TYPE'] = 'simple'
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Configuración de compresión
Compress(app)

# Configuración de caché
cache = Cache(app)

# Configuración de assets
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('css/main.scss', filters='scss', output='css/main.css')
assets.register('scss_all', scss)

js = Bundle('js/main.js', filters='jsmin', output='js/bundle.js')
assets.register('js_all', js)

def fix_image_path(path):
    """Corrige la ruta de la imagen para que sea válida."""
    logger.debug(f"Procesando ruta de imagen: {path}")
    
    if not path:
        return ''
        
    if path.startswith(('http://', 'https://')):
        return path

    # Si la ruta comienza con /static/, eliminar /static/ ya que url_for lo añadirá
    if path.startswith('/static/'):
        path = path[7:]  # Eliminar '/static/'
    
    # Verificar si el archivo existe
    full_path = os.path.join(app.static_folder, path)
    logger.debug(f"Buscando archivo en: {full_path}")
    
    if os.path.exists(full_path):
        return url_for('static', filename=path)
    
    logger.warning(f"Imagen no encontrada: {path}")
    return ''

@app.template_filter('glitch_text')
def glitch_text_filter(text):
    """Añade caracteres glitch al texto."""
    glitch_chars = '̴̢̧̨̡̛̛͎̣̲̪̜̘̱̖̰͖̰̳͍̰̖̗̬̦̼̰̦̼͔̠̥̭̼͉̩͚̭̟̳̬͔̦͕͎͖̤͚̯̺̺͈̗̯̳̪̤͔̪̙̺̺͎̯̺̺̦̯͖̤͚̯̺̺͈̗̯̳̪̤͔̪̙̺̺͎̯̺̺̦̯'
    return f"{text}{choice(glitch_chars)}"

@app.template_filter('sample')
def sample_filter(seq, n=None):
    """Filter para obtener una muestra aleatoria de una secuencia."""
    if not seq:
        return []
    return sample(seq, min(n or len(seq), len(seq)))

@app.context_processor
def utility_processor():
    return dict(glitch_text=glitch_text_filter)

@app.context_processor
def inject_items():
    return {'items': load_database()}

@cache.cached(timeout=300)
def load_database():
    """Carga y cachea la base de datos."""
    try:
        database_path = os.path.join(os.path.dirname(__file__), 'database.json')
        logger.debug(f"Cargando base de datos desde: {database_path}")
        with open(database_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            logger.info(f"Base de datos cargada: {len(data)} elementos")
            return data
    except Exception as e:
        logger.error(f"Error al cargar la base de datos: {e}")
        return []

# Rutas principales
@app.route('/')
def index():
    """Vista principal."""
    items = load_database()
    hero_image = "/imagen-0115.webp"
    
    # Por defecto, mostrar los últimos 12 items
    items = sorted(items, key=lambda x: x.get('date', ''), reverse=True)[:12]
    
    return render_template('index.html', items=items, hero_image=hero_image)

@app.route('/about')
def about():
    """Página Acerca de con información del proyecto."""
    # Cargar imágenes específicas para la página About
    about_images = {
        'philosophy': '/static/images/optimized/imagen-0001.webp',
        'aesthetics': '/static/images/optimized/imagen-0002.webp',
        'purpose': '/static/images/optimized/imagen-0003.webp',
        'manifesto': '/static/images/optimized/imagen-0004.webp'
    }
    
    return render_template('about.html', images=about_images)

@app.route('/archive')
def archive():
    """Página de archivo con búsqueda y filtrado."""
    items = load_database()
    tag_filter = request.args.get('tag')
    sort_by = request.args.get('sort', 'newest')
    
    # Obtener todos los tags únicos
    all_tags = set()
    for item in items:
        all_tags.update(item.get('tags', []))
    all_tags = sorted(list(all_tags))
    
    # Filtrar por tag si es necesario
    if tag_filter:
        items = [
            item for item in items 
            if tag_filter.lower() in [t.lower() for t in item['tags']]
        ]
        
    # Ordenar items
    if sort_by == 'oldest':
        items = sorted(items, key=lambda x: x.get('date', ''))
    else:  # newest por defecto
        items = sorted(items, key=lambda x: x.get('date', ''), reverse=True)
            
    return render_template('archive.html', 
                         items=items,
                         all_tags=all_tags,
                         current_tag=tag_filter)

@app.route('/entry/<item_id>')
def show_entry(item_id):
    """Vista detallada de una entrada."""
    try:
        logger.debug(f"Mostrando entrada {item_id}")
        items = load_database()
        logger.debug(f"Base de datos cargada: {len(items)} items")
        
        # Encontrar el item actual y su índice
        current_index = None
        current_item = None
        for i, item in enumerate(items):
            if str(item['id']) == str(item_id):
                current_index = i
                current_item = item.copy()  # Hacer una copia para no modificar el original
                break
        
        if not current_item:
            logger.error(f"Item {item_id} no encontrado")
            abort(404)
            
        # Procesar imagen del item actual
        if 'media' in current_item:
            current_item['media'] = fix_image_path(current_item['media'])
            logger.debug(f"Imagen procesada para item actual: {current_item['media']}")
            
        # Obtener items anterior y siguiente
        prev_item = items[current_index - 1].copy() if current_index > 0 else None
        next_item = items[current_index + 1].copy() if current_index < len(items) - 1 else None
        
        # Procesar imágenes de items anterior y siguiente
        if prev_item and 'media' in prev_item:
            prev_item['media'] = fix_image_path(prev_item['media'])
        if next_item and 'media' in next_item:
            next_item['media'] = fix_image_path(next_item['media'])
        
        # Obtener items relacionados basados en tags comunes
        related_items = []
        current_tags = set(current_item['tags'])
        for item in items:
            if item['id'] != current_item['id']:
                item_tags = set(item['tags'])
                if len(current_tags & item_tags) > 0:  # Si hay tags en común
                    related_item = item.copy()
                    if 'media' in related_item:
                        related_item['media'] = fix_image_path(related_item['media'])
                    related_items.append(related_item)
        
        # Obtener tags populares
        all_tags = []
        for item in items:
            all_tags.extend(item['tags'])
        tag_counter = Counter(all_tags)
        popular_tags = [tag for tag, _ in tag_counter.most_common(10)]
        
        # Determinar si es una entrada de blog
        is_blog = 'blog' in [tag.lower() for tag in current_item['tags']]
        template = 'entry-blog.html' if is_blog else 'entry.html'
        
        logger.debug(f"Renderizando template {template}")
        return render_template(template,
                             item=current_item,
                             prev_item=prev_item,
                             next_item=next_item,
                             related_items=related_items[:6],  # Limitar a 6 items relacionados
                             popular_tags=popular_tags)
    except Exception as e:
        logger.error(f"Error en show_entry: {e}", exc_info=True)
        return render_template('500.html'), 500

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    if not query:
        return redirect(url_for('index'))
    
    # Buscar en items
    items = load_database()
    results = []
    for item in items:
        # Buscar en título
        if query in item['type'].lower():
            results.append(item)
            continue
            
        # Buscar en contenido
        if query in item['content'].lower():
            results.append(item)
            continue
            
        # Buscar en tags
        if any(query in tag.lower() for tag in item['tags']):
            results.append(item)
            continue
    
    return render_template('archive.html', 
                         items=results, 
                         search_query=query)

@app.route('/blog')
def blog():
    """Vista del blog con estilo New Age de los 60s."""
    try:
        logger.debug("Iniciando vista del blog")
        items = load_database()
        logger.debug(f"Items cargados: {len(items)}")
        
        # Procesar items para el blog
        blog_items = []
        for item in items:
            try:
                logger.debug(f"Procesando item {item.get('id', 'unknown')}")
                # Crear una versión más espiritual del contenido
                spiritual_content = f"En la búsqueda de la verdad digital, {item.get('content', '').lower()}. " \
                                  f"A través de la expansión de la consciencia tecnológica, " \
                                  f"exploramos nuevas dimensiones de {', '.join(item.get('tags', []))}."
                
                # Añadir elementos new age a los tags
                new_age_tags = item.get('tags', []) + ['cosmic', 'consciousness', 'digital_spirit']
                
                # Procesar la ruta de la imagen si existe
                media = fix_image_path(item.get('media')) if 'media' in item else None
                
                # Asegurarse de que la imagen existe
                if media:
                    logger.debug(f"Imagen procesada para blog: {media}")
                
                blog_item = {
                    'id': item.get('id'),
                    'type': f" {item.get('type', 'Unknown')} ",
                    'content': spiritual_content,
                    'tags': new_age_tags,
                    'media': media
                }
                blog_items.append(blog_item)
                logger.debug(f"Item {item.get('id', 'unknown')} procesado correctamente")
            except Exception as item_error:
                logger.error(f"Error procesando item {item.get('id', 'unknown')}: {item_error}")
                continue
            
        logger.debug(f"Total de items procesados: {len(blog_items)}")
        return render_template('blog.html', items=blog_items)
    except Exception as e:
        logger.error(f"Error en blog: {e}", exc_info=True)
        return render_template('500.html'), 500

@app.route('/manifest')
def manifest():
    """Página del manifiesto."""
    return render_template('manifest.html', image='/static/images/optimized/imagen-0005.webp')

@app.route('/contact')
def contact():
    """Página de contacto."""
    return render_template('contact.html', image='/static/images/optimized/imagen-0006.webp')

@app.route('/void')
def void():
    """Página del void con efectos especiales."""
    void_images = [
        '/static/images/optimized/imagen-0007.webp',
        '/static/images/optimized/imagen-0008.webp',
        '/static/images/optimized/imagen-0009.webp'
    ]
    return render_template('void.html', images=void_images)

# Páginas de error
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    if app.debug:
        # Crear servidor LiveReload
        server = Server(app.wsgi_app)
        # Observar archivos para recargar automáticamente
        server.watch('static/')
        server.watch('templates/')
        server.watch('*.py')
        server.serve(port=5000)
    else:
        app.run(port=5000)
