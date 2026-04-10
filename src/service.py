#!/usr/bin/env python3
"""
Sistema de Gestión de Información
Módulo 3 — CRUD completo con persistencia
Módulo 5 — bulk_insert con *args/**kwargs
"""

from validate import validate_record
from file import load_data, save_data


DATA_FILE = "data/records.json"


class RecordService:
    """
    Servicio para gestionar registros con persistencia en archivo JSON.
    Implementa CRUD completo con validaciones, list comprehensions y lambdas.
    La persistencia se delega a file.py (load_data / save_data).
    """

    def __init__(self, filepath=DATA_FILE):
        self.filepath = filepath
        self.records  = {}   # {id: registro_completo}
        self.ids      = set()  # Set para IDs únicos (Módulo 1)
        self._load()

    # ──────────────────────────────────────────────
    # Persistencia — delega a file.py (Módulo 2)
    # ──────────────────────────────────────────────

    def _load(self):
        self.records = load_data(self.filepath)
        self.ids     = set(self.records.keys())

    def _save(self):
        save_data(self.records, self.filepath)

    # ──────────────────────────────────────────────
    # CREATE
    # ──────────────────────────────────────────────

    def new_register(self, record_data):
        """
        Crea un nuevo registro si es válido y el ID no existe.

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
        self._save()

        return True, f"Registro '{record_id}' creado exitosamente"

    def bulk_insert(self, records_list, *args, **kwargs):
        """
        Inserta múltiples registros de una vez.
        Módulo 5: demuestra uso real de *args y **kwargs.

        Args:
            records_list (list[dict]): Registros a insertar.
            *args:   Reservados para extensiones futuras.
            **kwargs:
                skip_errors (bool): Si True, continúa ante errores (default True).
                prefix (str):       Prefijo para los mensajes de resultado.

        Returns:
            tuple: (insertados: int, errores: int, detalle: list[str])
        """
        skip_errors = kwargs.get("skip_errors", True)
        prefix      = kwargs.get("prefix", "")

        inserted, errors, detail = 0, 0, []

        for record in records_list:
            ok, msg = self.new_register(record)
            tag = f"{prefix} " if prefix else ""
            if ok:
                inserted += 1
                detail.append(f"  ✓ {tag}{msg}")
            else:
                errors += 1
                detail.append(f"  ✗ {tag}{msg}")
                if not skip_errors:
                    break

        return inserted, errors, detail

    # ──────────────────────────────────────────────
    # READ
    # ──────────────────────────────────────────────

    def list_records(self, order_by="name"):
        """
        Retorna todos los registros ordenados por un campo dado.
        Usa lambda para ordenamiento dinámico y list comprehension.
        """
        sort_key = lambda r: r.get(order_by, "")
        return sorted(
            [record for record in self.records.values()],
            key=sort_key
        )

    def search_record(self, query):
        """
        Busca registros cuyo nombre o email contengan el texto (case-insensitive,
        ignora acentos). Usa list comprehension con condición múltiple.
        """
        import unicodedata

        def normalize(s: str) -> str:
            return unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode("utf-8").lower()

        q = normalize(query.strip())
        return [
            record for record in self.records.values()
            if q in normalize(record.get("name", ""))
            or q in normalize(record.get("email", ""))
        ]

    def get_record_by_id(self, record_id):
        record_id = str(record_id)
        if record_id not in self.ids:
            return False, f"No existe ningún registro con ID '{record_id}'"
        return True, self.records[record_id]

    # ──────────────────────────────────────────────
    # UPDATE
    # ──────────────────────────────────────────────

    def update_record(self, record_id, new_data):
        record_id = str(record_id)
        if record_id not in self.ids:
            return False, f"No existe ningún registro con ID '{record_id}'"

        current   = self.records[record_id].copy()
        candidate = {**current, **new_data, "id": record_id}

        is_valid, error = validate_record(candidate)
        if not is_valid:
            return False, f"Datos inválidos para la actualización: {error}"

        self.records[record_id] = candidate
        self._save()
        return True, f"Registro '{record_id}' actualizado exitosamente"

    # ──────────────────────────────────────────────
    # DELETE
    # ──────────────────────────────────────────────

    def delete_record(self, record_id):
        record_id = str(record_id)
        if record_id not in self.ids:
            return False, f"No existe ningún registro con ID '{record_id}'"

        del self.records[record_id]
        self.ids.discard(record_id)
        self._save()
        return True, f"Registro '{record_id}' eliminado correctamente"

    # ──────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────

    def get_records_count(self):
        return len(self.records)

    def create_record(self, record_data):
        return self.new_register(record_data)

    def get_all_records(self):
        return self.list_records()