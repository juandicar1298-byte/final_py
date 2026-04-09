#!/usr/bin/env python3
"""
Módulo 4 — Menú interactivo en consola (UI)
Conecta las opciones del menú al CRUD de RecordService.
"""

from colorama import init, Fore, Style
from service import RecordService

# Inicializar colorama (autoreset evita resetear manualmente cada línea)
init(autoreset=True)

# ──────────────────────────────────────────────
# Constantes de color / estilo
# ──────────────────────────────────────────────
C_TITLE   = Fore.CYAN  + Style.BRIGHT
C_OPTION  = Fore.WHITE + Style.BRIGHT
C_OK      = Fore.GREEN + Style.BRIGHT
C_ERROR   = Fore.RED   + Style.BRIGHT
C_INFO    = Fore.YELLOW
C_RESET   = Style.RESET_ALL

HEADER = f"  {'ID':<10} {'Nombre':<22} {'Email':<35}"
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
    """Imprime una tabla formateada con los registros."""
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
# Acciones del menú
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

    # Sub-opción: orden
    print(C_INFO + "\n  Ordenar por:")
    print("    1. Nombre")
    print("    2. ID")
    choice = input(C_OPTION + "  Selecciona (1/2) [por defecto: nombre]: " + C_RESET).strip()
    order = "id" if choice == "2" else "name"

    records = service.list_records(order_by=order)
    clear_line()
    display_records(records)


def action_search(service: RecordService):
    print_section("Buscar registro")
    query = input_field("Texto a buscar (nombre o email)")
    results = service.search_record(query)
    clear_line()
    display_records(results)
    print(C_INFO + f"\n  → {len(results)} resultado(s) encontrado(s)")


def action_get_by_id(service: RecordService):
    print_section("Obtener registro por ID")
    rid = input_field("ID del registro")
    ok, result = service.get_record_by_id(rid)
    if ok:
        print_ok(f"Registro encontrado:")
        print(f"  {C_OPTION}ID:    {C_RESET}{result['id']}")
        print(f"  {C_OPTION}Nombre:{C_RESET} {result['name']}")
        print(f"  {C_OPTION}Email: {C_RESET}{result['email']}")
    else:
        print_err(result)


def action_update(service: RecordService):
    print_section("Actualizar registro")
    rid = input_field("ID del registro a editar")

    # Verificar que existe antes de pedir campos
    ok, result = service.get_record_by_id(rid)
    if not ok:
        print_err(result)
        return

    print(C_INFO + "  Deja en blanco los campos que no desees modificar.")
    new_name  = input_field("Nuevo nombre", required=False)
    new_email = input_field("Nuevo email",  required=False)

    changes = {}
    if new_name:
        changes["name"] = new_name
    if new_email:
        changes["email"] = new_email

    if not changes:
        print_err("No se indicó ningún cambio.")
        return

    ok, msg = service.update_record(rid, changes)
    print_ok(msg) if ok else print_err(msg)


def action_delete(service: RecordService):
    print_section("Eliminar registro")
    rid = input_field("ID del registro a eliminar")

    # Confirmar antes de borrar
    confirm = input(
        C_ERROR + f"  ¿Seguro que deseas eliminar '{rid}'? (s/N): " + C_RESET
    ).strip().lower()

    if confirm != "s":
        print(C_INFO + "  Operación cancelada.")
        return

    ok, msg = service.delete_record(rid)
    print_ok(msg) if ok else print_err(msg)


# ──────────────────────────────────────────────
# Menú principal
# ──────────────────────────────────────────────

MENU_OPTIONS = {
    "1": ("Crear registro",           action_create),
    "2": ("Listar registros",         action_list),
    "3": ("Buscar registro",          action_search),
    "4": ("Obtener registro por ID",  action_get_by_id),
    "5": ("Actualizar registro",      action_update),
    "6": ("Eliminar registro",        action_delete),
    "0": ("Salir",                    None),
}


def print_menu(service: RecordService):
    print_title("Sistema de Gestión de Información")
    print(C_INFO + f"  Registros en sistema: {service.get_records_count()}\n")
    for key, (label, _) in MENU_OPTIONS.items():
        color = C_ERROR if key == "0" else C_OPTION
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
            # Ctrl+C o Ctrl+D cierran limpiamente
            print(C_INFO + "\n\n  Saliendo… ¡Hasta luego!")
            break

        if choice not in MENU_OPTIONS:
            print_err("Opción inválida. Por favor ingresa un número del menú.")
            press_enter()
            continue

        label, action = MENU_OPTIONS[choice]

        if action is None:          # Opción "Salir"
            print(C_INFO + "\n  ¡Hasta luego!\n")
            break

        try:
            action(service)
        except Exception as exc:    # Salvaguarda ante errores inesperados
            print_err(f"Error inesperado: {exc}")

        press_enter()