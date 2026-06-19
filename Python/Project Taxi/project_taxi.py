"""
NYC TAXI TRIP ANALYTICS DASHBOARD
Premium Dark Mode · Streamlit + Plotly
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(
    page_title="NYC Taxi Analytics",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# KONFIGURASI
# ─────────────────────────────────────────────────────────────────────────────
CSV_PATH = r"__lokasi folder__/data.xlsx"

LAT_MIN, LAT_MAX =  40.50,  40.90
LON_MIN, LON_MAX = -74.20, -73.70

TAXI_YELLOW = "#FFCC00"
TAXI_DARK   = "#1A1A1E"
CARD_BG     = "#26262C"
TEXT_MUTED  = "#9A9AAF"
GRID_COLOR  = "rgba(255,255,255,0.06)"

MONTH_ORDER = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December",
]

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow:wght@300;400;500;600;700;800&family=Barlow+Condensed:wght@500;700;800&display=swap');
:root {
    --yellow:#FFCC00; --dark:#1A1A1E; --surface:#26262C;
    --border:rgba(255,204,0,0.12); --text:#F0EDE6; --muted:#9A9AAF;
    --font:'Barlow',sans-serif; --font-cond:'Barlow Condensed',sans-serif;
}
html,body,[class*="css"]{font-family:var(--font)!important;color:var(--text)!important;background-color:var(--dark)!important;}
.stApp{background:var(--dark)!important;background-image:radial-gradient(ellipse 70% 50% at 90% 0%,rgba(255,204,0,0.05) 0%,transparent 60%),radial-gradient(ellipse 50% 40% at 10% 100%,rgba(255,204,0,0.03) 0%,transparent 55%);background-attachment:fixed;}
[data-testid="stSidebar"]{background:#111114!important;border-right:1px solid var(--border)!important;}
[data-testid="stSidebarContent"]{padding:1.5rem 1.2rem!important;}
.main .block-container{padding:1.5rem 2rem 3rem!important;max-width:1600px!important;}
.stSelectbox>div>div{background:var(--surface)!important;border:1px solid var(--border)!important;border-radius:8px!important;color:var(--text)!important;}
.stSelectbox>div>div:hover{border-color:var(--yellow)!important;}
.stMultiSelect>div>div{background:var(--surface)!important;border:1px solid var(--border)!important;border-radius:8px!important;}
.kpi-card{background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:1.4rem 1.6rem;position:relative;overflow:hidden;height:100%;}
.kpi-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,var(--yellow),transparent);}
.kpi-icon{font-size:1.3rem;margin-bottom:0.5rem;display:block;}
.kpi-label{font-family:var(--font);font-size:0.7rem;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;color:var(--muted);margin-bottom:0.4rem;}
.kpi-value{font-family:var(--font-cond);font-size:2.3rem;font-weight:800;color:var(--yellow);line-height:1;letter-spacing:-0.02em;}
.kpi-sub{font-size:0.76rem;color:var(--muted);margin-top:0.35rem;}
.section-heading{font-family:var(--font-cond);font-size:0.66rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:var(--yellow);display:flex;align-items:center;gap:8px;margin-bottom:0.25rem;}
.section-heading::before{content:'';display:inline-block;width:16px;height:2px;background:var(--yellow);border-radius:2px;}
.section-title{font-family:var(--font-cond);font-size:1.25rem;font-weight:700;color:#F0EDE6;margin:0 0 1rem;letter-spacing:-0.01em;}
.chart-card{background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:0.6rem 1.3rem 0.5rem;}
[data-testid="stSidebar"] label{color:var(--muted)!important;font-size:0.72rem!important;font-weight:600!important;letter-spacing:0.1em!important;text-transform:uppercase!important;}
#MainMenu,footer,header{visibility:hidden!important;}
hr{border-color:var(--border)!important;}
::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:var(--dark);}
::-webkit-scrollbar-thumb{background:rgba(255,204,0,0.25);border-radius:3px;}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# HELPER: Plotly base layout
# Subtitle diletakkan sebagai title chart Plotly (muncul di dalam chart card)
# ─────────────────────────────────────────────────────────────────────────────
def dark_layout(**kwargs):
    base = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor ="rgba(0,0,0,0)",
        font=dict(family="Barlow, sans-serif", color="#9A9AAF", size=11),
        margin=dict(l=10, r=10, t=36, b=10),
        xaxis=dict(gridcolor=GRID_COLOR,
                   linecolor="rgba(255,255,255,0.08)",
                   tickcolor="rgba(255,255,255,0.12)"),
        yaxis=dict(gridcolor=GRID_COLOR,
                   linecolor="rgba(255,255,255,0.08)",
                   tickcolor="rgba(255,255,255,0.12)"),
        hoverlabel=dict(bgcolor="#2E2E36", bordercolor=TAXI_YELLOW,
                        font=dict(family="Barlow, sans-serif", color="#F0EDE6")),
        legend=dict(bgcolor="rgba(38,38,44,0.85)",
                    bordercolor="rgba(255,204,0,0.15)", borderwidth=1,
                    font=dict(size=10)),
    )
    base.update(kwargs)
    return base

def chart_title(text):
    """Subtitle teks yang tampil di dalam area chart (di atas chart Plotly)."""
    return dict(
        text=text,
        font=dict(family="Barlow, sans-serif", size=10,
                  color="#9A9AAF", weight=600),
        x=0, xanchor="left",
        pad=dict(l=6, t=4),
    )


# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, sep=";", low_memory=False)

    def fix_coord(series: pd.Series) -> pd.Series:
        def _fix(val):
            s = str(val).strip()
            first_dot = s.find(".")
            if first_dot == -1:
                try:    return float(s)
                except: return np.nan
            integer = s[:first_dot]
            decimal = s[first_dot + 1:].replace(".", "")
            try:    return float(f"{integer}.{decimal}")
            except: return np.nan
        return series.apply(_fix)

    for col in ["pickup_latitude","pickup_longitude",
                "dropoff_latitude","dropoff_longitude"]:
        if col in df.columns:
            df[col] = fix_coord(df[col])

    mask = (df["pickup_latitude"].between(LAT_MIN, LAT_MAX) &
            df["pickup_longitude"].between(LON_MIN, LON_MAX))
    df = df[mask].copy()

    df["pickup_datetime"]  = pd.to_datetime(df["pickup_datetime"],
                                             format="%d/%m/%Y %H:%M", errors="coerce")
    df["dropoff_datetime"] = pd.to_datetime(df["dropoff_datetime"],
                                             format="%d/%m/%Y %H:%M", errors="coerce")
    df["month_num"]        = df["pickup_datetime"].dt.month
    df["Month Name"]       = df["pickup_datetime"].dt.strftime("%B")
    df["hour"]             = df["pickup_datetime"].dt.hour
    df["day_of_week"]      = df["pickup_datetime"].dt.strftime("%a")
    df["week_num"]         = df["pickup_datetime"].dt.isocalendar().week.astype(int)
    df["trip_duration_min"] = df["trip_duration"] / 60.0

    if "fare_amount" not in df.columns and "total_amount" not in df.columns:
        df["fare_amount"] = 3.0 + (df["trip_duration"] * 0.04)

    revenue_col  = ("total_amount" if "total_amount" in df.columns else "fare_amount")
    df["revenue"] = df[revenue_col]
    df = df[df["trip_duration"].between(60, 10800)].copy()
    df = df[df["passenger_count"].between(1, 6)].copy()
    return df.reset_index(drop=True)


with st.spinner("🚕  Memuat dataset NYC Taxi..."):
    df_full = load_data(CSV_PATH)


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="margin-bottom:2rem;padding-bottom:1.5rem;border-bottom:1px solid rgba(255,204,0,0.12);">
        <div style="font-family:'Barlow Condensed',sans-serif;font-size:1.6rem;font-weight:800;color:#FFCC00;letter-spacing:-0.01em;line-height:1;">🚕 NYC TAXI</div>
        <div style="font-family:'Barlow',sans-serif;font-size:0.68rem;font-weight:600;color:#9A9AAF;letter-spacing:0.15em;text-transform:uppercase;margin-top:0.2rem;">Trip Analytics · 2016</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div style="font-family:'Barlow',sans-serif;font-size:0.65rem;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:#FFCC00;margin-bottom:0.6rem;">▸ TIME FILTER</div>""", unsafe_allow_html=True)
    available_months = [m for m in MONTH_ORDER if m in df_full["Month Name"].unique()]
    selected_month   = st.selectbox("Select Month", ["All Months"] + available_months, index=0)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div style="font-family:'Barlow',sans-serif;font-size:0.65rem;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:#FFCC00;margin-bottom:0.6rem;">▸ PASSENGER</div>""", unsafe_allow_html=True)
    pax_options  = sorted(df_full["passenger_count"].unique().tolist())
    selected_pax = st.multiselect("Passenger Count", options=pax_options, default=pax_options)

    st.markdown(f"""
    <div style="margin-top:2.5rem;padding-top:1.2rem;border-top:1px solid rgba(255,204,0,0.1);">
        <div style="font-family:'Barlow',sans-serif;font-size:0.64rem;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;color:#9A9AAF;margin-bottom:0.7rem;">Dataset Info</div>
        <div style="font-family:'Barlow',sans-serif;font-size:0.78rem;color:#9A9AAF;line-height:2;">
        📅 Year: <span style="color:#F0EDE6;font-weight:600;">2016</span><br>
        🗃 Records: <span style="color:#FFCC00;font-weight:700;">{len(df_full):,}</span><br>
        🏙 City: <span style="color:#F0EDE6;font-weight:600;">New York City</span>
        </div>
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────────────────────────────────────
df = df_full.copy()
if selected_month != "All Months":
    df = df[df["Month Name"] == selected_month]
