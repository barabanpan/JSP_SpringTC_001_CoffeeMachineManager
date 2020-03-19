# server
import socket, pickle

from coffee_machine import CoffeeMachine

HOST = ''         # all available interfaces
PORT = 9097

coffee_machine = CoffeeMachine()

sock = socket.socket()
sock.bind((HOST, PORT)) # host, port
sock.listen(1)          # max queue of 1
print("Server: waiting for connections...")

while True:
    
    conn, addr = sock.accept()
    print(f"Connected: {addr}")

    data = conn.recv(1024) # receive 1 kb 
    message = data.decode()    

    if message == "get_bevs":
        bevs = coffee_machine.get_dict_of_available_beverages()
        bevs_string = pickle.dumps(bevs)

        conn.send(bevs_string)


    elif message.startswith("order_") and message[6:].isdigit():
        number = int(message[6:])
        coffee_machine.prepare_beverage(number)
        conn.send(f"{number} is ordered".encode())
        

    elif message == "get_stats":
        stats = coffee_machine.get_history()
        conn.send(stats.encode())
  
    elif message == "exit":
        break

    else:
        conn.send(f"Incorrect message ({message})".encode())
        
conn.close()