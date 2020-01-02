import tkinter as TK
from Client import network_Handle
from queue import Empty
import asyncio

class GUI(object):
    try:
        network = network_Handle()
    except:
        print("server not Found")
    
    def __init__(self):
        self.root = TK.Tk()
        self.root.title("ChatBox")
        self.root.geometry('500x500')
        self.mainWindow(self.root)
        
        await (self.network.receive())
        
        self.root.mainloop()
        
        
    def close(self):
        self.root.destroy()
    
    class mainWindow(object):
        def __init__(self, master):
            self.main = TK.Frame(master)
            self.main.pack()
            
            GUI.loginWindow(self.main)
    
    class loginWindow(object):
        def __init__(self, master):
            self.master = master
            self.window = TK.Frame(master)
            self.window.pack()
            
            self.inputFrame()
            self.submitFrame()
            
        def inputFrame(self):
            Frame = TK.Frame(self.window)
            Frame.pack()
            
            Label = TK.Label(Frame, text="Username:")
            Label.pack(side=TK.LEFT)
            
            self.Entry = TK.Entry(Frame)
            self.Entry.bind('<Return>', self.usernameSubmit)
            self.Entry.pack(side=TK.RIGHT)
            self.Entry.focus_set()
            
        def submitFrame(self):
            Frame = TK.Frame(self.window)
            Frame.pack()
            
            Button = TK.Button(Frame, text="Login", command=self.usernameSubmit)
            Button.pack()
            
        def usernameSubmit(self, event=None):
            GUI.network.send(msg=(self.Entry.get()))
            self.window.destroy()
            GUI.ChatWindow(self.master)
            
    class ChatWindow(object):
        my_msg = None
        
        def __init__(self, master):
            self.master = master
            self.window = TK.Frame(master)
            self.window.pack(fill=TK.BOTH)
            
            self.my_msg = TK.StringVar()
            
            self.chatBox()
            self.chatInput()
    
        def chatBox(self):
            Frame = TK.Frame(self.window)
            Frame.grid(row=0, column=1)
            
            scrollbar = TK.Scrollbar(Frame)
            scrollbar.pack(side=TK.RIGHT, fill=TK.Y)
            
            self.msg_list = TK.Listbox(Frame, yscrollcommand=scrollbar.set)
            self.msg_list.pack(side=TK.LEFT, fill=TK.BOTH)
            
            self.checkForListUpdate()
            
        def checkForListUpdate(self):
            try:
                msg = GUI.network.msg_recv.get_nowait()
            except Empty:
                pass
            else:
                self.msg_list.insert(TK.END, msg)
    
        def chatInput(self):
            Frame = TK.Frame(self.window)
            Frame.grid(row=1, column=1)
            
            self.entry_field = TK.Entry(Frame, textvariable=self.my_msg)
            self.entry_field.bind('<Return>', self.test_print)
            self.entry_field.pack()
              
            send_button = TK.Button(Frame, text='Send', command=self.test_print)
            send_button.pack()
    
        def test_print(self, event=None):
            GUI.network.send(msg=(self.entry_field.get()))
            if self.entry_field.get() == "/quit":
                GUI.close()
            else:
                self.my_msg.set("")


if __name__ == "__main__":
    '''
        Starts the network_Handle class.
        Creates the main application for Chatbox.
        Starts the ChatBox class.
        Starts the application.
    '''
    GUI()
    