import json
from typing import Any

from pyspark.sql import SparkSession


def load_json(file_path: str) -> dict[str, Any]:
    """Carrega um arquivo JSON do ABFS."""
    spark = SparkSession.builder.getOrCreate()
    df = spark.read.text(file_path)
    json_string = "".join(row.value for row in df.collect())
    return json.loads(json_string)
