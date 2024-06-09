import socket
import config
from functions import *



InitSlot()

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
listener.bind((config.listenerIP,config.slotPort))
listener.listen(0)

while True:
    print("Is Ready")
    connection, address = listener.accept()
    connection.send("Successfull".encode('utf8'))
    request = connection.recv(1024).decode('utf8')
    print(request)
    answer = StartGame(request)
    connection.send(answer.encode('utf8'))
    connection.close()