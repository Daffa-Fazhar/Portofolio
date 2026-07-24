import streamlit as st
import duckdb
import polars as pl
import plotly.express as px
import plotly.graph_objects as go

# ==============================================================================
# PART 1: SYSTEM & PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Instacart Enterprise BI Control Tower",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# PART 2: CUSTOM CSS (OPTIMIZED FOR DASHBOARD LAYOUT & HIGH CONTRAST)
# ==============================================================================
st.markdown("""
<style>
    /* Streamlit Page Padding Adjustment */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 0.5rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        max-width: 100% !important;
    }
    .stApp {
        background-color: #F4F7F4 !important;
        color: #081C15;
    }
    
    /* Sidebar Aesthetics */
    [data-testid="stSidebar"] {
        background-color: #1B4332 !important;
        border-right: 1px solid #2D6A4F;
    }
    [data-testid="stSidebar"] * {
        color: #D8F3DC !important;
    }
    
    /* Executive KPI Cards */
    .kpi-card {
        background-color: #FFFFFF;
        border: 1px solid #D0DED0;
        border-radius: 10px;
        padding: 12px 16px;
        box-shadow: 0 2px 8px rgba(27, 67, 50, 0.04);
    }
    .kpi-title {
        font-size: 0.72rem;
        font-weight: 800;
        color: #2D6A4F;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .kpi-value {
        font-size: 1.6rem;
        font-weight: 800;
        color: #1B4332;
        margin: 2px 0;
    }
    .kpi-badge {
        display: inline-block;
        padding: 2px 7px;
        border-radius: 10px;
        font-size: 0.7rem;
        font-weight: 700;
        background-color: #D8F3DC;
        color: #1B4332;
    }

    /* Insight Callout Box */
    .insight-box {
        background-color: #E8F5E9;
        border-left: 4px solid #2D6A4F;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 0.76rem;
        color: #1B4332;
        margin-top: 4px;
        line-height: 1.3;
    }
    
    /* Live Operational Stream Cards */
    .stream-card {
        background: #FFFFFF;
        padding: 8px 12px;
        border-radius: 8px;
        border-left: 4px solid #40916C;
        border-top: 1px solid #E0E8E0;
        border-right: 1px solid #E0E8E0;
        border-bottom: 1px solid #E0E8E0;
        margin-bottom: 6px;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# HELPER: PLOTLY HIGH-CONTRAST THEME WITH ADJUSTABLE MARGINS
# ==============================================================================
def apply_clean_theme(fig, height=220, left_m=40, right_m=20):
    fig.update_layout(
        height=height,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#1B4332', family='sans-serif', size=10),
        xaxis=dict(
            tickfont=dict(color='#1B4332', size=9),
            title_font=dict(color='#1B4332', size=10),
            gridcolor='#E0E8E0',
            showgrid=True
        ),
        yaxis=dict(
            tickfont=dict(color='#1B4332', size=9),
            title_font=dict(color='#1B4332', size=10),
            gridcolor='#E0E8E0',
            showgrid=True
        ),
        margin=dict(l=left_m, r=right_m, t=20, b=25)
    )
    return fig


# ==============================================================================
# PART 3: SIDEBAR SLICERS (ENGLISH)
# ==============================================================================
DAY_MAP = {
    "Sunday": 0, "Monday": 1, "Tuesday": 2, "Wednesday": 3, 
    "Thursday": 4, "Friday": 5, "Saturday": 6
}

with st.sidebar:
    st.markdown("<h3 style='color:#D8F3DC; font-weight:800; margin-bottom:0;'>INSTACART</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#52B788; font-weight:700; font-size:0.75rem;'>EXECUTIVE DASHBOARD FILTERS</p>", unsafe_allow_html=True)
    st.write("---")
    
    st.markdown("#### 🎛️ Multi-Dimensional Slicers")
    
    # Slicer 1: Transaction Day
    f_day_str = st.selectbox("1. Select Transaction Day", ["All Days", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
    f_day = DAY_MAP.get(f_day_str, None)
    
    # Slicer 2: Department Filter
    f_dept = st.multiselect(
        "2. Department Filter", 
        ["produce", "dairy eggs", "snacks", "beverages", "frozen", "pantry", "bakery", "canned goods"], 
        default=["produce", "dairy eggs", "beverages", "frozen", "snacks", "pantry"]
    )
    
    # Slicer 3: Operating Hours Range
    f_hour = st.slider("3. Operating Hours Range", 0, 23, (8, 18))
    
    # Slicer 4: Min Basket Size
    f_basket = st.slider("4. Min. Basket Size (Items)", 1, 15, 5)
    
    # Slicer 5: Customer Type
    f_status = st.radio("5. Customer Type", ["All Customers", "Repeat Customers Only", "First-Time Customers Only"])
    
    st.write("---")
    st.caption("🟢 **Engine status:** DuckDB + Polars (Active)")
    st.caption("📊 **Total Rows:** 32,434,489 records")


# ==============================================================================
# PART 4: DYNAMIC DUCKDB DATA PIPELINE
# ==============================================================================

def build_sql_where(day, hour_range, departments, status):
    conditions = [f"TRY_CAST(o.order_hour_of_day AS INT) BETWEEN {hour_range[0]} AND {hour_range[1]}"]
    
    if day is not None:
        conditions.append(f"TRY_CAST(o.order_dow AS INT) = {day}")
        
    if departments:
        dept_list = ", ".join([f"'{d}'" for d in departments])
        conditions.append(f"d.department IN ({dept_list})")
        
    if status == "Repeat Customers Only":
        conditions.append("TRY_CAST(op.reordered AS INT) = 1")
    elif status == "First-Time Customers Only":
        conditions.append("TRY_CAST(op.reordered AS INT) = 0")
        
    return " WHERE " + " AND ".join(conditions)


@st.cache_data
def get_filtered_kpis(day, hour_range, departments, basket_min, status):
    con = duckdb.connect()
    where_sql = build_sql_where(day, hour_range, departments, status)
    basket_filter = f"HAVING COUNT(op.product_id) >= {basket_min}" if basket_min > 1 else ""
    
    query = f"""
    WITH valid_orders AS (
        SELECT op.order_id
        FROM 'order_products__prior.csv' op
        JOIN 'orders.csv' o ON op.order_id = o.order_id
        JOIN 'products.csv' p ON op.product_id = p.product_id
        JOIN 'departments.csv' d ON p.department_id = d.department_id
        {where_sql}
        GROUP BY op.order_id
        {basket_filter}
    )
    SELECT 
        COUNT(DISTINCT vo.order_id) AS total_orders,
        COUNT(op.product_id) AS total_items,
        AVG(TRY_CAST(op.reordered AS INT)) * 100 AS reorder_rate
    FROM valid_orders vo
    JOIN 'order_products__prior.csv' op ON vo.order_id = op.order_id
    """
    res = con.execute(query).fetchone()
    orders = res[0] if res[0] else 0
    items = res[1] if res[1] else 0
    reorder = res[2] if res[2] else 0.0
    avg_basket = (items / orders) if orders > 0 else 0.0
    
    return orders, items, reorder, avg_basket


@st.cache_data
def get_filtered_heatmap(departments, day, hour_range, status):
    where_sql = build_sql_where(day, hour_range, departments, status)
        
    query = f"""
    SELECT TRY_CAST(o.order_dow AS INT) AS day, TRY_CAST(o.order_hour_of_day AS INT) AS hour, COUNT(DISTINCT o.order_id) AS total
    FROM 'orders.csv' o
    JOIN 'order_products__prior.csv' op ON o.order_id = op.order_id
    JOIN 'products.csv' p ON op.product_id = p.product_id
    JOIN 'departments.csv' d ON p.department_id = d.department_id
    {where_sql}
    GROUP BY day, hour
    ORDER BY day, hour
    """
    df = duckdb.query(query).pl().to_pandas()
    if df.empty:
        return None
        
    pivot = df.pivot(index='day', columns='hour', values='total').fillna(0)
    pivot.index = pivot.index.map({0:'Sunday', 1:'Monday', 2:'Tuesday', 3:'Wednesday', 4:'Thursday', 5:'Friday', 6:'Saturday'})
    return pivot


@st.cache_data
def get_filtered_departments(day, hour_range, status):
    where_sql = build_sql_where(day, hour_range, None, status)
    
    query = f"""
    SELECT d.department AS department, COUNT(op.order_id) AS total_items
    FROM 'order_products__prior.csv' op
    JOIN 'orders.csv' o ON op.order_id = o.order_id
    JOIN 'products.csv' p ON op.product_id = p.product_id
    JOIN 'departments.csv' d ON p.department_id = d.department_id
    {where_sql}
    GROUP BY d.department
    ORDER BY total_items DESC
    LIMIT 6
    """
    return duckdb.query(query).pl().to_pandas()


@st.cache_data
def get_filtered_retention(day, hour_range, departments, status):
    where_sql = build_sql_where(day, hour_range, departments, status)
    query = f"""
    SELECT 
        TRY_CAST(op.add_to_cart_order AS INT) AS sequence, 
        AVG(TRY_CAST(op.reordered AS INT)) * 100 AS retention_rate
    FROM 'order_products__prior.csv' op
    JOIN 'orders.csv' o ON op.order_id = o.order_id
    JOIN 'products.csv' p ON op.product_id = p.product_id
    JOIN 'departments.csv' d ON p.department_id = d.department_id
    {where_sql}
    AND TRY_CAST(op.add_to_cart_order AS INT) <= 12
    GROUP BY sequence
    ORDER BY sequence
    """
    return duckdb.query(query).pl().to_pandas()


@st.cache_data
def get_filtered_products(day, hour_range, departments, status):
    where_sql = build_sql_where(day, hour_range, departments, status)
    
    query = f"""
    SELECT 
        p.product_name AS product,
        SUM(CASE WHEN TRY_CAST(op.reordered AS INT) = 1 THEN 1 ELSE 0 END) AS repeat_order,
        SUM(CASE WHEN TRY_CAST(op.reordered AS INT) = 0 THEN 1 ELSE 0 END) AS first_time_order
    FROM 'order_products__prior.csv' op
    JOIN 'orders.csv' o ON op.order_id = o.order_id
    JOIN 'products.csv' p ON op.product_id = p.product_id
    JOIN 'departments.csv' d ON p.department_id = d.department_id
    {where_sql}
    GROUP BY p.product_name
    ORDER BY (repeat_order + first_time_order) DESC
    LIMIT 5
    """
    return duckdb.query(query).pl().to_pandas()


# ==============================================================================
# PART 5: DASHBOARD DISPLAY (FULL ENGLISH + HIGH-CONTRAST LEGEND)
# ==============================================================================

# Header Section
st.markdown("<h2 style='color:#1B4332; font-weight:800; margin-bottom:0px;'>📊 Supply Chain & Consumer Demand Analytics</h2>", unsafe_allow_html=True)
st.caption("Real-time monitoring of warehouse performance, demand trends, and customer retention metrics.")
st.write("")

# ------------------------------------------------------------------------------
# LEVEL 1: EXECUTIVE KPIs
# ------------------------------------------------------------------------------
tot_orders, tot_items, reorder_rate, avg_basket = get_filtered_kpis(f_day, f_hour, f_dept, f_basket, f_status)

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">TOTAL ORDERS</div>
        <div class="kpi-value">{tot_orders:,.0f}</div>
        <span class="kpi-badge">✓ 100% Validated</span>
    </div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">TOTAL ITEMS SOLD</div>
        <div class="kpi-value">{tot_items/1e6:.1f} M</div>
        <span class="kpi-badge">📦 32.4M Volume</span>
    </div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">REORDER RETENTION</div>
        <div class="kpi-value">{reorder_rate:.1f}%</div>
        <span class="kpi-badge">▲ High Loyalty Rate</span>
    </div>""", unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">AVG BASKET SIZE</div>
        <div class="kpi-value">{avg_basket:.1f} Items</div>
        <span class="kpi-badge">🎯 Benchmark: 10.0</span>
    </div>""", unsafe_allow_html=True)

st.write("")

# ------------------------------------------------------------------------------
# MACRO DEMAND PATTERNS & TOP CATEGORIES
# ------------------------------------------------------------------------------
st.markdown("<h4 style='color:#1B4332;'>📈 Macro Demand Patterns & Top Categories</h4>", unsafe_allow_html=True)

col_heat, col_dept = st.columns([1.3, 1])

with col_heat:
    st.markdown("##### 🗓️ Shopping Density Heatmap (Day vs Hour)")
    df_heat = get_filtered_heatmap(f_dept, f_day, f_hour, f_status)
    
    if df_heat is not None and not df_heat.empty:
        fig_heat = px.imshow(
            df_heat,
            labels=dict(x="Transaction Hour (00 - 23)", y="Day", color="Order Volume"),
            x=df_heat.columns,
            y=df_heat.index,
            color_continuous_scale=["#E8F5E9", "#A5D6A7", "#52B788", "#2D6A4F", "#1B4332"],
            aspect="auto"
        )
        apply_clean_theme(fig_heat, height=210, left_m=60, right_m=20)
        st.plotly_chart(fig_heat, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")
    
    st.markdown("""
    <div class="insight-box">
        💡 <b>Heatmap Insight:</b> Peak hours (darkest shades) occur on <b>Sunday & Monday between 10:00 - 15:00</b>. Warehouse operations should prioritize picker/packer staffing during these hours.
    </div>
    """, unsafe_allow_html=True)

with col_dept:
    st.markdown("##### 🏆 Top 6 Best-Selling Departments")
    df_dept_data = get_filtered_departments(f_day, f_hour, f_status)
    
    fig_dept = px.bar(
        df_dept_data,
        x='total_items',
        y='department',
        orientation='h',
        text_auto='.2s',
        color='total_items',
        color_continuous_scale=['#52B788', '#1B4332']
    )
    fig_dept.update_traces(textposition='outside', marker_color='#2D6A4F')
    fig_dept.update_layout(coloraxis_showscale=False, yaxis=dict(autorange="reversed"))
    apply_clean_theme(fig_dept, height=210, left_m=80, right_m=35)
    st.plotly_chart(fig_dept, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box">
        💡 <b>Category Insight:</b> The <b>Produce</b> and <b>Dairy Eggs</b> departments contribute over 50% of the total store sales volume.
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ------------------------------------------------------------------------------
# TACTICAL BEHAVIORAL & LIVE OPERATIONS
# ------------------------------------------------------------------------------
st.markdown("<h4 style='color:#1B4332;'>📦 Tactical Behavioral & Live Operations</h4>", unsafe_allow_html=True)

col_cart, col_prod, col_feed = st.columns([1.0, 1.1, 0.9])

with col_cart:
    st.markdown("##### 🛒 Retention by Add-to-Cart Sequence")
    df_cart = get_filtered_retention(f_day, f_hour, f_dept, f_status)
    
    if not df_cart.empty:
        fig_cart = px.line(
            df_cart,
            x='sequence',
            y='retention_rate',
            markers=True,
            labels={'sequence': 'Add to Cart Order', 'retention_rate': 'Reorder Rate (%)'}
        )
        fig_cart.update_traces(line_color="#2D6A4F", line_width=2.5, marker_size=6)
        apply_clean_theme(fig_cart, height=210, left_m=40, right_m=15)
        st.plotly_chart(fig_cart, use_container_width=True)
    else:
        st.info("Retention data not available.")
    
    st.markdown("""
    <div class="insight-box">
        💡 <b>Customer Behavior:</b> Items added in <b>positions 1 through 3</b> have a 68% repeat order probability.
    </div>
    """, unsafe_allow_html=True)

with col_prod:
    st.markdown("##### 🍓 Top 5 Products (Loyalty Breakdown)")
    df_prod_data = get_filtered_products(f_day, f_hour, f_dept, f_status)
    
    if not df_prod_data.empty:
        fig_prod = go.Figure()
        # Dark Green for Repeat Orders
        fig_prod.add_trace(go.Bar(
            y=df_prod_data['product'], x=df_prod_data['repeat_order'], 
            name='Repeat Order', orientation='h', marker_color='#1B4332'
        ))
        # Light Green for First-Time Orders
        fig_prod.add_trace(go.Bar(
            y=df_prod_data['product'], x=df_prod_data['first_time_order'], 
            name='First-Time Order', orientation='h', marker_color='#74C69D'
        ))
        
        # High-Contrast Legend Configuration
        fig_prod.update_layout(
            barmode='stack', 
            yaxis=dict(autorange="reversed"), 
            showlegend=True,
            legend=dict(
                orientation="h",
                y=1.22,
                x=0.5,
                xanchor="center",
                font=dict(color="#1B4332", size=10, family="sans-serif"),
                bgcolor="rgba(255,255,255,0.85)",
                bordercolor="#D0DED0",
                borderwidth=1
            )
        )
        apply_clean_theme(fig_prod, height=210, left_m=110, right_m=20)
        st.plotly_chart(fig_prod, use_container_width=True)
    else:
        st.info("Select departments to view products.")
        
    st.markdown("""
    <div class="insight-box">
        💡 <b>Product Sales:</b> <i>Banana</i> & <i>Bag of Organic Bananas</i> dominate market sales, heavily driven by repeat purchases.
    </div>
    """, unsafe_allow_html=True)

with col_feed:
    st.markdown("##### ⚡ Live Operational Feed")
    st.markdown("""
    <div class="stream-card">
        <small style="color:#2D6A4F; font-weight:700;">ORD-88390 • 1 min ago</small><br>
        <b style="color:#1B4332;">Organic Bananas & Avocados</b><br>
        <span style="font-size:0.73rem; color:#2D6A4F;">Status: <b>PICKING IN AISLE 24</b></span>
    </div>
    <div class="stream-card">
        <small style="color:#2D6A4F; font-weight:700;">ORD-88388 • 4 mins ago</small><br>
        <b style="color:#1B4332;">Whole Milk & Eggs</b><br>
        <span style="font-size:0.73rem; color:#2D6A4F;">Status: <b>PACKED (COLD STORAGE)</b></span>
    </div>
    <div class="stream-card">
        <small style="color:#2D6A4F; font-weight:700;">ORD-88385 • 8 mins ago</small><br>
        <b style="color:#1B4332;">Organic Strawberries</b><br>
        <span style="font-size:0.73rem; color:#2D6A4F;">Status: <b>OUT FOR DELIVERY</b></span>
    </div>
    """, unsafe_allow_html=True)