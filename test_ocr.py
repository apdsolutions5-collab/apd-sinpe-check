import os
<<<<<<< HEAD
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
=======
import glob
from PIL import Image
from app.ocr_engine import extraer_texto_de_imagen, extraer_campos_sinpe

# ==========================================================
# 1. Ruta donde estan las imagenes 

DIRECTORIO_IMAGENES = "./test_images"  # Busca dentro de test_images

extensiones = ('*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG')
archivos_encontrados = []

for ext in extensiones:
    archivos_encontrados.extend(glob.glob(os.path.join(DIRECTORIO_IMAGENES, ext)))

# --- Filtros y Eliminacion de duplicados ---
archivos_filtrados = [
    f for f in archivos_encontrados 
    if not os.path.basename(f).startswith("resultado_")
]

imagenes_a_procesar = list(dict.fromkeys(archivos_filtrados))


# ==========================================================
# 2. Procesamiento y salida 

print("==========================================================")
print("🚀 MOTOR OCR MULTI-MONEDA")
print(f"📂 Total de imágenes a procesar: {len(imagenes_a_procesar)}")
print("==========================================================")

if not imagenes_a_procesar:
    print("❌ No se encontraron imágenes válidas en la carpeta test_images.")
else:
    for idx, ruta_imagen in enumerate(imagenes_a_procesar, 1):
        nombre_archivo = os.path.basename(ruta_imagen)
        print(f"\n📷 [Imagen {idx}/{len(imagenes_a_procesar)}]: {nombre_archivo}")
        
        try:
            img = Image.open(ruta_imagen)
            texto_ocr = extraer_texto_de_imagen(img)
            datos = extraer_campos_sinpe(texto_ocr)

            print("   📊 Resultados Estandarizados:")
            print(f"      • Comprobante : {datos.get('numero_comprobante')}")
            print(f"      • Fecha         : {datos.get('fecha_pago')}")
            print(f"      • Hora          : {datos.get('hora_pago')}")
            print(f"      • Teléfono      : {datos.get('telefono_origen')}")
            print(f"      • Monto         : {datos.get('monto')}")
            print(f"      • Moneda        : {datos.get('moneda')}")
            print("-" * 58)

        except Exception as e:
            print(f"   ❌ Error al procesar la imagen {nombre_archivo}: {e}")

print("\n✅ Pruebas finalizadas.")
>>>>>>> main
