# Disclaimer: The base code is not my original work, I had modified it to complete this lab

#import network
import socket
import time

# Connect to Wi-Fi (replace SSID and password with your network details)
ssid = 'ME4550'
password = 'ME4550FA24'
username = "Not Jesse"

# Set up client to connect to server
try:
    server_ip = '192.168.1.20'  # Replace with the server Pico's IP address
    server_port = 8000

    addr = socket.getaddrinfo(server_ip, server_port)[0][-1]
    client_socket = socket.socket()

    client_socket.connect(addr)
    print("Connected to server")
    message = ""
    while message != "Close":
        message = input("Message: ")
        message =  username + ": " + message
        client_socket.send(message.encode('utf-8'))
        print("Message sent")

        # Receive response
        response = client_socket.recv(1024)
        print('Server response:', response.decode('utf-8'))

    
except Exception as e:
    print("Error:", e)


