import requests
import os
from azure.identity import ClientSecretCredential

## Get existing running jobs for a notebook item in fabric workspace
# This script retrieves the running jobs for a specific item in a 
# Fabric workspace using an SPN for authentication.

def get_access_token(tenant_id, client_id, client_secret, scope):
    """
    Get an access token using a service principal.
    """
    credential = ClientSecretCredential(tenant_id, client_id, client_secret)
    token = credential.get_token(scope)
    return token.token

def get_running_jobs(workspace_id, item_id, access_token, continuation_token=None):
    """
    Get a list of running jobs for an item in a notebook.
    """
    base_url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}/jobs/instances"
    if continuation_token:
        url = f"{base_url}?continuationToken={continuation_token}"
    else:
        url = base_url

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    tenant_id = os.getenv('FABRICSPN_TENANTID')
    client_id = os.getenv('FABRICSPN_CLIENTID')
    client_secret = os.getenv('FABRICSPN_SECRET')
    workspace_id = "a6e32b1d-3fb0-4cfe-a38b-3f812deb3334"  # Replace with your workspace ID
    item_id = "e439a96b-66e8-431d-b5f9-464ed6a2be5d"  # Replace with your item ID
    scope = "https://analysis.windows.net/powerbi/api/.default"  # Correct scope for client credential flow

    access_token = get_access_token(tenant_id, client_id, client_secret, scope)
    result = get_running_jobs(workspace_id, item_id, access_token)
    print(result)
