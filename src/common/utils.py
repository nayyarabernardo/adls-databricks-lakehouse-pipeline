def load_json(file_path):
    """Carrega um arquivo JSON do ABFS"""
    from pyspark.sql import SparkSession
    
    spark = SparkSession.builder.getOrCreate()
    
    df = spark.read.text(file_path)
    json_string = "".join([row.value for row in df.collect()])
    
    import json
    return json.loads(json_string)
