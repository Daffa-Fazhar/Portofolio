import streamlit as st
import base64

# ==========================================
# 1. KONFIGURASI HALAMAN UTAMA
# ==========================================
st.set_page_config(
    page_title="Daffa Farros Azhari | Portfolio & Services", 
    page_icon="⚡", 
    layout="wide"
)

# ==========================================
# 2. HELPER FUNCTION: BACA BACKGROUND IMAGE
# ==========================================
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return ""

# Deklarasi variabel background di paling atas (Mencegah NameError)
img_base64 = get_base64_image("background.png")

# ==========================================
# 3. HELPER FUNCTION: LIGHTBOX IMAGE (PERBAIKAN TRUE CENTER)
# ==========================================
def st_lightbox_image(image_path: str, img_id: str, caption: str = ""):
    """Merender gambar dengan fitur Pure CSS Lightbox (Pas di Tengah Layar)."""
    try:
        with open(image_path, "rb") as img_file:
            b64_str = base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.error(f"Waduh Bre, file '{image_path}' tidak ditemukan di folder project!")
        return

    html_code = f"""
    <style>
      #{img_id}-toggle {{
        display: none !important;
      }}
      .img-thumb-{img_id} {{
        cursor: zoom-in;
        width: 100%;
        border-radius: 8px;
        transition: transform 0.2s ease;
      }}
      .img-thumb-{img_id}:hover {{
        transform: scale(1.02);
      }}
      
      /* OVERLAY POPUP FULLSCREEN (FIXED VIEWPORT) */
      .overlay-{img_id} {{
        display: none;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        background: rgba(0, 0, 0, 0.92) !important;
        z-index: 99999999 !important;
        margin: 0 !important;
        padding: 0 !important;
      }}
      
      /* WADAH GAMBAR PAS DI TENGAH MONITOR */
      .overlay-content-{img_id} {{
        position: fixed !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        max-width: 90vw !important;
        max-height: 90vh !important;
        z-index: 100000000 !important;
        pointer-events: auto !important;
      }}

      .overlay-content-{img_id} img {{
        max-width: 90vw !important;
        max-height: 82vh !important;
        object-fit: contain !important;
        border-radius: 8px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.9);
      }}

      #{img_id}-toggle:checked ~ .overlay-{img_id} {{
        display: block !important;
      }}
      
      .caption-{img_id} {{
        text-align: center;
        font-size: 0.85rem;
        color: #a0aec0;
        margin-top: 6px;
        margin-bottom: 12px;
      }}
      .overlay-caption-{img_id} {{
        color: #e2e8f0;
        font-size: 0.9rem;
        margin-top: 10px;
        text-align: center;
        background: rgba(15, 20, 32, 0.8);
        padding: 6px 16px;
        border-radius: 6px;
        border: 1px solid rgba(255,255,255,0.1);
      }}
    </style>

    <!-- Checkbox Toggle -->
    <input type="checkbox" id="{img_id}-toggle">

    <!-- Thumbnail Gambar -->
    <label for="{img_id}-toggle" style="display: block; width: 100%;">
      <img class="img-thumb-{img_id}" src="data:image/png;base64,{b64_str}" alt="{caption}">
    </label>
    {f'<div class="caption-{img_id}">{caption}</div>' if caption else ''}

    <!-- Popup Fullscreen Zoom -->
    <div class="overlay-{img_id}">
      <label for="{img_id}-toggle" style="position: absolute; top:0; left:0; width:100%; height:100%; cursor: zoom-out;"></label>
      <div class="overlay-content-{img_id}">
        <img src="data:image/png;base64,{b64_str}" alt="{caption}">
        {f'<div class="overlay-caption-{img_id}">{caption}</div>' if caption else ''}
      </div>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)


# ==========================================
# 4. STYLING CSS GLOBAL (PERBAIKAN CONTAINMENT)
# ==========================================
css_code = """
<style>
    /* Background Gambar dengan Overlay Gelap */
    .stApp {
        background: linear-gradient(
            rgba(9, 10, 15, 0.85), 
            rgba(9, 10, 15, 0.93)
        ), 
        url("data:image/png;base64,GAMBAR_LOKAL_BASE64") !important;
        
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
    }
    
    /* Hover Cards untuk Bagian Jasa & Tools */
    .custom-card {
        background-color: rgba(15, 20, 32, 0.75) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        padding: 22px !important;
        border-radius: 12px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
        margin-bottom: 15px;
    }
    .custom-card:hover {
        transform: translateY(-5px) !important;
        border-color: rgba(0, 150, 255, 0.6) !important;
        box-shadow: 0 12px 40px 0 rgba(0, 150, 255, 0.2) !important;
        background-color: rgba(20, 28, 45, 0.9) !important;
    }
    
    /* Styling Badge Tools */
    .tool-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 6px;
        padding: 6px 14px;
        margin: 5px;
        font-family: monospace;
        font-size: 0.9rem;
        color: #e2e8f0;
    }
    .tool-badge img {
        width: 18px;
        height: 18px;
        object-fit: contain;
    }
    
    /* RESET PERIPHERAL STREAMLIT AGAR MELEPAS POSITION FIXED */
    [data-testid="stExpander"], 
    [data-testid="stExpanderDetails"],
    .stMarkdown,
    .element-container {
        transform: none !important;
        filter: none !important;
        backdrop-filter: none !important;
        perspective: none !important;
        contain: none !important;
    }
    
    /* Styling Expander Tanpa Backdrop Filter */
    [data-testid="stExpander"] {
        background-color: rgba(15, 20, 32, 0.75) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
        margin-bottom: 10px !important;
    }
