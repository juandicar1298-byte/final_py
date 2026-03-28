def dividir(a: float, b: float) -> float:
    return a / b   # Puede lanzar ZeroDivisionError


def leer_primera_linea(ruta: str) -> str:
    with open(ruta, "r", encoding="utf-8") as f:
        return f.readline().rstrip()


def menu() -> None:
    while True:
        print("\n=== MENÚ ===")
        print("1. Dividir dos números")
        print("2. Mostrar primera línea de un archivo")
        print("3. Salir")

        try:
            opcion = int(input("Seleccione una opción: "))

            if opcion == 1:
                a = float(input("Dividendo: "))
                b = float(input("Divisor:   "))
                resultado = dividir(a, b)
                print(f"Resultado: {resultado}")

            elif opcion == 2:
                ruta = input("Ruta del archivo: ")
                linea = leer_primera_linea(ruta)
                print(f"Primera línea: {linea}")

            elif opcion == 3:
                print("¡Hasta luego!")
                break

            else:
                print("Opción no válida. Elija 1, 2 o 3.")

        except ValueError:
            print("Error: ingrese un número válido.")
        except ZeroDivisionError:
            print("Error: no se puede dividir entre cero.")
        except FileNotFoundError:
            print("Error: el archivo no fue encontrado.")
        except Exception as e:
            # Captura cualquier error no previsto
            print(f"Error inesperado: {type(e).__name__}: {e}")


# --- Ejecución ---
menu()