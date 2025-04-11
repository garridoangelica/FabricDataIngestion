import unittest
import sys
import os
from azure.kusto.data.exceptions import KustoServiceError,KustoThrottlingError
from concurrent.futures import ThreadPoolExecutor, as_completed

import fabricdataingest.helloworld as hw
import fabricdataingest.eventhouse as evc
import fabricdataingest.utils as utils


class TestPackagename(unittest.TestCase):
    def test_print_hello(self, name="Microsoft"):
        # Call the function
        say_hello = hw.print_hello(name)
        # Assert the output
        self.assertEqual(say_hello, f"Hello {name}")

    def test_eventhouse_connector(self):
        kustoUri = os.getenv('FABRIC_KUSTO_URI')
        database = os.getenv('FABRIC_KUSTO_DATABASE')
        # Call the function
        ehc = evc.EventHouseConnector(kustoUri, database)
        # Assert the output
        self.assertEqual(ehc.kustoUri, kustoUri)
        self.assertEqual(ehc.database, database)

        id = "2"
        status = "InProgress"
        # Get the KQL Command
        kql_command = utils.buildAppendCommand(f'{id}', "bronze", f"Table{id}_TestCaseGitHub", f"{status}")
        response = ehc.execute_query(kql_command)
        self.assertEqual(response.errors_count, 0)

    def test_throttle_handling(self):
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
    suite.addTest(TestPackagename('test_print_hello'))
    suite.addTest(TestPackagename('test_eventhouse_connector'))
    suite.addTest(TestPackagename('test_throttle_handling'))
    # Run the test suite
    runner = unittest.TextTestRunner()
    runner.run(suite)