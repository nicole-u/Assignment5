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
        new_msgs = []
        # must return a list of DirectMessage objects containing all new messages
        return new_msgs

    def retrieve_all(self) -> list:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((self.dsuserver, 3021))

                message = {"token": self.token, "directmessage": "all"}

                sendfile = client_socket.makefile('w')
                recv = client_socket.makefile('r')
                sendfile.write(json.dumps(message) + "\r\n")
                sendfile.flush()
                # server_resp = json.loads(recv.readline())
                # client_socket.sendall(json.dumps(message).encode())
                server_response = client_socket.recv(1024).decode('utf-8')
                response = json.loads(server_response)
                if response['response']['type'] == 'ok':
                    all_messages = response['response']['messages']
                    return all_messages
                else:
                    print(f"Error: {response['response']['message']}")
                    return []
        except Exception as e:
            print(f"Error retrieving all messages: {e}")
            return []

if __name__ == "__main__":
    dm_time = DirectMessenger("168.235.86.101", "strawberry", "banana")
    print("Class instantiated")
    dm_time.send("Hello world", "ohhimark")
    all_msgs = dm_time.retrieve_all()
    print(all_msgs)
