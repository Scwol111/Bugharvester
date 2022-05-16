import socketserver

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        print(data)