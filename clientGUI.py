import tkinter as TK
from Client import network_Handle
import asyncio

class GUI(object):
    
    def __init__(self,loop):
        '''
            Creates the main GUI,
            Starts the network_Handler,
            Creates a list of persistant tasks that can be closed before the script ends.
            starts the loop for the updater,
            kicks off the main app
        '''
        self.root = TK.Tk()
        self.root.title("ChatBox")
        self.root.geometry('500x500')
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.loop = loop
        self.network = network_Handle()
        self.tasks = []
        
        self.tasks.append(self.loop.create_task(self.updater()))
        
        self.main_window()
        #self.root.mainloop()
    
    async def updater(self):
        '''
            Since the script is using asyncio coroutines the TK.mainloop won't work.
            This function uses the asyncio sleep and TK.update commands to do
            the same function.
        '''
        while True:
            await asyncio.sleep(1/100)
            self.root.update()
    
    def close(self):
        '''
            A closing function to start the connection closing, and stop all of the
            asyncio tasks, then closes the GUI.
        '''
        try:
            self.network.send("/quit")
        except: pass
        for task in self.tasks:
            task.cancel()
        self.root.destroy()
        
    def main_window(self):
        '''
            Creates the main frame the GUI uses and starts the login frame.
        '''
        self.mainWindow = TK.Frame(self.root)
        self.mainWindow.pack()
        
        self.loginFrame()
        
    def loginFrame(self):
        '''
            Creates the GUI for the login frame, and calls the Submit_button_handler
            function to start the coroutine for submiting the username to the server.
        '''
        
        self.loginframe = TK.Frame(self.mainWindow)
        self.loginframe.pack()
        
        label = TK.Label(self.loginframe, text="Username:")
        label.grid(row=0, column=0)
        
        self.username = TK.StringVar()
        
        self.usernameEntry = TK.Entry(self.loginframe, textvariable=self.username, width=50)
        self.usernameEntry.bind('<Return>', self.Submit_button_handler)
        self.usernameEntry.grid(row=0, column=1)
        self.usernameEntry.focus_set()
        
        self.submitButton = TK.Button(self.loginframe, text='login', command = self.Submit_button_handler)
        self.submitButton.grid(row=1, column=1)
        
    def Submit_button_handler(self, event=None):
        '''
            Just a button handler to start a coroutine.
        '''
        self.loop.create_task(self.usernameSubmit())
        
    async def usernameSubmit(self):
        '''
            Sends the username to the server, waits for a responce back.
            If the responce is a welcome message, it destroies the login frame
            and starts the chat frame. If the responce is not a welcome message,
            it tells the user the username is already taken, please try another.
            !!!IT ONLY CHECKS IF SOMEONE IS LOGGED IN WITH THE USERNAME!!!
        '''
        self.network.send(self.usernameEntry.get())
            
        self.welcomemsg = await self.loop.create_task(self.network.receive())
        
        if "Welcome" in self.welcomemsg:
            self.loginframe.destroy()
            self.chatFrame()
        else:
            self.username.set(self.welcomemsg)

    def chatFrame(self):
        '''
            Creates the GUI for the actual Chat App. It uses a chat box to
            display all of the receieved messages. It starts a coroutine for 
            checking the network_handle's reader for new messages from the server
            and runs the send_chat function when user tries to send a message.
        '''
        frame = TK.Frame(self.mainWindow)
        frame.pack()
        
        self.my_msg = TK.StringVar()
        self.users = list()
        self.connectedUsers = TK.Variable(value=self.users)
        
        scrollbar = TK.Scrollbar(frame)
        scrollbar.grid(row=0, column=1)
            
        self.msg_list = TK.Listbox(frame, width=50, height=20, yscrollcommand=scrollbar.set)
        self.msg_list.grid(row=0, column=0)
        self.msg_list.insert(TK.END, self.welcomemsg)
        
        self.connected_list = TK.Listbox(frame, height=20, listvariable=self.connectedUsers)
        self.connected_list.grid(row=0, column=2)
        self.connected_list.__contains__ = lambda str: str in self.connected_list.get(0, "end")
        
        self.chatEntry = TK.Entry(frame, textvariable=self.my_msg)
        self.chatEntry.bind('<Return>', self.send_chat)
        self.chatEntry.grid(row=1, column=0)
        self.chatEntry.focus_set()
        
        self.sendButton = TK.Button(frame, text='Send', command=self.send_chat)
        self.sendButton.grid(row=1, column=1)
        
        self.tasks.append(self.loop.create_task(self.checkForListUpdate()))
        
    async def checkForListUpdate(self):
        '''
            persistant coroutine for checking for new messages. Checks if it's a
            server message that contains a string of everyone connected.
            When it receives one, it adds the message to the end of the listbox.
        '''
        while True:
            msg = await self.loop.create_task(self.network.receive())
            if "$$$SERVER$$$" in msg:
                serverSTR = msg.strip("$$$SERVER$$$:")
                connected = list()
                for user in serverSTR.split(":"):
                    connected.append(user)
                self.connectedUsers.set(connected)
            else:
                self.msg_list.insert(TK.END, msg)
        
    def send_chat(self, event=None):
        '''
            Checks to see if the user is trying to quit, if the user is, it
            starts the closing function. Otherwise, is sends the user's message
            to the network_handle writer stream and resets the user input field.
        '''
        if self.chatEntry.get() == "/quit":
            self.close()
        else:
            self.network.send(self.chatEntry.get())
            self.my_msg.set("") 

if __name__ == "__main__":
    '''
        Starts the app.
    '''
    loop = asyncio.get_event_loop()
    App = GUI(loop)