from threading import Thread
from Message import *
from robot_datas import *
import time
from udp_server import UDPServer
import FaBo9Axis_MPU9250
import time
import sys


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
            self.IMU()
            print("*********************************************************************")

            time.sleep(0.1)
            
    def IMU(self):
        input_data: Dict[str, float] = {}
        
        try:
            
            mpu9250 = FaBo9Axis_MPU9250.MPU9250()
                
            accel = mpu9250.readAccel()
            input_data["accelerationX"] = accel['x']
            input_data["accelerationY"] = accel['y']
            input_data["accelerationZ"] = accel['z'] 

            gyro = mpu9250.readGyro()
            input_data["rotationX"] = gyro['x']
            input_data["rotationY"] = gyro['y'] 
            input_data["rotationZ"] = gyro['z'] 

            mag = mpu9250.readMagnet()
            input_data["MagnX"] = mag['x']
            input_data["MagnY"] = mag['y']
            input_data["MagnZ"] = mag['z']
            
        except BaseException:
            #OSError: 121 / IOError() ffi.errno

            imu_keys: List[str] = ["accelerationX", "accelerationY", "accelerationZ", "rotationX", "rotationY", "rotationZ", "MagnX", "MagnY", "MagnZ"]
            for i in imu_keys:
                input_data[i] = 0
        
        self.server.set_imu_datas(input_data)
        
        
