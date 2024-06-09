import socket
import config
from functions import *

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
listener.bind((config.listenerIP,config.slotPort))
listener.listen(0)

InitSlot()

while True:
    connection, address = listener.accept()
    connection.send("Successfull".encode('utf8'))
    request = connection.recv(1024)
    answer = StartGame(request)
    connection.send(answer.encode('utf8'))
    connection.close()