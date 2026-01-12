from pyspark.sql import functions as F
from src.silver.base import read_bronze, write_silver, add_ingestion_columns

def build_orders_silver(
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
            "customer_id",
            "order_status",
            "order_date",
            "required_date",
            "shipped_date",
            "store_id",
            "staff_id"
        )
        .filter(F.col("order_id").isNotNull())
    )


    df_final = add_ingestion_columns(df_clean)

    write_silver(
        spark,
        df_final,
        silver_table,
        silver_path
    )
