#!/usr/bin/env python3
"""
Sistema de Gestión de Información
Módulo de servicio - Almacenamiento en memoria
"""

from validate import validate_record


class RecordService:
    """
    Servicio para gestionar registros en memoria.
    Utiliza diccionarios para almacenar registros y sets para garantizar IDs únicos.
    """
    
    def __init__(self):
        """Inicializa el servicio con estructuras vacías"""
        self.records = {}  # Diccionario: {id: registro_completo}
        self.ids = set()   # Set para garantizar IDs únicos
    
    def create_record(self, record_data):
        """
        Crea un nuevo registro si es válido y el ID no existe.
        
        Args:
            record_data: Diccionario con id, name, email
            
        Returns:
            tuple: (éxito, mensaje)
        """
        # Validar estructura del registro
        is_valid, error = validate_record(record_data)
        if not is_valid:
            return False, f"Registro inválido: {error}"
        
        record_id = record_data.get("id")
        
        # Verificar si el ID ya existe
        if record_id in self.ids:
            return False, f"El ID '{record_id}' ya existe en el sistema"
        
        # Agregar el registro
        self.records[record_id] = record_data.copy()
        self.ids.add(record_id)
        
        return True, f"Registro '{record_id}' creado exitosamente"
    
    def get_all_records(self):
        """
        Retorna todos los registros almacenados.
        
        Returns:
            list: Lista de diccionarios con los registros
        """
        return list(self.records.values())
    
    def get_record_by_id(self, record_id):
        """
        Obtiene un registro específico por ID.
        
        Args:
            record_id: ID del registro a buscar
            
        Returns:
            dict: El registro si existe, None en caso contrario
        """
        return self.records.get(record_id)
    
    def delete_record(self, record_id):
        """
        Elimina un registro por ID.
        
        Args:
            record_id: ID del registro a eliminar
            
        Returns:
            tuple: (éxito, mensaje)
        """
        if record_id not in self.ids:
            return False, f"El registro con ID '{record_id}' no existe"
        
        del self.records[record_id]
        self.ids.discard(record_id)
        
        return True, f"Registro '{record_id}' eliminado"
    
    def get_records_count(self):
        """
        Retorna la cantidad de registros almacenados.
        
        Returns:
            int: Cantidad de registros
        """
        return len(self.records)
