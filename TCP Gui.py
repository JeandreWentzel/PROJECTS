
import tkinter
import tkinter.font as tkFont
import socket
import threading
import sys
import time


class ServerUI():
    local = "127.0.0.1"
    port = 5505
    global serverSock
    flag = False

    def __init__(self):
        '''
       The constructor of the relevant attributes of the initial class
        '''
        self.root = tkinter.Tk()
        self.root.title('Python Live chat-serverV1.0')
        # Window panel, layout with 4 frame panels
        self.frame = [tkinter.Frame(), tkinter.Frame(), tkinter.Frame(), tkinter.Frame()]
        # Display the scroll bar to the right of the message Text
        self.chatTextScrollBar = tkinter.Scrollbar(self.frame[0])
        self.chatTextScrollBar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        # Display the message Text, and bind the scroll bar above
        ft = tkFont.Font(family='Fixdsys', size=11)
        self.chatText = tkinter.Listbox(self.frame[0], width=70, height=18, font=ft)
        self.chatText['yscrollcommand'] = self.chatTextScrollBar.set
        self.chatText.pack(expand=1, fill=tkinter.BOTH)
        self.chatTextScrollBar['command'] = self.chatText.yview()
        self.frame[0].pack(expand=1, fill=tkinter.BOTH)

        # Scroll bar for input message Text
        self.inputTextScrollBar = tkinter.Scrollbar(self.frame[2])
        self.inputTextScrollBar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        # Enter the message Text and bind it to the scroll bar
        ft = tkFont.Font(family='Fixdsys', size=11)
        self.inputText = tkinter.Text(self.frame[2], width=70, height=8, font=ft)
        self.inputText['yscrollcommand'] = self.inputTextScrollBar.set
        self.inputText.pack(expand=1, fill=tkinter.BOTH)
        self.inputTextScrollBar['command'] = self.chatText.yview()
        self.frame[2].pack(expand=1, fill=tkinter.BOTH)

        # "Send" button
        self.sendButton = tkinter.Button(self.frame[3], text="send", width=10, command=self.sendMessage)
        self.sendButton.pack(expand=1, side=tkinter.Button and tkinter.RIGHT, padx=25, pady=5)

        # "Close" button
        self.closeButton = tkinter.Button(self.frame[3], text="shut down", width=10, command=self.close)
        self.closeButton.pack(expand=1, side=tkinter.RIGHT, padx=25, pady=5)
        self.frame[3].pack(expand=1, fill=tkinter.BOTH)

    def receiveMessage(self):
        """
        Receive message
        """
        # Establish Socket connection
        self.serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSock.bind((self.local, self.port))
        self.serverSock.listen(15)
        self.buffer = 1024
        self.chatText.insert(tkinter.END, "Server is ready.")

        # Cyclically accept client connection requests
        while True:
            self.connection, self.address = self.serverSock.accept()
            self.flag = True
            while True:
                # Receive messages sent by the client
                self.cientMsg = self.connection.recv(self.buffer).decode('utf-8')
                if not self.cientMsg:
                    continue
                elif self.cientMsg == 'Y':
                    self.chatText.insert(tkinter.END, 'The server has established a connection with the client.......')
                    self.connection.send(b'Y')
                elif self.cientMsg == 'N':
                    self.chatText.insert(tkinter.END, 'Failed to establish connection between server and client...........')
                    self.connection.send(b'N')
                else:
                    theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    self.chatText.insert(tkinter.END, 'Client' + theTime + 'Say：\n')
                    self.chatText.insert(tkinter.END, ' ' + self.cientMsg)

    def sendMessage(self):
        '''
        Send a message
        :return:
        '''

       
        message = self.inputText.get('1.0', tkinter.END)

        theTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.chatText.insert(tkinter.END, 'server' + theTime + "Say：\n")
        self.chatText.insert(tkinter.END, ' ' + message + '\n')
        if self.flag == True:
           
            self.connection.send(message.encode())
            self.inputText.delete(0.0, message.__len__() - 1.0)

        else:
           
            self.chatText.insert(tkinter.END, 'You have not established a connection with the client, the client cannot receive your message\n')
           
            self.inputText.delete(0.0, message.__len__() - 1.0)

    def close(self):
        '''
        Close the message window and exit
        :return:
        '''
        sys.exit()


    def startNewThread(self):
        '''
        Start a new thread to receive messages from the client
        :return:
        '''
        thread = threading.Thread(target=self.receiveMessage, args=())
        thread.setDaemon(True)
        thread.start()


def main():
    server = ServerUI()
    server.startNewThread()
    server.root.mainloop()


if __name__ == '__main__':
    main()
