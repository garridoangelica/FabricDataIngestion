import unittest
import sys
import os
import json

## If you would like to run locally, put the source path of where the src code is
# src_path = '<your directory>/FabricDataEng/DataIngestionFramework/src/'
# sys.path.insert(0, src_path)
from fabricdataingest.dags._daggen import DagGenerator

class TestDagGenerator(unittest.TestCase):

    def setUp(self):
        self.customer = "example_customer"
        self.notebookPath = "/path/to/notebook"
        self.timeoutInSeconds = 3600
        self.concurrency = 50
        self.dag_generator = DagGenerator(self.customer, self.notebookPath, self.timeoutInSeconds, self.concurrency)

    def test_parse_string_to_list(self):
        input_string = "a,b,c"
        expected_output = ["a", "b", "c"]
        self.assertEqual(self.dag_generator.parse_string_to_list(input_string), expected_output)

    def test_generate_json(self):
        tables = ["SalesLT.Customer.parquet"]
        expected_output = {
            "activities": [
                {
                    "name": "Notebookexample_customer_SalesLT.Customer.parquet",
                    "path": self.notebookPath,
                    "timeoutPerCellInSeconds": 90,
                    "args": {
                        "customer": self.customer,
                        "tableName": "SalesLT.Customer.parquet"
                    }
                }
            ],
            "timeoutInSeconds": self.timeoutInSeconds,
            "concurrency": self.concurrency
        }
        generated_json = self.dag_generator.generate_json(tables)
        self.assertEqual(json.loads(generated_json), expected_output)

    def test_generate_json_from_array(self):
        notebook_configs = [
            {
                "table": "SalesLT.Customer",
                "notebook_path": "/path/to/customer_notebook"
            },
            {
                "table": "SalesLT.Order",
                "dependencies": ["Notebookexample_customer_SalesLT.Customer"],
                "args": {"additional_param": "value"}
            }
        ]

        expected_output = {
            "activities": [
                {
                    "name": "Notebookexample_customer_SalesLT.Customer",
                    "path": "/path/to/customer_notebook",
                    "timeoutPerCellInSeconds": 90,
                    "args": {
                        "customer": "example_customer",
                        "tableName": "SalesLT.Customer"
                    }
                },
                {
                    "name": "Notebookexample_customer_SalesLT.Order",
                    "path": "/path/to/notebook",
                    "timeoutPerCellInSeconds": 90,
                    "args": {
                        "customer": "example_customer",
                        "tableName": "SalesLT.Order",
                        "additional_param": "value"
                    },
                    "dependsOn": ["Notebookexample_customer_SalesLT.Customer"]
                }
            ],
            "timeoutInSeconds": 3600,
            "concurrency": 50
        }

        generated_json = self.dag_generator.generate_json_from_array(notebook_configs)
        self.assertEqual(json.loads(generated_json), expected_output)

if __name__ == '__main__':
    # Create a test suite
    suite = unittest.TestSuite()
    # Add individual test cases to the suite
    suite.addTest(TestDagGenerator('test_parse_string_to_list'))
    suite.addTest(TestDagGenerator('test_generate_json'))
    suite.addTest(TestDagGenerator('test_generate_json_from_array'))
    # Run the test suite
    runner = unittest.TextTestRunner()
    runner.run(suite)
