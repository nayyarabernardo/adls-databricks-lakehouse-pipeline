from pyspark.sql import functions as F
from src.gold.setup.base import read_silver, write_gold, add_gold_metadata

def build_sales_ny_gold(
    spark,
    silver_base_path: str,
    gold_table: str,
    gold_path: str
):
    # ===== Read Silver =====
    df_orders = read_silver(
        spark,
        f"{silver_base_path}/orders"
    )

    # ===== Filter & Aggregate =====
    df_sales_ny = (
        df_orders
        .filter(
            (F.col("state") == "NY") &
            (F.col("status") == "Delivered") &
            (F.col("shipped_date").isNotNull())
        )
        .groupBy("shipped_date")
        .agg(
            F.round(F.sum("total_sale"), 2).alias("total_sale")
        )
    )

    # ===== Metadata =====
    df_sales_ny = add_gold_metadata(df_sales_ny)

    # ===== Write =====
    write_gold(
        spark,
        df_sales_ny,
        gold_table,
        gold_path
    )
