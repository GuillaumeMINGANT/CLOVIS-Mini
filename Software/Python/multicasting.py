from udp_server import *
from Controller import *
import time


bool = True
server = UDPServer("192.168.50.1", 50055, "test")
server.start()

controller = Controller(server, '/dev/ttyUSB0', 115200)
controller.start()
count = 0

while count<30:
    time.sleep(1)
    count += 1
controller.stop()
server.stop()
