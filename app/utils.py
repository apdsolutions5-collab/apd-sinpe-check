def limpiar_texto(texto):
    """Limpia el texto básico para buscar palabras clave."""
    if not texto:
        return ""
    return texto.lower().strip()