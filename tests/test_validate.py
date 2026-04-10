#!/usr/bin/env python3
"""
Módulo 6 — Pruebas para validate.py
Cubre: validate_id, validate_name, validate_email, validate_record
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from validate import validate_id, validate_name, validate_email, validate_record


# ──────────────────────────────────────────────
# validate_id
# ──────────────────────────────────────────────

class TestValidateId:

    def test_id_string_valido(self):
        ok, error = validate_id("J01")
        assert ok is True
        assert error == ""

    def test_id_numero_valido(self):
        ok, error = validate_id(123)
        assert ok is True

    def test_id_string_vacio(self):
        ok, error = validate_id("")
        assert ok is False
        assert error != ""

    def test_id_none(self):
        ok, error = validate_id(None)
        assert ok is False
        assert error != ""

    def test_id_tipo_invalido_lista(self):
        ok, error = validate_id(["J01"])
        assert ok is False


# ──────────────────────────────────────────────
# validate_name
# ──────────────────────────────────────────────

class TestValidateName:

    def test_nombre_valido(self):
        ok, error = validate_name("Juan Pérez")
        assert ok is True
        assert error == ""

    def test_nombre_dos_caracteres(self):
        ok, error = validate_name("Jo")
        assert ok is True

    def test_nombre_vacio(self):
        ok, error = validate_name("")
        assert ok is False
        assert error != ""

    def test_nombre_un_caracter(self):
        ok, error = validate_name("A")
        assert ok is False

    def test_nombre_solo_espacios(self):
        ok, error = validate_name("   ")
        assert ok is False

    def test_nombre_none(self):
        ok, error = validate_name(None)
        assert ok is False

    def test_nombre_tipo_invalido_numero(self):
        ok, error = validate_name(123)
        assert ok is False


# ──────────────────────────────────────────────
# validate_email
# ──────────────────────────────────────────────

class TestValidateEmail:

    def test_email_gmail_valido(self):
        ok, error = validate_email("juan@gmail.com")
        assert ok is True
        assert error == ""

    def test_email_hotmail_valido(self):
        ok, error = validate_email("maria@hotmail.com")
        assert ok is True

    def test_email_sin_arroba(self):
        ok, error = validate_email("juangmail.com")
        assert ok is False
        assert "arroba" in error or "@" in error

    def test_email_sin_punto_com(self):
        ok, error = validate_email("juan@correo.es")
        assert ok is False
        assert ".com" in error

    def test_email_vacio(self):
        ok, error = validate_email("")
        assert ok is False

    def test_email_none(self):
        ok, error = validate_email(None)
        assert ok is False

    def test_email_formato_invalido(self):
        ok, error = validate_email("no-es-valido")
        assert ok is False

    def test_email_dominio_org(self):
        ok, error = validate_email("test@empresa.org")
        assert ok is False


# ──────────────────────────────────────────────
# validate_record
# ──────────────────────────────────────────────

class TestValidateRecord:

    def test_registro_completo_valido(self):
        record = {"id": "J01", "name": "Juan Pérez", "email": "juan@gmail.com"}
        ok, error = validate_record(record)
        assert ok is True
        assert error == ""

    def test_registro_sin_id(self):
        record = {"name": "Juan Pérez", "email": "juan@gmail.com"}
        ok, error = validate_record(record)
        assert ok is False

    def test_registro_sin_nombre(self):
        record = {"id": "J01", "email": "juan@gmail.com"}
        ok, error = validate_record(record)
        assert ok is False

    def test_registro_email_invalido(self):
        record = {"id": "J01", "name": "Juan Pérez", "email": "sin-arroba"}
        ok, error = validate_record(record)
        assert ok is False

    def test_registro_vacio(self):
        ok, error = validate_record({})
        assert ok is False
