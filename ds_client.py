# Starter code for assignment 3 in ICS 32 Programming
# with Software Libraries in Python

# Replace the following placeholders with your information.

# Nicole Utama
# nutama@uci.edu
# 20267081

import socket
import ds_protocol as dsp
import json


def send(server: str, port: int, username: str, password: str, message: str, bio: str = None):
    '''
    The send function joins a ds server and sends a message, bio, or both

    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    '''
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server, port))
            response_msg = join(client_socket, username, password)
            msg_type = response_msg[0]
            token = response_msg[1]
            if msg_type == "ok":
                print("Connection successful")
                if bio is None:
                    post(client_socket, message, token)
                    print("Online post successful.")
                else:
                    post_bio(client_socket, bio, token)
                    print("Online bio successful.")
                    post(client_socket, message, token)
                    print("Online post successful.")
            else:
                print("Invalid. Please try again.")
    except:
        print("Error in connecting to the server. Your request could not be handled at this time.")


def join(client_socket: socket, user: str, pwd: str):
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
    extracted_msg = dsp.extract_json(server_msg)
    # print(extracted_msg)
    msg_type = extracted_msg[0]
    token = extracted_msg[2]
    # print("Token:" + token)
    return msg_type, token


def post(client_socket: socket, user_post, user_token):
    """
    The function to post something to the server.
    Takes a socket, a post, and the user token.
    """

    sendfile = client_socket.makefile('w')
    recv = client_socket.makefile('r')

    formatted_post = {"token": user_token, "post": {"entry": user_post, "timestamp": "1603167.8561"}}
    sendfile.write(json.dumps(formatted_post) + "\r\n")
    sendfile.flush()
    # print(recv.readline())


def post_bio(client_socket: socket, bio, user_token):
    """
    Basically the post function, but with the bio.
    Takes client socket, bio, and user token.
    """

    sendfile = client_socket.makefile('w')
    recv = client_socket.makefile('r')

    formatted_bio = {"token": user_token, "bio": {"entry": bio, "timestamp": ""}}
    sendfile.write(json.dumps(formatted_bio) + "\r\n")
    sendfile.flush()
    # print(recv.readline())
