import os
import streamlit as st
import base64

# ==========================================
# 0. LOKASI FOLDER BASE_DIR
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_image_path(file_name):
    """Mengembalikan jalur file absolut berbasis lokasi script ini."""
    return os.path.join(BASE_DIR, file_name)

# ==========================================
# 1. KONFIGURASI HALAMAN UTAMA (HIDE SIDEBAR)
# ==========================================
st.set_page_config(
    page_title="Daffa Farros Azhari | Portfolio", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. HELPER FUNCTION: BACA BACKGROUND IMAGE
# ==========================================
def get_base64_image(image_path):
    full_path = image_path if os.path.isabs(image_path) else get_image_path(image_path)
    try:
        with open(full_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return ""

img_base64 = get_base64_image("background.png")

# ==========================================
# 3. HELPER FUNCTION: PURE CSS LIGHTBOX
# ==========================================
def st_lightbox_image(image_path: str, img_id: str, caption: str = ""):
    """Merender gambar dengan fitur Pure CSS Lightbox Zoom."""
    full_path = image_path if os.path.isabs(image_path) else get_image_path(image_path)
    try:
        with open(full_path, "rb") as img_file:
            b64_str = base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.error(f"⚠️ File '{image_path}' tidak ditemukan di folder project!")
        return

    html_code = f"""
    <style>
      #{img_id}-toggle {{ display: none !important; }}
      .img-thumb-{img_id} {{
        cursor: zoom-in;
        width: 100%;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
      }}
      .img-thumb-{img_id}:hover {{
        transform: translateY(-2px) scale(1.01);
        border-color: rgba(56, 189, 248, 0.5);
        box-shadow: 0 8px 25px rgba(56, 189, 248, 0.2);
      }}
      .overlay-{img_id} {{
        display: none;
        position: fixed !important;
        top: 0 !important; left: 0 !important;
        width: 100vw !important; height: 100vh !important;
        background: rgba(5, 8, 15, 0.95) !important;
        backdrop-filter: blur(10px) !important;
        z-index: 99999999 !important;
      }}
      .overlay-content-{img_id} {{
        position: fixed !important;
        top: 50% !important; left: 50% !important;
        transform: translate(-50%, -50%) !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        max-width: 92vw !important; max-height: 92vh !important;
        z-index: 100000000 !important;
      }}
      .overlay-content-{img_id} img {{
        max-width: 90vw !important; max-height: 84vh !important;
        object-fit: contain !important;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.15);
      }}
      #{img_id}-toggle:checked ~ .overlay-{img_id} {{ display: block !important; }}
      .caption-{img_id} {{
        text-align: center; font-size: 0.85rem; color: #94a3b8; margin-top: 8px;
      }}
      .overlay-caption-{img_id} {{
        color: #f8fafc; font-size: 0.9rem; margin-top: 12px;
        background: rgba(15, 23, 42, 0.85); padding: 8px 20px;
        border-radius: 30px; border: 1px solid rgba(56, 189, 248, 0.3);
      }}
    </style>

    <input type="checkbox" id="{img_id}-toggle">
    <label for="{img_id}-toggle" style="display: block; width: 100%;">
      <img class="img-thumb-{img_id}" src="data:image/png;base64,{b64_str}" alt="{caption}">
    </label>
    {f'<div class="caption-{img_id}">🔍 {caption}</div>' if caption else ''}

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
# 4. CUSTOM STYLING (FIXED TAB RATA/FULL WIDTH + ICON SAFE)
# ==========================================
css_code = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* 1. AMAN KAN FONT ICON STREAMLIT */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], p, h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Sembunyikan Sidebar Total */
    [data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
    }

    html, body, [data-testid="stAppViewContainer"] {
        color: #f1f5f9 !important;
        background-color: #060913 !important;
    }

    /* Container layout */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1200px !important;
    }

    /* 2. BACKGROUND */
    [data-testid="stAppViewContainer"] {
        background: 
            radial-gradient(circle at 50% 0%, rgba(56, 189, 248, 0.08) 0%, transparent 60%),
            linear-gradient(rgba(6, 9, 19, 0.92), rgba(6, 9, 19, 0.98)),
            url("data:image/png;base64,GAMBAR_LOKAL_BASE64") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }

    /* 3. HERO PROFILE CARD */
    .profile-img-container img {
        border-radius: 16px !important;
        border: 2px solid rgba(56, 189, 248, 0.3) !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5) !important;
        object-fit: cover;
    }

    /* Social Pill Buttons */
    .social-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 6px 14px;
        color: #e2e8f0 !important;
        text-decoration: none !important;
        font-size: 0.88rem;
        font-weight: 500;
        transition: all 0.25s ease;
        margin-right: 8px;
        margin-top: 10px;
    }
    .social-pill:hover {
        background: rgba(56, 189, 248, 0.15);
        border-color: rgba(56, 189, 248, 0.5);
        color: #38bdf8 !important;
        transform: translateY(-2px);
    }

    /* 4. STAT CARDS KPI */
    .stat-box {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 14px;
        padding: 18px 12px;
        text-align: center;
        backdrop-filter: blur(6px);
    }
    .stat-number {
        font-size: 1.85rem;
        font-weight: 800;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stat-label {
        font-size: 0.76rem;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 4px;
    }

    /* 5. TABS STYLING (PERBAIKAN FULL WIDTH & RATA TENGAH) */
    .stTabs [data-baseweb="tab-list"] {
        display: flex !important;
        width: 100% !important;
        gap: 8px;
        background-color: rgba(15, 23, 42, 0.6);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .stTabs [data-baseweb="tab"] {
        flex: 1 !important;
        text-align: center !important;
        justify-content: center !important;
        height: 44px;
        border-radius: 8px;
        color: #94a3b8 !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 0 10px !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3) !important;
    }

    /* 6. CORE SKILL CARD BADGES */
    .skill-card {
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-left: 3px solid #38bdf8;
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 10px;
        font-size: 0.92rem;
        font-weight: 600;
        color: #e2e8f0;
        display: flex;
        align-items: center;
        gap: 10px;
        transition: all 0.2s ease;
    }
    .skill-card:hover {
        background: rgba(56, 189, 248, 0.1);
        border-color: rgba(56, 189, 248, 0.4);
        transform: translateX(4px);
    }

    /* 7. EXPANDER MODERN */
    [data-testid="stExpander"] {
        background: rgba(15, 23, 42, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.07) !important;
        border-radius: 12px !important;
        margin-bottom: 12px !important;
        overflow: hidden !important;
    }
    [data-testid="stExpander"]:hover {
        border-color: rgba(56, 189, 248, 0.3) !important;
    }

    /* 8. TECH BADGES */
    .tool-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 8px;
        padding: 8px 16px;
        margin: 4px;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.85rem;
        color: #e2e8f0 !important;
    }

    /* 9. SERVICES CARDS */
    .custom-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.7) 0%, rgba(11, 17, 32, 0.8) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        padding: 22px !important;
        border-radius: 14px !important;
        height: 100%;
    }

    /* WHATSAPP BUTTON */
    [data-testid="stLinkButton"] a {
        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%) !important;
        color: #ffffff !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        padding: 12px 24px !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 15px rgba(37, 211, 102, 0.3) !important;
        transition: all 0.25s ease !important;
    }
    [data-testid="stLinkButton"] a:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(37, 211, 102, 0.5) !important;
    }

    header[data-testid="stHeader"] { background: transparent !important; }
</style>
"""

st.markdown(css_code.replace("GAMBAR_LOKAL_BASE64", img_base64), unsafe_allow_html=True)

# ==========================================
# 5. HERO HEADER (PROFIL ATAS)
# ==========================================
with st.container():
    col_photo, col_info = st.columns([1, 3.8], gap="medium")
    
    with col_photo:
        st.markdown('<div class="profile-img-container">', unsafe_allow_html=True)
        st.image(get_image_path("foto_daffa.png"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_info:
        st.markdown("""
        <div style="padding-left: 5px;">
            <h1 style="font-size: 2.5rem; font-weight: 800; margin-bottom: 2px; color: #f8fafc;">
                Daffa Farros Azhari
            </h1>
            <p style="font-size: 1.15rem; color: #38bdf8; font-weight: 600; margin-bottom: 8px;">
                Data Analyst & Automation Specialist
            </p>
            <p style="font-size: 0.92rem; color: #94a3b8; margin-bottom: 12px;">
                📍 Sidoarjo, Indonesia
            </p>
            <p style="font-size: 1rem; color: #cbd5e1; max-width: 850px; line-height: 1.5; margin-bottom: 16px;">
                Mengubah data mentah dan kompleks menjadi <b style="color: #38bdf8;">insight akurat</b> serta <b style="color: #f59e0b;">sistem otomatisasi efisien</b> untuk mendukung keputusan bisnis bernilai tinggi.
            </p>
            <div>
                <a href="mailto:azharidaffa18@gmail.com" class="social-pill">📩 Email</a>
                <a href="https://linkedin.com/in/daffafarros" target="_blank" class="social-pill">💼 LinkedIn</a>
                <a href="https://github.com/Daffa-Fazhar/Portofolio" target="_blank" class="social-pill">💻 GitHub</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 6. QUICK METRICS BANNER (DIPISAH PROSES VS REAL CASE)
# ==========================================
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown('<div class="stat-box"><div class="stat-number">30+</div><div class="stat-label">Total Data Projects</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="stat-box"><div class="stat-number">9</div><div class="stat-label">Enterprise Cases (0 Complaint)</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="stat-box"><div class="stat-number">110M+</div><div class="stat-label">Rows Data Handled</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown('<div class="stat-box"><div class="stat-number">90%</div><div class="stat-label">Time Saved via Automation</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 7. TAB NAVIGATION (RATA FULL WIDTH)
# ==========================================
tab1, tab2, tab3 = st.tabs(["👤 Tentang Saya & Tech Stack", "📂 Portofolio Proyek", "💼 Layanan & Solusi Bisnis"])

# ==================== TAB 1: PERSONAL & CORE SKILLS ====================
with tab1:
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
    
    # 🎯 core skills section (clean 2-column grid)
    st.subheader("🎯 Core Competencies")
    st.write("Keahlian utama yang saya kuasai dalam mengolah dan mengotomatisasi data secara end-to-end:")
    
    sk_col1, sk_col2 = st.columns(2)
    with sk_col1:
        st.markdown('<div class="skill-card">✅ End to End Data Analytics</div>', unsafe_allow_html=True)
        st.markdown('<div class="skill-card">✅ SQL & Query Optimization</div>', unsafe_allow_html=True)
        st.markdown('<div class="skill-card">✅ Python for Data Analysis & Automation</div>', unsafe_allow_html=True)
        st.markdown('<div class="skill-card">✅ Advanced Microsoft Excel & VBA</div>', unsafe_allow_html=True)
    with sk_col2:
        st.markdown('<div class="skill-card">✅ Data Visualization & Reporting</div>', unsafe_allow_html=True)
        st.markdown('<div class="skill-card">✅ ETL & Data Processing</div>', unsafe_allow_html=True)
        st.markdown('<div class="skill-card">✅ Interactive Dashboard Development</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🛠️ Technical Stack & Frameworks")
    st.write("Teknologi dan kerangka kerja spesifik yang saya gunakan:")
    
    st.markdown("""
        <div style="margin-top: 15px; margin-bottom: 20px;">
            <span class="tool-badge">
                <img src="https://img.icons8.com/color/48/python--v1.png" width="18"/> Python (Polars, Pandas, DuckDB, Streamlit, OpenPyXL)
            </span>
            <span class="tool-badge">
                <img src="https://img.icons8.com/color/48/power-bi.png" width="18"/> Power BI / DAX
            </span>
            <span class="tool-badge">
                <img src="https://img.icons8.com/color/48/microsoft-excel-2019.png" width="18"/> Advanced Microsoft Excel & VBA
            </span>
            <span class="tool-badge">
                <img src="https://img.icons8.com/color/48/database.png" width="18"/> SQL (MySQL & SQL Server SSMS)
            </span>
        </div>
    """, unsafe_allow_html=True)

# ==================== TAB 2: PORTFOLIO & PROGRESS ====================
with tab2:
    st.subheader("Featured Projects & Technical Cases")
    st.write("Klik pada gambar di bawah untuk mengaktifkan fitur **Fullscreen Zoom**:")
    
    # ------------------ PROYEK 1: E-COMMERCE BIG DATA ------------------
    with st.expander("1. E-Commerce Engine: 110M+ Rows Analysis (Polars + DuckDB + Streamlit + Plotly)"):
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("""
            **Tantangan:** Menganalisis data transaksi e-commerce berukuran raksasa (>110 juta baris) tanpa mengalami kemacetan memori (*out-of-memory*) di komputer standar.  
            **Solusi:** Menggunakan **Polars** untuk pemrosesan data cepat berbasis memori dan **DuckDB** untuk query SQL yang sangat efisien langsung di atas file parket.  
            **Hasil:** Sistem dasbor Streamlit yang mampu memuat agregasi data miliaran rupiah dalam waktu kurang dari 2 detik!
            """)
        with col2:
            st_lightbox_image("Dashboard_110.png", img_id="dash_110", caption="Dashboard Analisis 110 Juta Data")

    # ------------------ PROYEK 2: OLIST RETAIL ANALYTICS ------------------
    with st.expander("2. Olist End-to-End Retail Analytics (Polars + SQL + Power BI)"):
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
    with st.expander("3. Instacart Market Basket Analysis (Polars + DuckDB + Streamlit + Plotly)"):
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
    with st.expander("4. Indonesia Regional Sales & Geographic Heatmap Analytics (Advanced Excel)"):
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
    with st.expander("5. Medical Analytics: Patients & Billing Executive Overview (Power BI + Excel)"):
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
    with st.expander("6. Commercial Sales Target vs Achievement & Operational Slicer System (Advanced Excel + VBA)"):
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("""
            **Tantangan:** Memantau ketercapaian target penjualan harian dan mingguan yang sering mengalami selisih (*gap*) antara barang masuk (*Sell-In*) dan keluar (*Sell-Out*).  
            **Solusi:** Menggabungkan *Advanced Excel Formulas*, *Conditional Formatting*, *Interactive Pivot Table*, *Slicers*, dan *VBA Macro* untuk kalkulasi otomatis.  
            **Hasil:** Panel kendali operasional lengkap dengan matriks *Achievement % (Gauge Chart)*, *Gap Unit*, *Timegone Rate*, serta performa tim *Promotor Name*.
            """)
        with col2:
            st_lightbox_image("Dashboard_monitoring.png", img_id="dash_mon", caption="Sales Monitoring Combination System")

    # ------------------ PROYEK 7: SPOTIFY ------------------
    with st.expander("7. Spotify Music Behavioral Analytics (Multi-Page Power BI & SSMS)", expanded=True):
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
    with st.expander("8. Financial Risk & Bank Loan Portfolio Analytics (Multi-Page Power BI)"):
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
    st.info("🔒 Catatan: Data sensitif dan nama perusahaan disamarkan untuk mematuhi Perjanjian Kerahasiaan (NDA).")
    
    with st.expander("🔒 Studi Kasus 1: Otomatisasi Konsolidasi Laporan Stok Ratusan Sheet"):
        st.markdown("""
        * **Kondisi Awal:** Tim operasional harus membuka **6 file stok barang** yang terpisah, merapikan sheet rekap bulanan horizontal yang memiliki banyak kolom kosong (*empty gaps*), dan menggabungkan data dari ratusan sheet barang secara manual satu per satu. Proses ini memakan waktu **4–6 jam kerja** setiap bulannya dan rawan kesalahan ketik (*human error*).
        * **Solusi Otomatisasi:** Mengembangkan program Python khusus yang secara otomatis mendeteksi pola tabel horizontal, melompati kolom kosong dengan cerdas, mengonsolidasikan ratusan sheet tersebut ke dalam satu dataset bersih, lalu menyusun laporan ringkasan bulanan yang rapi.
        * **Dampak Bisnis:** Waktu pengerjaan terpangkas dari **6 jam menjadi hanya 15 detik** dengan tingkat keakuratan data 100%.
        """)

    with st.expander("🔒 Studi Kasus 2: Penyatuan Format Invoice Multi-File Berantakan"):
        st.markdown("""
        * **Kondisi Awal:** Data transaksi tersebar di banyak file invoice individual dengan format baris yang tidak konsisten dan berantakan.
        * **Solusi Otomatisasi:** Mengembangkan skrip otomatisasi Python untuk memindai folder secara otomatis, mengekstrak nilai-nilai kunci dari setiap file invoice (seperti No. Invoice, Tanggal, Nominal, dan Nama Klien), lalu menyatukannya ke dalam satu dataset yang siap dianalisis.
        * **Dampak Bisnis:** Menghilangkan kebutuhan entri data manual harian, menghemat waktu administrasi hingga **95%**, dan mempercepat proses audit keuangan mingguan.
        """)

    with st.expander("🔒 Studi Kasus 3: Automasi & Penataan Data Perpajakan Multi-Sheet (Python ETL)"):
        st.markdown("""
        * **Kondisi Awal:** Pengolahan data transaksi perpajakan mentah yang tersebar di banyak sheet Excel membutuhkan proses pemilihan manual untuk mengkategorikan komponen perpajakan.
        * **Solusi Otomatisasi:** Membangun skrip otomatisasi berbasis Python untuk mengekstrak, membersihkan, dan mengelompokkan data dari berbagai sheet secara sistematis. Sistem secara otomatis memilah entitas menjadi kategori terstruktur: Master Data, DPP (Dasar Pengenaan Pajak), FP (Faktur Pajak), dan Penjualan Digunggung.
        * **Dampak Bisnis:** Mengubah data transaksi mentah yang terfragmentasi menjadi struktur database perpajakan yang rapi dan siap audit (audit-ready), serta memangkas waktu konsolidasi data pajak bulanan hingga 95%.
        """)

    with st.expander("🔒 Studi Kasus 4: Automasi Rekonsiliasi Rekening Koran"):
        st.markdown("""
        * **Kondisi Awal:** Proses ekstraksi dan rekonsiliasi data rekening koran perusahaan selama 12 bulan yang dilakukan dengan copy-paste & konversi manual.
        * **Solusi Otomatisasi:** Merancang arsitektur automasi pengolahan data rekening koran tahunan. Sistem secara cerdas melakukan parsing data mutasi, memisahkan kolom Debet dan Kredit secara presisi, menghitung saldo akhir otomatis per baris, dan menyusun laporan konsolidasi rekening secara instan.
        * **Dampak Bisnis:** Menghilangkan risiko kesalahan input manual (zero copy-paste), mempercepat proses pencatatan data perbulan hingga 90%, serta menghasilkan laporan keuangan yang siap audit dengan akurasi tinggi.
        """)

    # ------------------ SECTION KHUSUS: HACKATHON ------------------
    st.markdown("---")
    st.subheader("🏆 Hackathon & Competitive Case Studies")
    st.info("Halaman ini berisi rangkuman hasil kompetisi hackathon yang pernah diikuti, menampilkan proyek data analytics dan solusi teknis yang dikembangkan dalam konteks kompetitif.")
        
    with st.expander("Graduated Hackathon Data Analytics — Kementerian Komunikasi dan Digital RI x DQLab"):
        st.markdown("""**Tech Stack:** `Excel` • `Pandas` • `OpenPyXL` • `Rule Engine`""")
        col1, col2 = st.columns([1, 1.2])
        with col1:
            st.markdown("""
            * **Problem:** Menganalisis dan memproyeksikan keputusan bisnis investasi properti jangka panjang (10 tahun) dengan dinamika aturan bisnis yang kompleks.
            * **Solution:** Membangun algorithmic simulation engine menggunakan Python (pandas & openpyxl) yang memproyeksikan arus kas bulanan dan keputusan ekspansi secara otomatis.
            * **Impact:** Menghasilkan laporan proyeksi keuangan bulanan yang presisi dan audit-ready untuk seluruh pemilik aset.
            """)
        with col2:
            st.write("**Bagan Alur Kerja Simulasi Financial Ledger:**")
            st_lightbox_image("hackathon1.png", img_id="hk_1", caption="Skema Alur Simulasi Data")

    with st.expander("Top Finalist Hackathon: Retail Crisis & Recovery Visualization Challenge using Python"):
        st.markdown("""**Tech Stack:** `Pandas` • `Matplotlib` • `Numpy` • `Mlxtend (Apriori)` • `ETL`""")
        col1, col2 = st.columns([1, 1.2])
        with col1:
            st.markdown("""
            * **Problem:** Toko retail mengalami penurunan omzet selama 6 bulan berturut-turut akibat fokus hanya pada produk bestseller tradisional.
            * **Solution:** Merancang analytics pipeline menggunakan Python dengan 3-day Moving Average (MA) serta mengintegrasikan Algoritma Apriori untuk menemukan kombinasi produk cross-selling.
            * **Impact:** Berhasil mengidentifikasi produk Rising Star dengan tren pertumbuhan hingga +712% dan menghasilkan rekomendasi bundling berbasis nilai Lift (>= 2.0).
            """)
        with col2:
            st.write("**Hasil Dashboard Program**")
            hack2_tab1, hack2_tab2 = st.tabs(["Analisis Pertumbuhan", "Analisis Penjualan"])
            with hack2_tab1:
                st_lightbox_image("rising_star_index.png", img_id="rs_idx", caption="Pertumbuhan Relatif Produk Rising Star - Base 100")
            with hack2_tab2:
                st_lightbox_image("rising_star_actual.png", img_id="rs_act", caption="Nilai Penjualan Produk Rising Star - Nilai Asli")

    with st.expander("Score 100 SQL Hackathon: Sales Performance Root Cause Analysis"):
        st.markdown("""**Tech Stack:** `MySQL` • `Hierarchical Data Parsing` • `Population Statistics` • `Z-Score Analysis`""")
        col1, col2 = st.columns([1, 1.2])
        with col1:
            st.markdown("""
            * **Problem:** Distributor makanan mengalami kendala aktual penjualan yang stagnan meskipun angka PO tinggi.
            * **Solution:** Merancang kueri SQL murni pada MySQL 5.7 untuk melakukan penelusuran hierarki organisasi secara rekursif hingga ke Sales Manager Level 2.
            * **Impact:** Mendeteksi transaksi anomali secara presisi menggunakan kriteria matematis Z-score (|Z| > 3).
            """)
        with col2:
            st.write("**Bagan Arsitektur & Logika SQL**")
            st_lightbox_image("hackathon2.png", img_id="hk_2", caption="Bagan Arsitektur & Logika SQL")

# ==================== TAB 3: BUSINESS & SERVICES ====================
with tab3:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h2 style="color: #f8fafc; font-weight: 800; font-size: 2rem;">💡 Solusi Data & Automasi Bisnis</h2>
        <p style="color: #94a3b8; font-size: 1.05rem; max-width: 800px; margin: 0 auto;">
            Transformasi pengolahan data manual yang lambat dan rawan error menjadi sistem otomatis, interaktif, dan akurat.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 🌟 HERO POSTER BANNER (DITARUH DI ATAS 4 CARDS)
    # Fitur Zoom Lightbox dipasang agar klien bisa klik dan perjelas posternya
    st_lightbox_image("poster.png", img_id="service_poster", caption="Overview Solusi Data Analytics & Automation")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 4 CARDS DETAIL LAYANAN
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="custom-card">
            <h3 style="color: #38bdf8; margin-top:0; font-size: 1.15rem;">⚡ Otomatisasi Laporan</h3>
            <p style="font-size: 0.9rem; color: #cbd5e0;">Ubah proses input dan pengolahan data manual menjadi sistem otomatisasi.</p>
            <ul style="font-size: 0.83rem; color: #94a3b8; padding-left: 18px;">
                <li>Otomatisasi Input Data</li>
                <li>Rekap Laporan Otomatis</li>
                <li>Automasi Python & VBA Macros</li>
                <li>Batch Processing Multi-File</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="custom-card">
            <h3 style="color: #f59e0b; margin-top:0; font-size: 1.15rem;">📊 Dasbor Bisnis Interaktif</h3>
            <p style="font-size: 0.9rem; color: #cbd5e0;">Pantau performa bisnis secara visual dan ambil keputusan berbasis data presisi.</p>
            <ul style="font-size: 0.83rem; color: #94a3b8; padding-left: 18px;">
                <li>Target vs Achievement Monitoring</li>
                <li>Tren Performa Produk & Wilayah</li>
                <li>Analisis Perilaku Konsumen</li>
                <li>Dashboard Penjualan & Keuangan</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="custom-card">
            <h3 style="color: #10b981; margin-top:0; font-size: 1.15rem;">💻 Data Processing & BI</h3>
            <p style="font-size: 0.9rem; color: #cbd5e0;">Data berantakan? Saya bantu merapikan dan menyajikannya siap dianalisis.</p>
            <ul style="font-size: 0.83rem; color: #94a3b8; padding-left: 18px;">
                <li>Data Cleaning & Transformation</li>
                <li>Perancangan ETL Pipeline</li>
                <li>Query SQL & Pemodelan Data</li>
                <li>Big Data Engine (DuckDB & Polars)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="custom-card">
            <h3 style="color: #c084fc; margin-top:0; font-size: 1.15rem;">🔄 Custom Data Systems</h3>
            <p style="font-size: 0.9rem; color: #cbd5e0;">Bangun sistem custom sesuai kebutuhan bisnis Anda dari pengolahan hingga otomatisasi.</p>
            <ul style="font-size: 0.83rem; color: #94a3b8; padding-left: 18px;">
                <li>Web App Analytics (Streamlit)</li>
                <li>Custom Data Processing</li>
                <li>Ekstraksi Data (PDF to Excel)</li>
                <li>End-to-End Automation Workflow</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # CALL TO ACTION (WHATSAPP)
    st.markdown("""
    <div style="text-align: center; margin-top: 25px; margin-bottom: 20px;">
        <h3 style="color: #f8fafc; font-size: 1.4rem;">Siap Mengotomatiskan dan Mengoptimalkan Data Bisnis Anda?</h3>
        <p style="color: #94a3b8; margin-bottom: 20px; font-size: 0.95rem;">Klik tombol di bawah untuk diskusi atau konsultasi mengenai kebutuhan sistem Anda.</p>
    </div>
    """, unsafe_allow_html=True)
    
    c_left, c_mid, c_right = st.columns([1, 2, 1])
    with c_mid:
        st.link_button("💬 Hubungi Saya via WhatsApp", "https://wa.me/+6285604054640", use_container_width=True)
