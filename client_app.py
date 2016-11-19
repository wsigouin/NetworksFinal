import socket
import select
import sys

if __name__ == "__main__":

    host = 'localhost'
    port = 5000
    chatroom = 0

    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.settimeout(2)

    try:
        connection.connect((host, port))
    except:
        print('Connection Failed')
        sys.exit()

    print('Connected...')
    sys.stdout.flush()

    while 1:
        socket_list = [sys.stdin, connection]

        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

        for sock in read_sockets:
            if sock == connection:
                data = sock.recv(4096)
                data = data.decode()

                if not data:
                    print('\nDisconnected')
                    sys.exit()
                else:
                    sys.stdout.write(data)
                    sys.stdout.flush()

            else:
                msg = sys.stdin.readline()
                connection.send(msg.encode())
                sys.stdout.flush()

