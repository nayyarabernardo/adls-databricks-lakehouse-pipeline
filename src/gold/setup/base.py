from pyspark.sql import DataFrame, SparkSession, functions as F


def read_silver(spark: SparkSession, path: str) -> DataFrame:
    """Lê dados da camada Silver."""
    return spark.read.format("delta").load(path)


def add_gold_metadata(df: DataFrame) -> DataFrame:
    """Adiciona metadados de ingestão na camada Gold."""
    return df.withColumn("gold_ingestion_ts", F.current_timestamp())


def write_gold(
    spark: SparkSession,
    df: DataFrame,
    table_full_name: str,
    path: str,
) -> None:
    """Escreve dados na camada Gold e registra tabela."""
    (
        df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .save(path)
    )

    spark.sql(
        f"""
        CREATE TABLE IF NOT EXISTS {table_full_name}
        USING DELTA
        LOCATION '{path}'
        """
    )
