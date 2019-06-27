from tkinter import *
import socket
import threading

root = Tk()
root.geometry("600x400")
root.title("Chat")
myMessage = ''

def receive():
    while True:
        mylist.insert(END, s.recv(1024).decode())

def register():
    myName = name.get()
    nameMessage = '/n ' + myName
    s.sendall(nameMessage.encode())
    #receive()

def sendMessage(event):
    myMessage = txt.get()
    txt.delete(0,END)
    s.sendall(('/a ' + myMessage).encode())
    mylist.insert(END,'[me]: ' + myMessage)

left = Frame(root, borderwidth=2, relief="solid")
nameContainer = Frame(left, borderwidth=2, height=25)
display = Frame(left, borderwidth=2, width=600, height=300, relief="solid", background ='#FFFFFF')
inputing = Frame(left, borderwidth=2, relief="solid")

nameLabel = Label(nameContainer, text='Enter your name: ')
name = Entry(nameContainer, width = 70)
sendName = Button(nameContainer, text='Confirm', command=register)

scrollbar = Scrollbar(display)

txt = Entry(inputing, width = 600)

root.bind('<Return>', sendMessage)

left.pack(side="left", expand=True, fill="both")
nameContainer.pack(expand=True, fill="both", padx=5, pady=5)
display.pack(expand=True, fill="both", padx=5, pady=5)
inputing.pack(expand=True, fill="both", padx=5, pady=5)
nameLabel.pack(side=LEFT)
name.pack(side=LEFT)
sendName.pack(side=LEFT)
txt.pack()

scrollbar.pack(side = RIGHT, fill = BOTH)
mylist = Listbox(display, yscrollcommand = scrollbar.set )
   
mylist.pack(side = LEFT, fill = BOTH, expand=True)
scrollbar.config( command = mylist.yview )

s = socket.socket()

s.connect(('10.0.0.35',8888))

t1 = threading.Thread(target=receive)
t1.start()
root.mainloop()