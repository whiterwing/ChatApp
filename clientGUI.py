import tkinter as TK

class mainWindow(object):
    def __init__(self, master):
        self.main = TK.Frame(master)
        self.main.pack()
        
        loginWindow(self.main)

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
        print(self.Entry.get())
        self.window.destroy()
        ChatWindow(self.master)
        
class ChatWindow(object):
    def __init__(self, master):
        self.window = TK.Frame(master)
        self.window.pack()
        
        self.my_msg = TK.StringVar()
        
        self.chatBox()
        self.chatInput()

    def chatBox(self):
        Frame = TK.Frame(self.window)
        Frame.grid(row=0, column=1)
        
        scrollbar = TK.Scrollbar(Frame)
        scrollbar.pack(side=TK.RIGHT, fill=TK.Y)
        
        self.msg_list = TK.Listbox(Frame, height=15, width=50, yscrollcommand=scrollbar.set)
        self.msg_list.pack(side=TK.LEFT, fill=TK.BOTH)

    def chatInput(self):
        Frame = TK.Frame(self.window)
        Frame.grid(row=1, column=1)
        
        entry_field = TK.Entry(Frame, textvariable=self.my_msg)
        entry_field.bind('<Return>', self.test_print)
        entry_field.pack()
          
        send_button = TK.Button(Frame, text='Send', command=self.test_print)
        send_button.pack()

    def test_print(self, event=None):
        print(self.my_msg.get())
        self.my_msg.set("")


if __name__ == "__main__":
    '''
        Starts the network_Handle class.
        Creates the main application for Chatbox.
        Starts the ChatBox class.
        Starts the application.
    '''
    root = TK.Tk()
    root.title("ChatBox")
    root.geometry('500x500')
    Chatbox = mainWindow(root)
    root.mainloop()