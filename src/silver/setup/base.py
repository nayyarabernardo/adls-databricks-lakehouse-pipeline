from src.common.base import read_delta, write_delta_table, add_ingestion_columns

def read_bronze(spark, path: str):
    return read_delta(spark, path)

def write_silver(
    spark,
    df,
    table_full_name: str,
    path: str
):
    write_delta_table(
        spark,
        df,
        table_full_name,
        path
    )
