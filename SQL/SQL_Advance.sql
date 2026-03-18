SELECT * FROM umkm_jabar;
-- 1. Berapa jumlah baris dari tabel umkm_jabar?
 SELECT count(*) as total_baris FROM umkm_jabar; -- (kalau menuliskan tanpa as, nama kolomnya jadi count(*))
 SELECT kategori_usaha, count(*) as jumlah_kategori_usaha FROM umkm_jabar
 GROUP BY kategori_usaha; 
-- 2. Berapa jumlah umkm di kabupaten bekasi di tahun 2017?
 SELECT SUM(jumlah_umkm) as jumlah_umkm_kab_bekasi_2017 FROM umkm_jabar 
 WHERE nama_kabupaten_kota = "KABUPATEN BEKASI" AND tahun = 2017;
-- 3. Bagaimana tren jumlah umkm di kabupaten karawang dari tahun 2017 s/d 2021
 SELECT SUM(jumlah_umkm) as jumlah_umkm_kab_karawang_4_Tahun FROM umkm_jabar
 WHERE nama_kabupaten_kota = "KABUPATEN KARAWANG" AND tahun BETWEEN 2017 AND 2021;
 -- ATAU
 SELECT tahun, SUM(jumlah_umkm) as jumlah_umkm_kab_karawang_4_Tahun FROM umkm_jabar
 WHERE nama_kabupaten_kota = "KABUPATEN KARAWANG" AND tahun >=2017 AND tahun <= 2021 GROUP BY tahun;
-- Saya ingin memfilter > 250000
 SELECT tahun, SUM(jumlah_umkm) as jumlah_umkm_kab_karawang_4_Tahun FROM umkm_jabar
 WHERE nama_kabupaten_kota = "KABUPATEN KARAWANG" AND tahun >=2017 AND tahun <= 2021 
 GROUP BY tahun HAVING jumlah_umkm_kab_karawang_4_Tahun > 250000;
-- 4. Berapa jumlah rata-rata umkm setiap kategori usaha di setiap kabupaten/kota di jawa barat dari tahun ke tahun
 SELECT tahun, AVG(jumlah_umkm) as rata_rata_umkm FROM umkm_jabar GROUP BY tahun;
-- 5. Berapa jumlah rata-rata umkm di setiap kategori usaha per kabupaten/kota jawa barat pada tahun 2017
 SELECT kategori_usaha, tahun, AVG(jumlah_umkm) as rata_rata_umkm FROM umkm_jabar 
 WHERE tahun = 2017 GROUP BY kategori_usaha,tahun;
-- 6. Nilai minimum dan maksimum dari kolom jumlah_umkm
 SELECT 
 MIN(jumlah_umkm) as jumlah_sedikit,
 MAX(jumlah_umkm) as jumlah_terbanyak
 FROM umkm_jabar;
-- 7. Kategori usaha dengan jumlah umkm terbanyak dan tersedikit di Kabupaten Sukabumi pada tahun 2020
 SELECT kategori_usaha, tahun,
 MIN(jumlah_umkm) as kategori_usaha_terendah,
 MAX(jumlah_umkm) as kategori_usaha_tertinggi
 FROM umkm_jabar WHERE tahun = 2020 GROUP BY kategori_usaha, tahun; 
-- 8. Kabupaten atau kota apa yang memiliki jumlah umkm kurang dari 100.000 pada tahun 2020
 SELECT nama_kabupaten_kota, jumlah_umkm
 FROM umkm_jabar
 WHERE tahun = 2020 AND jumlah_umkm < 100000 ORDER BY jumlah_umkm ASC;
-- Sama seperti sebelumnya, apabila kalau ingin mengetaui total jumlah umkm pada tahun 2020
SELECT nama_kabupaten_kota, SUM(jumlah_umkm) as total_umkm
 FROM umkm_jabar
 WHERE tahun = 2020 AND jumlah_umkm < 100000  GROUP BY nama_kabupaten_kota ORDER BY total_umkm ASC;
-- WHERE tidak bisa memfilter agregat maka harus menggunakan HAVING
SELECT nama_kabupaten_kota, SUM(jumlah_umkm) as total_umkm
 FROM umkm_jabar
 WHERE tahun = 2020 GROUP BY nama_kabupaten_kota HAVING total_umkm < 100000 ORDER BY total_umkm ASC;
 
 
SELECT nama_kabupaten_kota, kategori_usaha, jumlah_umkm,
CASE WHEN jumlah_umkm > 100000 THEN "Tinggi"
WHEN jumlah_umkm < 100000 THEN "Rendah"
ELSE "Others"
END kategori_umkm
FROM umkm_jabar WHERE jumlah_umkm > 50000 ORDER BY jumlah_umkm DESC;
 