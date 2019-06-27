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

        # async message to massage queue
        celery_queue.delay(clientAddress,message.hex())

        #TODO: 按照需求上位机因回复要接受多少条目数据
        # replay message to client ()
        udpServer.connect(clientAddress)
        #udpServer.sendall()