if selected_pax:
    df = df[df["passenger_count"].isin(selected_pax)]
if len(df) == 0:
    st.warning("⚠️ Tidak ada data untuk kombinasi filter tersebut.")
    st.stop()


# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
period_label = selected_month if selected_month != "All Months" else "Full Year 2016"
st.markdown(f"""
<div style="margin-bottom:0.5rem;">
    <div style="font-family:'Barlow Condensed',sans-serif;font-size:2.1rem;font-weight:800;color:#F0EDE6;letter-spacing:-0.02em;line-height:1.1;">NYC TAXI TRIP ANALYTICS</div>
    <div style="font-family:'Barlow',sans-serif;font-size:0.82rem;color:#9A9AAF;margin-top:0.3rem;">
    Period: <span style="color:#FFCC00;font-weight:600;">{period_label}</span>
    &nbsp;·&nbsp;<span style="color:#F0EDE6;font-weight:600;">{len(df):,}</span> trips in view
    </div>
</div>
<div style="border-top:1px solid rgba(255,204,0,0.12);margin:0.8rem 0 1.5rem;"></div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# ROW 1 — KPI CARDS
# ─────────────────────────────────────────────────────────────────────────────
total_trips   = len(df)
total_revenue = df["revenue"].sum()
avg_dur_min   = df["trip_duration_min"].mean()
avg_dur_sec   = int((avg_dur_min % 1) * 60)
avg_dur_min_i = int(avg_dur_min)
avg_pax       = df["passenger_count"].mean()

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"""<div class="kpi-card"><span class="kpi-icon">🚖</span>
    <div class="kpi-label">Total Trips</div>
    <div class="kpi-value">{total_trips:,}</div>
    <div class="kpi-sub">Completed journeys</div></div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class="kpi-card"><span class="kpi-icon">💰</span>
    <div class="kpi-label">Total Revenue</div>
    <div class="kpi-value">${total_revenue:,.0f}</div>
    <div class="kpi-sub">Estimated earnings</div></div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class="kpi-card"><span class="kpi-icon">⏱</span>
    <div class="kpi-label">Avg Trip Duration</div>
    <div class="kpi-value">{avg_dur_min_i}m <span style="font-size:1.1rem;color:#9A9AAF;font-weight:500;">{avg_dur_sec:02d}s</span></div>
    <div class="kpi-sub">Per trip average</div></div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""<div class="kpi-card"><span class="kpi-icon">👤</span>
    <div class="kpi-label">Avg Passengers</div>
    <div class="kpi-value">{avg_pax:.2f}</div>
    <div class="kpi-sub">Per trip average</div></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# ROW 2 — HOURLY BAR + MONTHLY BAR
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""<div class="section-heading">TEMPORAL ANALYSIS</div>
<div class="section-title">Hourly Volume · Monthly Trend</div>""", unsafe_allow_html=True)

t1, t2 = st.columns([1.6, 1])

with t1:
    hourly = df.groupby("hour").size().reset_index(name="trips")
    fig_hr = go.Figure(go.Bar(
        x=hourly["hour"], y=hourly["trips"],
        marker=dict(color=hourly["trips"],
                    colorscale=[[0,"#2A2A32"],[0.5,"#8A6800"],[1,TAXI_YELLOW]],
                    line=dict(width=0)),
        hovertemplate="<b>%{x}:00h</b><br>%{y:,} trips<extra></extra>",
    ))
    fig_hr.update_layout(
        **dark_layout(height=280, bargap=0.12),
        title=chart_title("Trips by Hour of Day"),
    )
    fig_hr.update_xaxes(tickmode="array", tickvals=list(range(0,24,2)),
                        ticktext=[f"{h:02d}:00" for h in range(0,24,2)])
    fig_hr.update_yaxes(tickformat=",")

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_hr, use_container_width=True, config={"displayModeBar":False})
    st.markdown("</div>", unsafe_allow_html=True)

with t2:
    monthly = (df.groupby(["month_num","Month Name"]).size()
                 .reset_index(name="trips").sort_values("month_num"))
    fig_mo = go.Figure(go.Bar(
        x=monthly["Month Name"].str[:3], y=monthly["trips"],
        marker=dict(color=monthly["trips"],
                    colorscale=[[0,"#2A2A32"],[1,TAXI_YELLOW]],
                    line=dict(width=0)),
        hovertemplate="<b>%{x}</b><br>%{y:,} trips<extra></extra>",
    ))
    fig_mo.update_layout(
        **dark_layout(height=280, bargap=0.2),
        title=chart_title("Trips by Month"),
    )
    fig_mo.update_yaxes(tickformat=",")

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_mo, use_container_width=True, config={"displayModeBar":False})
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# ROW 3 — TREEMAP + MAP
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""<div class="section-heading">PASSENGER & GEOSPATIAL ANALYSIS</div>
<div class="section-title">Passenger Distribution · Pickup Density Map</div>""", unsafe_allow_html=True)

