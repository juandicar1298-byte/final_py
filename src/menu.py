#!/usr/bin/env python3
"""
Sistema de Gestión de Información
Módulo 4 + 5 — Menú interactivo en consola (UI)
Opción 7: Generar registros falsos con Faker
"""

from colorama import init, Fore, Style
from service import RecordService
from integration import generate_fake_records, build_record

init(autoreset=True)

# ──────────────────────────────────────────────
# Constantes de color / estilo
# ──────────────────────────────────────────────
C_TITLE  = Fore.CYAN   + Style.BRIGHT
C_OPTION = Fore.WHITE  + Style.BRIGHT
C_OK     = Fore.GREEN  + Style.BRIGHT
C_ERROR  = Fore.RED    + Style.BRIGHT
C_INFO   = Fore.YELLOW
C_FAKE   = Fore.MAGENTA + Style.BRIGHT
C_RESET  = Style.RESET_ALL

HEADER  = f"  {'ID':<10} {'Nombre':<22} {'Email':<35}"
DIVIDER = "  " + "─" * 67


# ──────────────────────────────────────────────
# Utilidades de presentación
# ──────────────────────────────────────────────

def clear_line():
    print()

def print_title(text: str):
    print(C_TITLE + "\n" + "═" * 52)
    print(C_TITLE + f"  {text}")
    print(C_TITLE + "═" * 52)

def print_section(text: str):
    print(C_INFO + f"\n  ── {text} ──")

def print_ok(msg: str):
    print(C_OK + f"  ✓ {msg}")

def print_err(msg: str):
    print(C_ERROR + f"  ✗ {msg}")

def display_records(records: list):
    if not records:
        print(C_INFO + "  (Sin registros)")
        return
    print(C_OPTION + HEADER)
    print(C_INFO   + DIVIDER)
    for r in records:
        print(f"  {str(r['id']):<10} {r['name']:<22} {r['email']:<35}")

def input_field(label: str, required: bool = True) -> str:
    """Pide un campo al usuario; si es requerido no acepta vacío."""
    while True:
        value = input(C_OPTION + f"  {label}: " + C_RESET).strip()
        if value or not required:
            return value
        print_err("Este campo no puede estar vacío.")

def press_enter():
    input(C_INFO + "\n  [Presiona Enter para continuar…]" + C_RESET)


# ──────────────────────────────────────────────
# Acciones del menú — Módulo 4
# ──────────────────────────────────────────────

def action_create(service: RecordService):
    print_section("Nuevo registro")
    record = {
        "id":    input_field("ID del registro"),
        "name":  input_field("Nombre completo"),
        "email": input_field("Email"),
    }
    ok, msg = service.new_register(record)
    print_ok(msg) if ok else print_err(msg)


def action_list(service: RecordService):
    print_section(f"Listado de registros ({service.get_records_count()} total)")
    print(C_INFO + "\n  Ordenar por:")
    print("    1. Nombre")
    print("    2. ID")
    choice = input(C_OPTION + "  Selecciona (1/2) [por defecto: nombre]: " + C_RESET).strip()
    order  = "id" if choice == "2" else "name"
    records = service.list_records(order_by=order)
    clear_line()
    display_records(records)


def action_search(service: RecordService):
    print_section("Buscar registro")
    query   = input_field("Texto a buscar (nombre o email)")
    results = service.search_record(query)
    clear_line()
    display_records(results)
    print(C_INFO + f"\n  → {len(results)} resultado(s) encontrado(s)")


def action_get_by_id(service: RecordService):
    print_section("Obtener registro por ID")
    rid = input_field("ID del registro")
    ok, result = service.get_record_by_id(rid)
    if ok:
        print_ok("Registro encontrado:")
        print(f"  {C_OPTION}ID:    {C_RESET}{result['id']}")
        print(f"  {C_OPTION}Nombre:{C_RESET} {result['name']}")
        print(f"  {C_OPTION}Email: {C_RESET}{result['email']}")
    else:
        print_err(result)


