"""
Membuat file data mentah (raw) dari angka resmi BPS.

Sumber:
- Kemiskinan: BPS, "Jumlah dan Persentase Penduduk Miskin Menurut Provinsi",
  tabel statistik tahun 2020-2025 (angka Maret; September 2024 & 2025).
  https://www.bps.go.id/id/statistics-table/3/UkVkWGJVZFNWakl6VWxKVFQwWjVWeTlSZDNabVFUMDkjMw%3D%3D/
- Pengangguran: BPS, "Tingkat Pengangguran Terbuka (TPT) Menurut Provinsi",
  Tabel Dinamis, angka Agustus 2020-2025.
  https://www.bps.go.id/id/query-builder
- Tanggal akses: 22 Oktober 2026.

Catatan:
- Tanda None berarti data belum tersedia (provinsi baru hasil pemekaran
  belum punya seri historis, atau September belum diterbitkan pada tabel).
- Nama provinsi sengaja dibiarkan seperti aslinya di BPS (huruf besar dan
  singkatan "KEP.") agar proses pembersihan di notebook terlihat nyata.
"""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"

PROVINSI = [
    "Aceh", "Sumatera Utara", "Sumatera Barat", "Riau", "Jambi",
    "Sumatera Selatan", "Bengkulu", "Lampung", "Kepulauan Bangka Belitung",
    "Kepulauan Riau", "DKI Jakarta", "Jawa Barat", "Jawa Tengah",
    "DI Yogyakarta", "Jawa Timur", "Banten", "Bali", "Nusa Tenggara Barat",
    "Nusa Tenggara Timur", "Kalimantan Barat", "Kalimantan Tengah",
    "Kalimantan Selatan", "Kalimantan Timur", "Kalimantan Utara",
    "Sulawesi Utara", "Sulawesi Tengah", "Sulawesi Selatan",
    "Sulawesi Tenggara", "Gorontalo", "Sulawesi Barat", "Maluku",
    "Maluku Utara", "Papua Barat", "Papua Barat Daya", "Papua",
    "Papua Selatan", "Papua Tengah", "Papua Pegunungan",
]

# Persentase penduduk miskin - Maret (%)
MISKIN_MARET = {
    2020: [14.99, 8.75, 6.28, 6.82, 7.58, 12.66, 15.03, 12.34, 4.53, 5.92,
           4.53, 7.88, 11.41, 12.28, 11.09, 5.92, 3.78, 13.97, 20.90, 7.17,
           4.82, 4.38, 6.10, 6.80, 7.62, 12.92, 8.72, 11.00, 15.22, 10.87,
           17.44, 6.78, 21.37, None, 26.64, None, None, None],
    2021: [15.33, 9.01, 6.63, 7.12, 8.09, 12.84, 15.22, 12.62, 4.90, 6.12,
           4.72, 8.40, 11.79, 12.80, 11.40, 6.66, 4.53, 14.14, 20.99, 7.15,
           5.16, 4.83, 6.54, 7.36, 7.77, 13.00, 8.78, 11.66, 15.61, 11.29,
           17.87, 6.89, 21.84, None, 26.86, None, None, None],
    2022: [14.64, 8.42, 5.92, 6.78, 7.62, 11.90, 14.62, 11.57, 4.45, 6.24,
           4.69, 8.06, 10.93, 11.34, 10.38, 6.16, 4.57, 13.68, 20.05, 6.73,
           5.28, 4.49, 6.31, 6.77, 7.28, 12.33, 8.63, 11.17, 15.42, 11.75,
           15.97, 6.23, 21.33, None, 26.56, None, None, None],
    2023: [14.45, 8.15, 5.95, 6.68, 7.58, 11.78, 14.04, 11.11, 4.52, 5.69,
           4.44, 7.62, 10.77, 11.04, 10.35, 6.17, 4.25, 13.85, 19.96, 6.71,
           5.11, 4.29, 6.11, 6.45, 7.38, 12.41, 8.70, 11.43, 15.15, 11.49,
           16.42, 6.46, 20.49, None, 26.03, None, None, None],
    2024: [14.23, 7.99, 5.97, 6.67, 7.10, 10.97, 13.56, 10.69, 4.55, 5.37,
           4.30, 7.46, 10.47, 10.83, 9.79, 5.84, 4.00, 12.91, 19.48, 6.32,
           5.17, 4.11, 5.78, 6.32, 7.25, 11.77, 8.06, 11.21, 14.57, 11.21,
           16.05, 6.32, 21.66, 18.13, 17.26, 17.44, 29.76, 32.97],
    2025: [12.33, 7.36, 5.35, 6.16, 7.19, 10.15, 12.08, 10.00, 5.00, 4.44,
           4.28, 7.02, 9.48, 10.23, 9.50, 5.63, 3.72, 11.78, 18.60, 6.16,
           5.19, 3.84, 5.17, 5.54, 6.71, 10.92, 7.60, 10.54, 13.24, 10.41,
           15.38, 5.81, 20.66, 17.95, 19.16, 19.71, 28.90, 30.03],
}

# Persentase penduduk miskin - September (%) - hanya tersedia 2024 & 2025
MISKIN_SEPTEMBER = {
    2024: [12.64, 7.19, 5.42, 6.36, 7.26, 10.51, 12.52, 10.62, 5.08, 4.78,
           4.14, 7.08, 9.58, 10.40, 9.56, 5.70, 3.80, 11.91, 19.02, 6.25,
           5.26, 4.02, 5.51, 5.38, 6.70, 11.04, 7.77, 10.63, 13.87, 10.71,
           15.78, 6.03, 21.09, 16.95, 18.09, 19.35, 27.60, 29.66],
    2025: [12.22, 7.24, 5.31, 6.30, 6.89, 9.85, 11.88, 9.66, 4.77, 4.26,
           4.03, 6.78, 9.39, 10.08, 9.30, 5.51, 3.42, 11.38, 17.50, 5.97,
           4.94, 3.73, 5.19, 5.47, 6.62, 10.52, 7.43, 10.14, 12.62, 10.18,
           15.25, 5.59, 19.58, 17.50, 17.82, 19.26, 29.45, 27.21],
}

