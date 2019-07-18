from udp_server import *
from Controller import *
import time
from detect_USB import find_arduino
from subprocess import check_output

hotspot = False

with open("server_settings", "r") as content:
	server_settings = {}
	content = [i.split("=") for i in content.read().split("\n")]
	for i in content:
		server_settings[i[0]] = i[1]

while hotspot == False:
    
    wifi_ip = check_output(['hostname', '-I'])
    wifi_ip = wifi_ip.decode("utf-8")[:-2].split(" ")
    for i in wifi_ip:
        if i == server_settings["server_ip"]:
            hotspot = True
            

server = UDPServer(server_settings["server_ip"], int(server_settings["server_port"]), server_settings["server_password"])
server.start()

controller = Controller(server, find_arduino(), int(server_settings["baud_rate"]))
controller.start()

while True:
    time.sleep(0.5)

     
controller.stop()
server.stop()


