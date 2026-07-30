import pandas as pd

# 1. Load Dataset
file_path = "1) iris.csv"
df = pd.read_csv(file_path)

# Cek kondisi awal data
print("--- Initial Data Overview ---")
print(f"Dataset shape: {df.shape}")
print("\nMissing values per column:")
print(df.isnull().sum())
print(f"\nTotal duplicate rows: {df.duplicated().sum()}")

# 2. Standardize Column Names (ubah ke lowercase & snake_case)
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace(".", "_", regex=False)
)

# 3. Handle Duplicate Rows
if df.duplicated().any():
    df = df.drop_duplicates().reset_index(drop=True)
    print(f"\nDuplicates removed. New dataset shape: {df.shape}")

# 4. Handle Missing Values
num_cols = df.select_dtypes(include=["float64", "int64"]).columns
for col in num_cols:
    if df[col].isnull().sum() > 0:
        df[col] = df[col].fillna(df[col].median())

cat_cols = df.select_dtypes(include=["object"]).columns
for col in cat_cols:
    df[col] = df[col].astype(str).str.strip().str.lower()
    if df[col].isnull().sum() > 0:
        df[col] = df[col].fillna(df[col].mode()[0])

# 5. Quick Verification & Export Result
print("\n--- Cleaned Data Summary ---")
print(df.info())
print("\nUnique categories in species:")
if "species" in df.columns:
    print(df["species"].value_counts())

# save file
output_file = "iris_cleaned.csv"
df.to_csv(output_file, index=False)
print(f"\nCleaned data successfully saved to '{output_file}'")