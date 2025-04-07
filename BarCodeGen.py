import os
import random
from barcode import EAN13
from barcode.writer import ImageWriter

# Carpeta donde se guardarán los códigos
carpeta_destino = r"C:\Users\T5809\BarcodesLyA"

# Crear la carpeta si no existe
os.makedirs(carpeta_destino, exist_ok=True)

# Generar 30 códigos de barra
for i in range(1, 31):
    # Generar número aleatorio de 12 dígitos (el 13° lo calcula EAN13)
    numero = ''.join([str(random.randint(0, 9)) for _ in range(12)])

    # Crear código de barras EAN13 con imagen PNG
    codigo = EAN13(numero, writer=ImageWriter())

    # Guardar en la carpeta especificada
    nombre_archivo = f"codigo_{i:02d}"
    ruta_completa = os.path.join(carpeta_destino, nombre_archivo)

    codigo.save(ruta_completa)

print("Códigos de barras generados y guardados en la carpeta:", carpeta_destino)
