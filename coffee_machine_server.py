import socket
import multiprocessing as mp


HOST = ''         # all available interfaces
PORT = 9097


def listen():
    sock = socket.socket()
    sock.bind((HOST, PORT))
    sock.listen(1)           # max queue of 1
    print("Server: waiting for connections...")

    while True:
        conn, addr = sock.accept()
        encoded_message = conn.recv(1024)   # receive 1 kb
        message = encoded_message.decode()

        print("Client says: {0}.".format(message))
    conn.close()


if __name__ == "__main__":
    # a seperate process that is listening to client messages
    process = mp.Process(target=listen)
    process.start()

    # a loop that reads commands from keyboard
    help_message = "help: stop - to stop server"
    while True:
        command = input()
        if command == "stop":
            process.terminate()  # hope zombie is not gonna eat memory
            break

        if command == "help":
            print(help_message)
            continue

        print('Your command is "{0}".'.format(command))
