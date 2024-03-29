from typing import List, Dict
from Point import *
import json


class RobotDatas:

    def __init__(self) -> None:
        self.motor_keys: List[str] = ["rAnkleRX", "lAnkleRX", "rAnkleRZ", "lAnkleRZ", "rShoulderRY", "lShoulderBaseRY",
                                      "rShoulderBaseRY", "lShoulderRY", "rShoulderRZ", "lShoulderRZ", "rKneeRX",
                                      "lKneeRX",
                                      "rHipRX", "lHipRX", "rHipRY", "lHipRY", "rHipRZ", "lHipRZ", "headRX", "rElbowRX",
                                      "lElbowRX",
                                      "torsoRY"]

        self.imu_keys: List[str] = ["accelerationX", "accelerationY", "accelerationZ", "rotationX", "rotationY",
                                    "rotationZ", "MagnX", "MagnY", "MagnZ"]

        # init targets  -- Consignes
        self.targets: Dict[str, float] = {}
        for i in self.motor_keys:
            self.targets[i] = 0

        # init current_position  -- Angles
        self.current_position: Dict[str, float] = {}
        for i in self.motor_keys:
            self.current_position[i] = 0

        # init imu_datas  --  Données IMU
        self.imu_data: Dict[str, float] = {}
        for i in self.imu_keys:
            self.imu_data[i] = 0

        # init lidar_data
        self.lidar_data: List[Point] = []

        # init angle_settings
        self.angle_settings: Dict[str, List[int, int]] = {}
        for i in self.motor_keys:
            self.angle_settings[i] = [0, 0]
            
        id: int = 2
        self.motor_id : Dict[str, int] = {}
        for i in self.motor_keys:
                self.motor_id[i] = id
                id += 1
        
        self.motor_targets_change : Dict[str, bool] = {}
        for i in self.motor_keys:
             self.motor_targets_change[i] = True
             
        self.motor_torque : Dict[str, int] = {}
        for i in self.motor_keys:
             self.motor_torque[i] = 0
             
        self.motor_speed : Dict[str, float] = {}
        for i in self.motor_keys:
             self.motor_speed[i] = 0
        
        self.init_motor_id()
        self.init_angle_settings()

    def __iter__(self):
        yield "current_position", self.current_position
        yield "motor_speed", self.motor_speed
        yield "motor_torque", self.motor_torque
        yield "imu_datas", self.imu_data
        yield "lidar_datas", self.lidar_data

    def __str__(self) -> str:
        return json.dumps(dict(self))

    def init_angle_settings(self):
        with open("motors_settings", "r") as content:
                motors_settings = {}
                content = [i.split("=") for i in content.read().split("\n")]
                for i in content:
                        if(len(i) == 2):
                                motors_settings[i[0]] = i[1].split(",")
                                for j, e in enumerate(motors_settings[i[0]]):
                                        motors_settings[i[0]][j] = int(e)
        
        for i in motors_settings:
                self.angle_settings[i] = motors_settings[i]
        

    def init_motor_id(self):
        with open("motors_id", "r") as content:
                content = [i.split("=") for i in content.read().split("\n")]
                for i in content:
                        if(len(i) == 2):
                                self.motor_id[i[0]] = int(i[1])
        

    def set_targets(self, input_target: Dict[str, float]):
        for i in input_target:
            if i in self.motor_keys:
                if input_target[i] > self.angle_settings[i][1]:
                    prev_val = self.targets[i]
                    self.targets[i] = self.angle_settings[i][1]
                    
                elif input_target[i] < self.angle_settings[i][0]:
                    prev_val = self.targets[i]
                    self.targets[i] = self.angle_settings[i][1]
                    
                else:
                    prev_val = self.targets[i]
                    self.targets[i] = input_target[i]
                if prev_val != self.targets[i]:
                    self.motor_targets_change[i] = True
                
    def set_motor_id(self, input_id: Dict[str, int]):
        for i in input_id:
            if i in self.motor_keys:
                self.motor_id[i] = input_id[i]
   
    def set_motor_change(self, input_change: Dict[str, bool]):
        for i in input_change:
            if i in self.motor_keys:
                self.motor_targets_change[i] = input_change[i] 
                
    def set_current_position_data(self, input_position: Dict[str, float]):
        for i in input_position:
            if i in self.motor_keys:
                self.current_position[i] = input_position[i]

    def set_imu_datas(self, input_data: Dict[str, float]):
        for i in input_data:
            if i in self.imu_keys:
                self.imu_data[i] = input_data[i]
                
    def set_motor_torque(self, input_torque: Dict[str, int]) -> None:
            for i in input_torque:
                    if i in self.motor_keys:
                        self.motor_torque[i] = input_torque[i]
                        
    def set_motor_speed(self, input_speed: Dict[str, int]) -> None:
            for i in input_speed:
                    if i in self.motor_keys:
                        self.motor_speed[i] = input_speed[i]
        

    def set_lidar_data(self, input_lidar: List[Point]):
        self.lidar_data = input_lidar
        
    def get_motor_torque(self):
            return self.motor_torque.copy()
        
    def get_motor_speed(self):
            return self.motor_speed.copy()
        
    def get_targets_data(self):
        return self.targets.copy()

    def get_current_position_data(self):
        return self.current_position.copy()

    def get_imu_data(self):
        return self.imu_data.copy()

    def get_lidar_data(self):
        return self.lidar_data.copy()

    def get_angle_settings_data(self):
        return self.angle_settings.copy()
        
    def get_motor_id(self):
        return self.motor_id.copy()
   
    def get_motor_targets_change(self):
        return self.motor_targets_change.copy()

    def copy(self):
        robot_copy = RobotDatas()
        robot_copy.angle_settings = self.angle_settings.copy()
        robot_copy.lidar_data = self.lidar_data.copy()
        robot_copy.imu_data = self.imu_data.copy()
        robot_copy.current_position = self.current_position.copy()
        robot_copy.targets = self.targets.copy()
        robot_copy.motor_id = self.motor_id.copy()
        robot_copy.motor_targets_change = self.motor_targets_change.copy()
        robot_copy.motor_torque = self.motor_torque.copy()
        robot_copy.motor_speed = self.motor_speed.copy()
        return robot_copy
