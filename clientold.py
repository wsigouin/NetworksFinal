import socket

#IP and port of communication
IP = 'localhost'
port = 5000
bLength = 1024

#create socket
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((IP, port))

text = input("Enter some text: ")
#encode text into BYTE format
socket.send(text.encode())
sLength = socket.recv(bLength)

#read bytes using big endian order, from the server
print("The server says that your string is ", int.from_bytes(sLength, 'big'), " characters long")
socket.close()
