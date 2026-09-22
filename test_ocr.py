import os
from app.utils import preprocesar_imagen
from app.ocr_engine import extraer_texto_de_imagen

carpeta = "test_images"
imagenes = [f for f in os.listdir(carpeta) if f.endswith(('.jpg', '.jpeg', '.png')) and f != "resultado_binario.png"]

if imagenes:
    ruta = os.path.join(carpeta, imagenes[0])
    print(f"Procesando imagen: {ruta}")
    
    # 1. Preprocesa la imagen
    img_limpia = preprocesar_imagen(ruta)
    
    # 2. Extraer texto 
    texto = extraer_texto_de_imagen(img_limpia)
    
    print("\n--- TEXTO EXTRAÍDO CON ÉXITO (spa) ---")
    print(texto)
    print("---------------------------------------")
else:
    print("No se encontraron imágenes en test_images/")