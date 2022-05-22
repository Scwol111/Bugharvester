from serverqueue import Queue
import time
import socket
import signal

class Server:
    def __init__(self, ip, port):
        self.queue = Queue(ip, port)
        self.shutdown_flag = False
        signal.signal(signal.SIGINT, self.shutdown)

    def start_server(self):
        self.queue.start_server()

    def stop_server(self):
        self.queue.stop_server()

    def run(self):
        self.start_server()
        while not self.shutdown_flag:
            time.sleep(1)
            while self.queue.exists():
                self.handle(self.queue.get())

    def shutdown(self, *args):
        self.shutdown_flag = True

    def handle(self, message):
        """    Prototype    """
        pass

    def send(self, ip, port, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        try:
            sock.sendall(bytes(message, 'ascii'))
        finally:
            sock.close()
