# Early Warning System Harga Pangan Strategis — Kab/Kota Jawa Barat

Proyek UAS mata kuliah **AI for Innovation**, Magister Inovasi Regional 2026/2027.

Sistem peringatan dini berbasis *machine learning* untuk memprediksi harga 5 komoditas pangan strategis
(beras medium, cabai merah keriting, cabai rawit merah, bawang merah, bawang putih) di 9 kab/kota
Jawa Barat dan memberi sinyal **lonjakan harga** sebelum terjadi, untuk mendukung Tim Pengendalian
Inflasi Daerah (TPID).

**Dashboard:** <https://dansek.github.io/ews-harga-pangan-jabar/>

## Struktur repositori

```
data/
  raw/pihps_jabar_harian.csv.gz     # data harian PIHPS 2019–2026 (semua komoditas)
  processed/                         # data mingguan hasil pembersihan (output notebook 01)
notebooks/
  01_pengambilan_data_dan_eda.ipynb  # komponen (f) & (g)
  02_analisis_prediksi_dan_peringatan_dini.ipynb  # komponen (e) & (h)
scripts/
  fetch_pihps.py                     # penarik data dari API PIHPS
docs/data/dashboard.json             # output notebook 02 untuk dashboard (GitHub Pages)
```

## Notebook (Google Colab)

| Notebook | Isi | Colab |
|---|---|---|
| 01 | Pengambilan data & EDA | [Buka di Colab](https://colab.research.google.com/github/dansek/ews-harga-pangan-jabar/blob/main/notebooks/01_pengambilan_data_dan_eda.ipynb) |
| 02 | Prediksi harga, peringatan dini lonjakan & uji kebutuhan AI | [Buka di Colab](https://colab.research.google.com/github/dansek/ews-harga-pangan-jabar/blob/main/notebooks/02_analisis_prediksi_dan_peringatan_dini.ipynb) |

## Hasil utama (periode uji Jan 2024 – Nov 2026)

- **Prediksi 4 minggu:** MAPE sistem hibrida 11,3 % vs Naive 13,0 % (keunggulan AI signifikan, uji Diebold-Mariano p < 0,05).
- **AI hanya dipakai di komoditas yang membutuhkannya:** cabai rawit merah & bawang merah. Beras, bawang putih, dan
  cabai merah keriting memakai Naive (dipilih pada validasi 2023).
- **Peringatan dini lonjakan > 10 %:** presisi alarm AI 0,50 vs 0,26–0,27 aturan non-AI pada jumlah alarm yang setara.

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
