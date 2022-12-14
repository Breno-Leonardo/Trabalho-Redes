import os
import threading
import time
import sys
import eel
from File import File
from ClientClass import Client


def close_callback(route, websockets):
    global client
    if not websockets:
        try:
            client.send(Client.DISCONNECT_MESSAGE)
            time.sleep(1)
            client.closeConnection()
            for thread in threading.enumerate():
                thread.join()

            sys.exit(0)
        except:
            sys.exit(0)


def listDirHashCodes():
    files_in_folder = os.listdir('./localFiles')
    path = str(os.path.abspath(__file__)).replace("main.py", "") + f"localFiles\\"
    hashCodes = []
    files = []
    for entry in files_in_folder:
        # Create full path
        fullPath = os.path.join(path, entry)
        if os.path.isfile(fullPath):
            file = File(fullPath, entry)
            files.append(file.obj())
            hashCodes.append(file.sha256_hash)
    return files, hashCodes


eel.init('www')
eel.start('index.html', block=False, mode='edge-app', close_callback=close_callback)

print("eel.start")

dirFiles, hashcodes = listDirHashCodes()
eel.showFiles(dirFiles)

writingFile = False


@eel.expose
def add_file(byteArray, fileName):
    global writingFile
    writingFile = True
    f = open("./localFiles/" + fileName, "wb")
    bytesList = list(byteArray.values())
    for b in bytesList:
        f.write(bytes([b]))
    f.close()
    writingFile = False


@eel.expose
def upload_file(file, copies):
    global client
    file["copies"] = int(copies)
    client.uploadFile(file)

@eel.expose
def delete_file(fileName):
    global writingFile
    writingFile = True
    path = str(os.path.abspath(__file__)).replace("main.py", "") + f"localFiles\\"
    fullPath = os.path.join(path, fileName)
    if os.path.exists(fullPath):
        os.remove(fullPath)
        print("File removed successfully")

    writingFile = False


print("Starting client")

client = Client(9000, eel.updateIp, eel.updateOnline, eel.updateDownloads)
client.online()
client.listen()

print("Starting Loop")

while True:
    _dirFiles, _hashcodes = listDirHashCodes()
    if not writingFile:
        if _hashcodes != hashcodes:
            hashcodes = _hashcodes
            eel.showFiles(_dirFiles)
    eel.sleep(1)
