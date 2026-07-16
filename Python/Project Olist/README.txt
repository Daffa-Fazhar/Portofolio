# Olist End-to-End Retail Analytics: Dynamic ETL Pipeline & Executive Dashboard

Repositori ini berisi proyek integrasi data lifecycle ritel e-commerce Olist, mulai dari pemrosesan pipa data (ETL backend) berkinerja tinggi hingga lapisan visualisasi informasi bisnis strategis (frontend).

Untuk dokumentasi kode program kodingan Python dan analisis bisnis yang sangat mendalam, silakan langsung membuka file Olist Retail Insights Documentation.pdf yang sudah saya print melalui kodingan "laporan_backend.html" di dalam repositori ini.

## Profil Developer
* Nama: Daffa Farros Azhari
* Peran: Data Analyst & Automation Specialist
* Teknologi Kunci: Python, Polars Engine (Rust-powered), Power BI, Data Modeling, Geospasial

## 1. Arsitektur Alur Sistem (High-Level Workflow)

###  Backend ETL Pipeline Engine
* Input: 9 file database CSV mentah terpisah (Orders, Payments, Products, Customers, dll).
* Proses: Optimasi kueri menggunakan Polars Lazy Evaluation dan agregasi koordinat spasial untuk mencegah pembengkakan data (row explosion).
* Output: Dua file master terpusat yang bersih dan siap pakai: `tabel_sales_master.csv` dan `tabel_geo_master.csv`.
* Dampak: Memangkas beban RAM hingga 70% dan mempercepat waktu tunggu eksekusi data dari hitungan menit menjadi hitungan detik.

### Frontend Business Dashboard
* Input: File data induk hasil olahan backend yang sudah bersih.
* Proses: Transformasi baris tabel menjadi visualisasi interaktif dinamis bertema Executive Dark Mode.
* Output: Dasbor interaktif pemantau KPI omset, tren penjualan bulanan, preferensi pembayaran, dan peta spasial wilayah.
* Dampak: Membantu pihak manajemen (C-Level) mengambil keputusan pemasaran dan logistik secara instan dan akurat.

## 2. Skema Database & Layout Visual

### A. Entity Relationship Diagram (ERD)
Rancangan relasi database awal antar tabel mentah ritel sebelum disatukan oleh Python:
![Olist ERD Architecture](Skema Database.png)

### B. Antarmuka Eksekutif Dashboard (Power BI)
Hasil akhir visualisasi data interaktif untuk monitoring performa bisnis (Total Sales R$ 466M+, Tren Bulanan, Kategori Teratas, Wilayah Spasial, dan Transaksi B2B):
![Olist Dashboard Layout](Dashboard.png)

## 3. Kesimpulan Singkat Proyek

1. Efisiensi Data: Kombinasi Lazy Evaluation Polars sukses mengatasi tantangan pemrosesan Big Data lokal dengan sangat cepat dan anti-lag.
2. Potensi Bisnis: Hasil analisis dasbor berhasil mengidentifikasi dominasi transaksi via Credit Card (76.49%), konsentrasi pasar terbesar di pesisir tenggara Brasil, serta adanya anomali positif berupa transaksi Whale Buyer (skala grosir) di atas R$ 1 Juta.