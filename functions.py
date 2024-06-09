import time
import random
import socket
import base64
import config
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

def StartGame(request):
    tickets = SimulateGame()
    return f"{tickets}"

def InitSlot():
    con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    con.connect((config.serverIP, config.serverPort))
    rd = con.recv(1024)
    print(rd.decode('utf8'))
    message = encrypt_string(f"initSlot {config.slotID} 1 {config.slotPrice}")
    con.send(message.encode('utf8'))
    rd = con.recv(1024).decode('utf8')
    while rd != "1":
        con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        con.connect((config.serverIP, config.serverPort))
        rd = con.recv(1024)
        print(rd.decode('utf8'))
        message = encrypt_string(f"changeSlotState {config.slotID}")
        con.send(message.encode('utf8'))
        rd = con.recv(1024).decode('utf8')
        con.close()
    con.close()
    return "Successful"

def encrypt_string(plain_text):
    key = base64.b64decode("LPjR6pHBsx2VvuYNYAaRZfGKsomvqsh3vAODL46dENw=")
    iv = base64.b64decode("nXJhi/OyX83gULxJv1UARQ==")
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plain_text.encode('utf-8')) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    encrypted_bytes = encryptor.update(padded_data) + encryptor.finalize()
    
    return base64.b64encode(encrypted_bytes).decode('utf-8')

def decrypt_string(cipher_text):
    key = base64.b64decode("LPjR6pHBsx2VvuYNYAaRZfGKsomvqsh3vAODL46dENw=")
    iv = base64.b64decode("nXJhi/OyX83gULxJv1UARQ==")
    cipher_text = cipher_text.decode('utf-8')
    cipher_text = base64.b64decode(cipher_text)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plain_text = decryptor.update(cipher_text) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plain_text = unpadder.update(plain_text) + unpadder.finalize()
    return plain_text.decode('utf-8')

def SimulateGame():
    time.sleep(10)
    return(random.randint(config.minTokensPay,config.maxTokensPay))