from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("", serverPort))
print("Ther server is ready to reveive")
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    message = message.decode()
    if (message == "exit"):
        break
    modifiedMessage = message.upper()
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)