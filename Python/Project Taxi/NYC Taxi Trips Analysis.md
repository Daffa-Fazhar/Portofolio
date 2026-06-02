NYC Taxi Trips Analysis

## Project Overview
Analisis dataset NYC Taxi Trips dengan lebih dari 1 juta baris data. 
Tujuan project ini adalah memahami pola perjalanan, vendor performance, 
dan distribusi trip berdasarkan waktu, lokasi, serta durasi.

## Tools & Technologies
- SQL Server Management Studio (SSMS) → data cleaning & preprocessing
- Python (Pandas, Plotly, Numpy, Streamlit) → data processing & visualization
- Streamlit → interactive dashboard
- Power BI → complementary visualization

## Challenges
- Dataset besar (> 1 juta rows) menyebabkan keterbatasan performa di Power BI.
- Visualisasi peta tidak dapat diproses optimal karena keterbatasan perangkat.

## Solutions
- Data cleaning dilakukan di SSMS untuk memastikan kualitas dataset.
- Visualisasi interaktif dibangun dengan Streamlit Python.
- Power BI tetap digunakan untuk ringkasan dashboard dengan sampling data.

## Key Insights
- Distribusi perjalanan berdasarkan jam, bulan, dan vendor.
- Analisis durasi perjalanan (≤ 60 menit).
- Market share antar vendor.
- Pickup locations dengan sampling 50,000 titik dari 879,043 filtered trips.

## Dataset
Dataset tersedia di Kaggle: https://www.kaggle.com/datasets/yasserh/nyc-taxi-trip-duration


