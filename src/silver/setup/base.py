from pyspark.sql import functions as F

def read_bronze(spark, path: str):
    return spark.read.format("delta").load(path)

def add_ingestion_columns(df):
    return df.withColumn("ingestion_ts", F.current_timestamp())

def write_silver(spark, df, table_full_name: str, path: str):
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
