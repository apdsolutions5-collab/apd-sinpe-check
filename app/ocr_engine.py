import os
import re
import pytesseract
from PIL import Image

# Configuración de ruta por defecto de Tesseract en Windows
ruta_tesseract_default = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
if os.path.exists(ruta_tesseract_default):
    pytesseract.pytesseract.tesseract_cmd = ruta_tesseract_default


def extraer_texto_de_imagen(imagen_procesada: Image.Image) -> str:
    """Extrae el texto mediante Tesseract OCR (idioma 'spa')."""
    try:
        texto = pytesseract.image_to_string(imagen_procesada, lang='spa')
        return texto.strip()
    except Exception as e:
        print(f"❌ Error en Tesseract OCR: {e}")
        return ""


def obtener_confianza_ocr(imagen_procesada: Image.Image) -> float:
    """Calcula el porcentaje de confianza promedio del texto detectado por Tesseract OCR."""
    try:
        datos = pytesseract.image_to_data(imagen_procesada, lang='spa', output_type=pytesseract.Output.DICT)
        confiabilidades = [int(conf) for conf in datos['conf'] if int(conf) > -1]
        
        if confiabilidades:
            promedio = sum(confiabilidades) / len(confiabilidades)
            return round(promedio, 2)
        return 0.0
    except Exception as e:
        print(f"❌ Error al obtener confianza de Tesseract OCR: {e}")
        return 0.0


def detectar_moneda_y_monto(texto_ocr: str) -> dict:
    """Detecta el monto y la moneda priorizando patrones con Colones, comas/puntos y etiquetas."""

    # 1. Patrón Cripto / Bitcoin
    patron_btc = r'(?:BTC|Bitcoin|sats|satoshis)\s*[:\.]?\s*(\d+(?:[\.,]\d+)?)|(\d+(?:[\.,]\d+)?)\s*(?:BTC|sats)'
    match_btc = re.search(patron_btc, texto_ocr, re.IGNORECASE)
    if match_btc:
        monto_val = match_btc.group(1) or match_btc.group(2)
        return {"monto_raw": monto_val, "monto_formateado": f"₿ {monto_val}", "moneda": "BTC"}

    # 2. Patrón Dólares (USD)
    patron_usd = r'(?:\$|USD|Dólares|Dolares)\s*[:\.]?\s*(\d{1,3}(?:[,\.]\d{3})*(?:[\.,]\d{2})?)'
    match_usd = re.search(patron_usd, texto_ocr, re.IGNORECASE)
    if match_usd and '$' in texto_ocr:
        monto_val = match_usd.group(1)
        return {"monto_raw": monto_val, "monto_formateado": f"$ {monto_val}", "moneda": "USD"}

    # 3. Colones (CRC)
    
    # Capa A: Monto seguido de la palabra 'Colones' (Caso BN SINPE: "2.000,00 Colones")
    patron_colones_post = r'(\d{1,3}(?:[\.,]\d{3})*(?:[\.,]\d{2}))\s*Colones'
    match_colones_post = re.search(patron_colones_post, texto_ocr, re.IGNORECASE)
    if match_colones_post:
        monto_val = match_colones_post.group(1).strip()
        return {"monto_raw": monto_val, "monto_formateado": f"₡ {monto_val}", "moneda": "CRC"}

    # Capa B: Etiqueta 'Monto' seguida de un número financiero (Caso BAC)
    patron_monto_etiqueta = (
        r'(?:Monto|Monto\s*Transferido|Monto\s*debitado|Monto\s*acreditado|Monto\s*transferencia)'
        r'\s*[:\.]?\s*[^0-9\n\r]*\s*(\d{1,3}(?:[,\.]\d{3})*(?:[\.,]\d{2})?)'
    )
    match_etiqueta = re.search(patron_monto_etiqueta, texto_ocr, re.IGNORECASE)
    if match_etiqueta:
        monto_val = match_etiqueta.group(1).strip()
        return {"monto_raw": monto_val, "monto_formateado": f"₡ {monto_val}", "moneda": "CRC"}

    # Capa C: Símbolo explícito de colón
    patron_simbolo = r'[\$£¢€₡]\s*(\d{1,3}(?:[,\.]\d{3})*(?:[\.,]\d{2})?)'
    match_simbolo = re.search(patron_simbolo, texto_ocr)
    if match_simbolo:
        monto_val = match_simbolo.group(1).strip()
        return {"monto_raw": monto_val, "monto_formateado": f"₡ {monto_val}", "moneda": "CRC"}

    return {"monto_raw": None, "monto_formateado": None, "moneda": "DESCONOCIDO"}


def extraer_campos_sinpe(texto_ocr: str) -> dict:
    """Extrae y estandariza comprobante, fecha, hora, teléfono y monto."""

    # 1. Comprobante / Referencia
    patron_comprobante = (
        r'(?:Número\s*de\s*(?:transacción|comprobante|referencia)|Comprobante|Referencia|FT)\s*[:\.]?\s*([A-Z0-9]{8,28})'
        r'|(\d{20,28})\s*(?:\n|\r\n)?\s*Comprobante'
    )
    match_comp = re.search(patron_comprobante, texto_ocr, re.IGNORECASE)
    comprobante = None
    if match_comp:
        comprobante = match_comp.group(1) or match_comp.group(2)

    # 2. Fecha
    patron_fecha = (
        r'(\d{2}[/\.-]\d{2}[/\.-]\d{2,4})'
        r'|(\d{1,2}\s+de\s+[a-zA-Z]+\s+de\s+\d{4})'
        r'|(\d{1,2}\s+[a-zA-Z]+\s+\d{4})'
    )
    match_fecha = re.search(patron_fecha, texto_ocr, re.IGNORECASE)
    fecha = None
    if match_fecha:
        fecha_raw = match_fecha.group(1) or match_fecha.group(2) or match_fecha.group(3)
        fecha = " ".join(fecha_raw.split())

    # 3. Hora (Formato 12h y 24h)
    patron_hora = r'(\d{1,2}:\d{2}(?::\d{2})?\s*(?:am|pm|AM|PM)?)'
    matches_hora = re.findall(patron_hora, texto_ocr)
    hora = None
    if matches_hora:
        for h in matches_hora:
            if re.search(r'(?:am|pm)', h, re.IGNORECASE):
                hora = h.strip()
                break
        if not hora and len(matches_hora) > 0:
            hora = matches_hora[0].strip()

    # 4. Teléfono (Busca números de 8 dígitos de CR)
    patron_telefono = (
        r'(?:teléfono|tel|monedero|destino|origen|hacia|desde)\s*(?:nº|n°|n)?\s*[:\.]?\s*([5678]\d{7})'
        r'|([5678]\d{7})\s*(?:\n|\r\n|\s)*(?:número\s*de\s*monedero|teléfono|tel)'
        r'|al\s+teléfono\s+Nº\s*([5678]\d{7})'
    )
    match_tel = re.search(patron_telefono, texto_ocr, re.IGNORECASE)
    telefono = None
    if match_tel:
        telefono = match_tel.group(1) or match_tel.group(2) or match_tel.group(3)

    # 5. Datos de Monto y Moneda
    datos_moneda = detectar_moneda_y_monto(texto_ocr)

    return {
        "numero_comprobante": comprobante,
        "fecha_pago": fecha,
        "hora_pago": hora,
        "telefono_origen": telefono,
        "monto": datos_moneda["monto_formateado"],
        "moneda": datos_moneda["moneda"],
        "monto_numerico": datos_moneda["monto_raw"],
    }


if __name__ == "__main__":
    print("Módulo ocr_engine optimizado.")