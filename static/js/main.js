// Efectos glitch
function addGlitchEffect(element) {
    element.addEventListener('mouseover', () => {
        element.style.animation = 'none';
        element.offsetHeight; // Trigger reflow
        element.style.animation = 'glitch 0.3s infinite';
    });

    element.addEventListener('mouseout', () => {
        element.style.animation = 'none';
    });
}

// Aplicar efectos glitch a elementos con la clase .glitch
document.addEventListener('DOMContentLoaded', () => {
    const glitchElements = document.querySelectorAll('.glitch');
    glitchElements.forEach(addGlitchEffect);

    // Inicializar efectos de hover en la grid
    const gridItems = document.querySelectorAll('.grid-item');
    gridItems.forEach(item => {
        item.addEventListener('mouseover', () => {
            item.style.transform = 'scale(1.02) rotate(-1deg)';
        });

        item.addEventListener('mouseout', () => {
            item.style.transform = 'scale(1) rotate(0)';
        });
    });

    // Inicializar formularios si existen
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            // Aquí iría la lógica de envío del formulario
            console.log('Formulario enviado');
        });
    });

    // Efectos de partículas en la página void si existe
    const voidContainer = document.querySelector('.void-container');
    if (voidContainer) {
        createVoidParticles();
    }
});

// Función para crear partículas en la página void
function createVoidParticles() {
    const particles = document.getElementById('particles');
    const numParticles = 100;

    for (let i = 0; i < numParticles; i++) {
        const particle = document.createElement('div');
        particle.className = 'void-particle';
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.top = `${Math.random() * 100}%`;
        particle.style.animation = `voidFloat ${5 + Math.random() * 10}s infinite`;
        particles.appendChild(particle);
    }
}

// Función para mensajes aleatorios en void
function showRandomMessage() {
    const messages = [
        "El vacío te observa",
        "¿Existe el pensamiento sin el pensador?",
        "La nada es todo y el todo es nada",
        "Entre el ser y el no ser",
        "Fragmentos de consciencia"
    ];

    const message = document.createElement('div');
    message.className = 'void-message glitch-text';
    message.textContent = messages[Math.floor(Math.random() * messages.length)];
    message.style.left = `${Math.random() * 80 + 10}%`;
    message.style.top = `${Math.random() * 80 + 10}%`;
    
    document.querySelector('.void-container').appendChild(message);
    message.style.opacity = 1;
    
    setTimeout(() => {
        message.style.opacity = 0;
        setTimeout(() => message.remove(), 500);
    }, 2000);
}

// Función para búsqueda en tiempo real en el archivo
function searchArchive(query) {
    const items = document.querySelectorAll('.archive-item');
    items.forEach(item => {
        const title = item.querySelector('.archive-title').textContent.toLowerCase();
        const content = item.querySelector('p').textContent.toLowerCase();
        const searchQuery = query.toLowerCase();

        if (title.includes(searchQuery) || content.includes(searchQuery)) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
}

// Función para filtrar por tags en el archivo
function filterByTag(tag) {
    const items = document.querySelectorAll('.archive-item');
    items.forEach(item => {
        const tags = Array.from(item.querySelectorAll('.archive-tag'))
            .map(tag => tag.textContent.toLowerCase());

        if (tag === 'TODOS' || tags.includes(tag.toLowerCase())) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
}