# Tingkat Pengangguran Terbuka - Agustus (%)
TPT_AGUSTUS = {
    2020: [6.59, 6.91, 6.88, 6.32, 5.13, 5.51, 4.07, 4.67, 5.25, 10.34,
           10.95, 10.46, 6.48, 4.57, 5.84, 10.64, 5.63, 4.22, 4.28, 5.81,
           4.58, 4.74, 6.87, 4.97, 7.37, 3.77, 6.31, 4.58, 4.28, 3.32,
           7.57, 5.15, 6.80, None, 4.28, None, None, None],
    2021: [6.30, 6.33, 6.52, 4.42, 5.09, 4.98, 3.65, 4.69, 5.03, 9.91,
           8.50, 9.82, 5.95, 4.56, 5.74, 8.98, 5.37, 3.01, 3.77, 5.82,
           4.53, 4.95, 6.83, 4.58, 7.06, 3.75, 5.72, 3.92, 3.01, 3.13,
           6.93, 4.71, 5.84, None, 3.33, None, None, None],
    2022: [6.17, 6.16, 6.28, 4.37, 4.59, 4.63, 3.59, 4.52, 4.77, 8.23,
           7.18, 8.31, 5.57, 4.06, 5.49, 8.09, 4.80, 2.89, 3.54, 5.11,
           4.26, 4.74, 5.71, 4.33, 6.61, 3.00, 4.51, 3.36, 2.58, 2.34,
           6.88, 3.98, 5.37, None, 2.83, None, None, None],
    2023: [6.03, 5.89, 5.94, 4.23, 4.53, 4.11, 3.42, 4.23, 4.56, 6.80,
           6.53, 7.44, 5.13, 3.69, 4.88, 7.52, 2.69, 2.80, 3.14, 5.05,
           4.10, 4.31, 5.31, 4.01, 6.10, 2.95, 4.33, 3.15, 3.06, 2.27,
           6.31, 4.31, 5.38, None, 2.67, None, None, None],
    2024: [5.75, 5.60, 5.75, 3.70, 4.48, 3.86, 3.11, 4.19, 4.63, 6.39,
           6.21, 6.75, 4.78, 3.48, 4.19, 6.68, 1.79, 2.73, 3.02, 4.86,
           4.01, 4.20, 5.14, 3.90, 5.85, 2.94, 4.19, 3.09, 3.13, 2.68,
           6.11, 4.03, 4.13, 6.48, 6.48, 4.05, 2.75, 1.32],
    2025: [5.64, 5.32, 5.62, 4.16, 4.26, 3.69, 3.41, 4.21, 4.45, 6.45,
           6.05, 6.77, 4.66, 3.46, 3.88, 6.69, 1.49, 3.06, 3.31, 4.82,
           3.97, 4.16, 5.18, 3.85, 5.99, 2.92, 4.21, 3.31, 3.42, 2.86,
           6.27, 4.55, 4.55, 6.85, 6.96, 4.04, 3.62, 1.68],
}

NASIONAL = [
    # tahun, kemiskinan_maret, kemiskinan_september, tpt_agustus
    (2020, 9.78, None, 7.07),
    (2021, 10.14, None, 6.49),
    (2022, 9.54, None, 5.86),
    (2023, 9.36, None, 5.32),
    (2024, 9.03, 8.57, 4.91),
    (2025, 8.47, 8.25, 4.85),
]


def tulis_kemiskinan():
    path = RAW / "kemiskinan_bps_2020_2025.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["provinsi", "tahun", "kemiskinan_maret", "kemiskinan_september"])
        for tahun in range(2020, 2026):
            for i, prov in enumerate(PROVINSI):
                maret = MISKIN_MARET[tahun][i]
                sept = MISKIN_SEPTEMBER.get(tahun, [None] * 38)[i]
                if maret is None and sept is None:
                    continue
                w.writerow([prov, tahun, "" if maret is None else maret,
                            "" if sept is None else sept])
    print("Dibuat:", path, "-", path.stat().st_size, "byte")


def tulis_tpt():
    path = RAW / "tpt_bps_2020_2025.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["PROVINSI", "TAHUN", "TPT_AGUSTUS"])
        for tahun in range(2020, 2026):
            for i, prov in enumerate(PROVINSI):
                nilai = TPT_AGUSTUS[tahun][i]
                if nilai is None:
                    continue
                # Sengaja dibuat "berantakan" seperti ekspor BPS:
                # huruf besar dan singkatan KEP. agar tahap pembersihan terlihat nyata.
                nama = prov.upper().replace("KEPULAUAN", "KEP.")
                w.writerow([nama, tahun, nilai])
    print("Dibuat:", path, "-", path.stat().st_size, "byte")


def tulis_nasional():
    path = RAW / "nasional_bps_2020_2025.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["tahun", "kemiskinan_maret", "kemiskinan_september", "tpt_agustus"])
        for row in NASIONAL:
            w.writerow(["" if v is None else v for v in row])
    print("Dibuat:", path, "-", path.stat().st_size, "byte")


if __name__ == "__main__":
    RAW.mkdir(parents=True, exist_ok=True)
    tulis_kemiskinan()
    tulis_tpt()
    tulis_nasional()
