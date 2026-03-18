Project – Medical Analytics (Excel + Power BI)



Tujuan dari project ini adalah menganalisis data kesehatan pasien dan billing dengan mengintegrasikan Excel sebagai tahap awal pembersihan data, lalu menghubungkannya ke Power BI untuk visualisasi interaktif. Project ini bertujuan memberikan insight terkait demografi pasien, kondisi medis, penyedia asuransi, serta tren billing dari tahun ke tahun.



Langkah Pengerjaan

1. Data Cleaning (Excel)
Menghapus duplikat dengan fitur Remove Duplicates, merapikan teks berantakan menggunakan fungsi kombinasi TRIM dan PROPER, menstandarkan format tanggal dengan fungsi DATE agar konsisten.
2. Data Modelling (Power BI)
Karena tanggal tidak terdeteksi otomatis, dibuat DAX CALENDAR untuk membangun tabel tanggal, Kalender kemudian dipecah menjadi kolom Hari, Bulan, Quarter, dan Tahun untuk analisis time-series, Relasi antar tabel dibangun agar data pasien, billing, dan asuransi dapat dianalisis secara terintegrasi.
3. Dashboard Development (Power BI)
* Menampilkan KPI utama: Total Patients, Total Billing Amount, Top Insurance Provider.
* Visualisasi distribusi pasien berdasarkan gender, kondisi medis (diabetes, hipertensi, kanker, dll.), serta penyedia asuransi.
* Tren billing dan jumlah pasien dari tahun ke tahun (2019–2024).
* Breakdown billing per provider dan kondisi medis untuk evaluasi performa layanan kesehatan.



Hasil

* Breakdown billing per provider dan kondisi medis untuk evaluasi performa layanan kesehatan.
* Data yang awalnya berantakan di Excel berhasil dibersihkan dan ditransformasikan menjadi insight yang rapi di Power BI.
* Analisis time-series dengan DAX Calendar memungkinkan evaluasi tren kesehatan dan biaya secara lebih akurat.

