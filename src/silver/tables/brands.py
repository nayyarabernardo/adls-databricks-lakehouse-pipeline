from src.silver.setup.base import read_bronze, write_silver, add_ingestion_columns

def build_brands_silver(
    spark,
    bronze_path: str,
    silver_table: str,
    silver_path: str
):
    df = read_bronze(spark, bronze_path)

    df_final = (
        df
        .select("brand_id", 
                "brand_name")
        .dropDuplicates()
    )

    df_final = add_ingestion_columns(df_final)

    write_silver(
        spark,
        df_final,
        silver_table,
        silver_path
    )
