from tkinter import *
import socket
import select
import sys
import threading

loginFields = 'Username', 'Server Address', 'Port'
chatField = 'output'

username = None
host = None
port = None
connection = None
log = None
root = None
listener = None
text = None

def printMessage(msg):
    log.configure(state=NORMAL)
    log.insert(INSERT,  msg + "\n")
    log.configure(state=DISABLED)
    return


class Listener(threading.Thread):
    flag = TRUE

    def run(self):
        global connection
        while self.flag:
            socket_list = [sys.stdin, connection]

            read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

            for sock in read_sockets:
                data = sock.recv(4096)
                if not data:
                    print('\nDisconnected')
                    sys.exit()
                else:
                    data = data.decode()
                    printMessage(data)
        print("all done!")



def sendMessage(msg):
    global connection
    global log
    global text
    connection.send(msg.get().encode())
    printMessage(username + ": " + msg.get())
    text = None
    return


def spawnChatWindow():
    global root
    global log
    global text
    t = Toplevel()
    row = Frame(t)


    log = Text(row, state=DISABLED, wrap=WORD)
    log.pack()
    text = StringVar()
    chat = Entry(row, textvariable=text)
    row.pack(side=TOP, fill=X, padx=5, pady=5)
    chat.pack(side=RIGHT, expand=YES, fill=X)

    t.bind('<Return>', (lambda event, e=text: sendMessage(e)))
    chatButton = Button(t, text='Send', command=(lambda e=text: sendMessage(e)))
    chatButton.pack(side=RIGHT, padx=5, pady=5)

    cqButton = Button(t, text='Quit', command=quit)
    cqButton.pack(side=RIGHT, padx=5, pady=5)

    global listener
    listener = Listener()
    listener.start()
    return


def fetchLogin(entries):
    entryarray = []
    for entry in entries:
        entryarray.append(entry[1].get())
    global username
    username = entryarray[0]
    global host
    host = entryarray[1]
    global port
    port = int(entryarray[2])

    print(username + " " + host + " " + str(port))

    global connection
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.settimeout(2)

    try:
        connection.connect((host, port))
    except Exception as e:
        print(str(e))
        print('Connection Failed')
        sys.exit()

    spawnChatWindow()
    return


def spawnLogin(root, fields):
    entries = []
    for field in fields:
        row = Frame(root)
        lab = Label(row, width=15, text=field, anchor='w')
        ent = Entry(row)
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        entries.append((field, ent))
    return entries


def quit():
    global listener
    listener.flag = FALSE
    print("thread should stop?" + str(listener.flag))
    return

if __name__ == '__main__':
    root = Tk()
    items = spawnLogin(root, loginFields)

    root.bind('<Return>', (lambda event, e=items: fetchLogin(e)))
    cButton = Button(root, text='Connect', command=(lambda e=items: fetchLogin(e)))
    cButton.pack(side=LEFT, padx=5, pady=5)

    qButton = Button(root, text='Quit', command=root.quit)
    qButton.pack(side=LEFT, padx=5, pady=5)

    root.mainloop()

