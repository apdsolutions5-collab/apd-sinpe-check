from fastapi import FastAPI, File, UploadFile, Form, HTTPException, status
import pytesseract
from PIL import Image
import io

from app.ocr_engine import extraer_texto_de_imagen, extraer_campos_sinpe

app = FastAPI(title="API de Verificación SINPE - OCR", version="1.0")

@app.get("/")
def read_root():
    return {"mensaje": "Servidor de Tesseract OCR para SINPE funcionando correctamente"}

@app.post("/extraer-texto/")
async def extraer_texto(file: UploadFile = File(...)):
    try:
        contenido = await file.read()
        imagen = Image.open(io.BytesIO(contenido))

        # Ejecutar Tesseract OCR especificando español ('spa')
        texto_extraido = pytesseract.image_to_string(imagen, lang='spa')

        return {
            "nombre_archivo": file.filename,
            "texto": texto_extraido.strip()
        }
    except Exception as e:
        return {"error": str(e)}

# ------------------------------------------------------------------
# KAN-31: Endpoint de validación de comprobante SINPE
# ------------------------------------------------------------------
@app.post("/api/v1/validate-payment")
async def validate_payment(
    file: UploadFile = File(...),
    expected_amount: float = Form(...)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo proporcionado debe ser una imagen válida."
        )

    try:
        contenido = await file.read()
        imagen = Image.open(io.BytesIO(contenido))

        # Extraer texto y procesar datos con el motor OCR del proyecto
        texto_extraido = extraer_texto_de_imagen(imagen)
        datos_sinpe = extraer_campos_sinpe(texto_extraido)

        # Validar si el monto numérico extraído coincide con el esperado
        monto_detectado = datos_sinpe.get("monto_numerico")
        monto_coincide = False

        if monto_detectado:
            try:
                # Normalizar el valor eliminando puntos de miles o comas
                monto_limpio = str(monto_detectado).replace(".", "").replace(",", ".")
                monto_float = float(monto_limpio)
                monto_coincide = abs(monto_float - expected_amount) < 0.01
            except ValueError:
                monto_coincide = False

        return {
            "exito": True,
            "nombre_archivo": file.filename,
            "monto_esperado": expected_amount,
            "monto_coincide": monto_coincide,
            "datos_comprobante": datos_sinpe,
            "texto_ocr_raw": texto_extraido
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar el comprobante: {str(e)}"
        )