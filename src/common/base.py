# from pyspark.sql import functions as F

# def read_delta(spark, path: str):
#     return spark.read.format("delta").load(path)

# def add_ingestion_columns(df):
#     return df.withColumn("ingestion_ts", F.current_timestamp())

# def write_delta_table(
#     spark,
#     df,
#     table_full_name: str,
#     path: str
# ):
#     (
#         df.write
#         .format("delta")
#         .mode("overwrite")
#         .option("overwriteSchema", "true")
#         .save(path)
#     )

#     spark.sql(f"""
#         CREATE TABLE IF NOT EXISTS {table_full_name}
#         USING DELTA
#         LOCATION '{path}'
#     """)
from pyspark.sql import functions as F
from pyspark.sql.utils import AnalysisException

def read_delta(spark, path: str):
    return spark.read.format("delta").load(path)

def add_ingestion_columns(df):
    return df.withColumn("ingestion_ts", F.current_timestamp())

def write_delta_table(
    spark,
    df,
    table_full_name: str,
    path: str
):
    # 🔒 garante que o path não existe sujo
    try:
        spark.read.format("delta").load(path)
        table_exists = True
    except AnalysisException:
        table_exists = False

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
