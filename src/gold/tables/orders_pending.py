from pyspark.sql import functions as F
from src.common.base import read_delta
from src.gold.setup.base import write_gold, add_gold_metadata

def build_orders_pending_gold(
    spark,
    silver_base_path: str,
    gold_table: str,
    gold_path: str
):
    # ===== Read Silver =====
    df_orders = read_delta(spark, f"{silver_base_path}/orders")
    df_customers = read_delta(spark, f"{silver_base_path}/customers")

    # ===== Pending aggregation =====
    df_pending = (
        df_orders
        .filter(F.lower(F.col("status")) == "pending")
        .groupBy(
            "customer_id",
            "store_name",
            "order_date"
        )
        .agg(
            F.sum("quantity").alias("total_items")
        )
    )

    # ===== Join customers =====
    df_joined = (
        df_pending.alias("p")
        .join(
            df_customers.alias("c"),
            "customer_id",
            "left"
        )
    )

    # ===== Only customers with complete contact =====
    df_final = (
        df_joined
        .filter(F.col("c.email").isNotNull())
        .filter(F.col("c.phone").isNotNull())
        .select(
            "customer_id",
            "order_date",
            "store_name",
            "total_items",
            F.col("c.first_name").alias("first_name_customer"),
            "c.email",
            "c.phone"
        )
    )

    # ===== Gold metadata =====
    df_final = add_gold_metadata(df_final)

    # ===== Write =====
    write_gold(
        spark,
        df_final,
        gold_table,
        gold_path
    )
