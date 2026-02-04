from typing import Any

from pyspark.sql import SparkSession

from src.config.settings import LAYER_PATHS


def ingest_table(metadata: dict[str, Any], spark: SparkSession) -> None:
    """Ingere uma tabela na camada Bronze."""
    table_name = metadata["table_name"]
    source = metadata["source"]

    source_path = source["path"]
    source_format = source["format"]
    source_opts = source.get("options", {})

    target_path = f"{LAYER_PATHS['bronze']}/{table_name}"

    df = spark.read.format(source_format)
    for k, v in source_opts.items():
        df = df.option(k, v)

    df = df.load(source_path)

    (
        df.write
        .mode("overwrite")
        .format("delta")
        .option("mergeSchema", "true")
        .save(target_path)
    )

    print(f"Bronze | {table_name} ingerida com sucesso")

