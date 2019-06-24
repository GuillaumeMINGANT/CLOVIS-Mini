from udp_server import *
import time
from Controller import Controller
server = UDPServer("192.168.43.154", 50055, "test")
server.start()
motor = Controller(server)

#motor.test()
blabla = server.listener.robot.get_targets_data()
blabla["torsoRY"] = 10
print(server.listener.robot.get_targets_data()["torsoRY"])