def action_update(service: RecordService):
    print_section("Actualizar registro")
    rid = input_field("ID del registro a editar")

    ok, result = service.get_record_by_id(rid)
    if not ok:
        print_err(result)
        return

    print(C_INFO + "  Deja en blanco los campos que no desees modificar.")
    new_name  = input_field("Nuevo nombre", required=False)
    new_email = input_field("Nuevo email",  required=False)

    changes = {}
    if new_name:
        changes["name"]  = new_name
    if new_email:
        changes["email"] = new_email

    if not changes:
        print_err("No se indicó ningún cambio.")
        return

    ok, msg = service.update_record(rid, changes)
    print_ok(msg) if ok else print_err(msg)


def action_delete(service: RecordService):
    print_section("Eliminar registro")
    rid     = input_field("ID del registro a eliminar")
    confirm = input(
        C_ERROR + f"  ¿Seguro que deseas eliminar '{rid}'? (s/N): " + C_RESET
    ).strip().lower()

    if confirm != "s":
        print(C_INFO + "  Operación cancelada.")
        return

    ok, msg = service.delete_record(rid)
    print_ok(msg) if ok else print_err(msg)


# ──────────────────────────────────────────────
# Acción Módulo 5 — Generar registros con Faker
# ──────────────────────────────────────────────

def action_generate_fake(service: RecordService):
    """
    Genera N registros falsos con Faker y los inserta en el sistema.
    Llama a bulk_insert que usa *args/**kwargs internamente.
    """
    print_section("Generar registros falsos con Faker")
    print(C_FAKE + "  Librería: faker  |  Locale: es_MX\n")

    # Pedir cantidad con validación
    while True:
        raw = input(C_OPTION + "  ¿Cuántos registros generar? [por defecto: 10]: " + C_RESET).strip()
        if raw == "":
            n = 10
            break
        try:
            n = int(raw)
            if n < 1:
                raise ValueError
            break
        except ValueError:
            print_err("Ingresa un número entero mayor a 0.")

    print(C_FAKE + f"\n  Generando {n} registros…\n")

    fake_records = generate_fake_records(n)

    # bulk_insert usa *args/**kwargs — skip_errors=True para no parar ante duplicados
    inserted, errors, detail = service.bulk_insert(
        fake_records,
        skip_errors=True,
        prefix="[Faker]"
    )

    for line in detail:
        print(C_OK + line if "✓" in line else C_ERROR + line)

    print(C_FAKE + f"\n  ── Resumen ──")
    print(C_OK   + f"  Insertados : {inserted}")
    if errors:
        print(C_ERROR + f"  Omitidos   : {errors} (ID duplicado)")
    print(C_INFO + f"  Total en sistema: {service.get_records_count()}")


# ──────────────────────────────────────────────
# Menú principal
# ──────────────────────────────────────────────

MENU_OPTIONS = {
    "1": ("Crear registro",                   action_create),
    "2": ("Listar registros",                 action_list),
    "3": ("Buscar registro",                  action_search),
    "4": ("Obtener registro por ID",          action_get_by_id),
    "5": ("Actualizar registro",              action_update),
    "6": ("Eliminar registro",                action_delete),
    "7": ("Generar registros falsos (Faker)", action_generate_fake),  # ← Módulo 5
    "0": ("Salir",                            None),
}


def print_menu(service: RecordService):
    print_title("Sistema de Gestión de Información")
    print(C_INFO + f"  Registros en sistema: {service.get_records_count()}\n")
    for key, (label, _) in MENU_OPTIONS.items():
        if key == "0":
            color = C_ERROR
        elif key == "7":
            color = C_FAKE
        else:
            color = C_OPTION
        print(color + f"  [{key}] {label}")
    clear_line()


def run_menu():
    """Bucle principal del menú interactivo."""
    service = RecordService()

    while True:
        print_menu(service)

        try:
            choice = input(C_OPTION + "  Selecciona una opción: " + C_RESET).strip()
        except (KeyboardInterrupt, EOFError):
            print(C_INFO + "\n\n  Saliendo… ¡Hasta luego!")
            break

        if choice not in MENU_OPTIONS:
            print_err("Opción inválida. Por favor ingresa un número del menú.")
            press_enter()
            continue

        label, action = MENU_OPTIONS[choice]

        if action is None:
            print(C_INFO + "\n  ¡Hasta luego!\n")
            break

        try:
            action(service)
        except Exception as exc:
            print_err(f"Error inesperado: {exc}")

        press_enter()