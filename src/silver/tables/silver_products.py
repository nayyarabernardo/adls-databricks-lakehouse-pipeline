from pyspark.sql import functions as F
from pyspark.sql import SparkSession

from src.silver.setup.base import add_ingestion_columns, read_bronze, write_silver


def build_products_silver(
    spark: SparkSession,
    bronze_path: str,
    silver_table: str,
    silver_path: str,
) -> None:
    """Constrói a tabela de produtos na camada Silver."""
    # ===== Reads =====
    df_products = read_bronze(spark, bronze_path)
    df_brands = read_bronze(spark, bronze_path.replace("products", "brands"))
    df_categories = read_bronze(spark, bronze_path.replace("products", "categories"))
    df_stocks = read_bronze(spark, bronze_path.replace("products", "stocks"))

    # ===== Stock agregado =====
    df_stock = (
        df_stocks
        .groupBy("product_id")
        .agg(
            F.sum("quantity").alias("total_stock")
        )
    )

    # ===== Products base =====
    df_products_clean = (
        df_products
        .select(
            "product_id",
            "product_name",
            "brand_id",
            "category_id",
            "model_year",
            "list_price"
        )
        .filter(F.col("product_id").isNotNull())
    )

    # ===== Joins =====
    df_joined = (
        df_products_clean.alias("p")
        .join(df_categories.alias("c"), "category_id", "left")
        .join(df_brands.alias("b"), "brand_id", "left")
        .join(df_stock.alias("s"), "product_id", "left")
    )

    # ===== Select final =====
    df_final = (
        df_joined
        .select(
            "product_id",
            "product_name",
            F.col("b.brand_name").alias("brand_name"),
            F.col("c.category_name").alias("category_name"),
            "model_year",
            "list_price",
            "total_stock"
        )
    )

    # ===== Ingestion metadata =====
    df_final = add_ingestion_columns(df_final)

    # ===== Write =====
    write_silver(
        spark,
        df_final,
        silver_table,
        silver_path
    )
