# =============================================================================
#  RETAIL CRISIS & RECOVERY — End-to-End Data Pipeline
#  Hackathon Theme: "Retail Crisis & Recovery"
#  Author  : Daffa Farros Azhari
#  Dataset : data_penjualan.xlsx
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.ticker import FuncFormatter
import warnings
import os
warnings.filterwarnings("ignore")

# ── PATH OTOMATIS: script akan cari file di folder yang sama dengan script ini
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
FILE_EXCEL = os.path.join(BASE_DIR, "data_penjualan.xlsx")
FILE_OUT   = os.path.join(BASE_DIR, "retail_crisis_recovery_dashboard.png")

# ── 0. GLOBAL STYLE ────────────────────────────────────────────────────────
DARK_BG      = "#0D0D0D"
PANEL_BG     = "#1A1A1A"
GOLD         = "#FFD700"
GOLD_LIGHT   = "#FFF176"
CRISIS_RED   = "#FF4C4C"
RECOVERY_GRN = "#00E676"
ACCENT_BLUE  = "#40C4FF"
TEXT_WHITE   = "#F5F5F5"
GRID_COLOR   = "#2A2A2A"

plt.rcParams.update({
    "figure.facecolor"  : DARK_BG,
    "axes.facecolor"    : PANEL_BG,
    "axes.edgecolor"    : "#333333",
    "axes.labelcolor"   : TEXT_WHITE,
    "axes.titlecolor"   : TEXT_WHITE,
    "xtick.color"       : TEXT_WHITE,
    "ytick.color"       : TEXT_WHITE,
    "text.color"        : TEXT_WHITE,
    "grid.color"        : GRID_COLOR,
    "grid.linewidth"    : 0.6,
    "font.family"       : "DejaVu Sans",
    "legend.facecolor"  : PANEL_BG,
    "legend.edgecolor"  : "#444444",
})

def fmt_idr(x, pos=None):
    """Format angka ke IDR Juta / Miliar."""
    if abs(x) >= 1e9:
        return f"Rp {x/1e9:.1f}M"
    return f"Rp {x/1e6:.0f}Jt"


# =============================================================================
# 1. DATA CLEANING & PREPARATION
# =============================================================================
print("=" * 60)
print("  RETAIL CRISIS & RECOVERY — DATA PIPELINE")
print("=" * 60)

df = pd.read_excel(FILE_EXCEL)

# Pastikan tipe data benar
df["tgl_transaksi"] = pd.to_datetime(df["tgl_transaksi"])
df["total_nilai"]   = pd.to_numeric(df["total_nilai"], errors="coerce")
df.dropna(subset=["total_nilai"], inplace=True)
df.sort_values("tgl_transaksi", inplace=True)
df.reset_index(drop=True, inplace=True)

print(f"\n✔  Dataset loaded  : {len(df):,} baris  |  {df['tgl_transaksi'].min().date()} → {df['tgl_transaksi'].max().date()}")
print(f"   Produk unik     : {df['nama_produk'].nunique()}")
print(f"   Null values     : {df.isnull().sum().sum()}")


# =============================================================================
# 2. TIME-SERIES AGGREGATION
# =============================================================================
daily = (df.groupby("tgl_transaksi")["total_nilai"]
           .sum()
           .reset_index()
           .rename(columns={"tgl_transaksi": "tanggal", "total_nilai": "revenue"}))

daily["rolling_7"]  = daily["revenue"].rolling(7, min_periods=1).mean()
daily["rolling_3"]  = daily["revenue"].rolling(3, min_periods=1).mean()

monthly = (df.groupby(df["tgl_transaksi"].dt.to_period("M"))["total_nilai"]
             .sum()
             .reset_index()
             .rename(columns={"tgl_transaksi": "bulan", "total_nilai": "revenue"}))

print(f"\n📅  Daily records   : {len(daily)}")
print(f"📅  Monthly records : {len(monthly)}")


# =============================================================================
# 3. CRISIS & RECOVERY DETECTION
# =============================================================================
# ── 3a. Baseline (median 7 hari pertama sebagai referensi normal)
baseline_revenue = daily.head(7)["revenue"].median()

# ── 3b. Peak — titik tertinggi sebelum krisis
peak_idx  = daily["revenue"].idxmax()
peak_row  = daily.loc[peak_idx]
PEAK_DATE = peak_row["tanggal"]
PEAK_VAL  = peak_row["revenue"]

