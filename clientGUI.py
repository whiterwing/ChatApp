import tkinter as TK
from Client import network_Handle
import asyncio

class GUI(object):
    network = network_Handle()
    tasks = []
    
    def __init__(self,loop):
        self.root = TK.Tk()
        self.root.title("ChatBox")
        self.root.geometry('500x500')
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        
        GUI.tasks.append(loop.create_task(self.updater()))
        GUI.tasks.append(loop.create_task(GUI.network.receive()))
        
        self.loginWindow(self.root)
        #self.root.mainloop()
    
    async def updater(self):
        while True:
            await asyncio.sleep(1/100)
            self.root.update()
    
        
    def close(self):
        try:
            GUI.network.send("/quit")
        except: pass
        for task in GUI.tasks:
            task.cancel()
        self.root.destroy()
    
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
            GUI.network.send(self.Entry.get())
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
            GUI.tasks.append(asyncio.get_event_loop().create_task(self.checkForListUpdate()))
    
        def chatBox(self):
            Frame = TK.Frame(self.window)
            Frame.grid(row=0, column=1)
            
            scrollbar = TK.Scrollbar(Frame)
            scrollbar.pack(side=TK.RIGHT, fill=TK.Y)
            
            self.msg_list = TK.Listbox(Frame, width=50, height=20, yscrollcommand=scrollbar.set)
            self.msg_list.pack(side=TK.LEFT, fill=TK.BOTH)
            
        async def checkForListUpdate(self):
            print("Starting Checker")
            while True:
                msg = await asyncio.get_event_loop().create_task(GUI.network.receive())
                self.msg_list.insert(TK.END, msg)
    
        def chatInput(self):
            Frame = TK.Frame(self.window)
            Frame.grid(row=1, column=1)
            
            self.entry_field = TK.Entry(Frame, textvariable=self.my_msg)
            self.entry_field.bind('<Return>', self.send_chat)
            self.entry_field.pack()
              
            send_button = TK.Button(Frame, text='Send', command=self.send_chat)
            send_button.pack()
    
        def send_chat(self, event=None):
            if self.entry_field.get() == "/quit":
                global App
                App.close()
            else:
                GUI.network.send(self.entry_field.get())
                self.my_msg.set("")


if __name__ == "__main__":
    '''
        Starts the network_Handle class.
        Creates the main application for Chatbox.
        Starts the ChatBox class.
        Starts the application.
    '''
    loop = asyncio.get_event_loop()
    App = GUI(loop)
    