left_col, right_col = st.columns([1, 1.5])

with left_col:
    pax_df = (df.groupby("passenger_count").size()
                .reset_index(name="trips")
                .sort_values("trips", ascending=False)
                .reset_index(drop=True))
    pax_df["pct"]   = (pax_df["trips"] / pax_df["trips"].sum() * 100).round(1)
    pax_df["label"] = pax_df["passenger_count"].apply(lambda x: f"{'👤'*int(x)}  {x} Pax")

    n = len(pax_df)
    color_seq = [TAXI_YELLOW,"#DEDEDE","#5A5A68","#4A4A58","#3A3A48","#2E2E3A"]
    colors = [color_seq[min(i, len(color_seq)-1)] for i in range(n)]

    fig_tree = go.Figure(go.Treemap(
        labels=pax_df["label"].tolist(), parents=[""]*n,
        values=pax_df["trips"].tolist(),
        customdata=pax_df[["trips","pct"]].values,
        texttemplate=(
            "<b>%{label}</b><br>"
            "<span style='font-size:1.05em;font-weight:700;'>%{customdata[1]:.1f}%</span><br>"
            "%{customdata[0]:,.0f} trips"
        ),
        hovertemplate="<b>%{label}</b><br>%{customdata[0]:,} trips · %{customdata[1]:.1f}%<extra></extra>",
        marker=dict(colors=colors, line=dict(width=2.5, color="#1A1A1E"),
                    pad=dict(t=18, b=4, l=4, r=4)),
        textfont=dict(family="Barlow, sans-serif", size=12),
    ))
    fig_tree.update_layout(
        **dark_layout(height=480, margin=dict(l=0, r=0, t=36, b=0)),
        title=chart_title("Passenger Count Distribution"),
    )

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_tree, use_container_width=True, config={"displayModeBar":False})
    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    MAP_SAMPLE = 50_000
    df_map = df.sample(MAP_SAMPLE, random_state=42) if len(df) > MAP_SAMPLE else df.copy()

    pickup_subtitle = (
        f"Pickup Locations — {len(df_map):,} sampled points"
        + (f"  ·  of {len(df):,} filtered trips" if len(df) > MAP_SAMPLE else "")
    )

    fig_map = px.scatter_mapbox(
        df_map, lat="pickup_latitude", lon="pickup_longitude",
        color_discrete_sequence=[TAXI_YELLOW],
        zoom=10.5, center={"lat":40.7128, "lon":-74.006},
        mapbox_style="carto-darkmatter",
    )
    fig_map.update_traces(marker=dict(size=3, opacity=0.4),
                          hovertemplate="Lat: %{lat:.4f}<br>Lon: %{lon:.4f}<extra></extra>")
    fig_map.update_layout(
        **dark_layout(height=480, margin=dict(l=0, r=0, t=36, b=0)),
        title=chart_title(pickup_subtitle),
    )

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_map, use_container_width=True,
                    config={"displayModeBar":True,
                            "modeBarButtonsToRemove":["select2d","lasso2d"]})
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# ROW 4 — DURATION HISTOGRAM + HEATMAP
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""<div class="section-heading">TRIP PATTERNS</div>
<div class="section-title">Duration Distribution · Day × Hour Heatmap</div>""", unsafe_allow_html=True)

r4a, r4b = st.columns([1, 1.4])

with r4a:
    df_dur  = df[df["trip_duration_min"] <= 60]["trip_duration_min"]
    avg_dur = df_dur.mean()

    fig_hist = go.Figure(go.Histogram(
        x=df_dur, nbinsx=40,
        marker=dict(color=TAXI_YELLOW, opacity=0.8, line=dict(width=0)),
        hovertemplate="%{y:,} trips<extra></extra>",
    ))
    fig_hist.add_vline(
        x=avg_dur, line_color="#FFFFFF", line_dash="dash", line_width=1.5,
        annotation=dict(text=f"Avg  {avg_dur:.1f} min",
                        font=dict(color="#FFFFFF", size=10, family="Barlow, sans-serif"),
                        bgcolor="rgba(38,38,44,0.9)", bordercolor=TAXI_YELLOW,
                        borderwidth=1, yref="paper", y=0.96),
    )
    fig_hist.update_layout(
        **dark_layout(height=320, bargap=0.06),
        title=chart_title("Trip Duration (≤ 60 min)"),
    )
    fig_hist.update_xaxes(title="Minutes")
    fig_hist.update_yaxes(title="Trips", tickformat=",")

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_hist, use_container_width=True, config={"displayModeBar":False})
    st.markdown("</div>", unsafe_allow_html=True)

with r4b:
    day_order  = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    heat_data  = df.groupby(["day_of_week","hour"]).size().reset_index(name="trips")
    heat_pivot = (heat_data.pivot(index="day_of_week", columns="hour", values="trips")
                            .reindex(day_order).fillna(0))

    fig_heat = go.Figure(go.Heatmap(
        z=heat_pivot.values,
        x=[f"{h:02d}:00" for h in heat_pivot.columns],
        y=heat_pivot.index.tolist(),
        colorscale=[[0,"#1A1A1E"],[0.25,"#3A2E00"],[0.6,"#8A6800"],
                    [0.85,"#D4A800"],[1,TAXI_YELLOW]],
        hovertemplate="<b>%{y} %{x}</b><br>%{z:,} trips<extra></extra>",
        showscale=True,
        colorbar=dict(thickness=10, len=0.85,
                      tickfont=dict(color="#9A9AAF",size=9), outlinewidth=0),
    ))
    fig_heat.update_layout(
        **dark_layout(height=320, margin=dict(l=10, r=55, t=36, b=10)),
        title=chart_title("Trip Intensity · Day × Hour"),
    )
    fig_heat.update_xaxes(tickangle=-45, tickfont=dict(size=9), gridcolor="rgba(0,0,0,0)")
    fig_heat.update_yaxes(gridcolor="rgba(0,0,0,0)")

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_heat, use_container_width=True, config={"displayModeBar":False})
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# ROW 5 — VENDOR PIE + LINE CHART
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""<div class="section-heading">VENDOR & EFFICIENCY</div>
<div class="section-title">Vendor Share · Avg Duration by Hour</div>""", unsafe_allow_html=True)