# ── 3c. Crisis Start — hari pertama rolling_7 turun >10% dari baseline
threshold_crisis = baseline_revenue * 0.90
crisis_start_mask = (daily["rolling_7"] < threshold_crisis) & (daily["tanggal"] > "2025-02-28")
CRISIS_START_IDX  = daily[crisis_start_mask].index[0] if crisis_start_mask.any() else None
CRISIS_START_DATE = daily.loc[CRISIS_START_IDX, "tanggal"] if CRISIS_START_IDX else None

# ── 3d. Lowest Point — trough minimum
trough_idx   = daily["revenue"].idxmin()
trough_row   = daily.loc[trough_idx]
TROUGH_DATE  = trough_row["tanggal"]
TROUGH_VAL   = trough_row["revenue"]

# ── 3e. Recovery Phase — setelah trough, rolling naik kembali >5% dari trough
post_trough  = daily[daily["tanggal"] > TROUGH_DATE].copy()
recovery_threshold = TROUGH_VAL * 1.05
recovery_mask = post_trough["rolling_7"] > recovery_threshold
RECOVERY_DATE = post_trough[recovery_mask]["tanggal"].iloc[0] if recovery_mask.any() else None

# ── 3f. Business Metrics
peak_to_trough_pct = (1 - TROUGH_VAL / PEAK_VAL) * 100
days_from_peak_to_trough = (TROUGH_DATE - PEAK_DATE).days
days_to_recovery = (RECOVERY_DATE - TROUGH_DATE).days if RECOVERY_DATE else None

print("\n" + "─" * 60)
print("  📊  BUSINESS METRICS — CRISIS DETECTION")
print("─" * 60)
print(f"  Peak Revenue   : {fmt_idr(PEAK_VAL)} pada {PEAK_DATE.date()}")
print(f"  Crisis Start   : {CRISIS_START_DATE.date() if CRISIS_START_DATE else 'N/A'}")
print(f"  Lowest Point   : {fmt_idr(TROUGH_VAL)} pada {TROUGH_DATE.date()}")
print(f"  Peak-to-Trough : -{peak_to_trough_pct:.1f}%  (dalam {days_from_peak_to_trough} hari)")
if RECOVERY_DATE:
    print(f"  Recovery Date  : {RECOVERY_DATE.date()}")
    print(f"  Recovery Speed : {days_to_recovery} hari setelah titik terendah")
else:
    print("  Recovery Phase : Belum terdeteksi dalam periode dataset")


# =============================================================================
# 4. DEEP DIVE — PRODUK TERDAMPAK & RECOVERY DRIVERS
# =============================================================================
crisis_dates  = [TROUGH_DATE, TROUGH_DATE + pd.Timedelta(days=1)]
crisis_df     = df[df["tgl_transaksi"].isin(crisis_dates)]
normal_days   = daily[daily["tanggal"] < "2025-03-01"]["tanggal"].unique()
normal_df     = df[df["tgl_transaksi"].isin(normal_days)]

n_normal_days = len(normal_days)
prod_normal   = normal_df.groupby("nama_produk")["total_nilai"].sum() / n_normal_days
prod_crisis   = crisis_df.groupby("nama_produk")["total_nilai"].sum() / len(crisis_dates)

impact_df         = pd.DataFrame({"normal_avg": prod_normal, "crisis_avg": prod_crisis}).fillna(0)
impact_df["drop"] = impact_df["normal_avg"] - impact_df["crisis_avg"]

# TOP 3 paling terdampak
top3_impacted = impact_df.sort_values("drop", ascending=False).head(3)

# TOP 3 recovery drivers (Mar 1-2 vs awal Februari)
early_df    = df[df["tgl_transaksi"] < "2025-02-15"]
late_df     = df[(df["tgl_transaksi"] >= "2025-03-01") & (df["tgl_transaksi"] < "2025-03-03")]
n_early     = early_df["tgl_transaksi"].nunique()
n_late      = late_df["tgl_transaksi"].nunique()
prod_early  = early_df.groupby("nama_produk")["total_nilai"].sum() / n_early
prod_late   = late_df.groupby("nama_produk")["total_nilai"].sum() / n_late

recovery_df            = pd.DataFrame({"early": prod_early, "late": prod_late}).fillna(0)
recovery_df["growth"]  = recovery_df["late"] - recovery_df["early"]
top3_recovery          = recovery_df.sort_values("growth", ascending=False).head(3)

