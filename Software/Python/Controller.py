from threading import Thread
from Message import *
from robot_datas import *
import time
from udp_server import UDPServer
import FaBo9Axis_MPU9250
import time
import sys
import serial


class Controller(Thread):

    def __init__(self, server: UDPServer, serial_port: str, baud_rate: int):
        Thread.__init__(self)
        self.server = server
        self.is_running = False
        self.ser = serial.Serial(serial_port, baud_rate)
        self.serial_port = serial_port
        self.baud_rate = baud_rate
            
    def run(self):
        self.is_running = True
        while self.is_running :
            self.IMU()
            self.send_new_targets()
            #self.ask_motor_datas()
            
            
    def stop(self):
        self.is_running = False
        
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
            
    def send_new_targets(self):
        motor_targets_change = self.server.get_motor_targets_change()
        motor_id = self.server.get_motor_id()
        motor_targets = self.server.get_targets_data()
        
        for i in motor_targets_change : 
            if motor_targets_change[i] == True:
                id = str(motor_id[i])
                targets = str(motor_targets[i]+180)
                message = bytes(id + ':' + targets +';', "ASCII")
                self.ser.write(message)
                self.server.set_motor_change({i:False})
                time.sleep(0.009)
                
    def ask_motor_datas(self):
        nb_motors = len(self.server.get_targets_data())
        message = bytes('0' + ':' + str(nb_motors) +';', "ASCII")
        self.ser.write(message)
        time.sleep(0.004 * nb_motors + 0.005)
        msg = self.ser.readline().decode("ASCII")[:-1]
        print(self.decode_motor_data(msg))
                
            
    def decode_motor_data(self, msg: str) -> List[List[str]]:
        raw_data = msg.split("/")
        raw_data = raw_data[:]
        data = []
        for i in raw_data:
            data += [i.split(':')]
        return data
            
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

            imu_keys: List[str] = ["accelerationX", "accelerationY", "accelerationZ", 
            "rotationX", "rotationY", "rotationZ", "MagnX", "MagnY", "MagnZ"]
            
            for i in imu_keys:
                input_data[i] = 0
        
        self.server.set_imu_datas(input_data)
        
        
