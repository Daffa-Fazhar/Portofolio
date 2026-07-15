import streamlit as st
import duckdb
import plotly.graph_objects as go
import plotly.express as px
import polars as pl
import os

# ==============================================================================
# 1. APPLICATION SETUP & PREMIUM DARK STYLE INJECTION (CSS)
# ==============================================================================
st.set_page_config(
    page_title="E-Commerce Big Data Analytics Server",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Deep Relative Pathing Management
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "ecommerce_data.db")

# Custom CSS Injection to perfectly replicate the executive dark-mode mockup
st.markdown("""
    <style>
        /* Base Application Workspace */
        .stApp {
            background-color: #0b0f19;
            color: #e2e8f0;
        }
        /* Sidebar Navigation Frame */
        [data-testid="stSidebar"] {
            background-color: #111625;
            border-right: 1px solid #1e293b;
        }
        /* Premium Floating KPI Cards */
        .premium-card {
            background: linear-gradient(145deg, #161d30 0%, #0f1320 100%);
            padding: 24px;
            border-radius: 12px;
            border: 1px solid #222f48;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            text-align: left;
            position: relative;
            overflow: hidden;
        }
        .premium-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; width: 100%; height: 4px;
        }
        .border-blue::before { background: #3b82f6; }
        .border-orange::before { background: #ea580c; }
        .border-green::before { background: #16a34a; }
        .border-purple::before { background: #9333ea; }
        
        .card-title {
            font-size: 12px;
            color: #64748b;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }
        .card-value {
            font-size: 34px;
            font-weight: 700;
            font-family: 'Segoe UI', Roboto, sans-serif;
            letter-spacing: -0.5px;
        }
        .card-subtitle {
            font-size: 11px;
            color: #475569;
            margin-top: 6px;
            font-weight: 500;
        }
    </style>
""", unsafe_allow_html=True)


# ==============================================================================
# 2. DATABASE CLIENT & META DATA BOUNDARY PIPELINE
# ==============================================================================
@st.cache_resource
def connect_database_engine():
    """Establishes a safe, high-speed connection engine to local DuckDB."""
    if not os.path.exists(DB_PATH):
        st.error(f"❌ Database Pipeline Error: File '{DB_PATH}' tidak ditemukan di relative path!")
        st.stop()
    return duckdb.connect(DB_PATH, read_only=True)

db_engine = connect_database_engine()

@st.cache_data(ttl=3600)
def pull_filter_boundaries():
    """Pre-loads filter parameters directly into pure Polars framework."""
    categories_list = db_engine.execute("""
        SELECT DISTINCT SPLIT_PART(category_code, '.', 1) as cat 
        FROM raw_ecommerce 
        WHERE category_code IS NOT NULL AND cat != ''
        ORDER BY cat
    """).pl()['cat'].to_list()
    
    brands_list = db_engine.execute("""
        SELECT brand, COUNT(*) as cnt 
        FROM raw_ecommerce 
        WHERE brand IS NOT NULL AND brand != ''
        GROUP BY 1 ORDER BY cnt DESC LIMIT 30
    """).pl()['brand'].to_list()
    
    return categories_list, brands_list

available_categories, available_brands = pull_filter_boundaries()


# ==============================================================================
# 3. INTERFACE COMPONENT: EXECUTIVE SIDEBAR CONTROLLER
# ==============================================================================
with st.sidebar:
    st.markdown("## ⚙️ Control Panel")
    st.markdown("Engine Filter: Querying over **110M+ operations** in real-time.")
    st.markdown("---")
    
    # 3.1 Month Selection (MoM Multi-Partition Filter)
    target_months = st.multiselect(
        "📅 Target Partition Range",
        options=["October 2019", "November 2019"],
        default=["October 2019", "November 2019"]
    )
    
    month_queries = []
    if "October 2019" in target_months: month_queries.append("month(CAST(event_time AS TIMESTAMP)) = 10")
    if "November 2019" in target_months: month_queries.append("month(CAST(event_time AS TIMESTAMP)) = 11")
    compiled_month_clause = f"({ ' OR '.join(month_queries) })" if month_queries else "1=0"
    
    # 3.2 Category Checklists
    chosen_categories = st.multiselect(
        "📁 Core Category Filter",
        options=available_categories,
        default=available_categories[:4] if available_categories else []
    )
    
    # 3.3 Brand Filters
    chosen_brands = st.multiselect(
        "🏷️ Manufacturer Brand Focus",
        options=available_brands,
        default=available_brands[:5] if available_brands else []
    )


# ==============================================================================
# 4. CORE COMPUTATIONAL PIPELINE (DYNAMIC SQL TRANSFORMATION ENGINE)
# ==============================================================================
# Compile isolated clauses to maximize columnar indexing speed
sql_filters = [compiled_month_clause]

