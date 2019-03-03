from server_comms import ServerComms
import threading
import time

class ApiRunner:
    def __init__(self):
        self.server = ServerComms("127.0.0.1", 8052)
        self.has_ended = False
        self.lock = threading.Lock()
        self.receive_thread = threading.Thread(target=self.read)
        self.receive_thread.start()

    def read(self):
        while not self.has_ended:
            message = self.server.read_message()
            print(message)
            # do something
    
    def send(self, type, payload):
        self.server.send_message(type, payload)