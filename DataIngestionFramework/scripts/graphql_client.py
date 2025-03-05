import requests
import os
from azure.identity import ClientSecretCredential

# Query data from Fabric GraphQL

def get_access_token(tenant_id, client_id, client_secret, scope):
    """
    Get an access token using a service principal.
    """
    credential = ClientSecretCredential(tenant_id, client_id, client_secret)
    token = credential.get_token(scope)
    return token.token

def query_fabric_graphql(query, graphql_endpoint, access_token):
    """
    Send a POST request to Fabric GraphQL with the given query.
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(graphql_endpoint, json={"query": query}, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    tenant_id = os.getenv('FABRICSPN_TENANTID')
    client_id = os.getenv('FABRICSPN_CLIENTID')
    client_secret = os.getenv('FABRICSPN_SECRET')
    graphql_endpoint = "https://a6e32b1d-3fb0-4cfe-a38b-3f812deb3334.za6.graphql.fabric.microsoft.com/v1/workspaces/a6e32b1d-3fb0-4cfe-a38b-3f812deb3334/graphqlapis/95b06a4b-3dca-451f-b24c-4ba5f177c770/graphql"
    scope = "https://analysis.windows.net/powerbi/api/.default"  # Correct scope for client credential flow

    query = """
    query {
      personPhones {
        items {
          BusinessEntityID
          PhoneNumber
          PhoneNumberTypeID
          ModifiedDate
        }
      }
    }
    """

    access_token = get_access_token(tenant_id, client_id, client_secret, scope)
    result = query_fabric_graphql(query, graphql_endpoint, access_token)
    print(result)
