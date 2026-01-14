from pyspark.sql import functions as F
from src.silver.setup.base import read_bronze, write_silver, add_ingestion_columns

def build_order_items_silver(
    spark,
    bronze_path: str,
    silver_table: str,
    silver_path: str
):
    df = read_bronze(spark, bronze_path)

    df_clean = (
        df
        .select(
            "order_id",
            "item_id",
            "product_id",
            "quantity",
            "list_price",
            "discount"
        )
        .filter(F.col("quantity") > 0)
        .filter(F.col("list_price") >= 0)
        .filter((F.col("discount") >= 0) & (F.col("discount") <= 1))
        .filter(F.col("order_id").isNotNull())
    )



    df_final = add_ingestion_columns(df_clean)

    write_silver(
        spark,
        df_final,
        silver_table,
        silver_path
    )
