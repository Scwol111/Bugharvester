from observerConfig import ObserverConfig
import socket
import os

def main():
    cfg = ObserverConfig(os.getenv("BUGHARVESTER_FOLDER") + "/bugHarvester-observer.cfg")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((cfg.worker["host"], cfg.worker["port"]))
        s.sendall(b"Hello, world")
        data = s.recv(1024)
        print(data.decode("utf-8"))

if (__name__ == "__main__"):
    main()