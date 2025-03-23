import socket

def client():

    s = socket.socket()
    host = "10.10.10.10"
    port = 5001

    s.connect((host, port))

    message = input("Enter your message: ")

    while message != "exit":

        s.send(message.encode())
        data = s.recv(1024).decode()
        print(f"Info received: {data}")

        message = input("Enter your message, type exit to leave: ")

    s.close()

if __name__ == "__main__":
    client()

