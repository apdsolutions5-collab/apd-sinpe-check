from PIL import Image, ImageOps, ImageEnhance

def limpiar_texto(texto):
    """Limpia el texto básico para buscar palabras clave."""
    if not texto:
        return ""
    return texto.lower().strip()

def preprocesar_imagen(ruta_imagen):
    """
    Aplica filtros básicos con Pillow a la imagen del comprobante:
    1. Convierte a escala de grises.
    2. Ajusta el contraste.
    3. Aplica binarización (blanco y negro puro).
    """
    # Abrir imagen o ruta 
    img = Image.open(ruta_imagen)
    
    # Convertir a escala de grises
    img_gris = ImageOps.grayscale(img)
    
    # Ajustar el contraste
    enhancer = ImageEnhance.Contrast(img_gris)
    img_contraste = enhancer.enhance(2.0)
    
    # Binarización
    img_binaria = img_contraste.point(lambda p: 255 if p > 128 else 0)
    
    return img_binaria

def guardar_imagen_procesada(img, ruta_destino):
    """Guarda la imagen en la ruta especificada"""
    img.save(ruta_destino)

def obtener_tamano_imagen(ruta_imagen):
    """Devuelve las dimensiones de la imagen."""
    with Image.open(ruta_imagen) as img:
        return img.size