import json
import socket
import threading


class Client:
    SERVER_HOST = "45.56.119.236"
    # SERVER_HOST = "127.0.0.1"

    SERVER_PORT = 9000
    DISCONNECT_MESSAGE = "!DISCONNECT"
    HEADER = 64
    FORMAT = 'utf-8'

    def __init__(self, PORT, ipAddressFunction, activeConnectionsFunction, numDownloadsFunction, HOST=SERVER_HOST):
        self.HOST = HOST
        self.PORT = PORT
        self.clientServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn, self.ender = None, None
        self.activeConnectionsFunction = activeConnectionsFunction
        self.ipAddressFunction = ipAddressFunction
        self.numDownloadsFunction = numDownloadsFunction
        print(f'Created Client Socket: HOST {self.HOST}, PORT {self.PORT}')
        # self.t = threading.Thread(target=self.listen_to_interrupt)
        self.startThread = threading.Thread(target=self.thread_listen)
        # self.t = multiprocessing.Process(target=self.listen_to_interrupt)
        # self.startThread = multiprocessing.Process(target=self.thread_listen)
        self.isAlive = True

    def closeConnection(self):
        print("closeConnection")
        # self.isAlive = False
        self.clientServer.close()
        # self.clientServer.close()

    def online(self):
        self.clientServer.connect((Client.SERVER_HOST, Client.SERVER_PORT))
        self.send(str(self.PORT))

    def uploadFile(self, message):
        self.send(f"[UPLOAD]{message}")
        with open("./localFiles/" + message["name"], 'rb') as file:
            for data in file.readlines():
                self.clientServer.sendall(data)

    def send(self, msg):
        message = msg.encode('utf-8')
        msg_length = len(message)
        send_length = str(msg_length).encode('utf-8')
        send_length += b' ' * (64 - len(send_length))
        self.clientServer.send(send_length)
        self.clientServer.send(message)

    def listen_to_interrupt(self):
        try:
            while True:
                input("Press enter to exit...")
                print("Exiting...")
                self.clientServer.close()
                exit()
        except KeyboardInterrupt:
            print("Exiting due to interruption...")
            self.clientServer.close()
            exit()

    def listen(self):
        self.startThread.start()
        pass

    def thread_listen(self):
        print(f'Client Socket Listening in: HOST {self.HOST}, PORT {self.PORT}')
        while self.isAlive:
            if self.clientServer.fileno() != -1:
                msg_length = self.clientServer.recv(Client.HEADER)
                print("msg_length: ", msg_length)
                msg_length = int(msg_length)
                message = self.clientServer.recv(msg_length).decode(Client.FORMAT)
                print("message: ", message)
                if message.startswith("[ACTIVE CONNECTIONS]"):
                    active_connections = message.strip().replace("[ACTIVE CONNECTIONS] ", "")
                    self.activeConnectionsFunction(active_connections)
                elif message.startswith("[IP ADDRESS]"):
                    ipAddress = message.strip().replace("[IP ADDRESS] ", "")
                    self.ipAddressFunction(ipAddress)
                elif message.startswith("[DOWNLOAD]"):
                    json_string = message.replace("[DOWNLOAD]", "").replace("'", "\"").strip()
                    fileInfo = json.loads(json_string)
                    print("fileInfo")
                    print(fileInfo)
                    print()

                    with open("./localFiles/" + fileInfo["name"], 'wb') as f:
                        lenBytes = 0
                        while lenBytes < fileInfo["sizeBytes"]:
                            data = self.clientServer.recv(fileInfo["sizeBytes"])
                            lenBytes += len(data)
                            print(lenBytes)
                            if not data:
                                break
                            # write data to a file
                            f.write(data)
                    f.close()
                    self.numDownloadsFunction()
                    print("finish white True sizeBytes")