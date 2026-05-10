import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 12345))
    print("Connected to the server. Type 'exit' to disconnect.")

    while True:
        command = input("Enter a command: ")
        client.send(command.encode())

        # If the command is 'exit', break from the loop
        if command.lower() == "exit":
            print("Disconnected from the server.")
            break

        # Receive and print the server's response
        response = client.recv(1024).decode()
        print(f"Server response: {response}")

    client.close()

if __name__ == "__main__":
    main()
