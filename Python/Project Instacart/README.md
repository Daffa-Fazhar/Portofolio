# Analisis Rantai Pasok dan Perilaku Konsumen Skala Big Data (Instacart Analytics)

## Konteks dan Problematika Utama
Proyek ini dirancang untuk menyelesaikan tantangan pemrosesan data transaksi e-commerce berskala besar, mencakup lebih dari 32,4 juta baris data dari dataset Instacart. Pada skala data ini, kendala utama yang sering muncul adalah tingginya latensi kueri dan potensi kemacetan memori (out-of-memory) ketika aplikasi harus merespons filter interaktif secara real-time.

## Arsitektur Solusi Teknis
   Untuk mengatasi hambatan performa tersebut, arsitektur data dibangun menggunakan pendekatan terintegrasi yang memisahkan beban kerja pemrosesan secara komputasional:
1. OLAP SQL Engine (DuckDB): Dimanfaatkan untuk mengeksekusi operasi JOIN kompleks pada lima tabel relasional (skema Snowflake) secara in-memory tanpa perlu memuat seluruh dataset mentah 
   ke RAM aplikasi.   
2. In-Memory Data Processing (Polars): Digunakan untuk kalkulasi dan agregasi multidimensi berkinerja tinggi, menghasilkan waktu pemrosesan sub-second untuk setiap perubahan filter.
3. Interactive Executive UI (Streamlit + Plotly): Menyajikan panel kendali eksekutif dengan kemampuan pencarian dan pemfilteran dinamis yang responsif.

## Alur Kerja Data Pipeline
Pemrosesan data berjalan secara runtut melalui lima tahapan utama:
- Ingesti Data: Membaca file mentah CSV dari direktori penyimpanan.
- Pemetaan Relasional: Mengintegrasikan tabel fakta transaksi (order_products__prior) dengan tabel-tabel dimensi (orders, products, departments, aisles) menggunakan DuckDB.
- Dynamic Slicing Layer: Menerapkan filter multidimensi di tingkat pengguna, seperti rentang jam operasional, hari transaksi, kategori departemen, hingga tipe pelanggan.
- Engine Agregasi: Memproses perhitungan metrik utama, matriks retensi, dan pemetaan heatmap menggunakan Polars.
- Visualisasi Eksekutif: Menampilkan output akhir berupa kartu KPI dan grafik interaktif di antarmuka Streamlit.

## Temuan Analitis dan Implikasi Bisnis
Berdasarkan hasil pengolahan data transaksi, diperoleh beberapa temuan analitis krusial:
1. Optimalisasi Sumber Daya Gudang:
   Analisis Shopping Density Heatmap menunjukkan bahwa lonjakan volume transaksi tertinggi (peak hours) terjadi secara konsisten pada hari Minggu dan Senin antara pukul 10:00 hingga 15:00.  
   Informasi ini memberikan dasar kuantitatif bagi manajemen rantai pasok untuk mengoptimalkan penjadwalan shift dan alokasi staf picker/packer di gudang pada jam-jam sibuk tersebut.
2. Pola Retensi dan Perilaku Keranjang Belanja:
   Evaluasi terhadap urutan penambahan barang ke keranjang (add-to-cart sequence) mengungkapkan bahwa produk yang dimasukkan pada urutan 1 hingga 3 memiliki probabilitas pembelian ulang 
   (repeat order rate) mencapai 68%. Hal ini menandakan bahwa barang di posisi awal keranjang merupakan produk kebutuhan harian utama (daily essentials) dengan tingkat loyalitas pelanggan 
   yang sangat tinggi.
3. Distribusi Kontribusi Kategori:
   Dari seluruh kategori produk yang ada, departemen Produce serta Dairy Eggs secara konsisten mendominasi pasar dengan menyumbangkan lebih dari 50% dari total volume penjualan toko. 

## Kesimpulan Teknis
Implementasi kombinasi DuckDB, Polars, dan Streamlit membuktikan bahwa arsitektur data modern mampu mengolah puluhan juta baris data transaksi menjadi dashboard analitis yang cepat, efisien dari sisi penggunaan memori, dan memberikan insight strategis yang siap dieksekusi oleh manajemen.