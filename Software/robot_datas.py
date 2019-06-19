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

        # init targets
        self.targets: Dict[str, float] = {}
        for i in self.motor_keys:
            self.targets[i] = 0

        # init current_position
        self.current_position: Dict[str, float] = {}
        for i in self.motor_keys:
            self.current_position[i] = 0

        # init imu_datas
        self.imu_datas: Dict[str, float] = {}
        for i in self.imu_keys:
            self.imu_datas[i] = 0

        # init lidar_datas
        self.lidar_datas: List[Point] = []

    def __iter__(self):
        yield "current_position", self.current_position
        yield "imu_datas", self.imu_datas
        yield "lidar_datas", self.lidar_datas

    def __str__(self) -> str:
        return json.dumps(dict(self))
