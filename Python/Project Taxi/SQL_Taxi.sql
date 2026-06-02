-- ==============================================================================
-- QUERY CLEANING & PROSES GEOSPATIAL LANGSUNG DARI TABEL TAXI_TRIPS
-- Siap digunakan untuk View atau langsung ditarik ke Power BI / Python
-- ==============================================================================
SELECT 
    id,
    vendor_id,
    
    -- 1. Merapikan Format Tanggal dan Waktu (Jika tipe datanya masih teks/varchar)
    -- Jika di database Anda kolom ini sudah bertipe DATETIME, hapus baris TRY_CONVERT ini dan ganti dengan kolom biasa
    TRY_CONVERT(DATETIME, pickup_datetime, 103) AS pickup_datetime,
    TRY_CONVERT(DATETIME, dropoff_datetime, 103) AS dropoff_datetime,
    
    passenger_count,
    trip_duration,

    -- 🌟 2. RUMUS PEMBERSIHAN KOORDINAT LONGITUDE (Target: -73.xxxxxx s/d -74.xxxxxx)
    -- Mengonversi ke FLOAT terlebih dahulu agar format scientific aman, lalu digeser desimalnya
    CAST(TRY_CAST(pickup_longitude AS FLOAT) / 100000000000000.0 AS DECIMAL(18, 6)) AS pickup_longitude,
    CAST(TRY_CAST(dropoff_longitude AS FLOAT) / 100000000000000.0 AS DECIMAL(18, 6)) AS dropoff_longitude,

    -- 🌟 3. RUMUS PEMBERSIHAN KOORDINAT LATITUDE (Target: 40.xxxxxx)
    CAST(TRY_CAST(pickup_latitude AS FLOAT) / 100000000000000.0 AS DECIMAL(18, 6)) AS pickup_latitude,
    CAST(TRY_CAST(dropoff_latitude AS FLOAT) / 100000000000000.0 AS DECIMAL(18, 6)) AS dropoff_latitude,
    
    store_and_fwd_flag,
    
    -- Membuat metrics bantuan untuk menghitung total perjalanan
    1 AS total_trips 

FROM taxi_trips -- Langsung menembak tabel utama Anda

WHERE 
    -- 🛑 FILTER OUTLIER & DATA SAMPAH
    -- Hanya mengambil data yang setelah digeser desimalnya masuk ke area geografis New York
    (TRY_CAST(pickup_latitude AS FLOAT) / 100000000000000.0 BETWEEN 40.5 AND 40.9)
    AND 
    (TRY_CAST(pickup_longitude AS FLOAT) / 100000000000000.0 BETWEEN -74.2 AND -73.7);