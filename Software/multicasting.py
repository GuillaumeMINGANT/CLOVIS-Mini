from udp_server import *
import time
bool = True
server = UDPServer("192.168.43.154", 50055, "test")
server.start()

for i in range(100):
    time.sleep(0.1)
