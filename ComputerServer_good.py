# Disclaimer: The base code is not my original work, I had modified it to complete this lab
import socket









hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
print(f"Starting server on {local_ip}")
    

# Creates the server socket that allows clients to connect
addr = socket.getaddrinfo(local_ip, 8000)[0][-1]


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
        
        
    except:
        bing = 0

    
    
    
    
        
    
    
    
    

