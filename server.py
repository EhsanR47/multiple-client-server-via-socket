import socket 
from threading import Thread 
import time
import sys
import json
import os
from subprocess import check_output
from datetime import datetime
import threading
import platform
import gevent
from gevent import subprocess

class Server():
    def __init__(self, socket,con):
        self.socket = con
        self.data = socket
        self.json_object = self.data.decode()
        self.writeFile()
        self.sendMsg()
        #self.endConnection()

    def writeFile(self):
        now = datetime.now()
        current_time = now.strftime("%H-%M-%S")
        # Writing to Client.json
        extension =".json"
        filename =  current_time + extension
        with open(filename, "w") as outfile:
            outfile.write(self.json_object)
            #print("Received")
        return str(filename)

    #Create result
    def oscp_Result(self):
        # Data to be written
        temp={}
        f = open(self.writeFile())
        temp = json.load(f)
        dic={}
        str1=""
        print(type(temp))
        print("self.json_object\n",temp)
        if temp['command_type']=="os":
            for i in range(len(temp['parameters'])):
                str1 += temp['parameters'][i]+' '
            str2= str(temp['command_name']) +" "+ str1
            dic={
                "given_os_command" : str2,
                "result" : self.os_Result(str2)
            }

        elif temp['command_type']=="compute":
            dic = {
                "given_math_expression" : temp['expression'],
                "result" : self.os_Compute(temp['expression'])
            }
        
        print("oscp_Result dic :\n",dic)
        now = datetime.now()
        current_time = now.strftime("%H-%M-%S")
        extension =".json"
        filename =  current_time + extension
        json_result = json.dumps(dic, indent = 10)
        with open('r-'+filename, "w") as outfile:
            outfile.write(json_result)
        return json_result


    def os_Result(self,in_os):
        self.in_os = in_os
        if platform.system() =="Windows":
            o1=subprocess.Popen(self.in_os, stdout=subprocess.PIPE, shell=True)
            self.result = str(o1.stdout.read().decode())
        else:
            result_lin = check_output(self.in_os, shell=True)
            #print(os.popen(self.in_os).read())
            #return(os.popen(self.in_os).read())
            self.result=result_lin.decode('utf-8')
        return self.result
        


    def os_Compute(self,in_compute):
        self.in_compute = in_compute
        if platform.system() =="Windows":
            str_win = "set /a "+ str(self.in_compute)
            p1=subprocess.Popen(str_win, stdout=subprocess.PIPE, shell=True)
            return str(p1.stdout.read().decode())

        else:
            #str_linux = f'echo "$({self.in_compute})"'
            #p2=subprocess.Popen(str_linux, stdout=subprocess.PIPE, shell=True)
            #return str(p2.stdout.read().decode())
            p2= check_output(f'echo "$(({self.in_compute}))"', shell=True)
            return(p2.decode())
            #return(eval(self.in_compute))

        #print((eval(self.in_compute)))
        #return(eval(self.in_compute))

    def sendMsg(self):
        rs = self.oscp_Result()
        print("rs: \n",rs)
        self.socket.send(rs.encode())
        #self.socket.send("Message Received!".encode())

    def endConnection(self):
        self.socket.close()


#input Ip and Port
TCP_IP = '127.0.0.1' 
TCP_PORT = 14200 
ADDR = (TCP_IP, TCP_PORT)

def handle_client(conn, addr):
    
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        con=conn
        msg = conn.recv(2048)
        if msg:
            Server(msg,con)
        else:
            time.sleep(1)

    #conn.close()

def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {TCP_IP}:{TCP_PORT}")
    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
    
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()


