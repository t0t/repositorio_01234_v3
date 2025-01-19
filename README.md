# BRUTAL_DATABASE

Una aplicación web Flask con diseño brutalista y tropical que explora temas metafísicos y filosóficos. La aplicación presenta una interfaz única que combina elementos retro-digitales con efectos glitch y una estética tropical.

![BRUTAL_DATABASE Screenshot](static/images/screenshot.png)

## 🌴 Características

- **Diseño Brutalista**: Interfaz minimalista y directa con efectos glitch
- **Navegación Intuitiva**: Menú principal fijo y navegación entre entradas
- **Visualización de Datos**: Presentación de entradas en un grid responsive
- **Efectos Visuales**: Animaciones glitch, efectos de hover y transiciones
- **Páginas Especiales**: 
  - HOME: Grid principal de entradas
  - ABOUT: Información sobre el proyecto
  - ARCHIVE: Búsqueda y filtrado de entradas
  - VOID: Experiencia interactiva especial

## 🚀 Tecnologías

- **Backend**: Flask (Python)
- **Frontend**: HTML5, TailwindCSS, JavaScript
- **Fuentes**: Google Fonts (Space Mono, Press Start 2P, etc.)
- **Almacenamiento**: JSON local
- **Efectos**: CSS3 Animations y Transitions

## 💻 Requisitos

- Python 3.8+
- Flask
- Navegador web moderno con soporte para CSS Grid y Flexbox

## 📦 Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/brutal-database.git
cd brutal-database
```

2. Crea un entorno virtual e instala las dependencias:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Inicia el servidor:
```bash
python app.py
```

4. Abre tu navegador en `http://localhost:5005`

## 🗂 Estructura del Proyecto

```
brutal-database/
├── app.py                 # Aplicación Flask principal
├── database.json         # Base de datos de entradas
├── requirements.txt      # Dependencias del proyecto
├── static/
│   ├── css/             # Estilos CSS
│   ├── js/              # Scripts JavaScript
│   └── images/          # Imágenes y media
└── templates/
    ├── base.html        # Template base
    ├── index.html       # Página principal
    ├── entry.html       # Página de entrada individual
    ├── about.html       # Página Acerca de
    ├── archive.html     # Archivo y búsqueda
    └── void.html        # Experiencia VOID
```

## 🎨 Personalización

### Añadir Nuevas Entradas

1. Edita `database.json`:
```json
{
  "id": 1,
  "type": "thought_fragment",
  "content": "Tu contenido aquí",
  "media": "/static/images/tu-imagen.jpg",
  "tags": ["tag1", "tag2"]
}
```

### Modificar Estilos

Los estilos principales se encuentran en:
- `static/css/main.css`
- Templates individuales (estilos específicos)
- TailwindCSS (clases utilitarias)

## 📱 Responsive Design

La aplicación es completamente responsive:
- Mobile: 1 columna
- Tablet: 2 columnas
- Desktop: 3 columnas + menú lateral

## 🌐 Deploy

### GitHub Pages (Frontend Estático)

1. Crea un nuevo repositorio en GitHub
2. Inicializa git y sube los cambios:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/tu-usuario/brutal-database.git
git push -u origin main
```

### Heroku (Aplicación Completa)

1. Crea una cuenta en Heroku
2. Instala Heroku CLI
3. Crea una nueva aplicación:
```bash
heroku create brutal-database
git push heroku main
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE.md](LICENSE.md) para más detalles.

## 🙏 Agradecimientos

- Inspirado en el diseño web brutalista
- Efectos glitch basados en técnicas de CSS moderno
- Comunidad Flask por su documentación y recursos
# repositorio_01234_v3
