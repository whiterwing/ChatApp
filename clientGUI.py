import tkinter as TK

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
        self.main = TK.Frame(master)
        self.main.pack()
        self.my_msg = TK.StringVar()
        
        self.read_frame = self.read_frame()
        self.input_frame = self.input_frame()

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
        
        login_label = TK.Label(self.login_popup, text="Usersname")
        login_label.grid(row=0, column=0)
        
        self.login_entry = TK.Entry(self.login_popup)
        self.login_entry.bind('<Return>', self.popup_submit)
        self.login_entry.grid(row=0, column=1)
        self.login_entry.focus_set()
        
        login_button = TK.Button(self.login_popup, text="Login", command=self.popup_submit)
        login_button.grid(row=1, columnspan=2)
        
    def popup_submit(self):
        '''
            Calls the Network.send function to send the Username to the Server.
            Sets the chat box to a default message.
            Destroys the popup window.
            
        '''
        self.my_msg.set(self.login_entry.get())
        print(self.my_msg.get())
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
        entry_field.bind('<Return>', print(self.my_msg.get()))
        entry_field.pack()
          
        send_button = TK.Button(input_frame, text='Send', command=print(self.my_msg.get()))
        send_button.pack()
          
        input_frame.pack()
    
if __name__ == "__main__":
    '''
        Starts the network_Handle class.
        Creates the main application for Chatbox.
        Starts the ChatBox class.
        Starts the application.
    '''
    top = TK.Tk()
    top.title("ChatBox")
    Chatbox = ChatBox(top)
    top.mainloop()