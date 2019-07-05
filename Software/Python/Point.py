import json

class Point:

    def __init__(self, angle: float, distance: float):
        self.angle: float = angle
        self.distance: float = distance

    def __iter__(self):
        yield "angle", self.angle
        yield "distance", self.distance

    def __str__(self) -> str:
        return json.dumps(dict(self))
