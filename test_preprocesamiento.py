import os
from app.utils import preprocesar_imagen, guardar_imagen_procesada

# Seleccionar la primera imagen de test_images
carpeta = "test_images"
imagenes = [f for f in os.listdir(carpeta) if f.endswith(('.jpg', '.jpeg', '.png'))]

if imagenes:
    ruta_entrada = os.path.join(carpeta, imagenes[0])
    ruta_salida = os.path.join(carpeta, "resultado_binario.png")

    try:
        img_binaria = preprocesar_imagen(ruta_entrada)
        guardar_imagen_procesada(img_binaria, ruta_salida)
        
        print(" ¡Prueba exitosa!")
        print(f"Modo de imagen: {img_binaria.mode} (1 = blanco y negro puro)")
        print(f"Resultado guardado en: {ruta_salida}")
    except Exception as e:
        print(f" Error: {e}")
else:
    print(" No hay imágenes en test_images para probar.")