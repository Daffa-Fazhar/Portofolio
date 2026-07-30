import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Load cleaned dataset
df = pd.read_csv('iris_cleaned.csv')

# Set visual style
sns.set_theme(style='whitegrid')

# ---------------------------------------------------------
# 1. BAR PLOT: Average Petal Length by Species
# ---------------------------------------------------------
avg_petal = df.groupby('species')['petal_length'].mean().reset_index().sort_values('petal_length', ascending=False)
plt.figure(figsize=(7, 4.5))
sns.barplot(data=avg_petal, x='petal_length', y='species', palette='viridis')
plt.title('Average Petal Length by Species', fontsize=12, fontweight='bold')
plt.xlabel('Mean Petal Length (cm)', fontsize=10)  
plt.ylabel('Species', fontsize=10)  
plt.tight_layout()
plt.savefig('bar_plot_horizontal.png', dpi=300)
plt.show()

# ---------------------------------------------------------
# 2. LINE CHART: Feature Trend Across Samples
# ---------------------------------------------------------
plt.figure(figsize=(8, 4.5))
plt.plot(
    df.index,
    df['sepal_length'],
    label='Sepal Length',
    color='#1f77b4',
    linewidth=1.5,
)
plt.plot(
    df.index,
    df['petal_length'],
    label='Petal Length',
    color='#2ca02c',
    linewidth=1.5,
)
plt.title(
    'Sepal Length vs Petal Length Across Samples',
    fontsize=12,
    fontweight='bold',
)
plt.xlabel('Sample Index', fontsize=10)
plt.ylabel('Length (cm)', fontsize=10)
plt.legend(title='Features', loc='upper left')
plt.tight_layout()
plt.savefig('line_chart.png', dpi=300)
plt.show()

# ---------------------------------------------------------
# 3. SCATTER PLOT: Sepal Length vs Sepal Width
# ---------------------------------------------------------
plt.figure(figsize=(7, 5))
sns.scatterplot(
    data=df,
    x='sepal_length',
    y='sepal_width',
    hue='species',
    style='species',
    s=70,
    palette='Set1',
)
plt.title('Sepal Length vs Sepal Width', fontsize=12, fontweight='bold')
plt.xlabel('Sepal Length (cm)', fontsize=10)
plt.ylabel('Sepal Width (cm)', fontsize=10)
plt.legend(title='Species', loc='upper right')
plt.tight_layout()
plt.savefig('scatter_plot.png', dpi=300)
plt.show()