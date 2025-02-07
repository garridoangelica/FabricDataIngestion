import unittest
import sys
import os

# Add the src/fabricdataingestion directory to the sys.path If I'm doing local dev
# src_path = 'C:\\Users\\agarrido\\GitRepos\\FabricDataEng\\DataIngestionFramework\\src'
# sys.path.insert(0, src_path)

import fabricdataingest.helloworld as hw
import fabricdataingest.eventhouse as evc
import fabricdataingest.utils as utils


class TestPackagename(unittest.TestCase):
    def test_print_hello(self,name="Microsoft"):
        # Call the function
        say_hello = hw.print_hello(name)
        # Assert the output
        self.assertEqual(say_hello, f"Hello {name}")

    def test_eventhouse_connector(self):
        kustoUri = "https://trd-jkycvhh5dttmmmh47b.z7.kusto.fabric.microsoft.com"
        database = "EventHouseDB"
        # Call the function
        ehc = evc.EventHouseConnector(kustoUri, database)
        # Assert the output
        self.assertEqual(ehc.kustoUri, kustoUri)
        self.assertEqual(ehc.database, database)

        id = "1"
        status = "InProgress"
        # Get the KQL Command
        kql_command = utils.buildAppendCommand(f'{id}', f"Table{id}_TestCase",f"{status}")
        response = ehc.execute_query(kql_command)
        self.assertEqual(response.errors_count, 0)

if __name__ == '__main__':
    # Create a test suite
    suite = unittest.TestSuite()
    # Add individual test cases to the suite
    suite.addTest(TestPackagename('test_print_hello'))
    # suite.addTest(TestPackagename('test_eventhouse_connector'))
    # Run the test suite
    runner = unittest.TextTestRunner()
    runner.run(suite)