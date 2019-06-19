from typing import List, Dict
from Point import *
import json


class RobotDatas:

    def __init__(self) -> None:
        self.motor_keys: List[str] = ["rAnkleRX", "lAnkleRX", "rAnkleRZ", "lAnkelRZ", "rShoulderRY", "lShoulderBaseRY",
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
        self.imu_datas: Dict[str, float] = {}
        for i in self.imu_keys:
            self.imu_datas[i] = 0

        # init lidar_datas
        self.lidar_datas: List[Point] = []

        # init angle_settings
        self.angle_settings: Dict[str, List[int, int]] = {}
        for i in self.motor_keys:
            self.angle_settings[i] = [0, 0]

        self.init_angle_settings()

    def __iter__(self):
        yield "current_position", self.current_position
        yield "imu_datas", self.imu_datas
        yield "lidar_datas", self.lidar_datas

    def __str__(self) -> str:
        return json.dumps(dict(self))

    def init_angle_settings(self):
        self.angle_settings["rAnkleRX"] = [-30, 30]
        self.angle_settings["lAnkleRX"] = [-30, 30]
        self.angle_settings["rAnkleRZ"] = [-30, 30]
        self.angle_settings["lAnkelRZ"] = [-30, 30]
        self.angle_settings["rShoulderRY"] = [-90, 0]
        self.angle_settings["lShoulderBaseRY"] = [-30, 30]
        self.angle_settings["rShoulderBaseRY"] = [-30, 30]
        self.angle_settings["lShoulderRY"] = [0, 90]
        self.angle_settings["rShoulderRZ"] = [-90, 90]
        self.angle_settings["lShoulderRZ"] = [-90, 90]
        self.angle_settings["rKneeRX"] = [-60, 0]
        self.angle_settings["lKneeRX"] = [-0, 60]
        self.angle_settings["rHipRX"] = [-90, 30]
        self.angle_settings["lHipRX"] = [-30, 90]
        self.angle_settings["rHipRY"] = [0, 90]
        self.angle_settings["lHipRY"] = [-90, 0]
        self.angle_settings["rHipRZ"] = [-20, 90]
        self.angle_settings["lHipRZ"] = [-90, 20]
        self.angle_settings["headRX"] = [-20, 20]
        self.angle_settings["rElbowRX"] = [0, 90]
        self.angle_settings["lElbowRX"] = [-90, 0]
        self.angle_settings["torsoRY"] = [-90, 90]

    def set_targets(self, input_target: Dict[str, float]):
        for i in input_target:
            if i in self.motor_keys:
                if input_target[i] > self.angle_settings[i][1]:
                    self.targets[i] = self.angle_settings[i][1]
                elif input_target[i] < self.angle_settings[i][0]:
                    self.targets[i] = self.angle_settings[i][1]
                else:
                    self.targets[i] = input_target[i]