</style>
"""

# Inject CSS ke Streamlit
st.markdown(css_code.replace("GAMBAR_LOKAL_BASE64", img_base64), unsafe_allow_html=True)

if not img_base64:
    st.error("file 'background.png' gak ketemu di folder project")

# ==========================================
# 5. SIDEBAR PROFIL
# ==========================================
with st.sidebar:
    st.image("foto_daffa.png") 
    st.title("Daffa Farros Azhari")
    st.subheader("Data Analyst & Automation Specialist")
    st.write("📍 Sidoarjo, Indonesia")
    st.write("Hubungi Saya:")
    st.markdown("[📩 Email](azharidaffa18@gmail.com) | [💼 LinkedIn](https://linkedin.com/in/daffafarros)")
    st.markdown("---")
    st.markdown("**Core Skills:**")
    st.code("✓ End to End Data Analytics \n✓ SQL & Query Optimization \n✓ Python for Data Analysis & Automation" \
            "\n✓ Advanced Microsoft Excel \n✓ Data Visualization \n✓ ETL & Data Processing \n✓ Dashboard Development")

# ==========================================
# 6. MAIN PAGE HERO SECTION
# ==========================================
st.markdown("""
<div class="animated-section">
    <h1>Daffa Farros Azhari 🖥️</h1>
    <p style="font-size: 1.2rem; color: #cbd5e0; max-width: 1000px;">
        Mengolah data mentah menjadi informasi yang akurat melalui analisis, otomatisasi, dan visualisasi 
        interaktif untuk mendukung pengambilan keputusan bisnis yang lebih efektif.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 7. TAB NAVIGATION
# ==========================================
tab1, tab2, tab3 = st.tabs(["👤 Tentang Saya & Tools", "📂 Portofolio Proyek", "💼 Layanan Bisnis & Jasa"])