print("\n" + "─" * 60)
print("  📃  TOP 3 PRODUK PALING TERDAMPAK SAAT KRISIS")
print("─" * 60)
for rank, (prod, row) in enumerate(top3_impacted.iterrows(), 1):
    print(f"  {rank}. {prod:<35}  Drop: {fmt_idr(row['drop'])}/hari")

print("\n  📜  TOP 3 PRODUK PENGGERAK RECOVERY")
print("─" * 60)
for rank, (prod, row) in enumerate(top3_recovery.iterrows(), 1):
    print(f"  {rank}. {prod:<35}  Growth: +{fmt_idr(row['growth'])}/hari")


# =============================================================================
# 5. HIGH-IMPACT VISUALIZATION (DARK MODE + GOLD ACCENTS)
# =============================================================================
fig = plt.figure(figsize=(20, 14), facecolor=DARK_BG)
fig.suptitle(
    "RETAIL CRISIS & RECOVERY ANALYSIS  ·  Feb–Mar 2025",
    fontsize=22, fontweight="bold", color=GOLD, y=0.97
)

gs = gridspec.GridSpec(
    2, 3, figure=fig,
    hspace=0.42, wspace=0.35,
    left=0.06, right=0.97, top=0.91, bottom=0.08
)

# ─────────────────────────────────────────────────────────────────────────────
# Panel 1 (Top-Wide): Daily Revenue + Crisis Annotations
# ─────────────────────────────────────────────────────────────────────────────
ax1 = fig.add_subplot(gs[0, :])

# Background shading
if CRISIS_START_DATE and TROUGH_DATE:
    ax1.axvspan(CRISIS_START_DATE, TROUGH_DATE,
                color=CRISIS_RED, alpha=0.12, label="Crisis Zone")
if TROUGH_DATE and RECOVERY_DATE:
    ax1.axvspan(TROUGH_DATE, RECOVERY_DATE,
                color=RECOVERY_GRN, alpha=0.10, label="Recovery Zone")

# Area + line
ax1.fill_between(daily["tanggal"], daily["revenue"],
                 alpha=0.15, color=ACCENT_BLUE)
ax1.plot(daily["tanggal"], daily["revenue"],
         color=ACCENT_BLUE, linewidth=1.6, alpha=0.7, label="Daily Revenue")
ax1.plot(daily["tanggal"], daily["rolling_7"],
         color=GOLD, linewidth=2.5, linestyle="-", label="7-Day Rolling Avg")

# Annotations
def annotate(ax, x, y, label, color, yoffset=6e6, xoffset=None):
    xo = xoffset or x
    ax.annotate(
        label,
        xy=(x, y), xytext=(xo, y + yoffset),
        fontsize=9, fontweight="bold", color=color,
        arrowprops=dict(arrowstyle="->", color=color, lw=1.4),
        bbox=dict(boxstyle="round,pad=0.3", fc=DARK_BG, ec=color, lw=1.2)
    )

# Peak
ax1.scatter([PEAK_DATE], [PEAK_VAL], color=GOLD, s=100, zorder=5)
annotate(ax1, PEAK_DATE, PEAK_VAL, f"PEAK\n{fmt_idr(PEAK_VAL)}", GOLD, yoffset=8e6)

# Crisis Start
if CRISIS_START_DATE:
    cs_rev = daily.loc[daily["tanggal"] == CRISIS_START_DATE, "revenue"].values[0]
    ax1.axvline(CRISIS_START_DATE, color=CRISIS_RED, linewidth=1.5, linestyle="--", alpha=0.8)
    ax1.scatter([CRISIS_START_DATE], [cs_rev], color=CRISIS_RED, s=100, zorder=5)
    annotate(ax1, CRISIS_START_DATE, cs_rev,
             f"CRISIS START\n{CRISIS_START_DATE.strftime('%d %b')}", CRISIS_RED,
             yoffset=10e6, xoffset=CRISIS_START_DATE - pd.Timedelta(days=3))

# Trough
ax1.scatter([TROUGH_DATE], [TROUGH_VAL], color=CRISIS_RED, s=130, zorder=5,
            marker="v", edgecolors="white", linewidth=0.8)
annotate(ax1, TROUGH_DATE, TROUGH_VAL,
         f"LOWEST POINT\n{fmt_idr(TROUGH_VAL)}\n(-{peak_to_trough_pct:.1f}%)",
         CRISIS_RED, yoffset=-20e6)

