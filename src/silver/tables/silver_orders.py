from pyspark.sql import functions as F
from src.silver.setup.base import read_bronze, write_silver, add_ingestion_columns

def build_orders_silver(
    spark,
    bronze_path: str,
    silver_table: str,
    silver_path: str
):
    # ===== Reads =====
    df_orders = read_bronze(spark, bronze_path)
    df_order_items = read_bronze(spark, bronze_path.replace("orders", "order_items"))
    df_stores = read_bronze(spark, bronze_path.replace("orders", "stores"))
    df_staffs = read_bronze(spark, bronze_path.replace("orders", "staffs"))

    # ===== Order Items =====
    df_items = (
        df_order_items
        .select(
            "order_id",
            "product_id",
            "quantity",
            "list_price",
            "discount",
            F.round(
                (F.col("list_price") * F.col("quantity")) * (1 - F.col("discount")),
                2
            ).alias("total_sale")
        )
    )

    # ===== Orders base =====
    df_orders_clean = (
        df_orders
        .filter(F.col("order_id").isNotNull())
        .withColumn(
            "status",
            F.when(F.col("order_status") == 1, "Pending")
             .when(F.col("order_status") == 2, "Processing")
             .when(F.col("order_status") == 3, "Shipped")
             .when(F.col("order_status") == 4, "Delivered")
             .otherwise("Unknown")
        )
    )

    # ===== Joins =====
    df_joined = (
        df_orders_clean.alias("ord")
        .join(df_stores.alias("st"), "store_id", "left")
        .join(df_staffs.alias("stf"), "staff_id", "left")
        .join(df_items.alias("oit"), "order_id", "left")
    )

    # ===== Select final =====
    df_final = (
        df_joined
        .select(
            "order_id",
            "customer_id",
            "status",
            "order_status",
            "order_date",
            "required_date",
            "shipped_date",

            F.col("st.store_name"),
            F.col("st.state"),
            F.col("st.city"),

            F.col("stf.first_name").alias("first_name_staff"),
            F.col("stf.active").alias("active_staff"),
            F.col("stf.email"),

            "product_id",
            "quantity",
            "total_sale",
            "list_price",
            "discount"
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
