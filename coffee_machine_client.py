# client
import socket, pickle

def get_dict_of_available_beverages():
    """Returns dictionary of available beverages."""

    sock = socket.socket()
    sock.connect(('localhost', 9097)) # what should be here for real coffee machine?
    sock.send("get_bevs".encode())  
    
    result_string = sock.recv(4096)
    result = pickle.loads(result_string)

    sock.close()
    return result

def order_n(number):
    """Sends order number to server."""

    sock = socket.socket()
    sock.connect(('localhost', 9097)) 
    sock.send(f"order_{number}".encode())  
    
    result = sock.recv(4096)
    
    sock.close()
    return result.decode()

def get_stats():
    """Returns coffee machine's statistics."""

    sock = socket.socket()
    sock.connect(('localhost', 9097))
    sock.send("get_stats".encode())  
    
    stats = sock.recv(16384)    # while True?

    sock.close()
    return stats.decode()


def stop_server(): 
    #?
    """Stops running server on coffee machine."""
    sock = socket.socket()
    sock.connect(('localhost', 9097)) 
    sock.send("exit".encode()) 

    sock.close()