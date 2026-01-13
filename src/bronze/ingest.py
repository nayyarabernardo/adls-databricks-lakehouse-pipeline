from src.common.utils import load_json
from src.bronze.upload import ingest_table
from src.config.settings import METADATA_BASE_PATH

def run_bronze_ingestion(spark, table_name: str | None = None):
    metadata_path = f"{METADATA_BASE_PATH}/bronze"

    try:
        if table_name:
            file_path = f"{metadata_path}/{table_name}.json"
            metadata = load_json(file_path)
            ingest_table(metadata, spark)

        else:
            files_df = (
                spark.read
                .format("binaryFile")
                .load(f"{metadata_path}/*.json")
            )

            json_files = [row.path for row in files_df.select("path").collect()]

            for file_path in json_files:
                metadata = load_json(file_path)
                ingest_table(metadata, spark)

    except Exception as e:
        print(f"Erro ao processar arquivos de metadata: {e}")
        raise
