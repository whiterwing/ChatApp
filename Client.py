import socket
from threading import Thread
import tkinter as TK


class network_Handle(object):
    def __init__(self):
        global Chatbox
        global top
        server_IP = "127.0.0.1"
        server_Port = 1234
        self.BUFFER_SIZE = 1024
        self.ADDR = (server_IP,server_Port)
        
        try:
            self.client_socket = socket.create_connection((server_IP, server_Port))
        except ConnectionRefusedError:
            print("No Server Found.")
        
        RECEIVE_THREAD = Thread(target=self.receive)
        RECEIVE_THREAD.start()
    
    def receive(self):
        while True:
            try:
                msg = self.client_socket.recv(self.BUFFER_SIZE).decode('utf-8')
                Chatbox.msg_list.insert(TK.END, msg)
            except OSError:
                break
            
    def send(self,event=None):
        msg = Chatbox.my_msg.get()
        if msg != "":
            print(msg)
        else:
            print("Message not found.")
        Chatbox.my_msg.set("")
        self.client_socket.send(bytes(msg, 'utf-8'))
        if msg=="/quit":
            self.client_socket.close()
            top.destroy()
            
    def on_closeing(self, event=None):
        Chatbox.my_msg.set("/quit")
        self.send()

class ChatBox(object):
    def __init__(self, master):
        global Network
        self.main = TK.Frame(master)
        self.main.pack()
        self.my_msg = TK.StringVar()
        
        self.popup = self.popup()
        
    def read_frame(self):
        chatbox_frame = TK.Frame(self.main)
        scrollbar = TK.Scrollbar(chatbox_frame)
        
        self.msg_list = TK.Listbox(chatbox_frame, height=15, width=50, yscrollcommand=scrollbar.set)
        scrollbar.pack(side=TK.RIGHT, fill=TK.Y)
        self.msg_list.pack(side=TK.LEFT, fill=TK.BOTH)
        chatbox_frame.pack()
          
    def input_frame(self):
      input_frame = TK.Frame(self.main)                        
      entry_field = TK.Entry(input_frame, textvariable=self.my_msg)
      entry_field.bind('<Return>', Network.send)
      entry_field.pack()
      
      send_button = TK.Button(input_frame, text='Send', command=Network.send)
      send_button.pack()
      
      input_frame.pack()

if __name__ == "__main__":
    Network = network_Handle()
    top = TK.Tk()
    top.title("ChatBox")
    top.protocol("WM_DELETE_WINDOW", Network.on_closeing)
    Chatbox = ChatBox(top)
    top.mainloop()