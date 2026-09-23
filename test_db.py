import json
from datetime import datetime
from app.database import engine, Base, SessionLocal
from app.models import SinpeTransaction
from app.crud import procesar_cobro_sinpe

# Crear/actualizar esquema
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # Limpiar datos previos de prueba
    db.query(SinpeTransaction).filter(SinpeTransaction.reference_number == "202503081518301").delete()
    db.commit()

    datos_comprobante = {
        "reference_number": "202503081518301",
        "amount": 15000.00,
        "currency": "CRC",
        "bank_origin": "BAC San José",
        "transaction_date": datetime(2026, 9, 22, 14, 30, 0),
        "image_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    }

    print("\n" + "="*50)
    print(" PRUEBA 1: Registro completo anonimizado")
    print("="*50)
    res1 = procesar_cobro_sinpe(db, datos_comprobante)
    print(f"Estado  : {res1['status']}")
    print(f"Mensaje : {res1['message']}")
    if "detalle" in res1:
        print("Detalle :")
        print(json.dumps(res1["detalle"], indent=4, ensure_ascii=False))

    print("\n" + "="*50)
    print(" PRUEBA 2: Duplicado por número de referencia")
    print("="*50)
    res2 = procesar_cobro_sinpe(db, datos_comprobante)
    print(f"Estado  : {res2['status']}")
    print(f"Motivo  : {res2.get('motivo')}")
    print(f"Mensaje : {res2['message']}")
    print("="*50 + "\n")

finally:
    db.close()