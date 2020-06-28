import socket


def send(message):
    sock = socket.socket()
    sock.connect(('localhost', 9097))

    sock.send(message.encode())
    sock.close()


if __name__ == "__main__":
    help_message = "help: stop client - to stop program"

    # a loop that reads commands from keyboard

    while True:
        message = input("Message to send: ")

        if message == "stop client":
            break

        if message == "help":
            print(help_message)
            continue

        try:
            send(message)
        except Exception:
            print("Connection problem, message was not sent.")
