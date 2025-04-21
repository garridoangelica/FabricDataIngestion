import unittest
import sys
import os
from azure.kusto.data.exceptions import KustoServiceError,KustoThrottlingError
from concurrent.futures import ThreadPoolExecutor, as_completed

import fabricdataingest.helloworld as hw
import fabricdataingest.eventhouse as evc
import fabricdataingest.utils as utils


class TestEventHouse(unittest.TestCase):
    def test_print_hello(self, name="Microsoft"):
        print("Print Hello World Test Case")
        # Call the function
        say_hello = hw.print_hello(name)
        # Assert the output
        self.assertEqual(say_hello, f"Hello {name}")

    def test_eventhouse_connector(self):
        print("Eventhouse Connector Test Case")
        # Set up the environment variables for Kusto connection
        kustoUri = os.getenv('FABRIC_KUSTO_URI')
        database = os.getenv('FABRIC_KUSTO_DATABASE')
        # Call the function
        ehc = evc.EventHouseConnector(kustoUri, database)
        # Assert the output
        self.assertEqual(ehc.kustoUri, kustoUri)
        self.assertEqual(ehc.database, database)

        status = ["InProgress", "Completed"]
        for id in range(3):
            for stat in status:  # Iterate over the status list
                # Get the KQL Command
                id += 1
                kql_command = utils.buildAppendCommand(f'{id}', "bronze", f"Table{id}_TestCaseGitHub", f"{stat}")
                response = ehc.execute_query(kql_command)
                self.assertEqual(response.errors_count, 0)

    def test_throttle_handling(self):
        print("Throttle Handling Test Case")
        # Set up the environment variables for Kusto connection
        kustoUri = os.getenv('FABRIC_KUSTO_URI')
        database = os.getenv('FABRIC_KUSTO_DATABASE')
        ehc = evc.EventHouseConnector(kustoUri, database)

        status = "InProgress"

        def execute_query(id):
            kql_command = utils.buildAppendCommand(f'{id}', "bronze", f"Table{id}_TestTrottle", f"{status}")
            try:
                ehc.execute_query(kql_command)
            except KustoThrottlingError as e:
                return e

        throttled = False
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(execute_query, id) for id in range(100)]  # Adjust the range as needed to trigger throttling
            for future in as_completed(futures):
                exception = future.result()
                if isinstance(exception, KustoThrottlingError):
                    throttled = True
                    print("Received 429 Too Many Requests.")
                    break
                elif exception:
                    print(f"Unexpected error: {exception}")
                    raise exception

        self.assertFalse(throttled, "Received 429 Too Many Requests error.")

if __name__ == '__main__':
    # Create a test suite
    suite = unittest.TestSuite()
    # Add individual test cases to the suite
    # Hello World Test Case for testing calling test cases
    suite.addTest(TestEventHouse('test_print_hello'))
    # Test Case to check if the EventHouseConnector sends data properly to the Kusto DB
    suite.addTest(TestEventHouse('test_eventhouse_connector'))
    # Test Case to check if the EventHouseConnector handles throttling properly
    # suite.addTest(TestEventHouse('test_throttle_handling'))  # Uncommented to include throttling test case
    # Run the test suite
    runner = unittest.TextTestRunner()
    runner.run(suite)