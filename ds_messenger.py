import socket
import json
import time
from pathlib import Path
import ds_client as dsc
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
	
  def _join_server(self, client_socket: socket):
      sendfile = client_socket.makefile('w')
      recv = client_socket.makefile('r')

      msg = {"join": {"username": self.username, "password": self.password, "token": ""}}
      sendfile.write(json.dumps(msg) + "\r\n")
      sendfile.flush()

      server_msg = recv.readline()
      extracted_msg = dsp.extract_json(server_msg)
      token = extracted_msg[2]
      return token

  def send(self, message:str, recipient:str) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(self.dsuserver, 3021)
            server_msg = self._join_server(client_socket)
            print("Server message", server_msg)

            timestamp = str(time.time())
            formatted_post = {"token": server_msg, "directmessage": {"entry": message, "recipient": recipient, "timestamp": timestamp}}
            
            client_socket.sendall(json.dumps(formatted_post).encode())
            response = client_socket.recv(1024).decode('utf-8')
            json_resp = json.loads(response)

            print("Json response", json_resp)
            if json_resp['response']['type'] == 'ok':
                  print("> " + json_resp['response']['message'] + "!\n")
                  return True
    except:
        print("Error with sending direct message.")
        return False
		
  def retrieve_new(self) -> list:
    new_msgs = []
    # must return a list of DirectMessage objects containing all new messages
    return new_msgs
 
  def retrieve_all(self) -> list:
    try:
          if not self.token:
              self._get_token()

          with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
              client_socket.connect((self.dsuserver, 3021))

              message = {"token": self.token, "directmessage": "all"}
              client_socket.sendall(json.dumps(message).encode())

              server_response = client_socket.recv(1024).decode('utf-8')
              
              response = json.loads(server_response)
              if response['response']['type'] == 'ok':
                  messages = response['response']['messages']
                  return messages
              else:
                  print(f"Error: {response['response']['message']}")
                  return []
    except Exception as e:
        print(f"Error retrieving all messages: {e}")
        return []
  

dm_time = DirectMessenger("168.235.86.101", "strawberry", "banana")
print("Class instantiated")
dm_time.send("Hello world", "ohhimark")