from pyspark.sql import functions as F
from src.silver.setup.base import read_bronze, write_silver, add_ingestion_columns

def build_stores_silver(
    spark,
    bronze_path: str,
    silver_table: str,
    silver_path: str
):
    df = read_bronze(spark, bronze_path)

    df_clean = (
    df
    .select(
        "store_id",
        "store_name",
        "phone",
        "email",
        "street",
        "city",
        "state",
        "zip_code"
    )
    .filter(F.col("store_id").isNotNull())
)


    df_final = add_ingestion_columns(df_clean)

    write_silver(
        spark,
        df_final,
        silver_table,
        silver_path
    )
