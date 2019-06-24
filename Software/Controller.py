from threading import Thread
from Message import *
from robot_datas import *
import time
from udp_server import UDPServer


class Controller(Thread):

    def __init__(self, server: UDPServer):
        Thread.__init__(self)
        self.server = server

    def data_recovery(self):
        while True:
            #self.server.listener.robot.set_targets(self.robot.get_targets_data())
            time.sleep(0.1)

    def test(self):
        for i in range(100):
            print("*********************************************************************")
            print(self.server.listener.robot.targets)
            print("*********************************************************************")

            time.sleep(0.1)
