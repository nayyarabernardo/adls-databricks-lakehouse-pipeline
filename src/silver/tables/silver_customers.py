from pyspark.sql import functions as F
from src.silver.setup.base import read_bronze, write_silver, add_ingestion_columns

def build_customers_silver(
    spark,
    bronze_path: str,
    silver_table: str,
    silver_path: str
):
    # ===== Read =====
    df_customers = read_bronze(spark, bronze_path)

    # ===== Clean =====
    df_clean = (
        df_customers
        .select(
            "customer_id",
            "first_name",
            "last_name",
            "phone",
            "email",
            "street",
            "city",
            "state",
            "zip_code"
        )
        .filter(F.col("customer_id").isNotNull())
        .filter(
            (F.col("phone").isNotNull()) &
            (~F.upper(F.col("phone")).isin("NULL", "NULL "))
        )
        .filter(
            (F.col("email").isNotNull()) &
            (~F.upper(F.col("email")).isin("NULL", "NULL "))
        )
    )

    # ===== Ingestion metadata =====
    df_final = add_ingestion_columns(df_clean)

    # ===== Write =====
    write_silver(
        spark,
        df_final,
        silver_table,
        silver_path
    )
