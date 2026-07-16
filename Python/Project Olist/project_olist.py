import polars as pl

def run_etl_olist():
    print("Starting ETL pipeline for Olist dataset...")
    
    # 1. Load data source (Lazy mode)
    orders_lazy = pl.scan_csv("olist_orders_dataset.csv")
    items_lazy = pl.scan_csv("olist_order_items_dataset.csv")
    payments_lazy = pl.scan_csv("olist_order_payments_dataset.csv")
    products_lazy = pl.scan_csv("olist_products_dataset.csv")
    translation_lazy = pl.scan_csv("product_category_name_translation.csv")
    customers_lazy = pl.scan_csv("olist_customers_dataset.csv")
    sellers_lazy = pl.scan_csv("olist_sellers_dataset.csv")
    geo_lazy = pl.scan_csv("olist_geolocation_dataset.csv")

    # 2. Aggregate geolocation to prevent row explosion
    geo_prepared = (
        geo_lazy
        .group_by("geolocation_zip_code_prefix")
        .agg([
            pl.col("geolocation_lat").mean().alias("lat"),
            pl.col("geolocation_lng").mean().alias("lng"),
            pl.col("geolocation_city").first().alias("city"),
            pl.col("geolocation_state").first().alias("state")
        ])
    )

    # 3. Build Sales Master Data
    print("Processing sales master dataframe...")
    sales_master_df = (
        orders_lazy
        .join(items_lazy, on="order_id", how="inner")
        .join(payments_lazy, on="order_id", how="left")
        .join(products_lazy, on="product_id", how="left")
        .join(translation_lazy, on="product_category_name", how="left")
        .join(customers_lazy.select(["customer_id", "customer_unique_id"]), on="customer_id", how="left")
        .select([
            "order_id",
            "customer_unique_id",
            "order_purchase_timestamp",
            "order_status",
            "product_id",
            "price",
            "freight_value",
            "payment_type",
            "payment_value",
            pl.col("product_category_name_english").alias("product_category")
        ])
        .collect()
    )

    # 4. Build Geospasial Master Data (Customer & Seller)
    print("Processing geospatial master dataframe...")
    customer_loc = (
        customers_lazy
        .join(geo_prepared, left_on="customer_zip_code_prefix", right_on="geolocation_zip_code_prefix", how="left")
        .select([
            pl.col("customer_unique_id").alias("user_id"),
            pl.lit("Customer").alias("user_type"),
            pl.col("customer_zip_code_prefix").alias("zip_code"),
            "lat",
            "lng",
            pl.col("customer_city").alias("city"),
            pl.col("customer_state").alias("state")
        ])
    )

    seller_loc = (
        sellers_lazy
        .join(geo_prepared, left_on="seller_zip_code_prefix", right_on="geolocation_zip_code_prefix", how="left")
        .select([
            pl.col("seller_id").alias("user_id"),
            pl.lit("Seller").alias("user_type"),
            pl.col("seller_zip_code_prefix").alias("zip_code"),
            "lat",
            "lng",
            pl.col("seller_city").alias("city"),
            pl.col("seller_state").alias("state")
        ])
    )

    geo_master_df = pl.concat([customer_loc, seller_loc]).collect()

    # 5. Export processed data to CSV for Power BI
    print("Exporting clean datasets to CSV...")
    sales_master_df.write_csv("tabel_sales_master.csv")
    geo_master_df.write_csv("tabel_geo_master.csv")
    
    print("ETL pipeline completed successfully.")

if __name__ == "__main__":
    run_etl_olist()