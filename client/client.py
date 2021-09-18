import socket
import sys
import json
from datetime import datetime
import argparse
#port:14200

class Client():
    def __init__(self, getip, getport, c_type, c_name, in_param, in_exp):
        self.getip = getip
        self.getport = getport
        self.c_type = c_type
        self.c_name = c_name
        self.in_param = in_param
        self.in_exp = in_exp
        self.dictionary={}
        # Data to be written
        if self.c_type=="os":
            self.dictionary = {
                "command_type" : self.c_type,
                "command_name" : self.c_name,
                "parameters" : self.in_param,
         }

        elif self.c_type=="compute":
            self.dictionary = {
                "command_type" : self.c_type,
                "expression" : self.in_exp
            }


        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.getip, self.getport))
        

        #connecting
        # self.context = zmq.Context()
        # print("Connecting to server...")
        # self.socket = self.context.socket(zmq.REQ)
        # self.socket.connect("tcp://{0}:{1}".format(self.getip, self.getport))
        self.sendMsg()
        self.save_Result()
        self.endConnection()



    #save and write json file
    def sv_Write(self):
        # Serializing json 
        json_object = json.dumps(self.dictionary, indent = 10)
        now = datetime.now()
        current_time = now.strftime("%H-%M-%S")
        # Writing to Client.json
        extension =".json"
        filename =  current_time + extension
        with open(filename, "w") as outfile:
            outfile.write(json_object)

        return json_object


    def save_Result(self):
        temp = self.resvMsg()
        now = datetime.now()
        current_time = now.strftime("%H-%M-%S")
        # Writing to Client.json
        extension =".json"
        filename =  "r-"+current_time + extension
        with open(filename, "w") as outfile:
            outfile.write(temp)


    def sendMsg(self):
        msg = self.sv_Write()
        print(msg)
        self.s.send(msg.encode())


    def resvMsg(self):
        data1 = self.s.recv(2048)
        #data2 = self.socket.recv(1024)
        #print(data2.decode())
        return data1.decode()

    def endConnection(self):
        self.s.close()




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile',
                    help="JSON file to be processed",
                    type=argparse.FileType('r'))
    arguments = parser.parse_args()

    # Loading a JSON object returns a dict.
    dic={}
    dic = json.load(arguments.infile)


    getip = "127.0.0.1"#input("Please enter Ip: ")
    getport = 14200#int(input("Please enter Port: "))
    #command_type = input("Please Enter Your command type: ")
    #command_name = input("Please Enter Your command name: ")
    #input_parameters = input("Enter elements of input parameters by space: ")
    #print("\n")
    #parameters = input_parameters.split()
    if dic['command_type']=="os":
        server= Client(getip, getport, dic['command_type'], dic['command_name'], dic['parameters'], None)
    elif dic['command_type'] =="compute":
        server= Client(getip, getport, dic['command_type'], None, None, dic['expression'])

if __name__ == "__main__":
    main()
