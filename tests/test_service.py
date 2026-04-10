#!/usr/bin/env python3
"""
Módulo 6 — Pruebas para service.py
Cubre: new_register, list_records, search_record,
       get_record_by_id, update_record, delete_record, bulk_insert
"""

import sys
import os
import tempfile
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from service import RecordService


# ──────────────────────────────────────────────
# Fixture: servicio con archivo temporal aislado
# ──────────────────────────────────────────────

@pytest.fixture
def service(tmp_path):
    """Crea un RecordService limpio en un directorio temporal por cada test."""
    filepath = str(tmp_path / "records.json")
    return RecordService(filepath=filepath)


# ──────────────────────────────────────────────
# CREATE — new_register
# ──────────────────────────────────────────────

class TestNewRegister:

    def test_crear_registro_valido(self, service):
        ok, msg = service.new_register({"id": "J01", "name": "Juan Pérez", "email": "juan@gmail.com"})
        assert ok is True
        assert "J01" in msg

    def test_id_duplicado_rechazado(self, service):
        service.new_register({"id": "J01", "name": "Juan Pérez", "email": "juan@gmail.com"})
        ok, msg = service.new_register({"id": "J01", "name": "Otro", "email": "otro@gmail.com"})
        assert ok is False
        assert "J01" in msg

    def test_nombre_vacio_rechazado(self, service):
        ok, msg = service.new_register({"id": "X01", "name": "", "email": "x@gmail.com"})
        assert ok is False

    def test_email_sin_arroba_rechazado(self, service):
        ok, msg = service.new_register({"id": "X01", "name": "Nombre", "email": "sinArroba"})
        assert ok is False

    def test_email_sin_punto_com_rechazado(self, service):
        ok, msg = service.new_register({"id": "X01", "name": "Nombre", "email": "x@correo.es"})
        assert ok is False

    def test_contador_incrementa(self, service):
        assert service.get_records_count() == 0
        service.new_register({"id": "A01", "name": "Ana", "email": "ana@gmail.com"})
        assert service.get_records_count() == 1
        service.new_register({"id": "B01", "name": "Beto", "email": "beto@gmail.com"})
        assert service.get_records_count() == 2


# ──────────────────────────────────────────────
# READ — list_records
# ──────────────────────────────────────────────

class TestListRecords:

    def test_lista_vacia_sin_registros(self, service):
        assert service.list_records() == []

    def test_ordenado_por_nombre(self, service):
        service.new_register({"id": "Z01", "name": "Zara López", "email": "zara@gmail.com"})
        service.new_register({"id": "A01", "name": "Ana García", "email": "ana@gmail.com"})
        service.new_register({"id": "M01", "name": "Mario Ruiz", "email": "mario@gmail.com"})
        records = service.list_records(order_by="name")
        nombres = [r["name"] for r in records]
        assert nombres == sorted(nombres)

    def test_ordenado_por_id(self, service):
        service.new_register({"id": "C01", "name": "Carlos", "email": "carlos@gmail.com"})
        service.new_register({"id": "A01", "name": "Ana",    "email": "ana@gmail.com"})
        service.new_register({"id": "B01", "name": "Beto",   "email": "beto@gmail.com"})
        records = service.list_records(order_by="id")
        ids = [r["id"] for r in records]
        assert ids == sorted(ids)

    def test_retorna_lista(self, service):
        service.new_register({"id": "J01", "name": "Juan", "email": "juan@gmail.com"})
        resultado = service.list_records()
        assert isinstance(resultado, list)


# ──────────────────────────────────────────────
# READ — search_record
# ──────────────────────────────────────────────

class TestSearchRecord:

    def test_busqueda_por_nombre_parcial(self, service):
        service.new_register({"id": "M01", "name": "María García", "email": "maria@gmail.com"})
        service.new_register({"id": "J01", "name": "Juan Pérez",   "email": "juan@hotmail.com"})
        results = service.search_record("garcia")
        assert len(results) == 1
        assert results[0]["id"] == "M01"

    def test_busqueda_por_email(self, service):
        service.new_register({"id": "M01", "name": "María", "email": "maria@gmail.com"})
        service.new_register({"id": "J01", "name": "Juan",  "email": "juan@hotmail.com"})
        results = service.search_record("hotmail")
        assert len(results) == 1
        assert results[0]["id"] == "J01"

    def test_busqueda_case_insensitive(self, service):
        service.new_register({"id": "A01", "name": "Ana Torres", "email": "ana@gmail.com"})
        assert len(service.search_record("ANA")) == 1
        assert len(service.search_record("ana")) == 1
        assert len(service.search_record("Ana")) == 1

    def test_busqueda_multiples_resultados(self, service):
        service.new_register({"id": "A01", "name": "Ana", "email": "ana@gmail.com"})
        service.new_register({"id": "B01", "name": "Beto", "email": "beto@gmail.com"})
        service.new_register({"id": "C01", "name": "Carlos", "email": "carlos@gmail.com"})
        results = service.search_record("gmail")
        assert len(results) == 3

    def test_busqueda_sin_resultados(self, service):
        service.new_register({"id": "J01", "name": "Juan", "email": "juan@gmail.com"})
        results = service.search_record("xyz_inexistente")
        assert results == []


