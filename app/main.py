import io
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends, status
from sqlalchemy.orm import Session
import pytesseract
from PIL import Image

from app.ocr_engine import extraer_texto_de_imagen, extraer_campos_sinpe, obtener_confianza_ocr
from app.database import get_db, Pago

app = FastAPI(title="API de Verificación SINPE - OCR", version="1.0")


@app.get("/")
def read_root():
    return {"mensaje": "Servidor de Tesseract OCR para SINPE funcionando correctamente"}


@app.post("/extraer-texto/")
async def extraer_texto(file: UploadFile = File(...)):
    try:
        contenido = await file.read()
        imagen = Image.open(io.BytesIO(contenido))

        # Ejecutar Tesseract OCR especificando español 'spa'
        texto_extraido = pytesseract.image_to_string(imagen, lang='spa')

        return {
            "nombre_archivo": file.filename,
            "texto": texto_extraido.strip()
        }
    except Exception as e:
        return {"error": str(e)}


@app.post("/api/v1/validate-payment")
async def validate_payment(
    file: UploadFile = File(..., description="Imagen del comprobante SINPE"),
    expected_amount: float = Form(
        ..., 
        description="Monto esperado a verificar", 
        examples=[2999.99]
    ),
    db: Session = Depends(get_db)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo proporcionado debe ser una imagen válida."
        )

    try:
        contenido = await file.read()
        imagen = Image.open(io.BytesIO(contenido))

        # Extraer texto, campos y nivel de confianza con OCR
        texto_extraido = extraer_texto_de_imagen(imagen)
        datos_sinpe = extraer_campos_sinpe(texto_extraido)
        confianza_ocr = obtener_confianza_ocr(imagen)

        num_comprobante = datos_sinpe.get("numero_comprobante")
        monto_detectado = datos_sinpe.get("monto_numerico")

        # 1. Validar si el comprobante ya existe en la base de datos
        es_duplicado = False
        if num_comprobante:
            pago_existente = db.query(Pago).filter(Pago.numero_comprobante == num_comprobante).first()
            if pago_existente:
                es_duplicado = True

        # 2. Validar si el monto numérico extraído coincide con el esperado
        monto_coincide = False
        if monto_detectado:
            try:
                # Normalizar el formato numérico (elimina comas de separador de miles)
                monto_str = str(monto_detectado).replace(",", "")
                monto_float = float(monto_str)
                monto_coincide = abs(monto_float - expected_amount) < 0.01
            except ValueError:
                monto_coincide = False

        # Determinar el estatus final del pago en español
        pago_valido = monto_coincide and (not es_duplicado) and (num_comprobante is not None)
        estatus_pago = "Válido" if pago_valido else "Inválido"

        # 3. Si la transacción es válida y nueva, la guardamos en SQLite
        if pago_valido:
            nuevo_pago = Pago(
                numero_comprobante=num_comprobante,
                monto=expected_amount,
                telefono_origen=datos_sinpe.get("telefono_origen"),
                fecha_pago=datos_sinpe.get("fecha_pago")
            )
            db.add(nuevo_pago)
            db.commit()

        # Respuesta estructurada limpia para KAN-33
        return {
            "estatus_pago": estatus_pago,
            "numero_referencia": num_comprobante,
            "porcentaje_confianza_ocr": confianza_ocr,
            "detalles": {
                "monto_esperado": expected_amount,
                "monto_coincide": monto_coincide,
                "es_duplicado": es_duplicado,
                "nombre_archivo": file.filename,
                "datos_comprobante": datos_sinpe,
                "texto_ocr_raw": texto_extraido
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar el comprobante: {str(e)}"
        )