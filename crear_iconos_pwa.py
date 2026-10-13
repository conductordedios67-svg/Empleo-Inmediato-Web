
from pathlib import Path
from PIL import Image, ImageDraw

CARPETA = Path("pwa/icons")
CARPETA.mkdir(parents=True, exist_ok=True)

TAMAnOS = [72, 96, 144, 192, 512]

for tamano in TAMAnOS:
    imagen = Image.new("RGB", (tamano, tamano), "#1565C0")
    dibujo = ImageDraw.Draw(imagen)

    # Maletín blanco
    escala = tamano / 512
    x1, y1 = int(100 * escala), int(190 * escala)
    x2, y2 = int(412 * escala), int(390 * escala)
    grosor = max(2, int(18 * escala))

    dibujo.rounded_rectangle(
        (x1, y1, x2, y2),
        radius=int(28 * escala),
        fill="white"
    )

    # Asa del maletín
    ax1, ay1 = int(190 * escala), int(130 * escala)
    ax2, ay2 = int(322 * escala), int(220 * escala)

    dibujo.rounded_rectangle(
        (ax1, ay1, ax2, ay2),
        radius=int(18 * escala),
        outline="white",
        width=grosor
    )

    # Franja azul sobre el maletín
    dibujo.rectangle(
        (x1, int(265 * escala), x2, int(305 * escala)),
        fill="#1565C0"
    )

    # Cierre central
    dibujo.rectangle(
        (
            int(235 * escala),
            int(265 * escala),
            int(277 * escala),
            int(305 * escala)
        ),
        fill="white"
    )

    ruta = CARPETA / f"icon-{tamano}.png"
    imagen.save(ruta, format="PNG")
    print(f"Icono creado: {ruta}")

print("Proceso terminado.")