if chosen_categories:
    cat_payload = ", ".join([f"'{c}'" for c in chosen_categories])
    where_conditions_cat = f"SPLIT_PART(category_code, '.', 1) IN ({cat_payload})"
    sql_filters.append(where_conditions_cat)
if chosen_brands:
    brand_payload = ", ".join([f"'{b}'" for b in chosen_brands])
    sql_filters.append(f"brand IN ({brand_payload})")

final_sql_where_statement = " WHERE " + " AND ".join(sql_filters)

@st.cache_data(ttl=600)
def process_analytical_matrix(where_clause):
    """Leverages DuckDB to crush big numbers and outputs pure Polars DataFrames."""
    
    # 4.1 Aggregating Master High-Level KPI Data (Sudah di-CAST ke DOUBLE)
    kpi_pl = db_engine.execute(f"""
        SELECT 
            COUNT(DISTINCT user_session) as total_sessions,
            COUNT(CASE WHEN event_type = 'cart' THEN 1 END) as total_cart,
            COUNT(CASE WHEN event_type = 'purchase' THEN 1 END) as total_purchase,
            COALESCE(SUM(CASE WHEN event_type = 'purchase' THEN CAST(price AS DOUBLE) END), 0) as total_revenue
        FROM raw_ecommerce {where_clause}
    """).pl()
    
    # 4.2 Aggregating Daily Operational Timeline Trend
    trend_pl = db_engine.execute(f"""
        SELECT 
            DATE_TRUNC('day', CAST(event_time AS TIMESTAMP)) as date,
            COUNT(DISTINCT user_session) as sessions,
            COUNT(CASE WHEN event_type = 'purchase' THEN 1 END) as purchases
        FROM raw_ecommerce {where_clause}
        GROUP BY 1 ORDER BY 1
    """).pl()

    # 4.3 Advanced Conversion Funnel Logic
    funnel_pl = db_engine.execute(f"""
        SELECT 
            COUNT(*) as volume,
            CASE 
                WHEN event_type = 'view' THEN '1. Product Views'
                WHEN event_type = 'cart' THEN '2. Add To Cart'
                WHEN event_type = 'purchase' THEN '3. Completed Purchase'
            END as step_label,
            CASE WHEN event_type = 'view' THEN 0 WHEN event_type = 'cart' THEN 1 ELSE 2 END as sort_order
        FROM raw_ecommerce {where_clause} AND event_type IN ('view', 'cart', 'purchase')
        GROUP BY 2, 3 ORDER BY sort_order ASC
    """).pl()
    
    # 4.4 Aggregating Peak Hourly Engagement Trends
    hourly_pl = db_engine.execute(f"""
        SELECT HOUR(CAST(event_time AS TIMESTAMP)) as hour_axis, COUNT(*) as velocity
        FROM raw_ecommerce {where_clause}
        GROUP BY 1 ORDER BY 1
    """).pl()

    # 4.5 Aggregating Financial Category Layout Performance (Sudah di-CAST ke DOUBLE)
    cat_perf_pl = db_engine.execute(f"""
        SELECT 
            SPLIT_PART(category_code, '.', 1) as category,
            SUM(CASE WHEN event_type = 'purchase' THEN CAST(price AS DOUBLE) END) as revenue,
            COUNT(CASE WHEN event_type = 'purchase' THEN 1 END) as orders
        FROM raw_ecommerce {where_clause}
        GROUP BY 1 ORDER BY revenue DESC LIMIT 5
    """).pl()

    # 4.6 Aggregating Elite Product Performance Framework
    top_products_pl = db_engine.execute(f"""
        SELECT 
            product_id, brand,
            COUNT(CASE WHEN event_type = 'view' THEN 1 END) as views,
            COUNT(CASE WHEN event_type = 'purchase' THEN 1 END) as sales
        FROM raw_ecommerce {where_clause}
        GROUP BY 1, 2 ORDER BY sales DESC LIMIT 5
    """).pl()

    return kpi_pl, trend_pl, funnel_pl, hourly_pl, cat_perf_pl, top_products_pl

# Fire pipeline execution
kpi, trend, funnel, hourly, cat_perf, top_products = process_analytical_matrix(final_sql_where_statement)


# ==============================================================================
# 5. BUSINESS INTELLIGENCE DASHBOARD INTERFACE DESIGN
# ==============================================================================
st.title("📊 E-Commerce Behavior Platform")
st.markdown("Architectural Multi-Month Dashboard — Driven by **DuckDB** & **Polars Core Engine**.")
st.markdown("---")

# 5.1 LAYER 1: LUXURY CARD METRICS RENDERING
col_m1, col_m2, col_m3, col_m4 = st.columns(4)

