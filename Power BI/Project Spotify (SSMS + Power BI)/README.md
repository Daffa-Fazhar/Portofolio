Spotify Data Analytics Dashboard

Proyek Overview

Proyek ini merupakan analisis mendalam perilaku mendengarkan musik pengguna Spotify. Dashboard ini dirancang untuk memberikan wawasan visual mengenai tren album, artis, frekuensi track, serta pola waktu mendengarkan. Proyek ini menggabungkan teknik pemrosesan data (ETL) menggunakan SQL Server (SSMS) dan visualisasi interaktif menggunakan Power BI.



Tech Stack \& Tools

* Data Processing \& Cleaning: SQL Server Management Studio (SSMS) - menangani format data mentah yang rusak dan restrukturisasi tabel.
* Data Modeling: Power BI Desktop (Power Query \& DAX).
* Visualisasi: Power BI Dashboard (Interactive Reports).



Key Features \& Analysis

* Dynamic Quadrant Analysis: Pengguna dapat menentukan threshold durasi dan frekuensi lagu menggunakan Field Parameters, yang kemudian mengategorikan data ke dalam 4 kuadran perilaku secara real-time.
* Time Intelligence: Implementasi perbandingan Year-over-Year (YoY) dan Year-to-Date (YTD) untuk melacak tren performa artis dan album dari tahun 2014 hingga 2024.
* Behavioral Heatmap: Visualisasi jam mendengarkan untuk mengidentifikasi pola kebiasaan pengguna sepanjang minggu.



Technical Highlights (DAX \& Modeling)

* Complex DAX: Menggunakan fungsi SWITCH(TRUE(), ...) untuk logika kuadran yang dinamis dan efisien.
* Calculated Tables: Membangun tabel baru untuk menampung metrik spesifik agar model data tetap ringan dan terstruktur.
* Data Cleansing: Mengatasi format data yang rusak dan melakukan normalisasi tabel agar siap dianalisis.



Dashboard Preview

* Dashboard 1: Ringkasan Tren Album, Artis, dan Tracks.
* Dashboard 2: Analisis Waktu Mendengarkan (Heatmap \& Quadrant Analysis).
* Dashboard 3: Detail Performa Artis \& Metrik Spesifik.





