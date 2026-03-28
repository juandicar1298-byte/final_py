def is_valid_password(password: str) -> bool:
    """
    Valida que una contraseña cumpla todas las reglas de seguridad.

    Reglas:
        1. Longitud mínima de 8 caracteres.
        2. Debe contener al menos un dígito.
        3. Debe contener al menos una letra mayúscula.
        4. No puede contener espacios.

    Retorna True si cumple todas las reglas, False si falla alguna.
    Usa retornos tempranos para claridad y facilidad de extensión.
    """
    if len(password) < 8:
        return False

    if not any(caracter.isdigit() for caracter in password):
        return False

    if not any(caracter.isupper() for caracter in password):
        return False

    if " " in password:
        return False

    return True


# ── Pruebas ────────────────────────────────────────────────────────────
casos = [
    ("Abcdefg1",  True,  "válida"),
    ("abcdefg1",  False, "sin mayúscula"),
    ("ABCDEFGH",  False, "sin número"),
    ("Ab1 defg",  False, "contiene espacio"),
    ("Ab1defg",   False, "muy corta (7 chars)"),
    ("Ab1defgh",  True,  "exactamente 8 chars"),
    ("A1bcdefgh", True,  "número al inicio"),
]

print(f"{'Contraseña':<15} {'Esperado':<10} {'Obtenido':<10} {'Caso'}")
print("-" * 55)
for pwd, esperado, descripcion in casos:
    obtenido = is_valid_password(pwd)
    estado = "✓" if obtenido == esperado else "✗ FALLA"
    print(f"{pwd:<15} {str(esperado):<10} {str(obtenido):<10} {descripcion}  {estado}")