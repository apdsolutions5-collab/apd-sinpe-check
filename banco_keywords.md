# Mapeo de Palabras Clave por Entidad Bancaria (SINPE OCR)

Este documento detalla las palabras clave recurrentes utilizadas para la extracción de datos (Monto, Fecha, Teléfono Emisor y Número de Referencia) en los comprobantes de diferentes bancos de Costa Rica.

## 1. BAC Credomatic
- **Monto**: `CRC`, `₡`, `Monto`, `Total pagado`
- **Fecha**: `Fecha`, `Fecha de transacción`, `Día`
- **Teléfono Emisor**: `Teléfono origen`, `Cuenta de origen`, `Origen`
- **Número de Referencia**: `Referencia`, `Comprobante Nº`, `Nº de transacción`

## 2. Banco Nacional de Costa Rica (BNCR)
- **Monto**: `Colones`, `Monto transferido`, `₡`, `Monto debitado`
- **Fecha**: `Fecha y hora`, `Realizado el`, `Fecha del pago`
- **Teléfono Emisor**: `Teléfono de retiro`, `Teléfono celular`
- **Número de Referencia**: `Número de comprobante`, `Referencia SINPE`, `Id transacción`, `Comprovante`

## 3. Banco de Costa Rica (BCR)
- **Monto**: `Monto total`, `Sumatoria`, `₡`, `Monto transferido`
- **Fecha**: `Fecha de operación`, `Emitido el`
- **Teléfono Emisor**: `Celular asociado`, `Teléfono origen`, `Transferido desde`
- **Número de Referencia**: `Consecutivo`, `Referencia numérica`, `Transacción`