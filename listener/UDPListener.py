import socket
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from listener.tasks import celery_queue
import logging


if __name__ == "__main__":  
    HOST = ''
    PORT = 8888

    udpServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpServer.bind((HOST, PORT))
    print("The server is ready to receive")
    while True:
        message,clientAddress = udpServer.recvfrom(2800)
        celery_queue.delay(clientAddress,message.hex())
        # print('链接地址',clientAddress,message)
