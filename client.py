import socket
from time import sleep, time
import csv, sys

class client:
    def __init__(self):
        pass

    def connect(self, host, port):
        self.host = host
        self.port = port

        try:
            self.server = socket.socket()
            self.server.connect((self.host, self.port))
            sleep(.1)
            self.server.send("0".encode())
        except:
            return 1
        else:
            return 0

    def send(self, message):
        self.server.send(message.encode())
        sleep(.1)
        data = self.server.recv(32).decode()
        if data == "ack":
            return True
        else:
            return False

    def receive(self):
        return self.server.recv(32).decode()

    def quit(self):
        self.server.close()

class receiver:
    def __init__(self):
        pass

    def connect(self, host, port):
        self.host = host
        self.port = port

        try:
            self.server = socket.socket()
            self.server.connect((self.host, self.port))
            sleep(.1)
            self.server.send("1".encode())
        except:
            return 1
        else:
            return 0

    def receive(self):
        data = self.server.recv(32).decode()

        if data:
            return data
        else:
            pass

    def quit(self):
        self.server.close()

connection = receiver()
client1 = connection.connect(ip, port)

print("Start!")
choice = input("Do you want to:\n\t1 - Take data\n\t2 - Stop\nEnter your choice: ")

test_num=0

while (int(choice) == 1):
    counter = 0
    start = time()

    with open('launch_acc'+str(test_num)+'.csv', 'w', encoding='UTF8') as f:
        with open('launch_ang'+str(test_num)+'.csv', 'w', encoding='UTF8') as a:
            writerF = csv.writer(f)
            writerF.writerow(['x', 'y', 'z', 'time'])
            writerA = csv.writer(a)
            writerA.writerow(['x', 'y', 'z', 'time'])
            while time()-start < 10:
                data = connection.receive()[1:].split(',')
                data.append(time()-start)
                if data:
                    if len(data) == 4:
                        writerA.writerow(data)
                        counter += 1
                data = connection.receive()[1:].split(',')
                data.append(time()-start)
                if data:
                    if len(data) == 4:
                        writerF.writerow(data)
                        counter += 1

    choice = input("Do you want to:\n\t1 - Take data\n\t2 - Stop\nEnter your choice: ")
    test_num += 1

connection.quit()
sys.exit()
