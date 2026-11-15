"""Costing rules: 10% consumption tax, material / labor / shipping separated."""
from __future__ import annotations

CONSUMPTION_TAX = 0.10  # standard rate 10% (national 7.8% + local 2.2%), verified by NTA


def material_line(qty: float, unit_price: float, tax_basis: str):
    """Return (subtotal_ex_tax, tax, subtotal_in_tax) yen, rounded to 2 decimals."""
    if tax_basis == "tax_included":
        ex = unit_price * qty / (1 + CONSUMPTION_TAX)
        tax = ex * CONSUMPTION_TAX
        incl = ex + tax
    else:
        ex = unit_price * qty
        tax = ex * CONSUMPTION_TAX
        incl = ex + tax
    return round(ex, 2), round(tax, 2), round(incl, 2)


def labor_line(rate_yen_per_8h: float, hours: float) -> float:
    """Labor pay = 8h unit rate x (hours / 8). Overheads are NOT included."""
    return round(rate_yen_per_8h * hours / 8.0, 2)
