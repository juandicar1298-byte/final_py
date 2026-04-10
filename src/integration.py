#!/usr/bin/env python3
"""
Sistema de Gestión de Información
Módulo 5 — Integración con librería externa: Faker
Genera registros falsos realistas para poblar el sistema.

Instalación:
    pip install faker
"""

from faker import Faker


# Instancia con localización en español latinoamericano
_faker = Faker("es_MX")
Faker.seed(42)   # Semilla fija para resultados reproducibles en pruebas


# ──────────────────────────────────────────────
# Función genérica con *args y **kwargs
# ──────────────────────────────────────────────

def build_record(*args, **kwargs):
    """
    Construye un diccionario de registro de forma flexible.
    Demuestra el uso de *args y **kwargs.

    Modos de uso:
        # Solo args posicionales (en orden: id, name, email)
        build_record("F01", "Ana Torres", "ana@gmail.com")

        # Solo kwargs
        build_record(id="F01", name="Ana Torres", email="ana@gmail.com")

        # Mixto: args primero, kwargs completan o sobreescriben
        build_record("F01", name="Ana Torres", email="ana@gmail.com")

    Args:
        *args:    Valores posicionales en orden (id, name, email).
        **kwargs: Campos nombrados; sobreescriben a los posicionales.

    Returns:
        dict: Registro con claves id, name, email.
    """
    fields = ["id", "name", "email"]

    # Mapear args posicionales a los campos en orden
    record = {fields[i]: str(v) for i, v in enumerate(args) if i < len(fields)}

    # kwargs completan o sobreescriben lo que haya en record
    record.update({k: str(v) for k, v in kwargs.items() if k in fields})

    return record


# ──────────────────────────────────────────────
# Helpers internos
# ──────────────────────────────────────────────

def _safe_email(name: str) -> str:
    """
    Genera un email garantizando que termine en .com.
    Faker a veces produce dominios .mx u .org que fallarían la validación.
    """
    local = (
        name.lower()
        .replace(" ", "")
        .replace("á", "a").replace("é", "e")
        .replace("í", "i").replace("ó", "o")
        .replace("ú", "u").replace("ñ", "n")
        .replace(".", "").replace(",", "")
    )[:15]   # Máximo 15 caracteres para el local

    domain = _faker.random_element(["gmail.com", "hotmail.com", "yahoo.com", "outlook.com"])
    return f"{local}@{domain}"


# ──────────────────────────────────────────────
# Generación de registros falsos
# ──────────────────────────────────────────────

def generate_fake_records(n=10, **overrides):
    """
    Genera una lista de n registros falsos usando Faker.

    Usa **kwargs (overrides) para fijar campos en todos los registros generados,
    útil en pruebas (ej: forzar un dominio de email específico).

    Args:
        n (int):       Cantidad de registros a generar. Por defecto: 10.
        **overrides:   Campos fijos para todos los registros.
                       Ejemplo: generate_fake_records(5, email="test@gmail.com")

    Returns:
        list[dict]: Lista de registros con id, name, email.
    """
    records = []

    for i in range(1, n + 1):
        name  = _faker.name()
        email = _safe_email(name)

        # Construir usando build_record con kwargs — uso real de la función genérica
        record = build_record(
            id    = f"F{i:03d}",
            name  = name,
            email = email,
        )

        # Aplicar overrides si se pasaron (sobreescriben los valores generados)
        record.update({k: str(v) for k, v in overrides.items() if k in record})

        records.append(record)

    return records