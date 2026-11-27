import urllib.request
import os

images = {
    "lobo.webp": "https://superpersonalizado.com/uploads/productos/_w700/33_wallart-lobo-multicapa.webp",
    "realmadrid.webp": "https://superpersonalizado.com/uploads/productos/_w700/740_wall-art-escudo-real-madrid-con-banner_1_20260514111033.webp",
    "rueda.webp": "https://superpersonalizado.com/uploads/productos/_w700/22_rueda-de-la-fortuna-portafotos-corazones_1_20260512093355.webp",
    "tigre.webp": "https://superpersonalizado.com/uploads/productos/_w700/34_wallart-tigre-vertical-v3.webp",
    "portamedallas.webp": "https://superpersonalizado.com/uploads/productos/_w700/27_portamedallas-natacion-renata-paola.webp",
    "barcelona.webp": "https://superpersonalizado.com/uploads/productos/_w700/738_wall-art-escudo-fc-barcelona-en-madera_1_20260514111013.webp",
    "goku_vegeta.webp": "https://superpersonalizado.com/uploads/productos/_w700/37_wallart-vegeta-goku-diptico.webp",
    "mama.webp": "https://superpersonalizado.com/uploads/productos/_w700/30_marco-te-amo-mama-frontal.webp",
    "letrero_policia.webp": "https://superpersonalizado.com/uploads/productos/_w700/22_letrero-escritorio-inspector-jefe-policia.webp",
    "llavero.webp": "https://superpersonalizado.com/uploads/productos/_w700/18_llavero-arbol-de-la-vida-pila.webp",
    "logo.png": "https://superpersonalizado.com/uploads/sitio/logo_sin_icono.png"
}

out_dir = os.path.join("public", "assets", "images")
os.makedirs(out_dir, exist_ok=True)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

for filename, url in images.items():
    filepath = os.path.join(out_dir, filename)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            with open(filepath, "wb") as f:
                f.write(data)
            print(f"Downloaded {filename}: {len(data)} bytes")
    except Exception as e:
        print(f"Failed {filename} ({url}): {e}")
