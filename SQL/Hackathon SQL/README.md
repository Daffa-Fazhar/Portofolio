SQL Anomaly Detection Hackathon Project

Pencapaian: Skor 100 (Perfect Score)



Deskripsi Proyek

Proyek ini dikembangkan dalam rangka mengikuti kompetisi SQL Hackathon. Tugas utamanya adalah mengidentifikasi transaksi anomali (outliers) dalam data order berdasarkan hierarki organisasi. Dengan menggunakan metode statistik Z-Score, proyek ini berhasil mendeteksi transaksi yang menyimpang secara signifikan dari rata-rata performa tim di level manajer tertentu.



Tantangan

Tantangan utama dalam proyek ini adalah:

1. Hierarchical Traversal: Menentukan Level 2 Manager untuk setiap order yang berada di posisi hirarki yang berbeda-beda menggunakan LEFT JOIN bertingkat.
2. Statistical Analysis: Mengimplementasikan deteksi anomali dengan ambang batas Z-Score > 3.
3. Data Formatting: Menyajikan data dalam format gabungan antara rekapitulasi jumlah anomali per manajer dan detail transaksi anomalinya menggunakan UNION ALL.



Pendekatan Teknis

Solusi ini diimplementasikan menggunakan MySQL Temporary Tables untuk efisiensi pemrosesan data:

* temp\_order\_level2: Melakukan mapping node\_id ke manajer Level 2 menggunakan recursive join logic.
* temp\_stats: Menghitung rata-rata dan standar deviasi populasi per manajer.
* temp\_outliers\_detail: Menghitung Z-Score dan memfilter data dengan ambang batas ABS(Z-Score) > 3.
* Output: Menggabungkan ringkasan jumlah anomali dengan rincian data per transaksi dalam satu tabel hasil.





