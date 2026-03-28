# ── Excepciones ────────────────────────────────────────────────────────
class VentaInvalidaError(ValueError):
    """La venta no tiene status 'ok'."""


# ── Funciones puras (lógica sin I/O) ──────────────────────────────────
def calcular_descuento(quantity: int, customer: str) -> float:
    """
    Determina el descuento total según cantidad y tipo de cliente.

    - Cantidad >= 10 → 10% de descuento
    - Cliente 'vip'  → +5% adicional
    """
    discount = 0.0
    if quantity >= 10:
        discount += 0.10
    if customer == "vip":
        discount += 0.05
    return discount


def calculate_sale_total(sale: dict) -> float:
    """
    Calcula el subtotal de una venta individual.

    Parámetros esperados en sale:
        status   -- debe ser "ok", si no lanza VentaInvalidaError
        price    -- precio unitario (float)
        qty      -- cantidad (int)
        customer -- tipo de cliente (str)

    Lanza VentaInvalidaError para ventas con status != "ok".
    """
    if sale.get("status") != "ok":
        raise VentaInvalidaError(
            f"Venta ignorada (status='{sale.get('status')}'): {sale}"
        )

    price    = sale["price"]
    quantity = sale["qty"]
    customer = sale.get("customer", "")

    discount = calcular_descuento(quantity, customer)
    subtotal = price * quantity
    subtotal -= subtotal * discount
    return subtotal


def calculate_total(sales: list[dict]) -> float:
    """
    Suma los totales de todas las ventas válidas.
    Las ventas inválidas se ignoran (no se suman ni se imprimen).
    """
    total = 0.0
    for sale in sales:
        try:
            total += calculate_sale_total(sale)
        except VentaInvalidaError:
            pass   # Ignoramos ventas inválidas silenciosamente
    return total


# ── I/O separada ───────────────────────────────────────────────────────
def report_invalid_sales(sales: list[dict]) -> None:
    """Imprime las ventas con status != 'ok' (separado del cálculo)."""
    for sale in sales:
        if sale.get("status") != "ok":
            print(f"Venta inválida: {sale}")


# ── Pruebas ────────────────────────────────────────────────────────────
ventas = [
    {"status": "ok",  "price": 100.0, "qty":  5, "customer": "normal"},  # sin descuento → 500.00
    {"status": "ok",  "price": 100.0, "qty": 10, "customer": "normal"},  # -10%          → 900.00
    {"status": "ok",  "price": 100.0, "qty": 10, "customer": "vip"},     # -15%          → 850.00
    {"status": "bad", "price": 200.0, "qty":  3, "customer": "normal"},  # inválida       → ignorada
    {"status": "ok",  "price":  50.0, "qty":  2, "customer": "vip"},     # solo -5%      →  95.00
]

# Total esperado: 500 + 900 + 850 + 95 = 2345.00
total = calculate_total(ventas)
print(f"Total ventas válidas: ${total:.2f}")   # → $2345.00

print()
report_invalid_sales(ventas)