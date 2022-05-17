from socketserver import BaseRequestHandler
import time

class ThreadedTCPRequestHandler(BaseRequestHandler):

    def recvAllData(self, timeout=2):
        self.request.setblocking(0)
        total_data=list()
        data=''
        begin=time.time()
        while 1:
            if total_data and time.time() - begin > timeout:
                break
            elif time.time() - begin > timeout * 2:
                break
            try:
                data = self.request.recv(1024).decode("utf-8")
                if data:
                    total_data.append(data)
                    begin = time.time()
                else:
                    time.sleep(0.1)
            except:
                pass
        return ''.join(total_data)

    def handle(self):
        data = self.recvAllData()
        print(data)
        print(len(data))