# Recovery
if RECOVERY_DATE:
    rec_rev = daily.loc[daily["tanggal"] == RECOVERY_DATE, "revenue"].values[0]
    ax1.axvline(RECOVERY_DATE, color=RECOVERY_GRN, linewidth=1.5, linestyle="--", alpha=0.8)
    ax1.scatter([RECOVERY_DATE], [rec_rev], color=RECOVERY_GRN, s=100, zorder=5)
    annotate(ax1, RECOVERY_DATE, rec_rev,
             f"RECOVERY PHASE\n{RECOVERY_DATE.strftime('%d %b')}",
             RECOVERY_GRN, yoffset=10e6)

ax1.yaxis.set_major_formatter(FuncFormatter(fmt_idr))
ax1.set_title("Daily Revenue Timeline — Crisis & Recovery Detection",
              fontsize=13, color=TEXT_WHITE, pad=10)
ax1.set_xlabel("Tanggal", fontsize=10)
ax1.set_ylabel("Revenue", fontsize=10)
import matplotlib.dates as mdates
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%Y"))
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=30, ha="right")
ax1.legend(loc="upper right", fontsize=9)
ax1.grid(True, axis="y", alpha=0.4)

# ─────────────────────────────────────────────────────────────────────────────
# Panel 2 (Bottom-Left): TOP 3 Produk Terdampak
# ─────────────────────────────────────────────────────────────────────────────
ax2 = fig.add_subplot(gs[1, 0])

labels2   = [p[:20] + "…" if len(p) > 20 else p for p in top3_impacted.index]
bars_norm = top3_impacted["normal_avg"].values
bars_cris = top3_impacted["crisis_avg"].values

x2 = np.arange(len(labels2))
w  = 0.35
b1 = ax2.bar(x2 - w/2, bars_norm, w, color=ACCENT_BLUE, alpha=0.85, label="Normal Avg/Day")
b2 = ax2.bar(x2 + w/2, bars_cris, w, color=CRISIS_RED, alpha=0.85, label="Crisis Avg/Day")

ax2.set_xticks(x2)
ax2.set_xticklabels(labels2, fontsize=8.5, rotation=15, ha="right")
ax2.yaxis.set_major_formatter(FuncFormatter(fmt_idr))
ax2.set_title("📃  Top 3 Produk Paling Terdampak", fontsize=11, color=CRISIS_RED, pad=8)
ax2.legend(fontsize=8)
ax2.grid(True, axis="y", alpha=0.3)

for b in b1:
    ax2.text(b.get_x() + b.get_width()/2, b.get_height() + 2e5,
             fmt_idr(b.get_height()), ha="center", fontsize=7.5, color=ACCENT_BLUE)
for b in b2:
    ax2.text(b.get_x() + b.get_width()/2, b.get_height() + 2e5,
             fmt_idr(b.get_height()), ha="center", fontsize=7.5, color=CRISIS_RED)

# ─────────────────────────────────────────────────────────────────────────────
# Panel 3 (Bottom-Mid): TOP 3 Recovery Drivers
# ─────────────────────────────────────────────────────────────────────────────
ax3 = fig.add_subplot(gs[1, 1])

labels3    = [p[:20] + "…" if len(p) > 20 else p for p in top3_recovery.index]
bars_early = top3_recovery["early"].values
bars_late  = top3_recovery["late"].values

x3 = np.arange(len(labels3))
ax3.bar(x3 - w/2, bars_early, w, color="#888888", alpha=0.85, label="Awal Feb Avg/Day")
ax3.bar(x3 + w/2, bars_late,  w, color=RECOVERY_GRN, alpha=0.85, label="Recovery Avg/Day")

ax3.set_xticks(x3)
ax3.set_xticklabels(labels3, fontsize=8.5, rotation=15, ha="right")
ax3.yaxis.set_major_formatter(FuncFormatter(fmt_idr))
ax3.set_title("📜  Top 3 Recovery Drivers", fontsize=11, color=RECOVERY_GRN, pad=8)
ax3.legend(fontsize=8)
ax3.grid(True, axis="y", alpha=0.3)

