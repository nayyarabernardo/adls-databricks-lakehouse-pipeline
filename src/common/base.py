from pyspark.sql import DataFrame, SparkSession, functions as F


def read_delta(spark: SparkSession, path: str) -> DataFrame:
    """Lê um dataset Delta no caminho informado."""
    return spark.read.format("delta").load(path)


def add_ingestion_columns(df: DataFrame) -> DataFrame:
    """Adiciona a coluna de timestamp de ingestão."""
    return df.withColumn("ingestion_ts", F.current_timestamp())


def write_delta_table(
    spark: SparkSession,
    df: DataFrame,
    table_full_name: str,
    path: str,
) -> None:
    """Escreve DataFrame em Delta e registra a tabela."""
    (
        df.write.format("delta")
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
