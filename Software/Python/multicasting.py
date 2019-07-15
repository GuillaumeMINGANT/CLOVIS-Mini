from udp_server import *
from Controller import *
import time


bool = True
server = UDPServer("192.168.50.1", 50055, "test")
server.start()

controller = Controller(server, '/dev/ttyUSB0', 115200)
controller.start()
count = 0
tst = 0
while count<200:
    time.sleep(0.5)
    count += 1
    #controller.send_new_targets()
   # controller.ask_motor_datas()
    #print(str(server.get_current_position_data()["rAnkleRZ"]) + ':' + str(server.get_motor_speed()["rAnkleRZ"]) + ':' + str(server.get_motor_torque()["rAnkleRZ"]))
    #print(tst) 
    tst += 1
     
controller.stop()
server.stop()


