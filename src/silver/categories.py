from pyspark.sql import functions as F
from src.silver.base import read_bronze, write_silver, add_ingestion_columns

def build_categories_silver(
    spark,
    bronze_path: str,
    silver_table: str,
    silver_path: str
):
    df = read_bronze(spark, bronze_path)

    df_clean = (
        df
        .select(
            "category_id",
            "category_name"
        )
        .filter(F.col("category_id").isNotNull())
    )



    df_final = add_ingestion_columns(df_clean)

    write_silver(
        spark,
        df_final,
        silver_table,
        silver_path
    )
