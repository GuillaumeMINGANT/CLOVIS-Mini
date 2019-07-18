from udp_server import *
from Controller import *
import time
from detect_USB import find_arduino
from subprocess import check_output


hotspot = False
while hotspot == False:
    
    wifi_ip = check_output(['hostname', '-I'])
    wifi_ip = wifi_ip.decode("utf-8")[:-2].split(" ")
    for i in wifi_ip:
        if i == '192.168.50.1':
            hotspot = True
            

server = UDPServer("192.168.50.1", 50055, "test")
server.start()

controller = Controller(server, find_arduino(), 115200)
controller.start()

count = 0
tst = 0
while count<2000:
    time.sleep(0.5)
    count += 1
    #controller.send_new_targets()
    # controller.ask_motor_datas()
    #print(str(server.get_current_position_data()["rAnkleRZ"]) + ':' + str(server.get_motor_speed()["rAnkleRZ"]) + ':' + str(server.get_motor_torque()["rAnkleRZ"]))
    #print(tst) 
    tst += 1
     
controller.stop()
server.stop()


