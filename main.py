from fastapi import FastAPI, File, UploadFile
import pytesseract
from PIL import Image
import io

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