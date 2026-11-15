"""Bundled verified snapshot catalog and labor rate lookup."""
from __future__ import annotations
import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"


def _load(name: str) -> list[dict]:
    with open(DATA_DIR / name, "r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def price_snapshot(record_id: str) -> dict | None:
    for row in _load("price_snapshots.csv"):
        if row["record_id"] == record_id:
            return row
    return None


def labor_rate(occupation_key: str, prefecture: str) -> float | None:
    for row in _load("labor_rates_long.csv"):
        if row["occupation_key"] == occupation_key and row["prefecture"] == prefecture:
            return float(row["value_yen"]) if row["value_yen"] else None
    return None
