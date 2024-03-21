# ds_protocol.py

# Starter code for assignment 3 in ICS 32 Programming
# with Software Libraries in Python

# Replace the following placeholders with your information.

# Nicole Utama
# nutama@uci.edu
# 20267081

"""
This module has the extract_json file that is used
in ds_client.py
"""

import json
import socket
import time
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.
DataTuple = namedtuple('DataTuple', ['type', 'message', 'token'])


def extract_json(json_msg: str) -> DataTuple:
    '''
    Call the json.loads function on a json string 
    and convert it to a DataTuple object
    '''
    try:
        json_obj = json.loads(json_msg)
        msg_type = json_obj['response']['type']
        if msg_type == "ok":
            msg_token = json_obj['response']['token']
            message = json_obj['response']['message']
        else:
            message = ""
            msg_token = ""
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
    except KeyError:
        print("JSON could not be extracted.")
    return DataTuple(msg_type, message, msg_token)

def extract_json_to_list(json_msg: str):
    '''
    Call the json.loads function on a json string 
    and convert it to a list
    '''
    json_info = []
    try:
        json_obj = json.loads(json_msg)
        msg_type = json_obj['response']['type']
        messages = json_obj['response']['messages']
        json_info.append(msg_type)
        for message in messages:
            json_info.append(message)
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
    return json_info

def _join(client_socket: socket, user: str, pwd: str):
    """
    This function connects the client code to the server.
    Takes client_socket, username, and password.
    """
    sendfile = client_socket.makefile('w')
    recv = client_socket.makefile('r')

    msg = {"join": {"username": user, "password": pwd, "token": ""}}
    # print(message)
    sendfile.write(json.dumps(msg) + "\r\n")
    sendfile.flush()

    server_msg = recv.readline()
    extracted_msg = extract_json(server_msg)
    # print(extracted_msg)
    # print("Token:" + token)
    return extracted_msg

def directmessage(dm, recipient, dsuserver, user, pwd):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((dsuserver, 3021))
            server_msg = _join(client, user, pwd)
            msg_token = server_msg[2]

            timestamp = str(time.time())
            formatted_post = {"token": msg_token, "directmessage": {"entry": dm, "recipient": recipient, "timestamp": timestamp}}
            sendfile = client.makefile('w')
            recv = client.makefile('r')
            sendfile.write(json.dumps(formatted_post) + "\r\n")
            sendfile.flush()
            server_resp = json.loads(recv.readline())
            if server_resp["response"]["type"] == "ok":
                return "Direct message successfully sent", msg_token
    except:
        print("Error with sending message through protocol.")
        return False
