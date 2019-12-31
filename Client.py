'''
This is the Client side of a chat application.
'''

import socket
from threading import Thread
import tkinter as TK
import sys

class network_Handle(object):
    '''
    This class is for the network portion of the application, 
    '''
    def __init__(self):
        '''
        Sets Chatbox and top to global vars.
        Sets the server's ip and which port to use, and the buffer size to send across the network.
        Trys to create the connection to the server, if the server can't be found, exits the script.
        Starts the thread for receiving messages from the server.
        '''
        global Chatbox
        global top
        server_IP = "127.0.0.1"
        server_Port = 1234
        self.ADDR = (server_IP,server_Port)
        self.BUFFER_SIZE = 10
        
        try:
            self.client_socket = socket.create_connection((server_IP, server_Port))
        except ConnectionRefusedError:
            print("No Server Found.")
            sys.exit()
        
        RECEIVE_THREAD = Thread(target=self.receive)
        RECEIVE_THREAD.start()
    
    def receive(self):
        '''
            Runs an infinate loop in it's own thread started from network_Handle.__init__, listening for
            messages from the server to add to the Chatbox's message log.
        '''
        while True:
            try:
                msg = self.client_socket.recv(self.BUFFER_SIZE).decode('utf-8')
                Chatbox.msg_list.insert(TK.END, msg)
            except OSError:
                break
            
    def send(self,event=None):
        '''
            Pulls the String out of Chatbox.my_msg, and makes sure it's not an empty string.
            Clears the chat input box.
            Sends the message to the Server.
            If the message is "/quit", closes the socket, and exits the GUI.
        '''
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

class ChatBox(object):
    '''
        Class to create and run the GUI.
    '''
    def __init__(self, master):
        '''
            Sets Network to the Global scope.
            Creats the main frame for the GUI
            Starts the login popup window.
        '''
        global Network
        self.main = TK.Frame(master)
        self.main.pack()
        self.my_msg = TK.StringVar()
        
        self.popup = self.popup()
        self.read_frame = self.read_frame()
        self.input_frame = self.input_frame()

    def popup(self):
        '''
            Creats the login popup window.
            Waits for the User to input a Username to be recognized by the server.
            Runs the popup_submit function.
        '''
        self.login_popup = TK.Tk()
        self.login_popup.title("Login")
        
        self.username = TK.StringVar()
        
        login_label = TK.Label(self.login_popup, text="Usersname")
        login_label.grid(row=0, column=0)
        
        login_entry = TK.Entry(self.login_popup, textvariable=self.my_msg)
        login_entry.grid(row=0, column=1)
        login_entry.focus_set()
        
        login_button = TK.Button(self.login_popup, text="Login", command=self.popup_submit)
        login_button.grid(row=1, columnspan=2)
        
    def popup_submit(self):
        '''
            Calls the Network.send function to send the Username to the Server.
            Sets the chat box to a default message.
            Destroys the popup window.
            
        '''
        print(self.my_msg.get())
        Network.send()
        self.my_msg.set("Type your message here.")
        self.login_popup.destroy()
        
    def read_frame(self):
        '''
            Creates the chat log for network_Handle.receive to populate.
        '''
        chatbox_frame = TK.Frame(self.main)
        scrollbar = TK.Scrollbar(chatbox_frame)
        
        self.msg_list = TK.Listbox(chatbox_frame, height=15, width=50, yscrollcommand=scrollbar.set)
        scrollbar.pack(side=TK.RIGHT, fill=TK.Y)
        self.msg_list.pack(side=TK.LEFT, fill=TK.BOTH)
        chatbox_frame.pack()
          
    def input_frame(self):
        '''
            Creates the Chatbox and sends input to network.send() to send to the Server.
        '''
        input_frame = TK.Frame(self.main)                        
        entry_field = TK.Entry(input_frame, textvariable=self.my_msg)
        entry_field.bind('<Return>', Network.send)
        entry_field.pack()
          
        send_button = TK.Button(input_frame, text='Send', command=Network.send)
        send_button.pack()
          
        input_frame.pack()
    
if __name__ == "__main__":
    '''
        Starts the network_Handle class.
        Creates the main application for Chatbox.
        Starts the ChatBox class.
        Starts the application.
    '''
    Network = network_Handle()
    top = TK.Tk()
    top.title("ChatBox")
    Chatbox = ChatBox(top)
    top.mainloop()