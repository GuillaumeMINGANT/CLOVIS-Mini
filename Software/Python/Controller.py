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
            self.ask_motor_datas()
            
            
    def stop(self):
        self.is_running = False
        
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
        motor_id = self.server.get_motor_id()
        
        nb_motors = len(self.server.get_targets_data())
        message = bytes('0' + ':' + str(nb_motors) +';', "ASCII")
        self.ser.write(message)
        time.sleep(0.002 * nb_motors + 0.005)
        
        try:
            msg = self.ser.readline().decode("ASCII")[:-2]
            data = self.decode_motor_data(msg)
            if len(data) != nb_motors:
                self.ask_motor_datas()
            else:
                new_values = {}
                new_torque = {}
                for i in data:
                    
                    if len(i) == 3:
                        motor_name = list(motor_id.keys())[list(motor_id.values()).index(int(i[0]))]
                        new_values[motor_name] = int(i[1]) - 180
                        new_torque[motor_name] = int(i[2]) if int(i[2]) <= 100 else - (int(i[2]) - 100)
                self.server.set_motor_torque(new_torque)
                self.server.set_current_position(new_values)
            
        except ValueError:
            self.ask_motor_datas()
            print("ERRORRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR")
                        
            
    def decode_motor_data(self, msg: str) -> List[List[str]]:
        raw_data = msg.split("/")
        raw_data = raw_data[:22]
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
        
        
