import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# 1. Load data hasil cleaning dari Task 1
df = pd.read_csv("iris_cleaned.csv")
# Ambil list kolom numerik
num_cols = df.select_dtypes(include=["float64", "int64"]).columns

# =========================================================
# 1. SUMMARY STATISTICS
# (Mean, Median, Mode, Std Dev)
# =========================================================
print("=== DESCRIPTIVE STATISTICS ===")

summary = pd.DataFrame(
    {
        "Mean": df[num_cols].mean(),
        "Median": df[num_cols].median(),
        "Mode": df[num_cols].mode().iloc[0],
        "Std Dev": df[num_cols].std(),
    }
).round(2)

print(summary)
print("\n" + "=" * 35 + "\n")

# =========================================================
# 2. VISUALISASI DISTRIBUSI DATA
# =========================================================
sns.set_theme(style="ticks")

# A. Histogram (Distribusi Fitur)
fig, axes = plt.subplots(2, 2, figsize=(9, 6))
fig.suptitle("Distribution of Numerical Variables", fontsize=12, fontweight="bold")

for i, col in enumerate(num_cols):
    ax = axes[i // 2, i % 2]
    sns.histplot(df[col], kde=True, ax=ax, color="#34495e")
    ax.set_title(f"Distribution of {col}")

plt.tight_layout()
plt.show()

# B. Boxplot (Outlier Check)
plt.figure(figsize=(8, 4))
sns.boxplot(data=df[num_cols], palette="Set2")
plt.title("Outlier Analysis (Boxplot)", fontweight="bold")
plt.ylabel("Size (cm)")
plt.show()

# C. Scatter Plot (Petal Length vs Petal Width)
plt.figure(figsize=(7, 5))
sns.scatterplot(
    data=df,
    x="petal_length",
    y="petal_width",
    hue="species",
    style="species",
    s=60,
    palette="deep",
)
plt.title("Petal Length vs Petal Width Relationship", fontweight="bold")
plt.tight_layout()
plt.show()

# =========================================================
# 3. KORELASI ANTAR FITUR
# =========================================================
corr = df[num_cols].corr()
print("=== CORRELATION MATRIX ===")
print(corr.round(3))

# Heatmap Correlation
plt.figure(figsize=(6, 4.5))
sns.heatmap(corr, annot=True, cmap="YlGnBu", fmt=".2f", cbar=True)
plt.title("Correlation Heatmap", fontweight="bold")
plt.tight_layout()
plt.show()