# ──────────────────────────────────────────────
# READ — get_record_by_id
# ──────────────────────────────────────────────

class TestGetRecordById:

    def test_obtener_registro_existente(self, service):
        service.new_register({"id": "M01", "name": "María", "email": "maria@gmail.com"})
        ok, result = service.get_record_by_id("M01")
        assert ok is True
        assert result["name"] == "María"
        assert result["email"] == "maria@gmail.com"

    def test_obtener_registro_inexistente(self, service):
        ok, result = service.get_record_by_id("ZZZ")
        assert ok is False
        assert isinstance(result, str)   # Debe retornar un mensaje de error


# ──────────────────────────────────────────────
# UPDATE — update_record
# ──────────────────────────────────────────────

class TestUpdateRecord:

    def test_actualizar_email_valido(self, service):
        service.new_register({"id": "J01", "name": "Juan", "email": "juan@gmail.com"})
        ok, msg = service.update_record("J01", {"email": "nuevo@hotmail.com"})
        assert ok is True
        _, r = service.get_record_by_id("J01")
        assert r["email"] == "nuevo@hotmail.com"

    def test_actualizar_nombre(self, service):
        service.new_register({"id": "J01", "name": "Juan", "email": "juan@gmail.com"})
        ok, msg = service.update_record("J01", {"name": "Juan Carlos"})
        assert ok is True
        _, r = service.get_record_by_id("J01")
        assert r["name"] == "Juan Carlos"

    def test_actualizar_email_invalido_rechazado(self, service):
        service.new_register({"id": "C01", "name": "Carlos", "email": "carlos@gmail.com"})
        ok, msg = service.update_record("C01", {"email": "no-es-valido"})
        assert ok is False

    def test_actualizar_id_inexistente(self, service):
        ok, msg = service.update_record("ZZZ", {"name": "Fantasma"})
        assert ok is False

    def test_actualizacion_persiste_otros_campos(self, service):
        service.new_register({"id": "A01", "name": "Ana", "email": "ana@gmail.com"})
        service.update_record("A01", {"name": "Anita"})
        _, r = service.get_record_by_id("A01")
        assert r["email"] == "ana@gmail.com"   # El email no debe cambiar


# ──────────────────────────────────────────────
# DELETE — delete_record
# ──────────────────────────────────────────────

class TestDeleteRecord:

    def test_eliminar_registro_existente(self, service):
        service.new_register({"id": "L01", "name": "Luis", "email": "luis@gmail.com"})
        ok, msg = service.delete_record("L01")
        assert ok is True

    def test_registro_eliminado_no_existe(self, service):
        service.new_register({"id": "L01", "name": "Luis", "email": "luis@gmail.com"})
        service.delete_record("L01")
        ok, _ = service.get_record_by_id("L01")
        assert ok is False

    def test_eliminar_id_inexistente(self, service):
        ok, msg = service.delete_record("ZZZ")
        assert ok is False

    def test_doble_eliminacion_falla(self, service):
        service.new_register({"id": "L01", "name": "Luis", "email": "luis@gmail.com"})
        service.delete_record("L01")
        ok, msg = service.delete_record("L01")
        assert ok is False

    def test_contador_decrementa(self, service):
        service.new_register({"id": "A01", "name": "Ana", "email": "ana@gmail.com"})
        service.new_register({"id": "B01", "name": "Beto", "email": "beto@gmail.com"})
        assert service.get_records_count() == 2
        service.delete_record("A01")
        assert service.get_records_count() == 1


# ──────────────────────────────────────────────
# bulk_insert (*args / **kwargs)
# ──────────────────────────────────────────────

class TestBulkInsert:

    def test_insercion_masiva_exitosa(self, service):
        registros = [
            {"id": "A01", "name": "Ana",    "email": "ana@gmail.com"},
            {"id": "B01", "name": "Beto",   "email": "beto@gmail.com"},
            {"id": "C01", "name": "Carlos", "email": "carlos@gmail.com"},
        ]
        inserted, errors, detail = service.bulk_insert(registros)
        assert inserted == 3
        assert errors == 0

    def test_skip_errors_ignora_duplicados(self, service):
        service.new_register({"id": "A01", "name": "Ana", "email": "ana@gmail.com"})
        registros = [
            {"id": "A01", "name": "Duplicado", "email": "dup@gmail.com"},
            {"id": "B01", "name": "Beto",      "email": "beto@gmail.com"},
        ]
        inserted, errors, detail = service.bulk_insert(registros, skip_errors=True)
        assert inserted == 1
        assert errors == 1

    def test_detalle_retorna_lista(self, service):
        registros = [{"id": "A01", "name": "Ana", "email": "ana@gmail.com"}]
        inserted, errors, detail = service.bulk_insert(registros)
        assert isinstance(detail, list)
        assert len(detail) == 1

    def test_prefix_kwarg_aparece_en_detalle(self, service):
        registros = [{"id": "A01", "name": "Ana", "email": "ana@gmail.com"}]
        _, _, detail = service.bulk_insert(registros, prefix="[TEST]")
        assert "[TEST]" in detail[0]
