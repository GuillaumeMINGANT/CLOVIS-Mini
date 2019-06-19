from functools import reduce
import json
from typing import Union


class Message:

    def __init__(self, message_id: int, message: str) -> None:
        self.parity_check = lambda msg: reduce(lambda x, y: int(x) ^ int(y),
                                               "".join([bin(msg[i])[2:] for i in range(len(msg))]), 0)
        self.id = message_id
        self.len = len(message)
        self.parity = self.parity_check(bytes(message, "utf8"))
        self.message = message
        self.content = dict()

    def create_json(msg: str):
        json_dict = json.loads(msg)
        rcv_msg = Message(0, "")
        rcv_msg.import_json(json_dict)
        return rcv_msg

    def verif(self) -> bool:
        if self.parity_check(bytes(self.message, "utf8")) != self.parity:
            print("Fatal Error: parity")
            return False
        elif len(self.message) != self.len:
            print("Fatal Error : length")
            return False
        else:
            return True

    def import_json(self, json_in):
        if "id" in json_in and "parity" in json_in and "len" in json_in and "message" in json_in:
            self.id = json_in["id"]
            self.parity = json_in["parity"]
            self.len = json_in["len"]
            self.message = json_in["message"]
            self.content = json.loads(self.message)

    def __iter__(self) -> Union[int, str]:
        yield "id", self.id
        yield "parity", self.parity
        yield "len", self.len
        yield "message", self.message

    def __str__(self) -> str:
        return json.dumps(dict(self))
