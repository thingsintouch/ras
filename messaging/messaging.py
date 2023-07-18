#import time
import zmq
#import itertools
import pickle

from common.logger import loggerINFO, loggerCRITICAL, loggerDEBUG


class SubscriberMultipart():
    def __init__(self,port):
        self.context = zmq.Context()  
        self.socket = self.context.socket(zmq.SUB)
        self.socket.setsockopt(zmq.RCVTIMEO, 1000) # Set timeout to 1 second
        self.socket.connect(f"tcp://localhost:{port}")
        self.port=port

    def subscribe(self, topic):
        loggerDEBUG(f"SUBSCRIPTION TO TOPIC: {topic}")
        self.socket.setsockopt(zmq.SUBSCRIBE, str(topic).encode('utf-8'))

    def receive(self):
        #loggerDEBUG("POINT 2 ############  before the BLOCKING self.socket.recv_multipart() ")
        try:
            topic_bytes, message_bytes = self.socket.recv_multipart() # this call is blocking
            #loggerDEBUG("POINT 3 ############  AFTER the BLOCKING -- no exception -- self.socket.recv_multipart() ")
            topic = topic_bytes.decode('utf-8')
            message = pickle.loads(message_bytes)
            loggerDEBUG(f"POINT 4 ##########  received TOPIC: {topic}, MESSAGE: {message}")
            return topic, message
        except Exception as e:
            #loggerDEBUG(f"POINT 3 and 4 -- EXCEPTION  - probably timeout - exception message: {e} ")
            return "error", ""

class PublisherMultipart():
    def __init__(self,port):
        self.context = zmq.Context()  
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(f"tcp://*:{port}")
        self.port=port

    def publish(self, topic, message):
        # loggerDEBUG(f"published TOPIC: {topic}, MESSAGE: {message}")
        topic_bytes = str(topic).encode('utf-8')
        message_bytes = pickle.dumps(message)
        self.socket.send_multipart([topic_bytes, message_bytes])
