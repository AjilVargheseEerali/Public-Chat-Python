import socket
import sys
from _thread import *
import threading
import time
from termcolor import colored   #for highlighting

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    IP_address = "127.0.0.1"
    Port = 8081
except:
    print(" Unable to start server. Try changing the port")
    sys.exit()

all_threads = [] 
server.bind((IP_address, Port))
print("Server running on port "+str(Port))
server.listen(100) 
list_of_clients = [] 
  
def clientthread(conn, addr):
    while True: 
            try: 
                message = conn.recv(2048)
                if message.decode()!="exit":
                    message_to_send = message.decode()
                    broadcast(message_to_send.encode(), conn) 
  
                elif message.decode() == "exit":
                    print(str(addr[0])+":"+str(addr[1]),end="")
                    print(" left the server")
                    esms = "exit"
                    conn.send(esms.encode())
                    remove(conn)
                    break
  
            except: 
                continue

def broadcast(message, connection):
    print("' "+message.decode()+" '")
    for clients in list_of_clients: 
        if clients!=connection: 
            try: 
                clients.send(message) 
            except: 
                clients.close()
                remove(clients)
  
def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection)

def shutdown():
    while True:
        cmd = input()
        if cmd == "quit":
            for client in list_of_clients:
                client.send(cmd.encode())
            server.close()
            break
        else:
            print("Server Running")

sd = threading.Thread(target=shutdown)
sd.start()
  
while True:
    try:
        conn, addr = server.accept() 
        list_of_clients.append(conn) 
        print(str(addr[0])+":"+str(addr[1]),end="")
        t=threading.Thread(target=clientthread,args=(conn,addr))
        all_threads.append(t)
        t.start()
    except:
        break

for th in all_threads:
    th.join()
sd.join()
print("Server has shutdown")