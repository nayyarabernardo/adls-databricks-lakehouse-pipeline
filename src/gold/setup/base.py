from pyspark.sql import functions as F
from pyspark.sql import DataFrame

def read_silver(spark, path: str) -> DataFrame:
    return spark.read.format("delta").load(path)

def add_gold_metadata(df: DataFrame) -> DataFrame:
    return df.withColumn("gold_ingestion_ts", F.current_timestamp())

def write_gold(
    spark,
    df: DataFrame,
    table_full_name: str,
    path: str
):
    (
        df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .save(path)
    )

    spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {table_full_name}
        USING DELTA
        LOCATION '{path}'
    """)
