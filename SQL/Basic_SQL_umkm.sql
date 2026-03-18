CREATE DATABASE umkm;
-- 1. Check Tabel umkm_jabar
 SELECT * FROM umkm_jabar;
-- 2. Tunjukkan Data UMKM di Kota Bandung
 SELECT * FROM umkm_jabar WHERE nama_kabupaten_kota = "KOTA BANDUNG";
-- 3. Data umkm dari tahun 2019 dan disusun berdasarkan kategori usaha
 SELECT * FROM  umkm_jabar WHERE tahun >= 2019 ORDER BY kategori_usaha;
-- 4. Data umkm tersebut dilimit sampai 10 baris saja
 SELECT * FROM  umkm_jabar WHERE tahun >=2019 ORDER BY kategori_usaha, tahun LIMIT 10;
-- 5. Kategori usaha yang tersedia
 SELECT DISTINCT kategori_usaha FROM umkm_jabar;
-- 6. Data umkm berkategori usaha MAKANAN dan FASHION
 SELECT * FROM umkm_jabar WHERE kategori_usaha IN ("MAKANAN","FASHION");
 SELECT * FROM umkm_jabar WHERE kategori_usaha = "MAKANAN" OR kategori_usaha = "FASHION";
-- 7. Data dengan kategori usaha FASHION di Kabupaten Karawang
 SELECT * FROM umkm_jabar WHERE kategori_usaha = "FASHION" AND nama_kabupaten_kota = "KABUPATEN KARAWANG";
-- 8. Seluruh data selain kategori usaha MAKANAN, KULINER, dan MINUMAN
 SELECT * FROM umkm_jabar WHERE kategori_usaha NOT IN ("MAKANAN", "KULINER", "MINUMAN");
-- 9. Tren jumlah UMKM di Kabupaten Tasikmalaya untuk kategori usaha BATIK pada tahun 2018 s.d. 2020
 SELECT nama_kabupaten_kota, kategori_usaha, jumlah_umkm, satuan, tahun
 FROM umkm_jabar WHERE nama_kabupaten_kota = "KABUPATEN TASIKMALAYA" 
 AND tahun <=2020 AND tahun >=2018
 AND kategori_usaha = "BATIK";
-- 10. UMKM kuliner terpusat pada tahun 2021 diantara Kota Bandung, Kabupaten Bandung, dan Kabupaten Bandung Barat.
 SELECT * FROM umkm_jabar WHERE nama_kabupaten_kota LIKE "%BANDUNG%" AND kategori_usaha = "KULINER" AND tahun = 2021;
-- 11. Kabupaten/Kota yang memiliki angka 7 pada digit ke 3 kode kabupaten/kota
 SELECT DISTINCT * FROM umkm_jabar WHERE kode_kabupaten_kota LIKE "__7%";