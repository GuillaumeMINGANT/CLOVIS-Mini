from __future__ import annotations
import socket
from threading import Thread
from typing import Optional
from Message import *
import hashlib


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

    class Listener(Thread):

        def __init__(self, ip: str, port: int, hash_pass: str) -> None:
            Thread.__init__(self)
            self.is_running: bool = False
            self.ip: str = ip
            self.port: int = port
            self.socket: socket.socket = socket.socket(socket.AF_INET,  # Internet
                                                       socket.SOCK_DGRAM)  # UDP
            self.hash_pass = hash_pass
            # A MODIFIER

            self.client_is_connected: bool = True
            self.client_ip: str = ""
            self.client_port: int = 0
            # ===========

            self.send_socket = socket.socket(socket.AF_INET,  # Internet
                                             socket.SOCK_DGRAM)

        def listen(self) -> None:
            """"Listen if there are messages arriving at the socket, determine the appropriate action and do it"""

            self.socket.bind((self.ip, self.port))
            while self.is_running:
                data, addr = self.socket.recvfrom(2048)  # buffer size is 1024 bytes

                 # DEBUG A ENLEVER PLUS TARD
                data_string = data.decode("utf-8")
                try:
                    message = Message.create_json(data_string)
                except ValueError:
                    print("Validation KO")
                    message = Message(0, "")
                if message.verif():
                    print("received message:", message.message)
                    if message.id == 1:
                        self.connection(message, addr)

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
            self.is_running = True
            self.listen()

        def stop(self) -> None:
            self.is_running = False

        def send(self, message: str, message_id: Optional[int] = 0):
            """"Send the data"""
            datas_to_send = Message(message_id, message)
            self.socket.sendto(bytes(str(datas_to_send), 'utf-8'), (self.client_ip, self.client_port))
