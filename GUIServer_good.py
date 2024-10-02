# Disclaimer: The base code is not my original work, I had modified it to complete this lab
# aclock.py micro-gui analog clock demo.

# Released under the MIT License (MIT). See LICENSE.
# Copyright (c) 2021-2022 Peter Hinch

# Initialise hardware and framebuf before importing modules.
import hardware_setup  # Create a display instance
from gui.core.ugui import Screen, ssd
from gui.widgets import Label, Dial, Pointer, CloseButton,Textbox  ,Button

# Now import other modules
from cmath import rect, pi
import uasyncio as asyncio
import time
from gui.core.writer import CWriter

# Font for CWriter
import gui.fonts.arial10 as font
from gui.core.colors import *
import network
import socket








#This is the server function, that creates a server
#It takes a textbox and label widget to print info to the screen
async def server(textBox, ipLabel):
    #reference your global variable to set as global

    ssid = 'ME4550'
    password = 'ME4550FA24'

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    # Wait for connection
    while not wlan.isconnected():
        time.sleep(1)
    print('Connected to Wi-Fi. IP:', wlan.ifconfig()[0])

    # Creates the server socket that allows clients to connect
    addr = socket.getaddrinfo(wlan.ifconfig()[0], 8000)[0][-1]


    #Hint: this is how you get your IP: wlan.ifconfig()[0]


    server_socket = socket.socket()
    server_socket.bind(addr)
    server_socket.listen(1)


    print('Listening on', addr)
    client = None
    while True:
        

        if client == None:
        # Wait for a client connection
            client, client_addr = server_socket.accept()
            print('Client connected from', client_addr)
            client.setblocking(0)
        try:
        # Receive data
            #data is the raw data from the client
            data = client.recv(1024)
            #the message variable 
            message = data.decode('utf-8')
            #Hint: add a global variable that removes the client in the if statement
            if data.decode('utf-8') == "ClearClient":
                client.send("Good Bye".encode('utf-8'))
                # Close connection
                client.close()
                client = None
                #reset global variable 
            #elif for returning/closing server
            else:
                client.send(data)
            #Update your labels/textbox
            textBox.append(data.decode('utf-8'))    #show IP in textbox
            ipLabel.value(wlan.ifconfig()[0])       #

        except:
            bing = 0
        await asyncio.sleep_ms(15)
        
        
        

        
            
        
        
        
        

class BaseScreen(Screen):
    def __init__(self):
        super().__init__()
        labels = {'bdcolor' : RED,
                  'fgcolor' : WHITE,
                  'bgcolor' : DARKGREEN,
                  'justify' : Label.CENTRE,
                  }
       
        wri = CWriter(ssd, font, GREEN, BLACK)  # verbose = True
        #Hint: probably need a call back for the button to clear clients/close sever
        
        txtbox = Textbox(wri,2,2,nlines = 10,width=180)
        lbl = Label(wri,200,2,text='                       ')

        self.reg_task(server(txtbox,lbl))
        CloseButton(wri)


def test():
    print('Chat Server.')
    Screen.change(BaseScreen)

test()