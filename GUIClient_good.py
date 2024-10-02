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


#This is the client function, that creates a server
#It takes a textbox and label widget to print info to the screen
async def client(textBox, ipLabel):
    #reference your global variable to set as global
    
    
    #WiFi needs to be the same as the server

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


    try:
        server_ip = '192.168.1.2'  # Replace with the server Pico's IP address, this will also be the IP to display
        server_port = 8000 #Need to change the server port as well

        ipLabel.value(server_ip)

        addr = socket.getaddrinfo(server_ip, server_port)[0][-1]
        client_socket = socket.socket()

        client_socket.connect(addr)
        print("Connected to server")
        message = ""
        while message != "Close":
            #Need a input for the message to get sent, you also need to add a username/name to the message
            message = input("GUI:")
            client_socket.send(message.encode('utf-8'))
            print("Message sent")

            # Receive response
            response = client_socket.recv(1024)
            
            print('Server response:', response.decode('utf-8')) 
            textBox.append(response.decode('utf-8'))             ###disp IP address
            # response.decode('utf-8') is the response from the server, this what should be used to output text to the screen
            
            await asyncio.sleep_ms(150)
    except Exception as e:
        print("Error:", e)
    

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
        self.reg_task(client(txtbox,lbl))

        
        CloseButton(wri)


def test():
    print('Chat Server.')
    Screen.change(BaseScreen)

test()