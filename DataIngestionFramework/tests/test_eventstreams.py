import unittest
import sys
import os
from azure.eventhub.exceptions import AuthenticationError

import fabricdataingest.helloworld as hw
import fabricdataingest.eventstreams as es
import fabricdataingest.utils as utils


class TestEventStreams(unittest.TestCase):
    def test_print_hello(self, name="Microsoft"):
        print("Print Hello World Test Case")
        # Call the function
        say_hello = hw.print_hello(name)
        # Assert the output
        self.assertEqual(say_hello, f"Hello {name}")
    
    def test_send_event_authentication_error(self):
        print("Testing EventStreams Authentication Error")
        # Use an invalid connection string to simulate an authentication error
        invalid_connection_string = "InvalidConnectionString"
        event_streams_conn = es.EventStreamsConn(invalid_connection_string)

        message = {"key": "value"}
        with self.assertRaises(ValueError) as context:
            event_streams_conn.send_event(message)
        
        self.assertIn("Connection string is either blank or malformed", str(context.exception))
        print("Caught ValueError as expected.")

    def test_eventstreams_connector(self):
        print("EventStreams Connector Test Case")
        # Set up the environment variables for EventStreams connection
        eventstreamsUri = os.getenv('SPARKEVENTSTREAMS_CONN')
        # Call the function
        events_conn = es.EventStreamsConn(eventstreamsUri)
        self.assertIsNotNone(events_conn, "Failed to create EventStreams connection.")

        status_ls = ['InProgress','Completed']
        for st in status_ls:
            for id in range(1,3):
                ms = utils.buildMessage(id, st)
                result = events_conn.send_event(ms)
                self.assertTrue(result, f"Failed to send event: {ms}")

if __name__ == '__main__':
    # Create a test suite
    suite = unittest.TestSuite()
    # Add individual test cases to the suite
    # Hello World Test Case for testing calling test cases
    suite.addTest(TestEventStreams('test_print_hello'))
    # EventStreams Connector Test Case failed with authentication error
    suite.addTest(TestEventStreams('test_send_event_authentication_error'))
    # EventStreams Connector Test Case
    suite.addTest(TestEventStreams('test_eventstreams_connector'))
    # Run the test suite
    runner = unittest.TextTestRunner()
    runner.run(suite)