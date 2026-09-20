# 🚀 APD SinpeCheck

**Módulo de Validación Automatizada de SINPE Móvil mediante OCR Local**  
_A.P.D. Software Solutions | Programa de Pasantías_

¡Bienvenido al equipo de desarrollo de A.P.D. Software Solutions! Durante esta semana estarás trabajando en el desarrollo de **APD SinpeCheck**, un MVP (Producto Mínimo Viable) diseñado para mitigar fraudes y automatizar la verificación de comprobantes de pago SINPE Móvil para nuestras PyMEs clientes.

Tu meta es dedicar **40 horas de desarrollo** distribuidas a lo largo de esta semana para construir un módulo robusto, reutilizable y eficiente.

---

## 🎯 Mensaje de Arranque (Lunes 21)

> _"Iniciamos hoy lunes con la fase de configuración de entorno y recolección de datos bancarios. Tu meta para las primeras 8 horas es completar los tickets **Ticket-001** (Servidor FastAPI corriendo localmente con dependencias de Tesseract instaladas) y **Ticket-002** (Mapeo visual y de texto de comprobantes reales del BAC, BCR y BNCR). ¡Mucho éxito en tu pasantía!"_

---

## 🛠️ Stack Tecnológico Asignado

- **Backend:** Python 3.10+ & FastAPI (Framework Web)
- **Motor OCR:** Tesseract OCR (Código libre local con paquete de idioma `spa`)
- **Base de Datos:** SQLite (Para control interno de duplicados y prevención de fraudes)
- **Frontend:** HTML5, CSS corporativo y JavaScript nativo (`Fetch API`)

---

## 📋 Backlog de Tickets para la Semana

### 📌 LUNES 21: Configuración y Análisis de Datos (8 Horas)

- **Ticket-001: Configuración del Entorno de Desarrollo (3h)**
  - _Descripción:_ Configurar entorno virtual (`venv`), archivo `requirements.txt` (`fastapi`, `uvicorn`, `pytesseract`, `Pillow`, `python-multipart`) e instalar Tesseract OCR en el sistema operativo local con el idioma español.
  - _Criterio de aceptación:_ Servidor FastAPI respondiendo en `http://localhost:8000/` con un estado `"online"`.
- **Ticket-002: Recolección y Mapeo de Comprobantes de Pago (5h)**
  - _Descripción:_ Crear una carpeta `/test_images` y almacenar capturas reales de comprobantes de Costa Rica (BAC, BCR, BNCR). Analizar y mapear en texto las palabras clave de cada banco (Monto, Teléfono, Referencia).

### 📌 MARTES 22: Motor de Extracción - Core OCR (8 Horas)

- **Ticket-003: Módulo de Preprocesamiento de Imágenes (4h)**
  - _Descripción:_ Desarrollar filtros con la librería `Pillow` (escala de grises, contraste y binarización) para limpiar las imágenes antes del OCR.
- **Ticket-004: Implementación de Tesseract y Regex (4h)**
  - _Descripción:_ Programar la extracción de texto y aplicar expresiones regulares (`re`) para aislar los 4 datos clave: Monto (₡), Fecha, Teléfono emisor y Número de referencia.

### 📌 MIÉRCOLES 23: API REST y Prevención de Fraude (8 Horas)

- **Ticket-005: Base de Datos Local para Control de Duplicados (4h)**
  - _Descripción:_ Diseñar una tabla en SQLite para registrar los números de referencia ya procesados y evitar el fraude por doble validación.
- **Ticket-006: Creación de Endpoints en FastAPI (4h)**
  - _Descripción:_ Desarrollar el endpoint `POST /api/v1/validate-payment` que reciba la imagen y el monto esperado, retornando si el pago es válido o no.

### 📌 JUEVES 24: Conexión Frontend y Prototipado Visual (8 Horas)

- **Ticket-007: Construcción de la Interfaz Web del Validador (4h)**
  - _Descripción:_ Programar la interfaz en modo oscuro idéntica al prototipo UI diseñado para el POS.
- **Ticket-008: Integración Frontend-Backend (4h)**
  - _Descripción:_ Conectar la UI con la API de FastAPI para mostrar en tiempo real las pantallas de carga, éxito (verde) o alerta (rojo).

### 📌 VIERNES 25: Aseguramiento, Documentación y Cierre (8 Horas)

- **Ticket-009: Pruebas de Estrés y Manejo de Errores (4h)**
  - _Descripción:_ Validar el comportamiento del sistema con imágenes corruptas, falsificadas o sin texto bancario.
- **Ticket-010: Documentación Técnica de Integración (4h)**
  - _Descripción:_ Documentar el manual de despliegue en este README para el equipo de planta de A.P.D.
