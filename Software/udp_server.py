from __future__ import annotations
import socket
from threading import Thread
from typing import Optional
from Message import *
import hashlib
from robot_datas import *


class UDPServer:

    def __init__(self, ip: str, port: int, password: Optional[str] = "") -> None:
        self.ip: str = ip
        self.port: int = port
        self.hash_pass = hashlib.sha1(bytes(password, "utf8")).hexdigest()
        self.listener = self.Listener(self.ip, self.port, self.hash_pass)

    def start(self) -> None:
        self.listener.start()

    def stop(self) -> None:
        self.listener.stop()

    def send(self, message: str, message_id: Optional[int] = 0):
        # if message_id == 1:

        self.listener.send(message, message_id)

    def get_robot_data(self):
        return self.listener.robot

    class Listener(Thread):

        def __init__(self, ip: str, port: int, hash_pass: str) -> None:
            Thread.__init__(self)
            self.is_running: bool = False
            self.ip: str = ip
            self.port: int = port
            self.socket: socket.socket = socket.socket(socket.AF_INET,  # Internet
                                                       socket.SOCK_DGRAM)  # UDP
            self.hash_pass = hash_pass
            self.robot = RobotDatas()

            self.client_is_connected: bool = True
            self.client_ip: str = ""
            self.client_port: int = 0

            self.send_socket = socket.socket(socket.AF_INET,  # Internet
                                             socket.SOCK_DGRAM)

        def listen(self) -> None:
            """
            Infinite loop for the server
            :return:
            None
            """
            self.socket.bind((self.ip, self.port))
            while self.is_running:
                data, addr = self.socket.recvfrom(2048)  # buffer size is 1024 bytes

                # DEBUG A ENLEVER PLUS TARD
                data_string = data.decode("utf-8")

                message = Message.check_message(data_string)
                if message.id == 1:
                    self.connection(message, addr)
                if message.id == 3:
                    self.send(str(self.robot), 4)
                if message.id == 5:
                    self.robot.set_targets(message.content)
                    self.send('{ "answer" : 1 }', 6)

        def verif_pass(self, pass_to_verif: str) -> bool:
            """"Verify if the password entered by client is the one of the server"""

            if self.hash_pass == pass_to_verif:
                print("Password accepted")
                return True
            else:
                print("Fatal Error : password error")
                return False

        def connection(self, message: Message, addr):
            """"If the password is correct, send the right message to finalise the connection with client"""

            if "pass" in message.content:
                if message.content["pass"] == self.hash_pass:
                    self.client_port = addr[1]
                    self.client_ip = addr[0]
                    self.send('{"answer" : "CONNECTED"}', 2)
                else:
                    print(addr)

        def run(self) -> None:
            """
            Start the listener
            :return:
            """
            self.is_running = True
            self.listen()

        def stop(self) -> None:
            """
            Stop the listener
            :return:
            """
            self.is_running = False

        def send(self, message: object, message_id: object = 0) -> object:
            """
            Send a message to the client
            :param message:
            The string to send
            :param message_id:
            The id of the message (default = 0)
            :return:
            None
            """
            datas_to_send = Message(message_id, message)
            self.socket.sendto(bytes(str(datas_to_send), 'utf-8'), (self.client_ip, self.client_port))
