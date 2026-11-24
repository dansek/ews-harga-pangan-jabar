"""Tarik data harga pangan harian PIHPS (Bank Indonesia) untuk kab/kota Jawa Barat.

Sumber : https://www.bi.go.id/hargapangan (Pasar Tradisional, tabel per daerah)
Output : data/raw/pihps_jabar_harian.csv  (format panjang/long)
         kolom: tanggal, kabkota_id, kabkota, kategori, komoditas, harga

Pemakaian:
    python scripts/fetch_pihps.py                      # 2019-01-01 s.d. hari ini
    python scripts/fetch_pihps.py --start 2024-01-01   # rentang lain

Catatan: API lambat untuk rentang panjang (1 tahun ~1 menit, 3 tahun timeout),
jadi data ditarik per bulan dan diparalelkan ringan (4 thread).
"""
from __future__ import annotations

import argparse
import datetime as dt
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd
import requests

BASE = "https://www.bi.go.id/hargapangan/WebSite/TabelHarga/"
PROV_JABAR = 12
HEADERS = {"User-Agent": "Mozilla/5.0 (research script)"}


def get_regencies(prov_id: int = PROV_JABAR) -> list[dict]:
    r = requests.get(BASE + "GetRefRegency", params={"price_type_id": 1, "ref_prov_id": prov_id},
                     headers=HEADERS, timeout=60)
    r.raise_for_status()
    return r.json()["data"]


def month_ranges(start: dt.date, end: dt.date):
    cur = start.replace(day=1)
    while cur <= end:
        nxt = (cur + dt.timedelta(days=32)).replace(day=1)
        yield max(cur, start), min(nxt - dt.timedelta(days=1), end)
        cur = nxt


def fetch_chunk(reg_id: int, reg_name: str, s: dt.date, e: dt.date, retries: int = 4) -> list[dict]:
    params = {
        "price_type_id": 1, "comcat_id": "", "province_id": PROV_JABAR, "regency_id": reg_id,
        "market_id": "", "tipe_laporan": 1,
        "start_date": s.isoformat(), "end_date": e.isoformat(),
    }
    for attempt in range(retries):
        try:
            r = requests.get(BASE + "GetGridDataDaerah", params=params, headers=HEADERS, timeout=90)
            r.raise_for_status()
            rows = r.json().get("data", [])
            break
        except Exception:  # noqa: BLE001 - jaringan/server kadang gagal, coba lagi
            if attempt == retries - 1:
                raise
            time.sleep(2 * (attempt + 1))

    out, kategori = [], None
    for row in rows:
        if row.get("level") == 1:
            kategori = row["name"].strip()
            continue
        nama = row["name"].strip()
        for k, v in row.items():
            if k in ("no", "name", "level"):
                continue
            harga = str(v).replace(",", "").strip()
            out.append({
                "tanggal": dt.datetime.strptime(k, "%d/%m/%Y").date(),
                "kabkota_id": reg_id, "kabkota": reg_name,
                "kategori": kategori, "komoditas": nama,
                "harga": float(harga) if harga.replace(".", "").isdigit() else None,
            })
    return out


def fetch_all(start: dt.date, end: dt.date, workers: int = 4) -> pd.DataFrame:
    regs = get_regencies()
    jobs = [(r["id"], r["name"], s, e) for r in regs for s, e in month_ranges(start, end)]
    records, done = [], 0
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(fetch_chunk, *j) for j in jobs]
        for f in as_completed(futs):
            records.extend(f.result())
            done += 1
            if done % 50 == 0 or done == len(jobs):
                print(f"  {done}/{len(jobs)} potongan selesai", flush=True)
    df = pd.DataFrame.from_records(records)
    df["tanggal"] = pd.to_datetime(df["tanggal"])
    return (df.drop_duplicates(["tanggal", "kabkota_id", "komoditas"])
              .sort_values(["kabkota", "komoditas", "tanggal"])
              .reset_index(drop=True))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2019-01-01")
    ap.add_argument("--end", default=dt.date.today().isoformat())
    ap.add_argument("--out", default=str(Path(__file__).resolve().parents[1] / "data/raw/pihps_jabar_harian.csv"))
    a = ap.parse_args()
    df = fetch_all(dt.date.fromisoformat(a.start), dt.date.fromisoformat(a.end))
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(a.out, index=False)
    print(f"Tersimpan {len(df):,} baris -> {a.out}")


if __name__ == "__main__":
    main()
