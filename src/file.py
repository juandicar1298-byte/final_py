#!/usr/bin/env python3
"""
Sistema de Gestión de Información
Módulo 2 — Persistencia en archivos JSON
"""

import json
import os


DEFAULT_PATH = os.path.join("data", "records.json")


def load_data(filepath=DEFAULT_PATH):
    """
    Carga los registros desde un archivo JSON.
    Si el archivo no existe, retorna un diccionario vacío.
    Si el archivo está dañado, muestra advertencia y retorna vacío.

    Args:
        filepath (str): Ruta del archivo JSON.

    Returns:
        dict: Diccionario {id: registro} o {} si no existe / hay error.
    """
    if not os.path.exists(filepath):
        return {}

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        print(f"  [Advertencia] El archivo '{filepath}' está dañado. Se arranca con datos vacíos.")
        return {}
    except OSError as e:
        print(f"  [Advertencia] No se pudo leer '{filepath}': {e}")
        return {}


def save_data(data, filepath=DEFAULT_PATH):
    """
    Guarda el diccionario de registros en un archivo JSON.
    Crea la carpeta padre automáticamente si no existe.

    Args:
        data (dict):     Diccionario {id: registro}.
        filepath (str):  Ruta del archivo JSON.

    Returns:
        bool: True si se guardó correctamente, False si hubo error.
    """
    try:
        parent = os.path.dirname(filepath)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except OSError as e:
        print(f"  [Error] No se pudo guardar en '{filepath}': {e}")
        return False