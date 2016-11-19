from tkinter import *
import socket
import select
fields = 'Username', 'Server Address', 'Port'


def fetch(entries):
    entryarray = []
    for entry in entries:
        entryarray.append(entry[1].get())

    username = entryarray[0]
    host = entryarray[1]
    port = int(entryarray[2])

    print(username + " " + host + " " + str(port))

    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.settimeout(2)

    try:
        connection.connect((host, port))
    except:
        print('Connection Failed')
        sys.exit()

    print('Connected...')


def makeform(root, fields):
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


if __name__ == '__main__':
    root = Tk()
    items = makeform(root, fields)

    root.bind('<Return>', (lambda event, e=items: fetch(e)))
    cButton = Button(root, text='Connect', command=(lambda e=items: fetch(e)))
    cButton.pack(side=LEFT, padx=5, pady=5)

    qButton = Button(root, text='Quit', command=root.quit)
    qButton.pack(side=LEFT, padx=5, pady=5)
    root.mainloop()
