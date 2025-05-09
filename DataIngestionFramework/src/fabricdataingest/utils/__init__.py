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
    datatable (SourceTableName: string, DestLakehouse: string, DestTableName: string, Status: string, LogTime: datetime, EventProcessedUtcTime: datetime, EventEnqueuedUtcTime: datetime, PartitionId: int)
    [
        'Table_{id}',"{lakehouse}", 'Table_{id}_{tablename}', "{status}", datetime({utc_time()}),datetime({utc_time()}),datetime({utc_time()}),0
    ]
    """
    return kql_command

def buildMessage(id, status):
    # Create a JSON message
    message = {
        'SourceTableName': f'Table_{id}',
        'DestLakehouse': 'BronzeLakehouse',
        'DestTableName': f'Table_{id}',
        'Status':status,
        'LogTime': utc_time()
    }
    return message

def isFabricSparkEnv():
    # Check for an environment variable that is specific to Fabric Spark
    return 'FABRIC_SPARK_ENV' in os.environ

def isLocalEnv():
    # Check for an environment variable that is specific to local development
    if 'LOCAL_ENV' in os.environ and 'GITHUB_ACTIONS_ENV' in os.environ:
        if os.environ['LOCAL_ENV'] == 'false' and os.environ['GITHUB_ACTIONS_ENV'] == 'true':
            return False
    return 'LOCAL_ENV' in os.environ

def isGithubWorkflowEnv():
    # Check for an environment variable that is specific to GitHub Actions
    return 'GITHUB_ACTIONS_ENV' in os.environ

__all__ = [
    "utc_time",
    "buildAppendCommand",
    "isFabricSparkEnv"
]