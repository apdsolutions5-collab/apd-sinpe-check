import os
import pytesseract
from PIL import Image

# Configuración de la ruta por defecto de Tesseract en Windows
ruta_tesseract_default = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
if os.path.exists(ruta_tesseract_default):
    pytesseract.pytesseract.tesseract_cmd = ruta_tesseract_default

def extraer_texto_de_imagen(imagen_procesada: Image.Image) -> str:
    """
    Recibe un objeto de imagen (PIL Image) procesado y extrae el texto usando Tesseract OCR en idioma español ('spa').
    """
    try:
        # Extracción utilizando el paquete de idioma español ('spa')
        texto = pytesseract.image_to_string(imagen_procesada, lang='spa')
        return texto.strip()
    except Exception as e:
        print(f"Error al ejecutar Tesseract OCR: {e}")
        return ""

if __name__ == "__main__":
    print("Módulo ocr_engine configurado con pytesseract (lang='spa').")