import os
import sys
from bluetooth import *


#os.system("sudo rfcomm release 0")
print("Server running...")
print("Turning on Bluetooth")
#os.system("bash /home/pi/py_projects/connectBT.sh")
hostMACAddress = 'DC:A6:32:54:8E:B7' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
backlog = 1
size = 1024

s = BluetoothSocket(RFCOMM)
s.bind((hostMACAddress, PORT_ANY))
s.listen(backlog)
try:
    #os.system("sudo rfcomm watch hci0")
    print("Conecting socket client...")
    client, clientInfo = s.accept()
    
    
    print("Connected!")
    with open("/home/pi/py_projects/PI_Incoming/imgr.jpg","wb+") as file:
        imSizeNum = int.from_bytes(client.recv(1),"big")
        imSize = 0
        for i in range(imSizeNum):
            imSize = imSize* 10 + int.from_bytes(client.recv(1),"big")
        for i in range(imSize):
            data = client.recv(1)
            file.write(data)
    with open("/home/pi/py_projects/PI_Incoming/imgt.jpg","wb+") as file:
        imSizeNum = int.from_bytes(client.recv(1),"big")
        imSize = 0
        for i in range(imSizeNum):
            imSize = imSize* 10 + int.from_bytes(client.recv(1),"big")
        for i in range(imSize):
            data = client.recv(1)
            file.write(data)

    os.system("./main.sh")
    with open("/home/pi/py_projects/result.txt","r") as file:
        client.send(file.read())
except:
    print("Closing socket")
    client.close()
    s.close()




#os.system("rfkill block bluetooth")