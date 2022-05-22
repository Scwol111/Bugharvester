import threading
from threadedtcprequesthandler import ThreadedTCPRequestHandler
from socketserver import ThreadingTCPServer

class Queue:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server = ThreadingTCPServer((ip, port), ThreadedTCPRequestHandler)
        self.server.queue = self
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.messages = []

    def start_server(self):
        self.server_thread.start()
        print("Server running on", str(self.ip) + ":" + str(self.port))

    def stop_server(self):
        self.server.shutdown()
        self.server.server_close()

    def add(self, message):
        self.messages.append(message)

    def view(self):
        return self.messages

    def get(self):
        return self.messages.pop()

    def exists(self):
        return len(self.messages)