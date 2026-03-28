def contar_lineas(ruta: str) -> int | None:
    """
    Abre un archivo, cuenta sus líneas y lo cierra de forma segura.
    - except: captura errores de apertura
    - else:   ejecuta la lógica cuando no hubo error
    - finally: garantiza el cierre del archivo
    Retorna el número de líneas, o None si hubo error.
    """
    archivo = None
    try:
        archivo = open(ruta, "r", encoding="utf-8")
    except FileNotFoundError:
        print(f"Error: el archivo '{ruta}' no existe.")
        return None
    except PermissionError:
        print(f"Error: sin permisos para leer '{ruta}'.")
        return None
    except OSError as e:
        print(f"Error al abrir el archivo: {e}")
        return None
    else:
        # Solo se ejecuta si open() tuvo éxito
        lineas = archivo.readlines()
        total = len(lineas)
        print(f"El archivo tiene {total} línea(s).")
        return total
    finally:
        # Se ejecuta SIEMPRE, haya o no error
        if archivo is not None:
            archivo.close()
        print("Operación finalizada.")


# --- Ejecución ---
ruta = input("Ingrese la ruta del archivo: ")
contar_lineas(ruta)