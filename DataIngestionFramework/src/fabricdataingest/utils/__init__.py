from datetime import datetime
import os

def utc_time():
    """
    # Get the current time in UTC
    # Convert to string
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

def buildAppendCommand(id, lakehouse,tablename,status):
    """
    Return KQL command 
    """
    kql_command = f"""
    .append SourceToBronzeLogs <|
    datatable (SourceTableID: string, DestLakehouse: string, DestTableName: string, Status: string, LogTime: datetime)
    [
        "{id}","{lakehouse}", "{tablename}", "{status}", datetime({utc_time()})
    ]
    """
    return kql_command

def isFabricSparkEnv():
    # Check for an environment variable that is specific to Fabric Spark
    return 'FABRIC_SPARK_ENV' in os.environ

__all__ = [
    "utc_time",
    "buildAppendCommand",
    "isFabricSparkEnv"
]