# Native Polars scalar extraction mechanism
val_sessions = kpi['total_sessions'][0] if kpi['total_sessions'][0] is not None else 0
val_cart = kpi['total_cart'][0] if kpi['total_cart'][0] is not None else 0
val_purchase = kpi['total_purchase'][0] if kpi['total_purchase'][0] is not None else 0
val_conversion = (val_purchase / val_sessions * 100) if val_sessions > 0 else 0.0

with col_m1:
    st.markdown(f'<div class="premium-card border-blue"><div class="card-title">Total Sessions</div><div class="card-value" style="color: #60a5fa;">{val_sessions:,}</div><div class="card-subtitle">Active Identity Logs</div></div>', unsafe_allow_html=True)
with col_m2:
    st.markdown(f'<div class="premium-card border-orange"><div class="card-title">Add To Cart</div><div class="card-value" style="color: #fb923c;">{val_cart:,}</div><div class="card-subtitle">Intentional Pipeline Volume</div></div>', unsafe_allow_html=True)
with col_m3:
    st.markdown(f'<div class="premium-card border-green"><div class="card-title">Purchases</div><div class="card-value" style="color: #4ade80;">{val_purchase:,}</div><div class="card-subtitle">Successful Checkouts Done</div></div>', unsafe_allow_html=True)
with col_m4:
    st.markdown(f'<div class="premium-card border-purple"><div class="card-title">Conversion Rate</div><div class="card-value" style="color: #c084fc;">{val_conversion:.2f}%</div><div class="card-subtitle">E-Commerce Efficiency Rate</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 5.2 LAYER 2: INTERACTIVE TIME TRENDS & CONVERSION FUNNELS
col_graph_left, col_graph_right = st.columns([1.3, 1])

with col_graph_left:
    st.markdown("#### 📉 Daily Transaction Trend Matrix")
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=trend['date'].to_list(), y=trend['sessions'].to_list(), name='Sessions Tracking', line=dict(color='#2563eb', width=2.5)))
    fig_trend.add_trace(go.Scatter(x=trend['date'].to_list(), y=trend['purchases'].to_list(), name='Purchases Tracking', line=dict(color='#10b981', width=2.5), yaxis='y2'))
    fig_trend.update_layout(
        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, tickfont=dict(color="#64748b")),
        yaxis=dict(title='Traffic Baseline', showgrid=False, tickfont=dict(color="#2563eb")),
        yaxis2=dict(title='Conversion Baseline', overlaying='y', side='right', showgrid=False, tickfont=dict(color="#10b981")),
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1)
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with col_graph_right:
    st.markdown("#### 🧪 Sales Funnel Performance Layout")
    fig_funnel = go.Figure(go.Funnel(
        y=funnel['step_label'].to_list(), 
        x=funnel['volume'].to_list(),
        textinfo="value+percent initial",
        marker=dict(color=["#f59e0b", "#ea580c", "#10b981"])
    ))
    fig_funnel.update_layout(
        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=140, r=20, t=20, b=20)
    )
    st.plotly_chart(fig_funnel, use_container_width=True)

# 5.3 LAYER 3: MARKET CATEGORIES, VELOCITY TARGETS & DELTA TABLES
col_b1, col_b2, col_b3 = st.columns([1, 1, 1.1])

with col_b1:
    st.markdown("#### 📊 Top Categories Revenue")
    fig_cat = px.bar(cat_perf, x='category', y='revenue', color='orders', color_continuous_scale='Bluered')
    fig_cat.update_layout(
        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, title='Macro Domain'), yaxis=dict(showgrid=False, title='Revenue Valuation ($)')
    )
    st.plotly_chart(fig_cat, use_container_width=True)

with col_b2:
    st.markdown("#### 🕒 Operational Peak Hours Velocity")
    fig_hour = px.line(hourly, x='hour_axis', y='velocity', markers=True)
    fig_hour.update_traces(line_color='#bc5090', marker=dict(size=6))
    fig_hour.update_layout(
        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, tickmode='linear', dtick=4, title='Hour Matrix Vector (UTC)'),
        yaxis=dict(showgrid=False, title='Event Logs Velocity')
    )
    st.plotly_chart(fig_hour, use_container_width=True)

with col_b3:
    st.markdown("#### 🏆 Top Products Performance Ledger")
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    # Streamlit natively handles Polars DataFrames cleanly
    st.dataframe(
        top_products,
        column_config={
            "product_id": "Product Identifier",
            "brand": "Manufacturer",
            "views": st.column_config.NumberColumn("Views Profile", format="%d 👁️"),
            "sales": st.column_config.NumberColumn("Purchases Profile", format="%d 💰")
        },
        use_container_width=True,
        hide_index=True
    )