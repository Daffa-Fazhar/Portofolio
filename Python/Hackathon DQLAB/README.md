# Retail Crisis & Recovery Analysis Dashboard (Feb - Mar 2025)

## Project Overview
Proyek ini merupakan hasil analisis data transaksi ritel untuk mendeteksi periode krisis (crisis detection) serta mengukur kecepatan pemulihan bisnis (recovery rate). Dashboard ini dibangun menggunakan Python (Pandas dan Matplotlib) untuk mengolah data mentah transaksi menjadi visualisasi analitis yang interaktif dan informatif, yang ditujukan untuk mendukung pengambilan keputusan strategis manajemen.

## Business Insights & Metrics Analysis

Berdasarkan visualisasi dashboard, berikut adalah poin analisis utama dari performa bisnis selama periode Februari - Maret 2025:

### 1. Daily Revenue Timeline (Crisis & Recovery Detection)
1. Peak Revenue: Bisnis mencapai pendapatan harian tertinggi sebesar Rp 124 Juta pada awal Februari 2025 yang dipicu oleh tren penjualan stabil.
2. Crisis Start (03 Mar): Terjadi penurunan pendapatan yang sangat tajam secara mendadak mulai tanggal 3 Maret 2025. 
3. Lowest Point: Penurunan mencapai titik terendah (palung) pada tanggal 4 Maret 2025 di angka Rp 70 Juta. Ini merepresentasikan penurunan drastis sebesar -43.2% dari titik puncak (Peak-to-Trough Drop).
4. Days Peak to Trough: Dibutuhkan waktu 26 hari dari masa kejayaan hingga menyentuh titik terendah krisis ini.
5. Recovery Phase (04 Mar): Bisnis menunjukkan resiliensi yang luar biasa dengan Recovery Speed hanya 1 hari. Segera setelah menyentuh titik terendah, grafik pendapatan langsung merangkak naik kembali menuju batas normal (7-Day Rolling Average).

### 2. Top 3 Produk Paling Terdampak (Crisis Impact)
1. Kaos Kaki (3 Pasang)
2. Kabel Data Fast Charging
3. Mouse Wireless

### 3. Top 3 Recovery Drivers (Faktor Pemulihan)
1. Sabun Cuci Cair 1.5L (Pendorong utama dengan lonjakan tertinggi mendekati Rp 6jt/hari)
2. Minyak Goreng Refill
3. Beras Premium 5kg

---

## Tech Stack & Data Structure

### Technology Used
1. Python (Core Processing)
2. Pandas (Data Cleaning, Aggregation, Time-Series & 7-Day Rolling Average Calculation)
3. Matplotlib (Custom Dark-Themed Dashboard Design & Data Visualization)

### Dataset Structure (Sample Input)
Data mentah yang diproses memiliki struktur sebagai berikut:
1. nomor_struk: ID unik untuk setiap transaksi penjualan.
2. tgl_transaksi: Tanggal terjadinya transaksi (Februari - Maret 2025).
3. kode_produk & nama_produk: Identifikasi barang yang terjual.
4. jumlah_terjual: Kuantitas produk yang dibeli dalam satu transaksi.
5. harga: Harga satuan per produk.
6. total_nilai: Total pendapatan per lini produk (jumlah_terjual dikali harga).

---

## Key Technical Highlights in Code
1. Time-Series Analysis: Menggunakan fungsi windowing Pandas untuk menghitung 7-Day Rolling Average guna melihat tren pendapatan jangka panjang tanpa terganggu fluktuasi harian yang ekstrem.
2. Conditional Masking & Detection: Membuat algoritma otomatis untuk mendeteksi koordinat persis kapan Crisis Start, Lowest Point, dan Recovery Phase terjadi berdasarkan ambang batas (threshold) deviasi pendapatan.
3. Advanced Matplotlib Layouts: Menggabungkan multi-plot (Grid Layout) menjadi satu kanvas dashboard yang rapi dengan kustomisasi penuh pada warna tema (Black & Gold palette), anotasi panah, dan label mata uang (IDR).