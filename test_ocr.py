import os
from app.utils import preprocesar_imagen
from app.ocr_engine import extraer_texto_de_imagen, extraer_campos_sinpe

"""
Script de prueba masiva para validación en consola [KAN-27].
Procesa todas las imágenes recolectadas en la carpeta 'test_images/' 
y extrae los 4 campos obligatorios (Comprobante, Fecha, Teléfono, Monto).
"""

carpeta_imagenes = "test_images"

def probar_todas_las_imagenes():
    if not os.path.exists(carpeta_imagenes):
        print(f" La carpeta '{carpeta_imagenes}' no existe.")
        return

    # Filtrar solo imágenes válidas omitiendo archivos generados/temporales
    extensiones_validas = ('.jpg', '.jpeg', '.png')
    imagenes = [
        f for f in os.listdir(carpeta_imagenes) 
        if f.lower().endswith(extensiones_validas) and not f.startswith("resultado_")
    ]

    if not imagenes:
        print(f" No se encontraron imágenes en '{carpeta_imagenes}/'.")
        return

    print("==========================================================")
    print(f" INICIANDO PRUEBAS MASIVAS DE OCR Y REGEX (KAN-27)")
    print(f" Total de imágenes a procesar: {len(imagenes)}")
    print("==========================================================\n")

    for idx, archivo_imagen in enumerate(imagenes, start=1):
        ruta_completa = os.path.join(carpeta_imagenes, archivo_imagen)
        print(f" [Imagen {idx}/{len(imagenes)}]: {archivo_imagen}")
        
        try:
            # 1. Preprocesar la imagen
            imagen_limpia = preprocesar_imagen(ruta_completa)
            
            # 2. Extraer texto plano con OCR
            texto_extraido = extraer_texto_de_imagen(imagen_limpia)
            
            # 3. Extraer campos estructurados con Regex
            campos = extraer_campos_sinpe(texto_extraido)
            
            print("    Campos extraídos:")
            print(f"      • Comprobante : {campos['numero_comprobante']}")
            print(f"      • Fecha       : {campos['fecha_pago']}")
            print(f"      • Teléfono    : {campos['telefono_origen']}")
            print(f"      • Monto       : {campos['monto']}")
        except Exception as e:
            print(f"    Error al procesar la imagen: {e}")
            
        print("-" * 58)

    print("\n Pruebas finalizadas con éxito para todas las imágenes.")

if __name__ == "__main__":
    probar_todas_las_imagenes()