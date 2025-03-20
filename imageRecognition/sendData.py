import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("192.168.138.143", 12352))  # Connect to server
inputuser = ''
while(inputuser != 'q'):
    inputuser = input("command\n")
    client_socket.sendall(inputuser.encode())

client_socket.close() 