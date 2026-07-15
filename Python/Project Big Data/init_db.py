import duckdb
import os

# Set jalur relatif ke folder aktif saat ini
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "ecommerce_data.db")

print("Memulai konversi 110 Juta baris CSV ke DuckDB...")

# Membuat koneksi sekaligus file database baru
con = duckdb.connect(DB_PATH)

# Mengonversi seluruh file CSV di folder ini menjadi satu tabel bernama raw_ecommerce
con.execute("""
    CREATE TABLE raw_ecommerce AS 
    SELECT * FROM read_csv_auto('*.csv', ALL_VARCHAR=TRUE)
""")

# Cek jumlah data untuk memastikan sukses
total_rows = con.execute("SELECT COUNT(*) FROM raw_ecommerce").fetchone()[0]

print(f"✅ PROSES SELESAI!")
print(f"📂 File berhasil dibuat: {DB_PATH}")
print(f"📊 Total data yang berhasil masuk: {total_rows:,} baris.")

con.close()