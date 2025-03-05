import unittest
from unittest.mock import patch, Mock
import os
import DataIngestionFramework.scripts.graphql_client as graphql_client

class TestGraphQLClient(unittest.TestCase):
    @patch('fabricdataingest.graphql_client.requests.post')
    @patch('fabricdataingest.graphql_client.ClientSecretCredential.get_token')
    def test_query_fabric_graphql(self, mock_get_token, mock_post):
        # Mock the access token
        mock_get_token.return_value = Mock(token="mock_access_token")

        # Mock the GraphQL response
        mock_response = Mock()
        mock_response.json.return_value = {
            "data": {
                "personPhones": {
                    "items": [
                        {
                            "BusinessEntityID": 1,
                            "PhoneNumber": "123-456-7890",
                            "PhoneNumberTypeID": 1,
                            "ModifiedDate": "2023-01-01T00:00:00Z"
                        }
                    ]
                }
            }
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        tenant_id = "mock_tenant_id"
        client_id = "mock_client_id"
        client_secret = "mock_client_secret"
        graphql_endpoint = "https://mock-graphql-endpoint"
        scope = "https://graph.microsoft.com/.default"

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

        access_token = graphql_client.get_access_token(tenant_id, client_id, client_secret, scope)
        result = graphql_client.query_fabric_graphql(query, graphql_endpoint, access_token)

        self.assertEqual(result["data"]["personPhones"]["items"][0]["BusinessEntityID"], 1)
        self.assertEqual(result["data"]["personPhones"]["items"][0]["PhoneNumber"], "123-456-7890")
        self.assertEqual(result["data"]["personPhones"]["items"][0]["PhoneNumberTypeID"], 1)
        self.assertEqual(result["data"]["personPhones"]["items"][0]["ModifiedDate"], "2023-01-01T00:00:00Z")

if __name__ == '__main__':
    unittest.main()
