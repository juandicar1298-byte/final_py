def calcular_promedio(texto: str) -> float | None:
    """
    Lee enteros separados por comas desde un string,
    calcula el promedio y maneja errores de conversión.
    Retorna None si la entrada está vacía o es inválida.
    """
    try:
        numeros = [int(n.strip()) for n in texto.split(",")]
    except ValueError as e:
        print(f"Error de conversión: {e}")
        return None

    if not numeros:
        print("Error: no se ingresaron números.")
        return None

    # Fix lógico: dividir entre len(numeros), no entre un valor fijo
    promedio = sum(numeros) / len(numeros)
    return promedio


# --- Ejecución ---
entrada = input("Ingrese enteros separados por comas: ")
resultado = calcular_promedio(entrada)

if resultado is not None:
    print(f"Promedio: {resultado:.2f}")