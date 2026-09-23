from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Modelo de la tabla de pagos para SQLite
class Pago(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)
    numero_comprobante = Column(String, unique=True, index=True)
    monto = Column(Float)
    telefono_origen = Column(String, nullable=True)
    fecha_pago = Column(String, nullable=True)

# Crear la tabla en la base de datos automáticamente si no existe
Base.metadata.create_all(bind=engine)

# Función generadora para la dependencia de FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()