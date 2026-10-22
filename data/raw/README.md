# Data mentah

Folder ini berisi data yang **diambil apa adanya** dari Badan Pusat Statistik (BPS), sebelum
dibersihkan. Tujuannya agar proses pembersihan di notebook bisa ditelusuri dan diverifikasi.

> Semua angka adalah data resmi BPS. Tidak ada nilai sintetis atau hasil interpolasi.
> Tanggal akses: **22 Oktober 2026**.

## 1. `kemiskinan_bps_2020_2025.csv`

Persentase penduduk miskin menurut provinsi.

| Kolom | Tipe | Keterangan |
|---|---|---|
| `provinsi` | teks | nama provinsi (format BPS) |
| `tahun` | bilangan bulat | 2020–2025 |
| `kemiskinan_maret` | desimal | persentase penduduk miskin, periode Maret (%) |
| `kemiskinan_september` | desimal | persentase penduduk miskin, periode September (%), hanya 2024–2025 |

Sumber: BPS, *Jumlah dan Persentase Penduduk Miskin Menurut Provinsi*.
<https://www.bps.go.id/id/statistics-table/3/UkVkWGJVZFNWakl6VWxKVFQwWjVWeTlSZDNabVFUMDkjMw%3D%3D/>

Catatan:

- 2020–2023 berisi **34 provinsi**; 2024–2025 berisi **38 provinsi** setelah pemekaran Papua.
- Kolom September kosong untuk 2020–2023 karena BPS belum menerbitkan angka tersebut
  pada tabel yang diakses.
- Angka Maret dan September **tidak boleh dibandingkan langsung** tanpa memperhatikan musim.

## 2. `tpt_bps_2020_2025.csv`

Tingkat Pengangguran Terbuka (TPT) menurut provinsi, periode Agustus.

| Kolom | Tipe | Keterangan |
|---|---|---|
| `PROVINSI` | teks | nama provinsi, **sengaja dibiarkan berantakan** (huruf besar, `KEP.`) |
| `TAHUN` | bilangan bulat | 2020–2025 |
| `TPT_AGUSTUS` | desimal | TPT (%) |

Sumber: BPS, *Tingkat Pengangguran Terbuka (TPT) dan Tingkat Partisipasi Angkatan Kerja (TPAK)
Menurut Provinsi*.
<https://www.bps.go.id/id/statistics-table/3/V2pOVWJWcHJURGg0U2pONFJYaExhVXB0MUhacVFUMDkjMyMwMDAw/>

Nama provinsi sengaja tidak dirapikan agar tahap *data cleaning* di notebook
(bagian 4) mencerminkan pekerjaan nyata: `DKI JAKARTA` → `DKI Jakarta`,
`KEP. RIAU` → `Kepulauan Riau`.

## 3. `nasional_bps_2020_2025.csv`

Angka nasional untuk pembanding.

| Kolom | Keterangan |
|---|---|
| `tahun` | 2020–2025 |
| `kemiskinan_maret` | kemiskinan nasional periode Maret (%) |
| `kemiskinan_september` | kemiskinan nasional periode September (%), hanya 2024–2025 |
| `tpt_agustus` | TPT nasional periode Agustus (%) |

## Hal yang perlu diwaspadai

1. **Pemekaran wilayah Papua (2022).** Papua dan Papua Barat kehilangan sebagian wilayahnya.
   Angka 2020–2023 dan 2024–2025 mengukur wilayah yang berbeda, sehingga keduanya
   tidak sebanding untuk analisis perubahan.
2. **Empat provinsi baru** (Papua Selatan, Papua Tengah, Papua Pegunungan, Papua Barat Daya)
   hanya memiliki data 2024–2025.
3. **Perbedaan periode survei.** Kemiskinan diukur Maret/September, TPT diukur Agustus.
4. **Pembulatan.** BPS menyajikan dua desimal; penjumlahan manual bisa berbeda tipis.

## Cara membuat ulang file ini

```bash
python scripts/build_dataset.py
```

Skrip tersebut menyimpan kembali ketiga CSV di atas ke folder `data/raw/`.
