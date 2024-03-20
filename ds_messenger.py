import socket
import json
import time
from pathlib import Path
import ds_protocol as dsp
from Profile import *

profile = Profile()

class DirectMessage:
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None


class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.port = 3021

    def send(self, message:str, recipient:str) -> bool:
        try:
            dm_attempt = dsp.directmessage(message, recipient, self.dsuserver, self.username, self.password)
            print(dm_attempt[0])
            self.token = dm_attempt[1]
        except:
            print("Error with sending direct message.")
            return False

    def retrieve_new(self) -> list:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((self.dsuserver, 3021))

                message = {"token": self.token, "directmessage": "new"}

                sendfile = client_socket.makefile('w')
                sendfile.write(json.dumps(message) + "\r\n")
                sendfile.flush()

                server_response = client_socket.recv(1024).decode('utf-8')
                response = json.loads(server_response)
                if response['response']['type'] == 'ok':
                    all_messages = response['response']['messages']
                    return all_messages
                else:
                    print(f"Error: {response['response']['message']}")
                    return []
        except:
            print(f"Error retrieving all messages.")
            return []

    def retrieve_all(self) -> list:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((self.dsuserver, 3021))

                message = {"token": self.token, "directmessage": "all"}

                sendfile = client_socket.makefile('w')
                sendfile.write(json.dumps(message) + "\r\n")
                sendfile.flush()

                server_response = client_socket.recv(1024).decode('utf-8')
                response = json.loads(server_response)
                if response['response']['type'] == 'ok':
                    all_messages = response['response']['messages']
                    return all_messages
                else:
                    print(f"Error: {response['response']['message']}")
                    return []
        except:
            print(f"Error retrieving all messages.")
            return []

if __name__ == "__main__":
    dm_time1 = DirectMessenger("168.235.86.101", "teatime", "iceecream")
    print("Class instantiated")
    dm_time1.send("whoopee", "strawberry")
    all_msgs = dm_time1.retrieve_all()
    print(all_msgs)
    new_msgs = dm_time1.retrieve_new()
    print(new_msgs)

    dm_time2 = DirectMessenger("168.235.86.101", "strawberry", "banana")
    print("Class instantiated")
    dm_time2.send("yippee", "teatime")
    all_msgs = dm_time2.retrieve_all()
    print(all_msgs)
    new_msgs = dm_time2.retrieve_new()
    print(new_msgs)
