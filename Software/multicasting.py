from udp_server import *
import time
bool = True
server = UDPServer("192.168.43.154", 50055, "test")
server.start()
while True:
    print(server.get_robot_data().targets)
    time.sleep(0.1)
