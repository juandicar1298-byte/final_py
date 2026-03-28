#!/usr/bin/env python3
"""
Sistema de Gestión de Información
Aplicación principal - Módulo 1
"""

from service import RecordService


def display_records(service):
    """Muestra todos los registros de forma formateada"""
    records = service.get_all_records()
    
    if not records:
        print("  (Sin registros)")
        return
    
    print(f"  {'ID':<10} {'Nombre':<20} {'Email':<30}")
    print("  " + "-" * 60)
    
    for record in records:
        print(f"  {str(record['id']):<10} {record['name']:<20} {record['email']:<30}")


def main():
    """Función principal del sistema"""
    print("\nSistema de Gestión de Información\n")
    
    # Inicializar servicio
    service = RecordService()
    
    # === Crear registros de ejemplo ===
    print("[1] Creando registros...")
    
    registros = [
        {"id": "J01", "name": "Juan Pérez", "email": "juanperez@gmail.com"},
        {"id": "M01", "name": "María García", "email": "mariagarcia@hotmail.com"},
        {"id": "C01", "name": "Carlos López", "email": "carloslopez@yahoo.com"},
    ]
    
    for registro in registros:
        success, message = service.create_record(registro)
        print(f"  • {message}")
    
    # === Listar todos los registros ===
    print(f"\n[2] Listando registros ({service.get_records_count()} total):")
    display_records(service)
    
    # === Intentar crear un registro con ID duplicado ===
    print("\n[3] Intentando crear registro con ID duplicado...")
    success, message = service.create_record(
        {"id": "J01", "name": "Pedro Ruiz", "email": "pedroruiz@gmail.com"}
    )
    print(f"  • {message}")
    
    # === Intentar crear registro con validaciones fallidas ===
    print("\n[4] Intentando crear registros con datos inválidos...")
    
    invalid_records = [
        {"id": "A01", "name": "", "email": "test@gmail.com"},  # Nombre vacío
        {"id": "B01", "name": "Ana", "email": "invalid-email"},   # Email sin @
        {"id": "D01", "name": "Diego", "email": "diego@hotmail.es"},   # Email sin .com
    ]
    
    for registro in invalid_records:
        success, message = service.create_record(registro)
        print(f"  • {message}")
    
    # === Listar registros finales ===
    print(f"\n[5] Estado final ({service.get_records_count()} registros):")
    display_records(service)
    
    print("\nSistema de Gestión de Información\n")


if __name__ == "__main__":
    main()
