# Superpersonalizado — Catálogo Web 3D & Corte Láser

Experiencia web interactiva 3D/WebGL desarrollada para **Superpersonalizado**, marca especializada en arte, figuras y piezas multicapa personalizadas cortadas en madera con tecnología láser de alta precisión.

![Three.js](https://img.shields.io/badge/Three.js-0.160.0-black?style=for-the-badge&logo=three.js)
![WebGL](https://img.shields.io/badge/WebGL-2.0-red?style=for-the-badge&logo=webgl)
![HTML5](https://img.shields.io/badge/HTML5-CSS3-orange?style=for-the-badge&logo=html5)
![WhatsApp](https://img.shields.io/badge/WhatsApp-Contact-25D366?style=for-the-badge&logo=whatsapp)

---

## 🌟 Características Principales

1. **Modelos 3D y Texturas de Madera en Tiempo Real:**
   - Placas de madera con relieve tridimensional, biselado suave perimetral (*chamfer edge*) y doble cara sellada.
   - Texturas generadas mediante canvas procedural con acabado satinado (`MeshPhysicalMaterial`, `clearcoat: 0.45` y `RoomEnvironment`).
   - Cara trasera con certificado de autenticidad, especificaciones técnicas de corte láser CNC ($\pm 0.1\text{ mm}$), código de barras y certificación FSC.

2. **Sección 1 — Hero Carousel (`#flavors`):**
   - 5 modelos estrella en órbita tridimensional (*Lobo Multicapa, Escudo Real Madrid, Rueda Romance, Tigre Vertical y Portamedallas*).
   - Control por arrastre con inercia física (*flick snap*), selector táctil/ratón, botón de avance y Autoplay inteligente.
   - Revelación circular de color de fondo y tipografía animada (*Archivo Black*).

3. **Sección 2 — Anatomía y Corte Láser (`#inside`):**
   - Transición fijada (*sticky pin* de 500vh): la pieza seleccionada viaja y ocupa el centro de la escena.
   - Giro dinámico de 4 fases:
     - **Paso 01:** Diseño & Vectorización (0° frontal).
     - **Paso 02:** Corte Láser Multicapa (180° reverso con ficha técnica).
     - **Paso 03:** Acabado a Mano y Sellado (360° frontal).
     - **Paso 04:** Presentación de la Pieza Maestra (720° giro completo).
   - Tormenta de virutas (*Wood Storm*): explosión radial de 20 astillas y virutas de madera en 3D hacia el catálogo.

4. **Sección 3 — Catálogo Exclusivo (`#shop`):**
   - Aterrizaje del *Traveler*: la pieza 3D se ancla con precisión dentro de su tarjeta.
   - Tarjetas con efecto Tilt 3D según el cursor.
   - Botón directo de **Pedir por WhatsApp** con mensaje preconfigurado por producto.
   - Botón `+` para añadir al carrito con animación de vuelo curvo en 3D hacia el navbar.

5. **Sección 4 — Personalizador de Pack 3 Piezas (`#range`):**
   - Selector interactivo de 3 ranuras con iluminación ambiental de madera.
   - Miniaturas con contador en vivo y botón para cotizar y pedir el pack con 15% de descuento vía WhatsApp.

6. **Integración con WhatsApp:**
   - Botón destacado en barra de navegación y botón flotante permanente en toda la web conectado a WhatsApp oficial (+58 412-7588395).

---

## 🚀 Despliegue Local

1. Clona el repositorio:
   ```bash
   git clone https://github.com/m3ruc01/personalizado.git
   ```
2. Coloca los archivos en la carpeta de tu servidor web (ej. XAMPP `htdocs/catalogo_productos_maderas` o servidor HTTP con Python/Node):
   ```bash
   # Opción servidor Python directo:
   cd public
   python -m http.server 8000
   ```
3. Abre en tu navegador:
   `http://localhost:8000/index.html` (o `http://localhost/catalogo_productos_maderas/public/index.html` en XAMPP).

---

## 🛠️ Tecnologías

- **Three.js (0.160.0)** & **RoomEnvironment**
- **JavaScript (ES Modules)**
- **CSS3 Moderno** (CSS Variables, Flexbox, Clamp, Backdrop Filter)
- **Google Fonts:** Archivo Black, Inter, DM Mono
