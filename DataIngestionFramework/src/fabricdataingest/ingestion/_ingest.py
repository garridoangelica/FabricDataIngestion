from delta.tables import *
import os
from pyspark.sql import SparkSession
from pyspark.sql.utils import AnalysisException

# spark = SparkSession.builder.appName("DataIngestion").getOrCreate()

def readFromPath(filePath, schema=None, fileType='parquet', options=None):
    """
    Read a file from a path and return a DataFrame.
    Use set of conditions to determine how to read the file. Based on schema, fileType, etc.
    """
    try:
        if fileType == 'parquet':
            if schema is not None:
                df = spark.read.schema(schema).parquet(filePath)
            else:
                df = spark.read.parquet(filePath)
        elif fileType == 'csv':
            if schema is not None:
                df = spark.read.schema(schema).csv(filePath)
            else:
                df = spark.read.csv(filePath)
        elif fileType == 'delta':
            if schema is not None:
                df = spark.read.schema(schema).format("delta").load(filePath)
            else:
                df = spark.read.format("delta").load(filePath)
        else:
            raise ValueError(f"File type {fileType} not supported. Please use parquet, csv, or delta.")
        return df
    except AnalysisException as e:
        print(f"Error reading {fileType} file from {filePath}: {e}")
        return None

def writeToPath(df, filePath, mode='overwrite', fileType='parquet', options=None):
    """
    Write a DataFrame to a file path.
    Use set of conditions to determine how to write the file. Based on schema, fileType, etc.
    """
    try:
        if fileType == 'parquet':
            df.write.mode(mode).parquet(filePath)
        elif fileType == 'csv':
            df.write.mode(mode).csv(filePath)
        elif fileType == 'delta':
            df.write.mode(mode).format("delta").save(filePath)
        else:
            raise ValueError(f"File type {fileType} not supported. Please use parquet, csv, or delta.")
    except Exception as e:
        print(f"Error writing {fileType} file to {filePath}: {e}")

def readDeltaTable(path_or_table):
    """
    Read a delta table from the lakehouse. Returns DeltaTable object.
    This function returns a DeltaTable object, NOT a DataFrame.

    :param path_or_table: Path to the Delta table or the table name.
    """
    try:
        if os.path.exists(path_or_table):
            return DeltaTable.forPath(spark, path_or_table)
        else:
            return DeltaTable.forName(spark, path_or_table)
    except AnalysisException as e:
        print(f"Error reading Delta table from {path_or_table}: {e}")
        return None
    

def mergeDeltaTable(target, source, condition):
    """
    Merge a source dataframe into a target Delta table.
    """
    (target.alias("target")
     .merge(source.alias("source"), condition)
        .whenMatchedUpdateAll()
        .whenNotMatchedInsertAll()
        .execute())
    return