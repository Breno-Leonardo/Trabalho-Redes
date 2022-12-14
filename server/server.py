import errno
import socket
import threading
import json

SERVER = '45.56.119.236'
# SERVER = 'localhost'
PORT = 9000
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"
CONNECTIONS = {}
HEADER = 64
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server.bind(ADDR)
except socket.error as e:
    print(str(e))


def send_message(conn, msg):
    message = msg.encode('utf-8')
    msg_length = len(message)
    send_length = str(msg_length).encode('utf-8')
    send_length += b' ' * (64 - len(send_length))
    conn.send(send_length)
    conn.send(message)


def handle_client(conn, addr):
    global CONNECTIONS
    print(f"[NEW CONNECTION] {addr} connected")
    CONNECTIONS[(addr[0] + ":" + str(addr[1]))] = conn
    for connection in CONNECTIONS.values():
        active_connections = f"[ACTIVE CONNECTIONS] {threading.active_count() - 3}"
        send_message(connection, active_connections)
    connected = True
    try:
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print("received msg:")
            print(msg)
            print()
            print()
            if msg == DISCONNECT_MESSAGE:
                print(f"Disconnected: {addr}")
                CONNECTIONS.pop((addr[0] + ":" + str(addr[1])))
                for connection in CONNECTIONS.values():
                    active_connections = f"[ACTIVE CONNECTIONS] {threading.active_count() - 3}"
                    send_message(connection, active_connections)
                connected = False
            elif msg.startswith("[UPLOAD]"):
                json_string = msg.replace("[UPLOAD]", "").replace("'", "\"").strip()
                fileInfo = json.loads(json_string)
                print("fileInfo")
                print(fileInfo)
                print()

                with open(fileInfo["name"], 'wb') as f:
                    lenBytes = 0
                    while lenBytes < fileInfo["sizeBytes"]:
                        data = conn.recv(fileInfo["sizeBytes"])
                        lenBytes += len(data)
                        print(lenBytes)
                        if not data:
                            break
                        # write data to a file
                        f.write(data)
                f.close()
                print("finish white True sizeBytes")
                print("Sending to peers")

                copied_connections = CONNECTIONS.copy()
                copied_connections.pop((addr[0] + ":" + str(addr[1])))
                num_copies = len(copied_connections.values()) if len(copied_connections.values()) > fileInfo["copies"] else fileInfo["copies"]
                if num_copies >= 1:
                    for i, connection in enumerate(copied_connections.values()):
                        if i > num_copies:
                            break
                        send_message(connection, f"[DOWNLOAD]{fileInfo}")
                        with open(fileInfo["name"], 'rb') as file:
                            for data in file.readlines():
                                connection.sendall(data)
            else:
                active_connections = f"[ACTIVE CONNECTIONS] {threading.active_count() - 3}"
                ipAddress = f"[IP ADDRESS] {addr[0]}"
                send_message(conn, active_connections)
                send_message(conn, ipAddress)

    except socket.error as e:
        # Handle connection forcibly closed by remote host
        if e.errno == errno.ECONNRESET:
            print("[!] Connection from {} forcibly closed by remote host".format(addr))
            CONNECTIONS.pop((addr[0] + ":" + str(addr[1])))
        else:
            print(e)
    conn.close()


def start():
    global CONNECTIONS
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


def listen_to_interrupt():
    try:
        while True:
            input("Press enter to exit...\n")
            print("Exiting...")
            server.close()
            exit()
    except KeyboardInterrupt:
        print("Exiting due to interruption...")
        server.close()
        exit()


print("[SERVER STARTING]...")
t = threading.Thread(target=listen_to_interrupt)
t.start()
startThread = threading.Thread(target=start)
startThread.start()
