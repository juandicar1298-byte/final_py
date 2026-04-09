#!/usr/bin/env python3
"""
Sistema de Gestión de Información
Aplicación principal
"""

from service import RecordService


# ──────────────────────────────────────────────
# Utilidades de presentación
# ──────────────────────────────────────────────

HEADER = f"  {'ID':<10} {'Nombre':<22} {'Email':<35}"
DIVIDER = "  " + "-" * 67


def display_records(records):
    """Imprime una tabla formateada con los registros recibidos."""
    if not records:
        print("  (Sin registros)")
        return

    print(HEADER)
    print(DIVIDER)
    for r in records:
        print(f"  {str(r['id']):<10} {r['name']:<22} {r['email']:<35}")


def section(number, title):
    print(f"\n[{number}] {title}")


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

def main():
    print("\n" + "=" * 50)
    print("  Sistema de Gestión de Información")
    print("=" * 50)

    service = RecordService()

    # ── 1. CREATE ─────────────────────────────
    section(1, "Creando registros (new_register)")

    registros = [
        {"id": "J01", "name": "Juan Pérez",    "email": "juanperez@gmail.com"},
        {"id": "M01", "name": "María García",   "email": "mariagarcia@hotmail.com"},
        {"id": "C01", "name": "Carlos López",   "email": "carloslopez@yahoo.com"},
        {"id": "A01", "name": "Ana Martínez",   "email": "anamartinez@gmail.com"},
        {"id": "L01", "name": "Luis Fernández", "email": "luisfernandez@gmail.com"},
    ]

    for r in registros:
        ok, msg = service.new_register(r)
        print(f"  {'✓' if ok else '✗'} {msg}")

    # ── 2. CREATE — errores esperados ─────────
    section(2, "Intentos de creación inválidos")

    invalids = [
        {"id": "J01", "name": "Pedro Ruiz",  "email": "pedroruiz@gmail.com"},  # ID duplicado
        {"id": "B01", "name": "",             "email": "test@gmail.com"},        # Nombre vacío
        {"id": "D01", "name": "Diego",        "email": "sin-arroba"},            # Email sin @
        {"id": "E01", "name": "Elena",        "email": "elena@correo.es"},       # No termina en .com
    ]

    for r in invalids:
        ok, msg = service.new_register(r)
        print(f"  {'✓' if ok else '✗'} {msg}")

    # ── 3. LIST — ordenado por nombre ────────
    section(3, f"Listando registros ordenados por nombre ({service.get_records_count()} total)")
    display_records(service.list_records(order_by="name"))

    # ── 4. LIST — ordenado por ID ─────────────
    section(4, "Listando registros ordenados por ID")
    display_records(service.list_records(order_by="id"))

    # ── 5. SEARCH ─────────────────────────────
    section(5, "Búsqueda por texto: 'garcia'")
    results = service.search_record("garcia")
    display_records(results)
    print(f"  → {len(results)} resultado(s) encontrado(s)")

    section(5.1, "Búsqueda por texto: 'gmail'")
    results = service.search_record("gmail")
    display_records(results)
    print(f"  → {len(results)} resultado(s) encontrado(s)")

    section(5.2, "Búsqueda sin resultados: 'xyz123'")
    results = service.search_record("xyz123")
    display_records(results)
    print(f"  → {len(results)} resultado(s) encontrado(s)")

    # ── 6. GET BY ID ──────────────────────────
    section(6, "Obtener registro por ID: 'M01'")
    ok, result = service.get_record_by_id("M01")
    if ok:
        print(f"  Encontrado → {result}")
    else:
        print(f"  ✗ {result}")

    section(6.1, "Obtener registro por ID inexistente: 'ZZZ'")
    ok, result = service.get_record_by_id("ZZZ")
    print(f"  {'Encontrado' if ok else '✗'} → {result}")

    # ── 7. UPDATE ─────────────────────────────
    section(7, "Actualizando email de 'J01'")
    ok, msg = service.update_record("J01", {"email": "juanperez.nuevo@gmail.com"})
    print(f"  {'✓' if ok else '✗'} {msg}")

    section(7.1, "Actualización con email inválido en 'C01'")
    ok, msg = service.update_record("C01", {"email": "no-es-valido"})
    print(f"  {'✓' if ok else '✗'} {msg}")

    section(7.2, "Actualización de ID inexistente 'ZZZ'")
    ok, msg = service.update_record("ZZZ", {"name": "Fantasma"})
    print(f"  {'✓' if ok else '✗'} {msg}")

    # ── 8. DELETE ─────────────────────────────
    section(8, "Eliminando registro 'L01'")
    ok, msg = service.delete_record("L01")
    print(f"  {'✓' if ok else '✗'} {msg}")

    section(8.1, "Intentando eliminar 'L01' de nuevo (ya no existe)")
    ok, msg = service.delete_record("L01")
    print(f"  {'✓' if ok else '✗'} {msg}")

    # ── 9. Estado final ───────────────────────
    section(9, f"Estado final ({service.get_records_count()} registros) — ordenado por nombre")
    display_records(service.list_records(order_by="name"))

    print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    main()