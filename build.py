#!/usr/bin/env python3
"""Build postal_codes.* and bank_codes.* from source data."""
import csv, json, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTAL_URL = ("https://raw.githubusercontent.com/donma/"
              "TaiwanAddressCityAreaRoadChineseEnglishJSON/master/CityCountyData.json")

def build_postal():
    raw = urllib.request.urlopen(POSTAL_URL, timeout=30).read().decode("utf-8-sig")
    rows = []
    for city in json.loads(raw):
        # The source repeats these as pseudo-cities; keep them under their real county/city.
        if city["CityName"] in ("釣魚臺", "南海島"):
            continue
        for a in city["AreaList"]:
            rows.append({
                "zip3": a["ZipCode"],
                "city": city["CityName"],
                "district": a["AreaName"],
                "city_en": city["CityEngName"],
                "district_en": a["AreaEngName"],
            })
    rows.sort(key=lambda r: r["zip3"])
    # Note: one zip3 can cover several districts (e.g. 300 Hsinchu City, 600 Chiayi City).
    keys = [(r["zip3"], r["city"], r["district"]) for r in rows]
    assert len(keys) == len(set(keys)), "duplicate record"
    assert all(len(r["zip3"]) == 3 and r["zip3"].isdigit() for r in rows), "bad zip3 format"
    spot = {"103": "大同區", "105": "松山區", "330": "桃園區", "414": "烏日區", "911": "竹田鄉"}
    by = {r["zip3"]: r["district"] for r in rows}
    for k, v in spot.items():
        assert by.get(k) == v, f"spot check failed: {k} -> {by.get(k)}"
    return rows

def build_banks():
    rows = list(csv.DictReader(open(ROOT / "data/banks_source.csv", encoding="utf-8")))
    rows.sort(key=lambda r: r["code"])
    for r in rows:
        r["sources"] = r["sources"].split(";")
    return rows

def write(name, rows, fields):
    out = ROOT / name
    out.with_suffix(".json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with open(out.with_suffix(".csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: (";".join(v) if isinstance(v, list) else v) for k, v in r.items()})

if __name__ == "__main__":
    postal = build_postal()
    banks = build_banks()
    write("postal_codes", postal, ["zip3", "city", "district", "city_en", "district_en"])
    write("bank_codes", banks, ["code", "name", "short_name", "category", "sources"])
    print(f"postal: {len(postal)} records, banks: {len(banks)} records")
