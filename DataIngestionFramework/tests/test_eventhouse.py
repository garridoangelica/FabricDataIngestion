import unittest

import sys
import os
# Add the src directory to the sys.path
import fabricdataingest.helloworld as hw
import fabricdataingest.eventhouse as evc

class TestPackagename(unittest.TestCase):
    def test_print_hello(self,name="Angelica"):
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

if __name__ == '__main__':
    unittest.main()