# ==================== TAB 1: PERSONAL & TOOLS ====================
with tab1:
    st.markdown('<div class="animated-section">', unsafe_allow_html=True)
    st.subheader("Professional Journey")
    st.write("""
    Mengubah data mentah menjadi insight yang bernilai melalui analisis, otomatisasi, dan visualisasi data. Berpengalaman membangun
    solusi menggunakan Python, SQL, Excel, Power BI, Polars, Pandas, dan DuckDB untuk membangun alur analisis
    yang efisien, akurat, dan mendukung pengambilan keputusan berbasis data.
    """)
    
    st.write("""
    Ketertarikan terhadap dunia data mendorong saya untuk terus belajar dan mengeksplorasi berbagai teknologi maupun pendekatan baru.
    Setiap proyek menjadi kesempatan untuk membangun solusi yang lebih efisien, mudah dipahami, dan memberikan manfaat nyata 
    bagi pengguna maupun kebutuhan bisnis.
    """)
    
    st.markdown("---")
    st.subheader("Technical Skills")
    st.write("Teknologi dan kerangka kerja yang saya gunakan untuk mengeksekusi proyek data:")
    
    st.markdown("""
        <div style="margin-bottom: 20px;">
            <span class="tool-badge">
                <img src="https://img.icons8.com/color/48/python--v1.png"/> Python (Polars, Pandas, DuckDB, Streamlit, Openpyxl, Matplotlib)
            </span>
            <span class="tool-badge">
                <img src="https://img.icons8.com/color/48/power-bi.png"/> Power BI / DAX
            </span>
            <span class="tool-badge">
                <img src="https://img.icons8.com/color/48/microsoft-excel-2019.png"/> Advanced Microsoft Excel & VBA
            </span>
            <span class="tool-badge">
                <img src="https://img.icons8.com/color/48/database.png"/> SQL (MySQL & SQL Server Management Studio)
            </span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== TAB 2: PORTFOLIO & PROGRESS ====================
with tab2:
    st.subheader("Featured Projects & Technical Cases")
    st.write("Klik pada gambar proyek di bawah untuk melihat visualisasi secara penuh (Zoom):")
    
    # ------------------ PROYEK 1: E-COMMERCE BIG DATA ------------------
    with st.expander("🚀 1. E-Commerce Engine: 110M+ Rows Analysis (Polars + DuckDB + Streamlit + Plotly)"):
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("""
            **Tantangan:** Menganalisis data transaksi e-commerce berukuran raksasa (>110 juta baris) tanpa mengalami kemacetan memori (*out-of-memory*) di komputer standar.  
            **Solusi:** Menggunakan **Polars** untuk pemrosesan data cepat berbasis memori dan **DuckDB** untuk query SQL yang sangat efisien langsung di atas file parket.  
            **Hasil:** Sistem dasbor Streamlit yang mampu memuat agregasi data miliaran rupiah dalam waktu kurang dari 2 detik!
            """)
        with col2:
            st_lightbox_image("Dashboard_110.png", img_id="dash_110", caption="Dashboard Analisis 110 Juta Data (Klik untuk zoom)")

    # ------------------ PROYEK 2: OLIST RETAIL ANALYTICS ------------------
    with st.expander("⚡ 2. Olist End-to-End Retail Analytics (Polars + SQL + Power BI)"):
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("""
            **Tantangan:** Mengintegrasikan 9 tabel transaksi ritel masif yang berantakan dengan risiko duplikasi data pada pemetaan wilayah koordinat.  
            **Solusi:** Membangun pipa ETL di Python dengan optimasi query SQL, kemudian menyajikannya ke dalam dasbor Power BI yang interaktif.  
            **Hasil:** Dasbor finansial multi-page untuk memantau performa penjualan produk dan analisis kepuasan pelanggan secara dinamis.
            """)
        with col2:
            st_lightbox_image("Dashboard_olist.png", img_id="dash_olist", caption="Interactive Power BI Executive Dashboard")

    # ------------------ PROYEK 3: INSTACART MARKET BASKET ANALYSIS ------------------
    with st.expander("🛒 3. Instacart Market Basket Analysis (Polars + DuckDB + Streamlit + Plotly)"):
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("""
            **Tantangan:** Menganalisis perilaku belanja (*Market Basket Analysis*) dari dataset masif berisi lebih dari 32,4 juta baris transaksi tanpa mengalami *lag* atau *loading* yang lama.  
            **Solusi:** Membangun *data pipeline* berkinerja tinggi menggunakan **DuckDB** (OLAP engine) dan **Polars** yang diintegrasikan ke dalam Python Streamlit untuk *querying* super cepat.  
            **Hasil:** Dashboard operasional berlatensi rendah (*sub-second response*) dengan tema hijau elegan, menampilkan *Peak Operating Hours*, *Retention Rate*, dan *Loyalty Breakdown* secara *real-time*.
            """)
        with col2:
            st_lightbox_image("Dashboard_market.png", img_id="dash_market", caption="Dashboard BI Instacart - 32.4M Rows Processed")
    
    # ------------------ PROYEK 4: INDONESIA REGIONAL SALES ------------------
    with st.expander("🗺️ 4. Indonesia Regional Sales & Geographic Heatmap Analytics (Advanced Excel)"):
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("""
            **Tantangan:** Menyajikan pemetaan sebaran penjualan produk secara nasional secara intuitif, sehingga manajemen puncak dapat dengan cepat memahami distribusi geografis dan profitabilitas tiap wilayah untuk pengambilan keputusan strategis.  
            **Solusi:** Mengembangkan dashboard *Dark Theme* interaktif di Excel dengan integrasi *Geospatial Map*, kalkulasi profitabilitas (*Order Priority High/Medium/Low*), serta *multi-slicer* berbasis tahun, bulan, dan tipe barang.  
            **Hasil:** Visualisasi distribusi pendapatan antar provinsi (seperti NTB, Riau, Kalbar) yang memudahkan analisis pasar secara regional.
            """)
        with col2:
            st_lightbox_image("Dashboard_peta.png", img_id="dash_peta", caption="Indonesia Regional Geographic Sales Dashboard")

    # ------------------ PROYEK 5: MEDICAL ANALYTICS ------------------
    with st.expander("🏥 5. Medical Analytics: Patients & Billing Executive Overview (Power BI + Excel)"):
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("""
            **Tantangan:** Memantau tren klaim asuransi kesehatan, tren rawat pasien, dan total *billing* medis senilai Rp1,40+ Miliar secara terpusat.  
            **Solusi:** Membangun *Executive Healthcare Dashboard* dengan integrasi filter gender, *Insurance Provider* (Cigna, Medicare, Aetna), serta pemetaan kondisi medis (*Medical Condition Distribution*).  
            **Hasil:** Laporan eksekutif yang memperlihatkan penurunan/kenaikan tren pasien harian & tahunan (2019-2024) untuk optimalisasi layanan kesehatan.
            """)
        with col2:
            st_lightbox_image("Dashboard_kesehatan.png", img_id="dash_kes", caption="Medical Analytics & Billing Overview Dashboard")
    
    # ------------------ PROYEK 6: SALES MONITORING ------------------
    with st.expander("📊 6. Commercial Sales Target vs Achievement & Operational Slicer System (Advanced Excel + VBA)"):
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("""
            **Tantangan:** Memantau ketercapaian target penjualan harian dan mingguan yang sering mengalami selisih (*gap*) antara barang masuk (*Sell-In*) dan keluar (*Sell-Out*).  
            **Solusi:** Menggabungkan *Advanced Excel Formulas*, *Conditional Formatting*, *Interactive Pivot Table*, *Slicers*, dan *VBA Macro* untuk kalkulasi otomatis.  
            **Hasil:** Panel kendali operasional lengkap dengan matriks *Achievement % (Gauge Chart)*, *Gap Unit*, *Timegone Rate*, serta performa tim *Promotor Name*.
            """)
        with col2:
            st_lightbox_image("Dashboard_monitoring.png", img_id="dash_mon", caption="Sales Monitoring Combination System (Target vs Achievement)")
    
    # ------------------ PROYEK 7: SPOTIFY ------------------
    with st.expander("🎧 7. Spotify Music Behavioral Analytics (Multi-Page Power BI & SSMS)", expanded=True):
        col1, col2 = st.columns([1, 1.2])
        with col1:
            st.markdown("""
            **Overview:** Analisis mendalam perilaku mendengarkan musik di Spotify menggunakan **SQL Server (SSMS)** untuk ETL dan **Power BI** untuk visualisasi.
            
            **Highlight Teknis:**
            * **Dynamic Quadrant Analysis:** Logika `SWITCH(TRUE(), ...)` berbasis *Field Parameters*.
            * **Time Intelligence:** YoY & YTD tracking (2014-2024).
            * **Behavioral Heatmap:** Peta kebiasaan jam mendengarkan harian/mingguan.
            
            **Tech Stack:** `Power BI` • `DAX` • `SQL Server SSMS`
            """)
        with col2:
            st.write("**🖼️ Pilih Halaman Dashboard:**")
            sp_tab1, sp_tab2, sp_tab3 = st.tabs(["Page 1: Tren Album/Artis", "Page 2: Heatmap & Quadrant", "Page 3: Detail Matriks"])
            with sp_tab1:
                st_lightbox_image("Spotify1.png", img_id="sp_1", caption="Page 1 - Ringkasan Tren Album & Artis")
            with sp_tab2:
                st_lightbox_image("Spotify2.png", img_id="sp_2", caption="Page 2 - Behavioral Heatmap & Quadrant")
            with sp_tab3:
                st_lightbox_image("Spotify3.png", img_id="sp_3", caption="Page 3 - Detail Performa Artis (DAX Table)")

    # ------------------ PROYEK 8: BANK LOAN ------------------
    with st.expander("🏦 8. Financial Risk & Bank Loan Portfolio Analytics (Multi-Page Power BI)"):
        col1, col2 = st.columns([1, 1.2])
        with col1:
            st.markdown("""
            **Overview:** Dashboard manajemen risiko portofolio pinjaman bank senilai **$435.7M Funded Amount** untuk analisis performa kredit.
            
            **Highlight Teknis:**
            * **Risk Ratio Analysis:** Memisahkan *Good Loan* (86.2%) vs *Bad Loan* (13.8%).
            * **Geographic Distribution:** Sebaran pemohon via US Map & analisis *Debt-to-Income (DTI)*.
            
            **Tech Stack:** `Power BI` • `DAX` • `Financial Modeling`
            """)
        with col2:
            st.write("**🖼️ Pilih Halaman Dashboard:**")
            loan_tab1, loan_tab2, loan_tab3 = st.tabs(["Page 1: Summary", "Page 2: Overview Map", "Page 3: Granular Details"])
            with loan_tab1:
                st_lightbox_image("Loan1.png", img_id="loan_1", caption="Page 1 - Summary Good vs Bad Loan Status")
            with loan_tab2:
                st_lightbox_image("Loan2.png", img_id="loan_2", caption="Page 2 - Overview US Geographic Distribution")
            with loan_tab3:
                st_lightbox_image("Loan3.png", img_id="loan_3", caption="Page 3 - Details Granular Transaction Grid")

    # ------------------ SECTION KHUSUS: AUTOMATION VAULT ------------------
    st.markdown("---")
    st.subheader("⚙️ Enterprise Automation Case Studies (NDA Cleared)")
    st.info("Catatan: Data sensitif dan nama perusahaan disamarkan untuk mematuhi Perjanjian Kerahasiaan (NDA).")
    
    with st.expander("🔒 Studi Kasus 1: Otomatisasi Konsolidasi Laporan Stok Ratusan Sheet"):
        st.markdown("""
        * **Kondisi Awal:** Tim operasional harus membuka **6 file stok barang** yang terpisah, merapikan sheet rekap bulanan horizontal yang memiliki banyak kolom kosong (*empty gaps*), dan menggabungkan data dari ratusan sheet barang secara manual satu per satu. Proses ini memakan waktu **4–6 jam kerja** setiap bulannya dan rawan kesalahan ketik (*human error*).
        * **Solusi Otomatisasi:** Mengembangkan program Python khusus yang secara otomatis mendeteksi pola tabel horizontal, melompati kolom kosong dengan cerdas, mengonsolidasikan ratusan sheet tersebut ke dalam satu dataset bersih, lalu menyusun laporan ringkasan bulanan yang rapi.
        * **Dampak Bisnis:** Waktu pengerjaan terpangkas dari **6 jam menjadi hanya 15 detik** dengan tingkat keakuratan data 100%. Tim operasional kini bisa fokus pada analisis stok, bukan memindahkan data.
        """)

    with st.expander("🔒 Studi Kasus 2: Penyatuan Format Invoice Multi-File Berantakan"):
        st.markdown("""
        * **Kondisi Awal:** Data transaksi tersebar di banyak file invoice individual (satu file hanya berisi satu invoice) dengan format baris yang tidak konsisten dan berantakan dan juga terdapat beberapa file dengan isi 1 filenya berisi banyak invoice.
        * **Solusi Otomatisasi:** Mengembangkan skrip otomatisasi Python untuk memindai folder secara otomatis, mengekstrak nilai-nilai kunci dari setiap file invoice (seperti No. Invoice, Tanggal, Nominal, dan Nama Klien), lalu menyatukannya ke dalam satu dataset yang siap dianalisis.
        * **Dampak Bisnis:** Menghilangkan kebutuhan entri data manual harian, menghemat waktu administrasi hingga **95%**, dan mempercepat proses audit keuangan mingguan.
        """)

    with st.expander("🔒 Studi Kasus 3: Automasi & Penataan Data Perpajakan Multi-Sheet (Python ETL)"):
        st.markdown("""
        * **Kondisi Awal:** Pengolahan data transaksi perpajakan mentah yang tersebar di banyak sheet Excel membutuhkan proses pemilihan manual untuk mengkategorikan komponen perpajakan. Proses manual ini berisiko tinggi terjadi human error dan memakan waktu rekapitulasi yang lama.
        * **Solusi Otomatisasi:** Membangun skrip otomatisasi berbasis Python untuk mengekstrak, membersihkan, dan mengelompokkan data dari berbagai sheet secara sistematis. Sistem secara otomatis memilah entitas menjadi kategori terstruktur: Master Data, DPP (Dasar Pengenaan Pajak), FP (Faktur Pajak), dan Penjualan Digunggung.
        * **Dampak Bisnis:** Mengubah data transaksi mentah yang terfragmentasi menjadi struktur database perpajakan yang rapi dan siap audit (audit-ready), serta memangkas waktu konsolidasi data pajak bulanan hingga 95%.
        """)

    with st.expander("🔒 Studi Kasus 4: Automasi Rekonsiliasi Rekening Koran"):
        st.markdown("""
        * **Kondisi Awal:** Proses ekstraksi dan rekonsiliasi data rekening koran perusahaan selama 12 bulan yang dilakukan dengan copy-paste & konversi manual. Cara ini sangat lambat, sering memicu formatting error, serta menyulitkan pemisahan mutasi debit, kredit, dan perhitungan saldo berjalan (running balance).
        * **Solusi Otomatisasi:** Merancang arsitektur automasi pengolahan data rekening koran tahunan. Sistem secara cerdas melakukan parsing data mutasi, memisahkan kolom Debet dan Kredit secara presisi, menghitung saldo akhir otomatis per baris, dan menyusun laporan konsolidasi rekening secara instan.
        * **Dampak Bisnis:** Menghilangkan risiko kesalahan input manual (zero copy-paste), mempercepat proses pencatatan data perbulan dari perusahaan yang hasilnya bisa memangkas waktu kerja hingga 90% dibandingkan metode manual, serta menghasilkan laporan keuangan yang siap audit dengan akurasi tinggi.
        """)

    # ------------------ SECTION KHUSUS: HACKATHON ------------------
    st.markdown("---")
    st.subheader("🏆 Hackathon & Case Studies")
    st.info("Halaman ini berisi rangkuman hasil kompetisi hackathon yang pernah diikuti, menampilkan proyek data analytics dan solusi teknis yang dikembangkan dalam konteks kompetitif.")
        
    with st.expander("Graduated Hackathon Data Analytics — Kementerian Komunikasi dan Digital RI x DQLab"):
        st.markdown("""**Tech Stack:** `Excel` • `Pandas` • `OpenPyXL` • `Rule Engine`""")
        col1, col2 = st.columns([1, 1.2])
        with col1:
            st.markdown("""
            * **Problem:** Menganalisis dan memproyeksikan keputusan bisnis investasi properti (pembangunan & penyewaan kos) jangka panjang (10 tahun) dengan dinamika aturan bisnis yang kompleks, batas threshold modal dinamis, serta perubahan harga sewa yang tidak bisa diakomodasi oleh rumus Excel statis.
            * **Solution:** Membangun algorithmic simulation engine menggunakan Python (pandas & openpyxl) yang memproyeksikan arus kas bulanan, keputusan ekspansi kamar berdasarkan kondisi threshold rasio modal, serta mitigasi perubahan aturan (rules) bisnis secara otomatis dari berkas masukan (input file).
            * **Impact:** Menghasilkan laporan proyeksi keuangan bulanan yang presisi dan audit-ready (simulasi.xlsx) mencakup rekapitulasi saldo harian/bulanan, pertumbuhan unit kamar, dan ringkasan portofolio aset akhir (Sheet Harta) untuk seluruh pemilik aset.
            """)
        with col2:
            st.write("**Bagan ini menggambarkan bagaimana skrip simulation.py bekerja mengolah raw rules menjadi financial ledger:**")
            st_lightbox_image("hackathon1.png", img_id="hk_1", caption="Skema Alur Simulasi Data")

    with st.expander("Top Finalist Hackathon: Retail Crisis & Recovery Visualization Challenge using Python"):
        st.markdown("""**Tech Stack:** `Pandas` • `Matplotlib` • `Numpy` • `Mlxtend (Apriori)` • `ETL`""")
        col1, col2 = st.columns([1, 1.2])
        with col1:
            st.markdown("""
            * **Problem:** Toko retail (DQFresh Mart) mengalami penurunan omzet selama 6 bulan berturut-turut akibat fokus hanya pada produk bestseller tradisional, sehingga luput mendeteksi produk tersembunyi yang permintaannya sedang melonjak (Rising Stars) namun sering kehabisan stok.
            * **Solution:** Merancang analytics pipeline menggunakan Python (pandas, matplotlib, mlxtend) dengan mengaplikasikan 3-day Moving Average (MA) untuk memisahkan tren naik (>= 12 hari berturut-turut) serta mengintegrasikan Algoritma Apriori untuk menemukan kombinasi produk cross-selling (Potential Packaging).
            * **Impact:** Berhasil mengidentifikasi produk Rising Star dengan tren pertumbuhan hingga +712 % dan menghasilkan rekomendasi bundling berbasis nilai Lift (>= 2.0), yang disajikan melalui 2 grafik publication-grade (Indeks Pertumbuhan Relatif Base 100 & Trend Sales Asli).
            """)
        with col2:
            st.write("**Hasil Dashboard Program**")
            hack2_tab1, hack2_tab2 = st.tabs(["Analisis Pertama", "Analisis Kedua"])
            with hack2_tab1:
                st_lightbox_image("rising_star_index.png", img_id="rs_idx", caption="Analisis Pertumbuhan Relatif Produk Rising Star - Base 100")
            with hack2_tab2:
                st_lightbox_image("rising_star_actual.png", img_id="rs_act", caption="Analisis Nilai Penjualan Produk Rising Star - Nilai Penjualan Asli")

    with st.expander("Score 100 SQL Hackathon: Sales Performance Root Cause Analysis"):
        st.markdown("""**Tech Stack:** `MySQL` • `Hierarchical Data Parsing` • `Population Statistics` • `Z-Score Analysis`""")
        col1, col2 = st.columns([1, 1.2])
        with col1:
            st.markdown("""
            * **Problem:** PT XYZ (Distributor Makanan Kering) mengalami kendala aktual penjualan yang stagnan meskipun angka Purchase Order (PO) tinggi, diduga akibat distribusi pemesanan sales lapangan yang tidak merata dan terdistorsi di berbagai level manajemen.
            * **Solution:** Merancang kueri SQL murni pada MySQL 5.7 (tanpa fitur modern seperti CTE atau Window Functions) untuk melakukan penelusuran hierarki organisasi secara rekursif hingga ke Sales Manager Level 2, kemudian menghitung statistik populasi.
            * **Impact:** Mendeteksi transaksi anomali secara presisi menggunakan kriteria matematis Z-score(|Z| > 3), serta menyajikan laporan single-output yang menggabungkan summary total anomali per manager dan detail log transaksi outlier.
            """)
        with col2:
            st.write("**Bagan Arsitektur & Logika SQL**")
            st_lightbox_image("hackathon2.png", img_id="hk_2", caption="Bagan Arsitektur & Logika SQL")

# ==================== TAB 3: BUSINESS & SERVICES ====================
with tab3:
    st.subheader("💡 Masih Mengolah Data Secara Manual? Mari Buat Data Anda Menjadi Lebih Cepat dan Terstruktur")
    st.write("Saya membantu UMKM, pelaku usaha, dan profesional mengubah proses manual menjadi sistem data yang lebih terstruktur, otomatis, dan mudah dipahami")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="custom-card">
            <h3 style="color: #d4af37; margin-top:0;">⚡ Otomatisasi Laporan</h3>
            <p style="font-size: 0.95rem; color: #cbd5e0;">Ubah proses input dan pengolahan data manual yang berulang-ulang menjadi sistem otomatisasi.</p>
            <ul style="font-size: 0.85rem; color: #a0aec0; padding-left: 20px;">
                <li>Otomatisasi Input Data</li>
                <li>Rekap Laporan Otomatis</li>
                <li>Automasi Python & VBA Macros</li>
                <li>Pengolahan File Berulang (Batch Processing)</li>
                <li>Sistem Pelaporan Terjadwal</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="custom-card">
            <h3 style="color: #d4af37; margin-top:0;">📊 Dasbor Bisnis Interaktif</h3>
            <p style="font-size: 0.95rem; color: #cbd5e0;">Pantau performa bisnis secara visual dan ambil keputusan berdasarkan data.</p>
            <ul style="font-size: 0.85rem; color: #a0aec0; padding-left: 20px;">
                <li>Monitoring Target vs Achievement</li>
                <li>Tren Performa Produk & Wilayah</li>
                <li>Analisis Perilaku & Preferensi Konsumen</li>
                <li>Dashboard Penjualan & Keuangan</li>
                <li>Dashboard Operasional</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="custom-card">
            <h3 style="color: #d4af37; margin-top:0;">💻 Data Processing & Business Intelligence</h3>
            <p style="font-size: 0.95rem; color: #cbd5e0;">Data berantakan? Saya bantu mengubahnya menjadi data yang terstruktur dan siap dianalisis.</p>
            <ul style="font-size: 0.85rem; color: #a0aec0; padding-left: 20px;">
                <li>Data Cleaning & Transformation</li>
                <li>Perancangan ETL Pipeline</li>
                <li>Query SQL & Pemodelan Data</li>
                <li>Olah Big Data (DuckDB & Polars)</li>
                <li>Analytics via Excel & Power BI</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="custom-card">
            <h3 style="color: #d4af37; margin-top:0;">🔄 Custom Data System & Automation</h3>
            <p style="font-size: 0.95rem; color: #cbd5e0;">Bangun sistem custom sesuai kebutuhan bisnis Anda. Mulai dari pengolahan data, dashboard, hingga otomatisasi end-to-end.</p>
            <ul style="font-size: 0.85rem; color: #a0aec0; padding-left: 20px;">
                <li>Web App Analytics (Streamlit)</li>
                <li>Custom Data Upload & Processing System</li>
                <li>Ekstraksi Data Otomatis (PDF to Excel)</li>
                <li>Custom Business Monitoring System</li>
                <li>End-to-End Automation Workflow</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    st.markdown('<div class="animated-section" style="text-align: center; margin-top: 20px;">', unsafe_allow_html=True)
    st.subheader("Siap Mengotomatiskan dan Mengoptimalkan Data Bisnis Anda?")
    st.write("Silakan klik tombol di bawah untuk menjadwalkan sesi konsultasi gratis membahas kebutuhan sistem bisnis Anda.")
    st.link_button("💬 Hubungi Saya via WhatsApp (Konsultasi Gratis)", "https://wa.me/+6285604054640")
    st.markdown('</div>', unsafe_allow_html=True)
