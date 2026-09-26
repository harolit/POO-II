"""
Funciones auxiliares y utilidades generales.
"""
from datetime import datetime


def formato_fecha(fecha_str):
    """Formatea fechas para visualización."""
    try:
        return datetime.strptime(fecha_str, '%Y-%m-%d').strftime('%d/%m/%Y')
    except Exception:
        return fecha_str


def validar_email(email: str) -> bool:
    """Valida formato básico de email."""
    return '@' in email and '.' in email.split('@')[-1]


def validar_nota(nota) -> bool:
    """Valida que la nota esté entre 0.0 y 5.0."""
    try:
        n = float(nota)
        return 0.0 <= n <= 5.0
    except (ValueError, TypeError):
        return False


def calcular_promedio(notas_ponderadas):
    """Calcula promedio ponderado: [(nota, ponderacion), ...]"""
    if not notas_ponderadas:
        return 0.0
    total = sum(n * (p / 100) for n, p in notas_ponderadas)
    return round(total, 2)