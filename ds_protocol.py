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
from collections import namedtuple
import ds_client as dsc

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


def directmessage(dm: dict, user, pwd):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        msg_info = dsc.join(client, user, pwd)
        print(msg_info)