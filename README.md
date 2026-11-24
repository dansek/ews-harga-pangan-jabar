# Early Warning System Harga Pangan Strategis — Kab/Kota Jawa Barat

Proyek UAS mata kuliah **AI for Innovation**, Magister Inovasi Regional 2026/2027.

Sistem peringatan dini berbasis *machine learning* untuk memprediksi harga 5 komoditas pangan strategis
(beras medium, cabai merah keriting, cabai rawit merah, bawang merah, bawang putih) di 9 kab/kota
Jawa Barat dan memberi sinyal **lonjakan harga** sebelum terjadi, untuk mendukung Tim Pengendalian
Inflasi Daerah (TPID).

## Struktur repositori

```
data/
  raw/pihps_jabar_harian.csv.gz     # data harian PIHPS 2019–2026 (semua komoditas)
  processed/                         # data mingguan hasil pembersihan (output notebook 01)
notebooks/
  01_pengambilan_data_dan_eda.ipynb  # komponen (f) & (g)
scripts/
  fetch_pihps.py                     # penarik data dari API PIHPS
docs/                                # dashboard (GitHub Pages)
```

## Notebook (Google Colab)

| Notebook | Isi | Colab |
|---|---|---|
| 01 | Pengambilan data & EDA | [Buka di Colab](https://colab.research.google.com/github/dansek/ews-harga-pangan-jabar/blob/main/notebooks/01_pengambilan_data_dan_eda.ipynb) |

## Sumber data

Pusat Informasi Harga Pangan Strategis Nasional (PIHPS), Bank Indonesia —
<https://www.bi.go.id/hargapangan>. Harga harian pasar tradisional, 9 kab/kota pantauan di Jawa Barat:
Kota Bandung, Kota Bekasi, Kota Bogor, Kota Cirebon, Kab. Cirebon, Kota Depok, Kota Sukabumi,
Kota Tasikmalaya, Kab. Tasikmalaya.

Menarik ulang data:

```bash
pip install pandas requests
python scripts/fetch_pihps.py --start 2019-01-01
```
