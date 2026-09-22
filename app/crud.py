from sqlalchemy.orm import Session
from app.models import SinpeTransaction

def obtener_transaccion_por_referencia(db: Session, reference_number: str):
    return db.query(SinpeTransaction).filter(SinpeTransaction.reference_number == reference_number).first()

def obtener_transaccion_por_hash(db: Session, image_hash: str):
    if not image_hash:
        return None
    return db.query(SinpeTransaction).filter(SinpeTransaction.image_hash == image_hash).first()

def procesar_cobro_sinpe(db: Session, data: dict):
    reference_number = data.get("reference_number")
    image_hash = data.get("image_hash")

    # 1. Validar por número de referencia duplicado
    transaccion_existente = obtener_transaccion_por_referencia(db, reference_number)
    if transaccion_existente:
        return {
            "status": "DENEGADO",
            "motivo": "COMPROBANTE_DUPLICADO",
            "message": f"El comprobante '{reference_number}' ya fue procesado el {transaccion_existente.processed_at.strftime('%Y-%m-%d %H:%M:%S')}."
        }

    # 2. Validar si la misma imagen ya fue subida antes
    hash_existente = obtener_transaccion_por_hash(db, image_hash)
    if hash_existente:
        return {
            "status": "DENEGADO",
            "motivo": "IMAGEN_DUPLICADA",
            "message": f"La imagen enviada ya fue procesada previamente con la referencia '{hash_existente.reference_number}'."
        }

    # 3. Guardar transacción anonimizada si pasa las validaciones
    nueva_transaccion = SinpeTransaction(
        reference_number=reference_number,
        amount=data.get("amount"),
        currency=data.get("currency", "CRC"),
        bank_origin=data.get("bank_origin"),
        transaction_date=data.get("transaction_date"),
        image_hash=image_hash
    )
    
    db.add(nueva_transaccion)
    db.commit()
    db.refresh(nueva_transaccion)

    return {
        "status": "APROBADO",
        "message": "Comprobante verificado y registrado exitosamente.",
        "detalle": {
            "id": nueva_transaccion.id,
            "referencia": nueva_transaccion.reference_number,
            "monto": nueva_transaccion.amount,
            "moneda": nueva_transaccion.currency,
            "banco": nueva_transaccion.bank_origin,
            "fecha_comprobante": str(nueva_transaccion.transaction_date)
        }
    }