import os
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