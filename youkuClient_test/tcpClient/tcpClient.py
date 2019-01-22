from socket import *
def get_client():
    client = socket(AF_INET,SOCK_STREAM)
    client.connect(('127.0.0.1',8080))
    return client