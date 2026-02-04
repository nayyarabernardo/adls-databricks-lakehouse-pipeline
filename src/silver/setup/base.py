from pyspark.sql import DataFrame, SparkSession

from src.common.base import add_ingestion_columns, read_delta, write_delta_table


def read_bronze(spark: SparkSession, path: str) -> DataFrame:
    """Lê dados da camada Bronze."""
    return read_delta(spark, path)


def write_silver(
    spark: SparkSession,
    df: DataFrame,
    table_full_name: str,
    path: str,
) -> None:
    """Escreve dados na camada Silver."""
    write_delta_table(spark, df, table_full_name, path)
