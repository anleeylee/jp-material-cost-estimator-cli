"""Estimate workbook CLI.

Input CSV columns:
  item_id, kind(material|labor), description, qty, unit_price_yen,
  price_tax_basis(tax_included|tax_excluded), snapshot_ref,
  occupation_key, prefecture, hours, shipping_cost_yen
"""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path

from . import catalog, costing


def estimate(rows: list[dict]) -> dict:
    items, notes = [], []
    total_ex = total_tax = total_incl = total_labor = total_shipping = 0.0

    for row in rows:
        kind = row.get("kind", "material").strip()
        out = {"item_id": row.get("item_id", ""), "kind": kind,
               "description": row.get("description", ""), "provenance": "", "note": ""}

        if kind == "labor":
            occ = row.get("occupation_key", "")
            pref = row.get("prefecture", "")
            rate = catalog.labor_rate(occ, pref)
            hours = float(row.get("hours") or 0)
            if rate is None:
                out["note"] = f"no labor rate for {occ}/{pref}; excluded from total"
                notes.append(out["note"])
                items.append(out)
                continue
            pay = costing.labor_line(rate, hours)
            out.update({"rate_yen_per_8h": rate, "hours": hours, "labor_yen": pay,
                        "provenance": "REGISTRY:MLIT-public-works-labor-rate"})
            total_labor += pay
            items.append(out)
            continue

        snapshot_ref = row.get("snapshot_ref", "")
        snapshot = catalog.price_snapshot(snapshot_ref) if snapshot_ref else None
        if snapshot:
            price = float(snapshot["price_tax_included_yen"] or snapshot["price_tax_excluded_yen"])
            basis = "tax_included" if snapshot["price_tax_included_yen"] else "tax_excluded"
            out["provenance"] = f"REGISTRY:{snapshot_ref}:{snapshot['verification_status']}"
            if snapshot["verification_status"] != "VERIFIED_PRICE_SNAPSHOT":
                out["note"] = "snapshot pending human verification"
        else:
            price = float(row.get("unit_price_yen") or 0)
            basis = row.get("price_tax_basis", "tax_excluded")
            out["provenance"] = "USER_SUPPLIED:price-not-verified"
            out["note"] = "user-entered price; engine does not verify it"

        qty = float(row.get("qty") or 0)
        ex, tax, incl = costing.material_line(qty, price, basis)
        shipping = float(row.get("shipping_cost_yen") or 0)
        out.update({"qty": qty, "unit_price_yen": price, "price_tax_basis": basis,
                    "subtotal_ex_tax_yen": ex, "consumption_tax_yen": tax,
                    "subtotal_in_tax_yen": incl, "shipping_yen": shipping})
        total_ex += ex; total_tax += tax; total_incl += incl; total_shipping += shipping
        items.append(out)

    grand_total = round(total_incl + total_shipping + total_labor, 2)
    return {
        "items": items,
        "totals": {
            "materials_ex_tax_yen": round(total_ex, 2),
            "consumption_tax_yen": round(total_tax, 2),
            "materials_in_tax_yen": round(total_incl, 2),
            "shipping_yen": round(total_shipping, 2),
            "labor_yen": round(total_labor, 2),
            "grand_total_yen": grand_total,
        },
        "notes": notes,
        "scope": "Materials (tax included) + shipping + labor only. Excludes site management, general overhead, demolition, waste disposal and provisional works.",
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="Offline Japanese construction estimate workbook.")
    ap.add_argument("--input", required=True)
    ap.add_argument("--output")
    ap.add_argument("--format", choices=["csv", "json"], default="json")
    args = ap.parse_args(argv)

    with open(args.input, "r", encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    report = estimate(rows)

    if not args.output:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    if args.format == "json":
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        fields = ["item_id", "kind", "description", "qty", "unit_price_yen", "price_tax_basis",
                  "subtotal_ex_tax_yen", "consumption_tax_yen", "subtotal_in_tax_yen",
                  "labor_yen", "shipping_yen", "provenance", "note"]
        with open(out, "w", encoding="utf-8-sig", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
            w.writeheader()
            for it in report["items"]:
                w.writerow(it)
            w.writerow({f: "" for f in fields})
            w.writerow({"item_id": "TOTAL", "description": report["scope"],
                        "subtotal_ex_tax_yen": report["totals"]["materials_ex_tax_yen"],
                        "consumption_tax_yen": report["totals"]["consumption_tax_yen"],
                        "subtotal_in_tax_yen": report["totals"]["materials_in_tax_yen"],
                        "labor_yen": report["totals"]["labor_yen"],
                        "shipping_yen": report["totals"]["shipping_yen"]})


if __name__ == "__main__":
    main()
