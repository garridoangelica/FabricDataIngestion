import logging
from datetime import datetime
from azure.eventhub import EventHubProducerClient, EventData
import json
import fabricdataingest.utils as utils
import os

class EventStreamsConn:
    """
    Class to initiate and send json to Event Streams
    Initial Params:
        Connection String: connection string of Event Streams
    """
    def __init__(self, connection_str,_log=logging.INFO):
        self.logger = logging.getLogger(__name__)
        self.connection_str = connection_str
        self.producer = None

    def _create_producer(self):
        try:
            # Create a producer client to send messages to the event hub
            self.logger.info("Creating Event Hub Producer Client")
            producer= EventHubProducerClient.from_connection_string(conn_str=self.connection_str)
            return producer
        except ValueError as e:
            self.logger.error(f"Unexpected error: {e}")
            raise

    def _close_producer(self):
        # Close the producer
        self.producer.close()
        self.producer = None
    
    def send_event(self, message):
        try: 
            if self.producer == None:
                self.producer = self._create_producer()
            # Create a batch
            event_data_batch = self.producer.create_batch()
            # Add the JSON message to the batch
            event_data_batch.add(EventData(json.dumps(message)))
            # Send the batch of events to the event hub
            self.producer.send_batch(event_data_batch)
            # self._close_producer()
            return True
        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")
            raise