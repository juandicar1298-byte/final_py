#!/usr/bin/env python3
"""
Sistema de Gestión de Información
Módulo de servicio — CRUD completo con persistencia en archivo JSON
Módulo 3
"""

import json
import os

from validate import validate_record


DATA_FILE = os.path.join("data", "records.json")


class RecordService:
    """
    Servicio para gestionar registros con persistencia en archivo JSON.
    Implementa CRUD completo con validaciones, list comprehensions y lambdas.
    """

    def __init__(self, filepath=DATA_FILE):
        """
        Inicializa el servicio y carga los datos persistidos.

        Args:
            filepath: Ruta del archivo JSON de persistencia
        """
        self.filepath = filepath
        self.records = {}   # {id: registro_completo}
        self.ids = set()    # Set para garantizar IDs únicos
        self._load_from_file()

    # ──────────────────────────────────────────────
    # Persistencia
    # ──────────────────────────────────────────────

    def _load_from_file(self):
        """Carga los registros desde el archivo JSON (si existe)."""
        if not os.path.exists(self.filepath):
            return

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            # list comprehension: reconstruir ids a partir de las claves cargadas
            self.records = data if isinstance(data, dict) else {}
            self.ids = {record_id for record_id in self.records}

        except (json.JSONDecodeError, OSError) as e:
            print(f"  [Advertencia] No se pudo cargar '{self.filepath}': {e}")
            self.records = {}
            self.ids = set()

    def _save_to_file(self):
        """Persiste todos los registros en el archivo JSON.
        Crea la carpeta padre automaticamente si no existe."""
        try:
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.records, f, ensure_ascii=False, indent=2)
        except OSError as e:
            print(f"  [Error] No se pudo guardar en '{self.filepath}': {e}")

    # ──────────────────────────────────────────────
    # CREATE
    # ──────────────────────────────────────────────

    def new_register(self, record_data):
        """
        Crea un nuevo registro si es válido y el ID no existe.

        Args:
            record_data (dict): Diccionario con id, name, email

        Returns:
            tuple: (éxito: bool, mensaje: str)
        """
        is_valid, error = validate_record(record_data)
        if not is_valid:
            return False, f"Registro inválido: {error}"

        record_id = str(record_data.get("id"))

        if record_id in self.ids:
            return False, f"El ID '{record_id}' ya existe en el sistema"

        self.records[record_id] = {**record_data, "id": record_id}
        self.ids.add(record_id)
        self._save_to_file()

        return True, f"Registro '{record_id}' creado exitosamente"

    # ──────────────────────────────────────────────
    # READ — listar y buscar
    # ──────────────────────────────────────────────

    def list_records(self, order_by="name"):
        """
        Retorna todos los registros ordenados por un campo dado.

        Lambda: clave de ordenamiento dinámica según 'order_by'.

        Args:
            order_by (str): Campo por el que se ordena ('id', 'name', 'email')

        Returns:
            list[dict]: Lista de registros ordenada
        """
        sort_key = lambda r: r.get(order_by, "")   # lambda para ordenamiento dinámico

        # list comprehension: extraer valores y ordenar
        return sorted(
            [record for record in self.records.values()],
            key=sort_key
        )

    def search_record(self, query):
        """
        Busca registros cuyo nombre o email contengan el texto dado (case-insensitive).

        List comprehension: filtrado en una sola expresión.

        Args:
            query (str): Texto a buscar

        Returns:
            list[dict]: Registros que coinciden con la búsqueda
        """
        q = query.lower().strip()

        # list comprehension con condición múltiple
        return [
            record for record in self.records.values()
            if q in record.get("name", "").lower()
            or q in record.get("email", "").lower()
        ]

    def get_record_by_id(self, record_id):
        """
        Obtiene un registro por ID exacto.

        Args:
            record_id (str): ID del registro

        Returns:
            tuple: (éxito: bool, dict | mensaje: str)
        """
        record_id = str(record_id)
        if record_id not in self.ids:
            return False, f"No existe ningún registro con ID '{record_id}'"

        return True, self.records[record_id]

    # ──────────────────────────────────────────────
    # UPDATE
    # ──────────────────────────────────────────────

    def update_record(self, record_id, new_data):
        """
        Actualiza los campos de un registro existente.
        Solo actualiza los campos presentes en new_data; el ID no puede cambiar.

        Args:
            record_id (str): ID del registro a actualizar
            new_data (dict): Campos nuevos (name y/o email)

        Returns:
            tuple: (éxito: bool, mensaje: str)
        """
        record_id = str(record_id)

        if record_id not in self.ids:
            return False, f"No existe ningún registro con ID '{record_id}'"

        # Construir registro candidato para validar
        current = self.records[record_id].copy()
        candidate = {**current, **new_data, "id": record_id}

        is_valid, error = validate_record(candidate)
        if not is_valid:
            return False, f"Datos inválidos para la actualización: {error}"

        self.records[record_id] = candidate
        self._save_to_file()

        return True, f"Registro '{record_id}' actualizado exitosamente"

    # ──────────────────────────────────────────────
    # DELETE
    # ──────────────────────────────────────────────

    def delete_record(self, record_id):
        """
        Elimina un registro por ID.

        Args:
            record_id (str): ID del registro a eliminar

        Returns:
            tuple: (éxito: bool, mensaje: str)
        """
        record_id = str(record_id)

        if record_id not in self.ids:
            return False, f"No existe ningún registro con ID '{record_id}'"

        del self.records[record_id]
        self.ids.discard(record_id)
        self._save_to_file()

        return True, f"Registro '{record_id}' eliminado correctamente"

    # ──────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────

    def get_records_count(self):
        """Retorna la cantidad de registros almacenados."""
        return len(self.records)

    # Alias de compatibilidad con módulos anteriores
    def create_record(self, record_data):
        return self.new_register(record_data)

    def get_all_records(self):
        return self.list_records()