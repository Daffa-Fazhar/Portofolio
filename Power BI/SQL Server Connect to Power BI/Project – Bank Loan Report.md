Project – Bank Loan Report (SQL Server + Power BI)



Tujuan dari pembuatan project ini adalah membangun istem analisis pinjaman bank dengan mengintegrasikan SQL Server Management Studio (SSMS) dan Microsoft Power BI. Project ini bertujuan untuk menampilkan KPI utama, tren pinjaman, serta kualitas loan (Good vs Bad Loan) dalam bentuk dashboard interaktif yang mendukung pengambilan keputusan berbasis data.



Langkah Pengerjaan

1. Data Extraction (SQL Server)
Menggunakan query SQL (SELECT \* FROM bank\_loan\_data) untuk memanggil data mentah. Dan Membuat query tambahan untuk menghitung KPI seperti: (Total Loan Applications, Total Funded Amount, Total Amount Received, Average Rate \& DTI, Good Loan vs Bad Loan Percentage, dsb)
2. Data Cleaning \& Transformation (Power Query)
Membersihkan data (menghapus null, memperbaiki format tanggal, normalisasi tipe data) dan membuat kolom baru untuk data data yang tidak sesuai ketentuan seperti perhitungan Average Interest Rate dan DTI. 
3. Data Modelling \& DAX (Power BI)
Membuat measure baru menggunakan DAX untuk KPI dinamis, seperti: MTD (Month-to-Date) dan  PMTD (Previous Month-to-Date) metrics, Good Loan Applications, Funded Amount, Amount Received, Bad Loan Applications, Funded Amount, dan Amount Received, Bad Loan Applications, Funded Amount, dan Amount Received.
Menggunakan fungsi DAX seperti CALCULATE, FORMAT, SUM, AVERAGE, dan SWITCH untuk perhitungan kompleks.
4. Dashboard Development (Power BI)
* Menampilkan KPI utama (Applications, Funded Amount, Payments, Interest Rate, DTI)
* Visualisasi breakdown berdasarkan Month, State, Term, Employee Length, Purpose, Home Ownership.
* Analisis kualitas pinjaman melalui Good vs Bad Loan.
* Menambahkan filter interaktif (Grade, Loan Status, dll.) untuk validasi hasil query SQL dengan Power BI.



Hasil

* Dashboard interaktif yang menampilkan tren aplikasi pinjaman, distribusi berdasarkan demografi, serta kualitas loan.
* Validasi hasil antara query SQL dan DAX memastikan akurasi data.
* Memberikan insight bisnis yang relevan bagi stakeholder, seperti: Pinjaman paling banyak digunakan untuk Debt Consolidation, distribusi pinjaman berdasarkan lama bekerja dan status kepemilikan rumah, perbandingan performa Good Loan vs Bad Loan.

