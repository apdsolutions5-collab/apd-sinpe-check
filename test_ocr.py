import os
from app.utils import preprocesar_imagen
from app.ocr_engine import extraer_texto_de_imagen, extraer_campos_sinpe

carpeta = "test_images"
imagenes = [f for f in os.listdir(carpeta) if f.endswith(('.jpg', '.jpeg', '.png')) and f != "resultado_binario.png"]

if imagenes:
    ruta = os.path.join(carpeta, imagenes[0])
    print(f"Procesando imagen: {ruta}\n")
    
    # 1. Preprocesar e Imagen a texto
    img_limpia = preprocesar_imagen(ruta)
    texto = extraer_texto_de_imagen(img_limpia)
    
    # 2. Extraer campos con Regex
    campos = extraer_campos_sinpe(texto)
    
    print("--- CAMPOS EXTRAÍDOS CON REGEX (KAN-26) ---")
    for clave, valor in campos.items():
        print(f"{clave}: {valor}")
    print("-------------------------------------------")
else:
    print("No se encontraron imágenes en test_images/")