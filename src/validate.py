#!/usr/bin/env python3
"""
Sistema de Gestión de Información
Módulo de validaciones base
"""

import re


def validate_id(record_id):
    """
    Valida que el ID sea válido (no vacío y de tipo válido)
    
    Args:
        record_id: ID a validar
        
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    if record_id is None or record_id == "":
        return False, "El ID no puede estar vacío"
    
    if not isinstance(record_id, (str, int)):
        return False, "El ID debe ser string o número"
    
    return True, ""


def validate_name(name):
    """
    Valida que el nombre sea válido
    
    Args:
        name: Nombre a validar
        
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    if not name or not isinstance(name, str):
        return False, "El nombre es requerido y debe ser texto"
    
    if len(name.strip()) < 2:
        return False, "El nombre debe tener al menos 2 caracteres"
    
    return True, ""


def validate_email(email):
    """
    Valida que el email tenga @ y termine con .com
    
    Args:
        email: Email a validar
        
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    if not email or not isinstance(email, str):
        return False, "El email es requerido y debe ser texto"
    
    if "@" not in email:
        return False, "El email debe contener @"
    
    if not email.endswith(".com"):
        return False, "El email debe terminar con .com"
    
    # Patrón para validar estructura básica
    pattern = r"^[a-zA-Z0-9_.%+-]+@[a-zA-Z0-9.-]+\.com$"
    
    if not re.match(pattern, email):
        return False, "El formato del email no es válido"
    
    return True, ""


def validate_record(record_data):
    """
    Valida un registro completo
    
    Args:
        record_data: Diccionario con los datos del registro
        
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    # Validar ID
    is_valid, error = validate_id(record_data.get("id"))
    if not is_valid:
        return False, error
    
    # Validar nombre
    is_valid, error = validate_name(record_data.get("name"))
    if not is_valid:
        return False, error
    
    # Validar email
    is_valid, error = validate_email(record_data.get("email"))
    if not is_valid:
        return False, error
    
    return True, ""