Hackathon Python DQLab x Uji Kompetensi  
Retail Crisis & Recovery – Visualization Challenge

# Latar Belakang
DQFresh Mart adalah sebuah mini mart dengan satu cabang. Selama bertahun-tahun, toko ini sukses menjual produk-produk tradisional andalan. Namun, dalam 6 bulan terakhir penjualan menurun drastis dan jumlah pengunjung berkurang.  

Strategi awal manajemen adalah:  
- Mempertahankan produk bestseller  
- Mengurangi eksperimen produk baru  
- Memperbesar stok produk historis terbaik  
- Menekan risiko inventory  

Namun Sophia, manajer toko, menemukan pola berbeda melalui analisis data internal:  
- Data transaksi penjualan  
- Data stok harian 

Ia mendapati beberapa produk kecil justru menunjukkan tren pertumbuhan konsisten, meski kontribusi revenue masih kecil. Produk ini sering luput dari perhatian sistem maupun kasir karena stoknya cepat habis. Sophia kemudian memutuskan menambah stok produk tersebut dan membuat paket bundling dengan produk lain yang sering dibeli bersamaan.

### Tujuan Hackathon
Peserta diminta menghasilkan analisis teknis yang sama dengan Sophia menggunakan Python, tanpa data stok harian, dengan output berupa:  
- `retail_insight.xlsx`  
- `rising_star_index.png`  
- `rising_star_actual.png`  

Script utama: solusi-retail.py  
Dataset: sales_transaction.csv (periode 30 hari, sudah bersih)  

### 🛠️ Versi Python & Library
- Python 3.10 – 3.14  
- matplotlib 3.10.7  
- pandas 2.3.1  
- mlxtend 0.23.4  
- openpyxl 3.1.5  

### Output
1. Rising Star: produk dengan tren naik konsisten ≥ 12 hari (moving average 3 hari).  
2. Potential Packaging: kombinasi produk dengan algoritma Apriori (support ≥ 0.01, lift ≥ 2).  
3. Visualisasi: grafik pertumbuhan relatif (Base 100) dan nilai penjualan aktual.  


### Catatan
Hackathon ini merupakan bagian dari DQLab x Uji Kompetensi dengan tema "Retail Crisis & Recovery".  
