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
import ds_messenger as dsm

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
        message = json_obj['response']['message']
        if msg_type == "ok":
            msg_token = json_obj['response']['token']
        else:
            msg_token = ""
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
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
        message = json_obj['response']['message']
        if msg_type == "ok":
            msg_token = json_obj['response']['token']
        else:
            msg_token = ""
        json_info.append(msg_token)
        json_info.append(msg_type)
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

def directmessage(dm, recipient, user, pwd):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(("168.235.86.101", 3021))
        server_msg = _join(client, user, pwd)
        msg_info = []
        for item in server_msg:
            msg_info.append(item)
        print(msg_info)
        msg_token = msg_info[2]
        formatted_post = {"token": msg_token, "directmessage": {"entry": dm, "recipient": recipient, "timestamp": str(time.time())}}
        print(formatted_post)
        sendfile = client.makefile('w')
        recv = client.makefile('r')
        sendfile.write(json.dumps(formatted_post) + "\r\n")
        sendfile.flush()
        print(recv.readline)

print(directmessage("Hello world", "ohhimark", "strawberry", "banana"))