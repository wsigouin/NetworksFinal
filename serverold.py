import socket

#Host and port are set here, cna be changed for different machines
IP = 'localhost'
port = 5015
#Buffer length of 1024 is standard
bLength = 1024

#creation of socket
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((IP,port))
#one message, listening a single time
socket.listen(1)

connection, address = socket.accept()

#recieving the message
text = connection.recv(bLength)
sLength = len(text.decode())

#connetion will only accept bytes, so it must be converted (max 4 bytes, big endian format, unsigned)
sLengthBytes = sLength.to_bytes(4, byteorder='big', signed=False)

#text is recieved as bytes, decode() automatically uses UTF8 to display
print ("Input was:", text.decode(), " @ ",sLength, " characters long")
connection.send(sLengthBytes)


connection.close();
