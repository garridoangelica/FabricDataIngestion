from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.kusto.data.exceptions import KustoServiceError, KustoThrottlingError
import logging
from datetime import datetime
import fabricdataingest.utils as utils
import os
from tenacity import retry, stop_after_attempt, wait_random_exponential, retry_if_exception_type, before_sleep_log, after_log

class EventHouseConnector:
    """
    Class to initiate and execute KQL queries
    Initial Params:
        Kusto URI: URI of your event house
        Database: name of the database
    """
    def __init__(self, kustoUri, database,_log=logging.INFO):
        self.logger = logging.getLogger(__name__)
        self.kustoUri = kustoUri
        self.database = database
        self.client = self._create_client()
        
    def _create_client(self):
        if utils.isFabricSparkEnv(): 
            def token_provider():
                return mssparkutils.credentials.getToken(self.kustoUri)
            kcsb = KustoConnectionStringBuilder.with_token_provider(self.kustoUri, token_provider)
        
        elif utils.isLocalEnv(): 
            ### Asssuming it's local dev. Authenticate with AAD
            kcsb = KustoConnectionStringBuilder.with_aad_device_authentication(self.kustoUri)

        elif utils.isGithubWorkflowEnv(): 
            client_id = os.getenv('FABRICSPN_CLIENTID')
            client_secret = os.getenv('FABRICSPN_SECRET')
            tenant_id =  os.getenv('FABRICSPN_TENANTID')
            kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(self.kustoUri,client_id, client_secret, tenant_id)
        else:
            raise ValueError(f"Environment not supported. Please use local, Fabric, or GitHub Workflow.")
        return KustoClient(kcsb)

    @retry(
        retry=retry_if_exception_type(KustoThrottlingError),
        wait=wait_random_exponential(multiplier=5,min=10, max=60),
        stop=stop_after_attempt(5),
        reraise=True
    )
    def execute_query_with_retry(self, kql_command):
        try:
            self.logger.info(f'Executing KQL command: {kql_command}')
            response = self.client.execute(self.database, kql_command)
            self.logger.info("Query executed successfully!")
            return response
        except KustoThrottlingError as e:
            self.logger.warning(f"KustoThrottlingError encountered: {kql_command[159:171]}")
            raise e
        except KustoServiceError as e:
            self.logger.error(f"KustoServiceError: {e}")
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            raise e

    def execute_query(self, kql_command):
        try:
            return self.execute_query_with_retry(kql_command)
        except KustoThrottlingError as e:
            self.logger.error(f"Failed to execute query after retries due to throttling: {kql_command[159:171]}")
            raise e