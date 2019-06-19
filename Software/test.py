from robot_datas import *
from Message import *
import json
import ast
import hashlib
import getpass
"""
msg = str(Message(1, '{"a" : 12, "b":"coucou"}'))

parity_check = lambda msg: reduce(lambda x, y: int(x) ^ int(y),
                                  "".join([bin(msg[i])[2:] for i in range(len(msg))]), 0)

dico = json.loads(msg)

rcv_msg = Message(0, "")
rcv_msg = Message.create_json(msg)
print(rcv_msg.verif())
print(type(rcv_msg))



new_dico = json.dumps(rcv_msg.message)
new_dico.replace("\\",'')
d = json.loads(new_dico)
d = json.loads(d)
"""
msg = Message(1, '{"a" : 12, "b":"coucou"}')
# new = Message.create_json(msg)
# print(type(new.content))
# print(new.content["a"])
print(msg)
print(msg.content)
msg.create_json(msg)
print(msg)
print(msg.content)
