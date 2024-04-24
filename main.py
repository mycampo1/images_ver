import os
import pytesseract
import re
from pdf2image import convert_from_path
from PIL import Image, ImageFilter, ImageEnhance

# Ruta al ejecutable de Tesseract (ajusta esto según tu instalación)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Ruta a la carpeta que contiene los archivos PDF
pdf_folder = "C:/Users/Marlon Campo/Downloads/EXONERACIONES/2022"

# Función para procesar una página de PDF
def process_pdf_page(pdf_image, pdf_path, page_number):
    # Convertir la imagen PDF a una imagen PIL
    pil_image = pdf_image.convert("RGB")

    # Aplicar filtros y técnicas de mejora de imagen
    filtered_image = pil_image.filter(ImageFilter.MedianFilter(size=3))
    enhanced_image = ImageEnhance.Contrast(filtered_image).enhance(1.5)

    # Aplicar OCR a la imagen mejorada
    page_text = pytesseract.image_to_string(enhanced_image)

    # Buscar el código estudiantil y el número de resolución
    codigo_estudiantil_match = re.search(r"código estudiantil:\s*(\d+)", page_text, re.IGNORECASE)
    numero_resolucion_match = re.search(r"RESOLUCIÓN No\. (\d+)", page_text, re.IGNORECASE)

    if codigo_estudiantil_match and numero_resolucion_match:
        codigo_estudiantil = codigo_estudiantil_match.group(1)
        numero_resolucion = numero_resolucion_match.group(1)

        # Construir el nuevo nombre del archivo
        new_pdf_name = f"{codigo_estudiantil}_{numero_resolucion}_promedio.pdf"
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