v_col, d_col = st.columns([1, 2])

with v_col:
    vd = df.groupby("vendor_id").size().reset_index(name="trips")
    vd["vendor"] = vd["vendor_id"].map({1:"Vendor 1", 2:"Vendor 2"})

    fig_pie = go.Figure(go.Pie(
        labels=vd["vendor"], values=vd["trips"], hole=0.6,
        marker=dict(colors=[TAXI_YELLOW,"#4A4A58"],
                    line=dict(color="#1A1A1E",width=3)),
        textfont=dict(family="Barlow, sans-serif",size=11,color="#F0EDE6"),
        hovertemplate="<b>%{label}</b><br>%{value:,} trips · %{percent}<extra></extra>",
    ))
    fig_pie.update_layout(
        **dark_layout(height=300, margin=dict(l=10,r=10,t=36,b=10)),
        title=chart_title("Vendor Market Share"),
        showlegend=True,
        annotations=[dict(text=f"{vd['trips'].sum():,}<br>trips",
                          x=0.5, y=0.5, showarrow=False,
                          font=dict(size=13, color=TAXI_YELLOW,
                                    family="Barlow Condensed, sans-serif"))],
    )
    fig_pie.update_layout(legend=dict(orientation="v", x=1.0, y=0.5, font=dict(size=11)))

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar":False})
    st.markdown("</div>", unsafe_allow_html=True)

