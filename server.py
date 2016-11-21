import socket
import select


def broadcast_data(sock, message):
    message = message.encode()
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock:
            try:
                socket.send(message)
            except:
                print(str(socket) + " has disconnected")
                socket.close()
                CONNECTION_LIST.remove(socket)

if __name__ == "__main__":

    CONNECTION_MASTER = []
    CONNECTION_LIST = []
    CONNECTION_MASTER.append(CONNECTION_LIST)
    RECV_BUFFER = 4096
    PORT = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)

    CONNECTION_LIST.append(server_socket)

    print("Chat server started on port " + str(PORT))

    while 1:
        read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST, [], [])

        for sock in read_sockets:
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print("Client (%s, %s) connected" % addr)

                outData = "\n[" + str(addr) + "]" + " has entered room\n"
                
                broadcast_data(sockfd, outData)

            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        data = data.decode()
                        data = (str(sock.getpeername()) + " says: " + data)
                        broadcast_data(sock, data)

                except Exception as e:
                    print("Client (%s, %s) is offline" % addr)
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue

    server_socket.close()
