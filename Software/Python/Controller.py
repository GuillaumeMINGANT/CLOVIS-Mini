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
        self.buff = []
        self.last_send = time.time()
        
            
    def run(self):
        self.is_running = True
        while self.is_running :
            start = time.time()
            self.IMU()
            self.send_new_targets()
            self.ask_motor_datas()
            print(time.time() - start)
            
            
    def stop(self):
        self.is_running = False
        
    def pos_to_bytes(pos :int) -> [int, int]:
        lsb = pos % 256
        msb = (pos - lsb) // 256
        return [msb,lsb]
    
    def send_new_targets(self):
        motor_targets_change = self.server.get_motor_targets_change()
        motor_id = self.server.get_motor_id()
        motor_targets = self.server.get_targets_data()
        
        message = [255, 255, 255]
        for i in motor_targets_change : 
            if motor_targets_change[i] == True:
                message += [motor_id[i]] + Controller.pos_to_bytes(int((motor_targets[i] + 180) * 2.84))
                self.server.set_motor_change({i:False}) 
        message += [254, 254, 254]
        if len(message) > 6:
            self.ser.write(message)
                   
                            
    def ask_motor_datas(self):
        motor_id = self.server.get_motor_id()
        nb_motors = len(motor_id)
        msg = [255, 255, 255, nb_motors, 254, 254, 254]
        self.ser.write(msg)
        time.sleep(0.005 * nb_motors)
        
        try:
            
            while self.ser.in_waiting != 0: 
                caract = int.from_bytes(self.ser.read(), byteorder='big')           
                self.buff += [caract]
                if len(self.buff) == 3:
                    if self.buff[0] != 255 and self.buff[1] != 255 and self.buff[2] != 255 :
                        self.buff = []
                elif len(self.buff) > 6:
                    if self.buff[len(self.buff) -1] == 254 and self.buff[len(self.buff) - 2] == 254 and self.buff[len(self.buff) - 3] == 254 :
                        raw_data = self.buff[3:-3]
                        self.buff = []
                        if len(raw_data)/nb_motors == 7:                            
                            for i in range(nb_motors):
                                name = list(motor_id.keys())[list(motor_id.values()).index(raw_data[i*7])]
                                self.server.set_current_position({name : int((((raw_data[(i*7) + 1] * 256) + raw_data[(i*7) + 2]) / 2.84) - 180)})
                                speed = (raw_data[(i*7) + 3] * 256) + raw_data[(i*7) + 4]
                                self.server.set_motor_speed({name : - (int(speed * (100/1024))) if speed <= 1023 else int((speed - 1023 ) * (100/1024)) })
                                torque = (raw_data[(i*7) + 5] * 256) + raw_data[(i*7) + 6]
                                self.server.set_motor_torque({name : - (int(torque * (100/1024))) if torque <= 1023 else int((torque - 1023 ) * (100/1024))})
        
        except:
            self.ask_motor_datas()
                        
        
            
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
        
        
