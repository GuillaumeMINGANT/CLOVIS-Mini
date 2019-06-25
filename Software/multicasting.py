from udp_server import *
from Controller import *
import time
bool = True
server = UDPServer("192.168.4.9", 50055, "test")
server.start()
controller = Controller(server)
while True:
    print(server.get_imu_datas())
    controller.IMU()
    time.sleep(0.1)
