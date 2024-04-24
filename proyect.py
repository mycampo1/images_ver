import os
import pytesseract
import re
from pdf2image import convert_from_path
from PIL import Image, ImageFilter, ImageEnhance

# Ruta al ejecutable de Tesseract (ajusta esto según tu instalación)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Ruta a la carpeta que contiene los archivos PDF
pdf_folder = "C:/Users/Marlon Campo/Downloads/DRIVE NUEVO/ACTAS 2023-1/2023-1"

# Definir la expresión regular para buscar el patrón y los números
pattern = r"8\.1\.2[-/]?(?:-1)?/(\d+)"

# Diccionario para realizar un seguimiento de los números
number_counts = {}

# Función para procesar una página de PDF
def process_pdf_page(pdf_image, pdf_path, page_number):
    # Convertir la imagen PDF a una imagen PIL
    pil_image = pdf_image.convert("RGB")

    # Aplicar filtros y técnicas de mejora de imagen
    filtered_image = pil_image.filter(ImageFilter.MedianFilter(size=3))
    enhanced_image = ImageEnhance.Contrast(filtered_image).enhance(1.5)

    # Guardar la imagen mejorada (opcional, solo para visualización)
    enhanced_image.save(f"enhanced_page_{page_number}.jpg")

    # Aplicar OCR a la imagen mejorada
    page_text = pytesseract.image_to_string(enhanced_image)

    # Buscar el patrón y extraer los números usando expresiones regulares
    match = re.search(pattern, page_text)
    if match:
        extracted_number = match.group(1)

        # Verificar si el número ya existe en el diccionario y agregar sufijo si es necesario
        if extracted_number in number_counts:
            number_counts[extracted_number] += 1
            new_pdf_name = f"{extracted_number}-{number_counts[extracted_number]}.pdf"
        else:
            number_counts[extracted_number] = 1
            new_pdf_name = f"{extracted_number}.pdf"

        new_pdf_path = os.path.join(pdf_folder, new_pdf_name)

        # Renombrar el archivo
        os.rename(pdf_path, new_pdf_path)

        print(f"Renamed {pdf_file} to {new_pdf_name} (Page {page_number})")

# Procesar cada archivo PDF
for pdf_file in os.listdir(pdf_folder):
    if pdf_file.lower().endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, pdf_file)

        # Convertir las páginas del PDF en imágenes con resolución reducida
        pdf_images = convert_from_path(pdf_path, dpi=150)  # Ajusta la resolución según tu necesidad

        # Procesar cada imagen (página) del PDF
        for page_number, pdf_image in enumerate(pdf_images, start=1):
            process_pdf_page(pdf_image, pdf_path, page_number)

