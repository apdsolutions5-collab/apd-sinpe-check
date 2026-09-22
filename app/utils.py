from PIL import Image, ImageOps, ImageEnhance

def limpiar_texto(texto):
    """Limpia el texto básico para buscar palabras clave."""
    if not texto:
        return ""
    return texto.lower().strip()

def preprocesar_imagen(ruta_imagen):

   
    #Abrir imagen o ruta 
    img = Image.open(ruta_imagen)
    
    # 1. Escala de grises
    img_gris = ImageOps.grayscale(img)
    
    # 2. Ajuste de contraste
    enhancer = ImageEnhance.Contrast(img_gris)
    img_contraste = enhancer.enhance(2.0)
    
    # 3. Binarización a blanco y negro 
    img_binaria = img_contraste.point(lambda p: 255 if p > 128 else 0).convert('1')
    
    return img_binaria

def guardar_imagen_procesada(img, ruta_destino):
    """Guarda la imagen procesada en la ruta especificada."""
    img.save(ruta_destino)

def obtener_tamano_imagen(ruta_imagen):
    """Devuelve las dimensiones (ancho, alto) de la imagen."""
    with Image.open(ruta_imagen) as img:
        return img.size