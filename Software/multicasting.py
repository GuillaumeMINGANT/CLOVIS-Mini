from udp_server import *
import time

bool = True
server = UDPServer("127.0.0.1", 50055, "test")
server.start()

for i in range(100):
    time.sleep(0.1)
