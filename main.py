import cv2

from pyzbar.pyzbar import decode

def read_barcode(image_path):
    # Leer la imagen
    image = cv2.imread(image_path)
    
    # Decodificar el código de barras
    decoded_objects = decode(image)
    
    # Mostrar resultados
    for obj in decoded_objects:
        barcode_type = obj.type
        barcode_data = obj.data.decode("utf-8")
        print("Tipo de código de barras:", barcode_type)
        print("Datos del código de barras:", barcode_data)

# Ruta de la imagen con el código de barras
image_path = "./img/codigo_test.png"

# Llamar a la función para leer el código de barras
# read_barcode(image_path)

from datetime import datetime
import barcode
from barcode.writer import ImageWriter

def generate_barcode(product_name, entry_date):
    # Concatenar el nombre del producto y la fecha de ingreso para obtener un código único
    code_data = f"{product_name}_{entry_date.strftime('%Y%m%d')}"
    
    # Crear un objeto de código de barras
    barcode_class = barcode.get_barcode_class('code128')
    barcode_instance = barcode_class(code_data, writer=ImageWriter())
    
    # Guardar el código de barras como una imagen
    filename = barcode_instance.save('barcode')
    
    return filename

# Nombre del producto
product_name = "Producto1"

# Fecha de ingreso a la bodega
entry_date = datetime.now()

# Generar el código de barras
barcode_filename = generate_barcode("leche", entry_date)

print("Código de barras generado:", barcode_filename)