# ─────────────────────────────────────────────────────────────────────────────
# Panel 4 (Bottom-Right): KPI Scorecard
# ─────────────────────────────────────────────────────────────────────────────
ax4 = fig.add_subplot(gs[1, 2])
ax4.set_xlim(0, 1)
ax4.set_ylim(0, 1)
ax4.axis("off")
ax4.set_facecolor(PANEL_BG)

ax4.text(0.5, 0.97, "📋  KEY BUSINESS METRICS",
         ha="center", va="top", fontsize=12, fontweight="bold", color=GOLD)

kpis = [
    ("Peak Revenue",        f"{fmt_idr(PEAK_VAL)}",         TEXT_WHITE),
    ("Trough Revenue",      f"{fmt_idr(TROUGH_VAL)}",       CRISIS_RED),
    ("Peak-to-Trough Drop", f"-{peak_to_trough_pct:.1f}%",  CRISIS_RED),
    ("Days Peak → Trough",  f"{days_from_peak_to_trough} hari", CRISIS_RED),
    ("Recovery Speed",
     f"{days_to_recovery} hari" if days_to_recovery else "Ongoing",
     RECOVERY_GRN),
    ("Total Revenue Feb",   f"{fmt_idr(monthly.loc[monthly['bulan']==pd.Period('2025-02'), 'revenue'].values[0])}",
     ACCENT_BLUE),
    ("Total Revenue Mar",   f"{fmt_idr(monthly.loc[monthly['bulan']==pd.Period('2025-03'), 'revenue'].values[0])}",
     ACCENT_BLUE),
    ("Produk Unik",         f"{df['nama_produk'].nunique()}",    TEXT_WHITE),
]

y_pos = 0.85
for label, val, color in kpis:
    ax4.text(0.05, y_pos, label,  ha="left",  va="center", fontsize=9,  color="#AAAAAA")
    ax4.text(0.95, y_pos, val,    ha="right", va="center", fontsize=10,
             fontweight="bold", color=color)
    ax4.axhline(y_pos - 0.045, xmin=0.02, xmax=0.98, color="#2A2A2A", linewidth=0.8)
    y_pos -= 0.11

# Watermark / footer
fig.text(0.5, 0.005,
         "Hackathon: Retail Crisis & Recovery  ·  Data: Feb–Mar 2025  ·  Powered by Python + Matplotlib",
         ha="center", fontsize=8, color="#555555")

plt.savefig(FILE_OUT, dpi=160, bbox_inches="tight", facecolor=DARK_BG)
print(f"\n✅  Dashboard saved → {FILE_OUT}")


# =============================================================================
# 6. FINAL BUSINESS SUMMARY REPORT
# =============================================================================
print("\n" + "=" * 60)
print("  EXECUTIVE SUMMARY — SIAP UNTUK PITCHING")
print("=" * 60)
print(f"""
📌 SITUASI
   Bisnis berjalan stabil di Februari 2025 dengan rata-rata
   pendapatan ~{fmt_idr(baseline_revenue)}/hari. Titik tertinggi
   dicapai pada {PEAK_DATE.date()} di angka {fmt_idr(PEAK_VAL)}.

📃 KRISIS
   Mulai {CRISIS_START_DATE.date() if CRISIS_START_DATE else 'N/A'}, tren revenue mulai
   merosot tajam. Titik terendah (Lowest Point) terjadi pada
   {TROUGH_DATE.date()} dengan revenue hanya {fmt_idr(TROUGH_VAL)} —
   penurunan sebesar {peak_to_trough_pct:.1f}% dari puncak
   (dalam {days_from_peak_to_trough} hari).

   Produk paling terdampak:
   → {top3_impacted.index[0]}
   → {top3_impacted.index[1]}
   → {top3_impacted.index[2]}

📜 PEMULIHAN
   Tanda pemulihan terdeteksi {days_to_recovery} hari setelah
   trough. Penggerak utamanya adalah produk kebutuhan rumah
   tangga dan bahan pokok:
   → {top3_recovery.index[0]}
   → {top3_recovery.index[1]}
   → {top3_recovery.index[2]}

💡 REKOMENDASI STRATEGIS
   1. BUFFER STOCK — Prioritaskan stok produk recovery drivers
      (bahan pokok & peralatan dapur) sebagai jaring pengaman.
   2. EARLY WARNING — Pasang alert otomatis jika rolling-7-day
      revenue turun >10% dari baseline.
   3. PRODUCT MIX — Diversifikasi ke kategori kebutuhan dasar
      yang terbukti resisten terhadap krisis.
""")