with d_col:
    dur_hour = (df.groupby(["hour","vendor_id"])["trip_duration_min"]
                  .mean().reset_index())
    v_colors = {1: TAXI_YELLOW, 2: "#8A8A9A"}

    fig_line = go.Figure()
    for vid in sorted(df["vendor_id"].unique()):
        sub = dur_hour[dur_hour["vendor_id"] == vid]
        fig_line.add_trace(go.Scatter(
            x=sub["hour"], y=sub["trip_duration_min"],
            name=f"Vendor {vid}", mode="lines+markers",
            line=dict(color=v_colors.get(vid,"#888"), width=2.5),
            marker=dict(size=5, color=v_colors.get(vid,"#888"),
                        line=dict(width=1.5, color="#1A1A1E")),
            hovertemplate="<b>%{x}:00h</b><br>Avg %{y:.1f} min<extra></extra>",
        ))
    fig_line.update_layout(
        **dark_layout(height=300),
        title=chart_title("Avg Trip Duration by Hour · Per Vendor"),
    )
    fig_line.update_xaxes(tickmode="array", tickvals=list(range(0,24,2)),
                          ticktext=[f"{h:02d}:00" for h in range(0,24,2)],
                          title="Hour of Day")
    fig_line.update_yaxes(title="Avg Duration (min)")

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_line, use_container_width=True, config={"displayModeBar":False})
    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="border-top:1px solid rgba(255,204,0,0.1);margin-top:1.5rem;padding:1rem 0 0.5rem;text-align:center;">
    <span style="font-family:'Barlow',sans-serif;font-size:0.7rem;color:#4A4A58;letter-spacing:0.06em;">
    NYC TAXI TRIP ANALYTICS DASHBOARD &nbsp;·&nbsp;
    Data Analyst Portfolio Project &nbsp;·&nbsp;
    Built with Streamlit & Plotly
    </span>
</div>
""", unsafe_allow_html=True)
