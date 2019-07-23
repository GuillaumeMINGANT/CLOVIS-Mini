from functools import reduce
import json
from typing import Union


class Message:

    def __init__(self, message_id: int, message: str) -> None:
        """
        Creat a new Message
        :param message_id:
        Id of the message
        :param message:
        Content of the message
        """
        self.parity_check = lambda msg: reduce(lambda x, y: int(x) ^ int(y),
                                               "".join([bin(msg[i])[2:] for i in range(len(msg))]), 0)
        self.id = message_id
        self.len = len(message)
        self.parity = self.parity_check(bytes(message, "utf8"))
        self.message = message
        self.content = dict()

    def create_from_json(msg: str):
        """
        Load a json file and store it in a message object
        :return:
        """
        json_dict = json.loads(msg)
        rcv_msg = Message(0, "")
        rcv_msg.import_json(json_dict)
        return rcv_msg

    def verif(self) -> bool:
        """
        Check if the message is corrupted
        :return:
        Bool (True if not corrupted, else False)
        """
        if self.parity_check(bytes(self.message, "utf8")) != self.parity:
            return False
        elif len(self.message) != self.len:
            return False
        else:
            return True

    def check_message(data_string: str):
        """
        Check if the received message can be transform in a Message object, if it is possible, return
        a Message containing the received data, if it failed it return an empty Message with ID = 0
        :return:
        A Message object
        """
        try:
            message = Message.create_from_json(data_string)
        except ValueError:
            return Message(0, "")
        if message.verif():
            return message
        else:
            return Message(0, "")

    def import_json(self, json_in):
        """
        If it is possible, load the data of a Json string into the Message object
        :param json_in:
        The Json to read
        :return:
        None
        """
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
        """
        Convert the message to a Json object
        :return:
        str : the Json object
        """
        return json.dumps(dict(self))
