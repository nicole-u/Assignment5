import socket
import json
import time
from pathlib import Path
import ds_protocol as dsp
import ds_client as dsc
from Profile import *

profile = Profile()


class DirectMessage:
    """
    Class that a Direct Message is instantiated with.
    """
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None


class DirectMessenger:
    """
    The messenger.
    """
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.port = 3021

    def send(self, message: str, recipient: str) -> bool:
        """
        Function to send
        """
        dm_attempt = dsp.directmessage(message, recipient, self.dsuserver, self.username, self.password)
        try:
            if type(dm_attempt) is not None:
                print(dm_attempt[0])
                self.token = dm_attempt[1]
                return True
        except TypeError:
            print("Error with sending direct message through messenger.")
            return False

    def retrieve_new(self) -> list:
        """
        Function to retrieve new messages
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((self.dsuserver, 3021))
                join_msg = dsc.join(client_socket, self.username, self.password)
                self.token = join_msg[2]
                message = {"token": self.token, "directmessage": "new"}

                sendfile = client_socket.makefile('w')
                recv = client_socket.makefile('r')
                sendfile.write(json.dumps(message) + "\r\n")
                sendfile.flush()

                server_response = recv.readline()
                response = json.loads(server_response)
                if response["response"]["type"] == 'ok':
                    all_messages = response["response"]["messages"]
                    msg_list = []
                    i = 0
                    for msg in all_messages:
                        new_msg = DirectMessage()
                        new_msg.message = all_messages[i]["message"]
                        new_msg.recipient = all_messages[i]["from"]
                        new_msg.timestamp = all_messages[i]["timestamp"]
                        i += 1
                        msg_list.append(new_msg)
                    return msg_list
        except:
            print("Error retrieving the new messages.")
            return []

    def retrieve_all(self) -> list:
        """
        Function to retrieve all messages
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((self.dsuserver, 3021))
                join_msg = dsc.join(client_socket, self.username, self.password)
                self.token = join_msg[2]
                message = {"token": self.token, "directmessage": "all"}

                sendfile = client_socket.makefile('w')
                recv = client_socket.makefile('r')
                sendfile.write(json.dumps(message) + "\r\n")
                sendfile.flush()
                response = recv.readline()
                server_response = json.loads(response)

                if server_response["response"]["type"] == 'ok':
                    all_messages = server_response["response"]["messages"]
                    msg_list = []
                    i = 0
                    for msg in all_messages:
                        new_msg = DirectMessage()
                        new_msg.message = all_messages[i]["message"]
                        new_msg.recipient = all_messages[i]["from"]
                        new_msg.timestamp = all_messages[i]["timestamp"]
                        i += 1
                        msg_list.append(new_msg)
                    return msg_list
                else:
                    print(f"Error: {server_response['response']['message']}")
                    return []
        except:
            print("Error retrieving all messages.")
            return []
