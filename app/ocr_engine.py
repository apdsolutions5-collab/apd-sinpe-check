import os
import re
import pytesseract
from PIL import Image

# Configuración de la ruta por defecto de Tesseract en Windows
ruta_tesseract_default = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
if os.path.exists(ruta_tesseract_default):
    pytesseract.pytesseract.tesseract_cmd = ruta_tesseract_default

def extraer_texto_de_imagen(imagen_procesada: Image.Image) -> str:
    """
    [KAN-25] Recibe un objeto de imagen (PIL Image) procesado y extrae 
    el texto usando Tesseract OCR configurado en idioma español ('spa').
    """
    try:
        texto = pytesseract.image_to_string(imagen_procesada, lang='spa')
        return texto.strip()
    except Exception as e:
        print(f"Error al ejecutar Tesseract OCR: {e}")
        return ""

def extraer_campos_sinpe(texto_ocr: str) -> dict:
    """
    [KAN-26] Aplica Expresiones Regulares (Regex) sobre el texto extraído por el OCR 
    para aislar limpiamente los 4 campos obligatorios de comprobantes SINPE Móvil:
    - Número de comprobante o referencia
    - Fecha y hora del pago
    - Teléfono de origen
    - Monto de la transacción estandarizado en colones (₡)
    """
    # 1. Patrón Regex para Número de comprobante / Referencia
    patron_comprobante = r'(?:Número\s*de\s*transacción|Comprobante|Referencia|FT)\s*[:\.]?\s*([A-Z0-9]{6,20})'
    
    # 2. Patrón Regex para Fecha del pago
    patron_fecha = r'(\d{2}/\d{2}/\d{4}(?:\s+\d{2}:\d{2}:\d{2}\s*(?:am|pm|AM|PM)?)?)'

    # 3. Patrón Regex para Teléfono origen
    patron_telefono = r'(?:Teléfono|Tel|Desde)\s*[:\.]?\s*(\d{8})'

    # 4. Patrón Regex para Monto
    patron_monto = r'(?:Monto|Monto\s*Transferido)\s*[:\.]?\s*[\$£¢€₡E]?\s*(\d{1,3}(?:[,\.]\d{3})*(?:[\.,]\d{2})?)'

    # Búsquedas utilizando los patrones Regex
    match_comprobante = re.search(patron_comprobante, texto_ocr, re.IGNORECASE)
    match_fecha = re.search(patron_fecha, texto_ocr)
    match_telefono = re.search(patron_telefono, texto_ocr, re.IGNORECASE)
    match_monto = re.search(patron_monto, texto_ocr, re.IGNORECASE)

    # Formatear el monto asegurando el símbolo de Colones (₡)
    monto_limpio = None
    if match_monto:
        monto_extraido = match_monto.group(1).replace(',', '.').strip()
        monto_limpio = f"₡ {monto_extraido}"

    return {
        "numero_comprobante": match_comprobante.group(1) if match_comprobante else None,
        "fecha_pago": match_fecha.group(1) if match_fecha else None,
        "telefono_origen": match_telefono.group(1) if match_telefono else None,
        "monto": monto_limpio
    }

if __name__ == "__main__":
    print("Módulo ocr_engine listo.")