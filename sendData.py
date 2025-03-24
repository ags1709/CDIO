import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("192.168.138.130", 12358))  # Connect to server
inputuser = ''
while(inputuser != 'q'):
    inputuser = input("command\n")
    client_socket.sendall(inputuser.encode())

client_socket.close() 


# client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# dataToSend = "Hello with UDP message 2"
# client_socket.sendto(dataToSend.encode(), ("localhost", 12345))