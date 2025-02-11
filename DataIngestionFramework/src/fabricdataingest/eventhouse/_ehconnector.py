from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.kusto.data.exceptions import KustoServiceError
import logging
from datetime import datetime
import fabricdataingest.utils as utils
import os 

class EventHouseConnector:
    """
    Class to initiate and execute KQL queries
    Initial Params:
        Kusto URI: URI of your event house
        Database: name of the database
    """
    def __init__(self, kustoUri, database,env='Fabric',_log=logging.INFO):
        self.logger = logging.getLogger(__name__)
        self.kustoUri = kustoUri
        self.database = database
        self.env = env
        self.client = self._create_client()
        
    def _create_client(self):
        if utils.isFabricSparkEnv(): 
            def token_provider():
                return mssparkutils.credentials.getToken(self.kustoUri)
            kcsb = KustoConnectionStringBuilder.with_token_provider(self.kustoUri, token_provider)
        elif self.env == 'local':
            ### Asssuming it's local dev. Authenticate with AAD
            kcsb = KustoConnectionStringBuilder.with_aad_device_authentication(self.kustoUri)
        elif self.env == 'Workflow':
            client_id = os.getenv('FABRICSPN_CLIENTID')
            client_secret = os.getenv('FABRICSPN_SECRET')
            tenant_id =  os.getenv('FABRICSPN_SUBID')
            kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(self.kustoUri,client_id, client_secret, tenant_id)
        else:
            raise ValueError(f"Environment {self.env} not supported. Please use local, Fabric, or Workflow.")
        return KustoClient(kcsb)

    def execute_query(self, kql_command):
        try:
            self.logger.info(f'Logging to EvenHouse {kql_command}')
            response = self.client.execute(self.database, kql_command)
            if response.errors_count == 0:
                self.logger.info("Query executed successfully!")
            return response

        except KustoServiceError as e:
            self.logger.error(f"KustoClientError: {e}")